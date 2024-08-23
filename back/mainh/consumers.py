import cv2  # type: ignore
import json
import subprocess
import numpy as np  # type: ignore
from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore
import os
import base64
import asyncio
from datetime import datetime
from myapp.models import save_gaze_data  # Assuming your model is named save_gaze_data
from channels.db import database_sync_to_async  # type: ignore

class IrisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Connected")
        self.capture = cv2.VideoCapture(0)  # Initialize webcam capture
        if not self.capture.isOpened():
            print("Error: Failed to open webcam.")
            return

        # Create directory to save images if it doesn't exist
        self.save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_images')
        os.makedirs(self.save_dir, exist_ok=True)

        self.send_task = asyncio.create_task(self.send_frames())

    async def send_frames(self):
        start_time = datetime.now()
        gaze_simulation_started = False

        while self.capture.isOpened():
            ret, frame = self.capture.read()
            if not ret:
                print("Error: Failed to retrieve frame from the webcam.")
                break

            # Check if it's time to switch to gaze simulation
            if (datetime.now() - start_time).total_seconds() >= 60:
                if not gaze_simulation_started:
                    gaze_simulation_started = True
                    # Start gaze simulation subprocess
                    self.capture.release()
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    parent_dir = os.path.dirname(current_dir)
                    back_dir = os.path.dirname(parent_dir)
                    gaze_dir = os.path.join(back_dir, 'gaze detection')
                    target_file = os.path.join(gaze_dir, '1.py')
                    self.gaze_process = subprocess.Popen(['python', target_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # Create a task to read gaze output continuously
                    self.read_gaze_task = asyncio.create_task(self.read_gaze_output())

            else:
                # Process the frame with the iris detection model
                try:
                    processed_frame = await self.run_iris_detection(frame)

                    # Save the processed frame
                    if processed_frame is not None:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                        save_path = os.path.join(self.save_dir, f'processed_frame_{timestamp}.jpg')
                        cv2.imwrite(save_path, processed_frame)
                        print(f'Frame saved to {save_path}')

                        _, buffer = cv2.imencode('.jpg', processed_frame)
                        frame_data = buffer.tobytes()
                        encoded_frame = base64.b64encode(frame_data).decode('utf-8')  # Encode to base64 string for JSON serialization

                        await self.send(text_data=json.dumps({
                            'frame': encoded_frame,
                        }))
                        print("Frame sent")
                    else:
                        print("Warning: Processed frame is None.")

                except cv2.error as e:
                    print(f"OpenCV error occurred: {e}")
                    continue

            # Control the frame rate to 10 frames per second
            await asyncio.sleep(0.1)

    async def read_gaze_output(self):
        while True:
            gaze_output = self.gaze_process.stdout.readline().strip()
            if gaze_output:
                try:
                    gaze_data = json.loads(gaze_output)
                    await self.send(text_data=json.dumps({
                        'gaze_output': gaze_data,
                    }))
                    print("Gaze output sent:", gaze_data)

                    # Save the gaze data to the database
                    await self.save_gaze(gaze_data)

                except json.JSONDecodeError:
                    print("Failed to decode gaze output:", gaze_output)

    async def save_gaze(self, data):
        # Extract the gaze coordinates from the data
        gaze_x = data.get('gaze_x')
        gaze_y = data.get('gaze_y')

        if gaze_x is None or gaze_y is None:
            print("Error: Missing gaze data.")
            return

        # Save the new gaze data entry
        await database_sync_to_async(self._save_gaze_data)(gaze_x, gaze_y)
        print(f"Saved gaze data: x={gaze_x}, y={gaze_y}")

        # Manage the total count to keep only the last 10 entries
        await database_sync_to_async(self._manage_gaze_data_limit)()

    @staticmethod
    def _save_gaze_data(gaze_x, gaze_y):
        # Save the new gaze data entry
        gaze_entry = save_gaze_data(gaze_x=gaze_x, gaze_y=gaze_y)
        gaze_entry.save()

    @staticmethod
    def _manage_gaze_data_limit():
        total_entries = save_gaze_data.objects.count()
        if total_entries > 100000:
            # Delete the oldest entries, keeping only the last 10
            excess_entries = total_entries - 100000
            save_gaze_data.objects.order_by('timestamp')[:excess_entries].delete()
            print(f"Deleted {excess_entries} oldest entries, keeping only the last 10.")

    async def run_iris_detection(self, frame):
        # Encode the frame to a byte stream
        _, frame_buffer = cv2.imencode('.jpg', frame)
        frame_bytes = frame_buffer.tobytes()

        # Call the external iris detection script with the frame bytes as input
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        back_dir = os.path.dirname(parent_dir)
        distance_dir = os.path.join(back_dir, 'iris')
        target_file = os.path.join(distance_dir, 'segmentation_mask.py')
        self.iris_detection_process = subprocess.Popen(['python', target_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = self.iris_detection_process.communicate(input=frame_bytes)

        # Check if the process ended successfully
        if self.iris_detection_process.returncode != 0:
            print(error.decode('utf-8'))
            raise subprocess.CalledProcessError(self.iris_detection_process.returncode, self.iris_detection_process.args, output=output, stderr=error)

        # Decode the output bytes back to an image
        nparr = np.frombuffer(output, np.uint8)
        processed_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if processed_frame is None:
            print("Warning: Processed frame is None after decoding.")
        return processed_frame

    async def disconnect(self, close_code):
        if hasattr(self, 'capture'):
            self.capture.release()
        if hasattr(self, 'send_task'):
            self.send_task.cancel()
        if hasattr(self, 'read_gaze_task'):
            self.read_gaze_task.cancel()
        print("Disconnected")
