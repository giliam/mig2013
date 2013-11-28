/* HTML Recording script by Maxime Ernoult */

navigator.getUserMedia = (navigator.getUserMedia || 
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia);
                    // raccourci cross-browser
mediaRecorder = null //Object MediaRecorder
audioElement = document.getElementById('audio'); //L'object audio pour le direct play
mediaStream = null; //Le flux LocalMediaStream

var recording = false;


onload = function(){
    /* Au chargement, si l'API MediaRecorder est supportée, 
    on initialise l'entrée audio avec l'API getUserMedia */
    if (typeof MediaRecorder === 'undefined' || !navigator.getUserMedia){
        alert('MediaRecorder is unsupported');
    } 
    else{
        navigator.getUserMedia({audio: true},
            initRecording,
            function(err) {
		        console.log("The following error occured: " + err);
		    }
        );
    }
};

function initRecording(localMediaStream){
    /* Initialise l'enregistrement */
    mediaRecorder = new MediaRecorder(localMediaStream);
    mediaRecorder.ondataavailable = mediaOnDataAvailable;
    mediaStream = localMediaStream;

    console.log('getUserMedia initialisé');  
}    

function main(){
    /* Decide quelle action lancer lorsque le bouton est togglé */
    if (!recording){
        try{
            startRecord();
            recording = true;
            changeLogoBG('green');
        }
        catch (e){
            console.log("Erreur d'enregistremnt\n" + e);
        }
    }
    else{
        try{
            stopRecord();
            recording = false;
            changeLogoBG('white');
        }
        catch (e){
            console.log("Erreur d'arrêt\n" + e);
        }
    }

}

function startRecord(){
    /* Lance un enregistrement */
    mediaRecorder.start();
    var audioElement = document.getElementById('audio');
    audioElement.src = window.URL.createObjectURL(mediaStream);
    console.log('recording');
    

}

function stopRecord(){
    /* Stopper et clore un enregistrement */
	if (mediaStream){
		/* Si on enregistre */
		console.log('stopRecord');
        var audioElement = document.getElementById('audio');
		audioElement.src = '';
        mediaRecorder.stop();		
	}
    
}

function mediaOnDataAvailable(data){
    /* A la fin de l'enregistrement, récupère le blob dans data 
       et lance le traitement                                       */
    console.log("Data available !!!");
    console.log(data);

    //Rend le blob disponible au chargement
    var link = document.getElementById('dlLink');
    link.href = window.URL.createObjectURL(data.data);
    link.innerHTML = "dl";



}

function changeLogoBG(color){
    /* Change la couleur d'arrière-plan du logo microphone */
    if (!color){
        color = 'white';
    }
    document.getElementById("microphone").style.backgroundColor = color;
    return color;
}
