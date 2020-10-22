function videoPoctoring() {
    const video = document.getElementById('video');
    console.log("Coming to script")
    Promise.all([
        faceapi.nets.mtcnn.loadFromUri('quizer/models'),

    ]).then(
        startVideo
    )

    function startVideo() {

        console.log('coming to start video');
        navigator.getUserMedia(
            {
                video: {}
            },
            stream => video.srcObject = stream,
            err => console.log(err)
        )
    }
    let notHere = 0, twoPerson = 0;
    const canvas = document.createElement('canvas');
    canvas.height = 300;
    canvas.width = 500;
    video.addEventListener('play', () => {
        setInterval(async () => {
            if (video.srcObject.active == false) {
                window.close();
            }
            const d2 = await faceapi.detectAllFaces(video, new faceapi.MtcnnOptions());
            if (d2.length == 0) {
                notHere += 1;
                if (notHere > 60) {
                    notHere = 0;
                    //Capture image now and send it to server
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    let dataUrl = canvas.toDataURL();
                    $.ajax({
                        url: "/regular-checks/",
                        type: "POST",
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                            "type": "NotHere",
                            "id": "{{quiz.id}}",
                            "imgBase64": dataUrl
                        },
                    })

                }
            }
            else if (d2.length == 2) {
                twoPerson += 1;
                if (twoPerson > 10) {
                    twoPerson = 0;
                    //Capture image now and send it to server
                    $.ajax({
                        url: "/regular-checks/",
                        type: "POST",
                        data: {
                            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                            "type": "TwoPerson",
                            "id": "{{quiz.id}}",
                            "imgBase64": dataUrl
                        },
                    })
                }
            }
            else {
                twoPerson = 0;
                notHere = 0;
            }
        }, 1000)
    })
}
