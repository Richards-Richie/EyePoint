import React, { useEffect, useRef, useState } from 'react';

const IrisDetectionComponent = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [gazeOutput, setGazeOutput] = useState('');
    const [showImage, setShowImage] = useState(true);
    const [gazePoints, setGazePoints] = useState([]); // Store last 20 gaze points
    const socketUrl = 'ws://localhost:8000/ws/iris/';

    useEffect(() => {
        const socket = new WebSocket(socketUrl);

        socket.onopen = () => {
            console.log("WebSocket connection established.");
        };

        socket.onmessage = (event) => {
            const parsedData = JSON.parse(event.data);
            if (parsedData.frame) {
                // Handle video frame data as you already do...
                const byteCharacters = atob(parsedData.frame);
                const byteNumbers = new Array(byteCharacters.length).fill(0).map((_, i) => byteCharacters.charCodeAt(i));
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], { type: 'image/jpeg' });
                const url = URL.createObjectURL(blob);
                if (videoRef.current) {
                    videoRef.current.src = url;
                    setShowImage(true);
                }
                // Hide image after 60 seconds
                setTimeout(() => {
                    setShowImage(false);
                }, 60000);
            } else if (parsedData.gaze_output) {
                console.log('gaze_output:', parsedData.gaze_output);
        
                // Assuming gaze_output is an object with properties 'gaze_x' and 'gaze_y'
                const gazeCoords = [parsedData.gaze_output.gaze_x, parsedData.gaze_output.gaze_y];
                const normPos = [gazeCoords[0] / 1920, gazeCoords[1] / 1080];
                setGazeOutput(normPos.toString());
                setShowImage(false);
                updateGazePoints(normPos); // Update gaze points and redraw dots
            }
        };
        

        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        socket.onclose = () => {
            console.log("WebSocket connection closed.");
        };

        return () => {
            socket.close();
        };
    }, []);

    const updateGazePoints = (normPos) => {
        if (!canvasRef.current) return;
        const canvas = canvasRef.current;
        const [normX, normY] = normPos;
        const x = normX * canvas.width;
        const y = normY * canvas.height;

        setGazePoints(prevGazePoints => {
            const newGazePoints = [...prevGazePoints, { x, y }];
            if (newGazePoints.length > 20) {
                newGazePoints.shift(); // Remove the oldest point if we have more than 20
            }
            drawDots(newGazePoints);
            return newGazePoints;
        });
    };

    const drawDots = (points) => {
        if (!canvasRef.current) return;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        // Clear the canvas before drawing
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw each dot at the gaze points
        points.forEach(({ x, y }) => {
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI); // Draw a circle (dot) at (x, y)
            ctx.fillStyle = 'red';
            ctx.fill();
        });
    };

    return (
        <div>
            {showImage && <img ref={videoRef} alt="Iris Detection Video Stream" />}
            <canvas ref={canvasRef} width="1920" height="1080" style={{ border: '1px solid black' }} />
            <div>Gaze Output: {gazeOutput}</div>
        </div>
    );
};

export default IrisDetectionComponent;
