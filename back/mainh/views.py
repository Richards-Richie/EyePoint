import os
from django.http import JsonResponse
import subprocess

def start_video_feed(request):
    # Logic to start the video feed (if needed)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    back_dir=os.path.dirname(parent_dir)
    distance_dir = os.path.join(back_dir, 'distance')
    target_file = os.path.join(distance_dir, 'a.py')
    print(target_file)

    # if not os.path.isfile(target_file):
    #     context = {
    #         'output': '',
    #         'errors': f"Target file not found: {target_file}"
    #     }
    #     return render(request, 'result.html', context)

    try:
        print("try")
        result = subprocess.run(['python', target_file], capture_output=True, text=True)
        print("run")
        output = result.stdout
        errors = result.stderr
        context = {
            'output': output,
            'errors': errors
        }
    except Exception as e:
        context = {
            'output': '',
            'errors': str(e)
        }
    return JsonResponse({'status': 'Video feed started'})

def stop_video_feed(request):
    # Logic to stop the video feed (if needed)
    return JsonResponse({'status': 'Video feed stopped'})
