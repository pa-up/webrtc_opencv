async function initializeCamera() {
    const inputVideo = document.getElementById('inputVideo');
    const outputImage = document.getElementById('outputImage');

    try {
        inputVideo.srcObject = await navigator.mediaDevices.getUserMedia({ video: true });
        inputVideo.addEventListener('loadedmetadata', () => {
            inputVideo.play();
            setInterval(() => {
                sendFrameToServer(inputVideo);
            }, 200);
        });
    } catch (err) {
        console.error('Error accessing camera: ', err);
    }

    socket.on('output_video', (data) => {
        outputImage.src = 'data:image/jpeg;base64,' + data;
    });
}

function sendFrameToServer(video) {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth ;
    canvas.height = video.videoHeight  ;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const data = canvas.toDataURL('image/jpeg', 0.8).split(',')[1];
    socket.emit('input_video', data);
}
