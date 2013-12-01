/* HTML5Script 
An audio recorder for the speech recognition project
of the mig2013 SE team */

navigator.getUserMedia = (navigator.getUserMedia || 
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia);
                    // cross-browser shortcut

mediaRecorder = null //Object MediaRecorder
audioElement = document.getElementById('audio'); //L'object audio pour le direct play
mediaStream = null; //Le flux LocalMediaStream

var recording = false;

var user = "demo";
var hashedPass = "8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762";
var clientDB = "demo"

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
    var microphone = document.getElementById('microphone');
    microphone.className = "";
};

function initRecording(localMediaStream){
    /* Initialise l'enregistrement */
    mediaRecorder = new MediaRecorder(localMediaStream);
    mediaRecorder.ondataavailable = mediaOnDataAvailable;
    mediaStream = localMediaStream;

    console.log('getUserMedia initialised');  
}    

function main(){
    /* Decide quelle action lancer lorsque le bouton est togglé */
    var microphone = document.getElementById('microphone');
    if (!recording){
        try{
            microphone.className = "wobble animated";
            microphone.style.borderColor = '#003173';
            startRecord();
            recording = true;
            //changeLogoBG('green');
        }
        catch (e){
            console.log("Recording issue\n" + e);
        }
    }
    else{
        try{
            stopRecord();
            recording = false;
            //changeLogoBG('white');
            microphone.className = "";
            microphone.style.borderColor = 'white';
        }
        catch (e){
            console.log("Recording stop issue\n" + e);
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

function mediaOnDataAvailable(blob){
    /* A la fin de l'enregistrement, récupère le blob dans data 
       et lance le traitement                                       */

    var SERVERURL;

    //Log dans la console
    console.log("Data available !!!");
    console.log(blob);

    //Envoie à la console une adresse de téléchargement de l'échantillon
    console.log(window.URL.createObjectURL(blob.data));

    //Communique les data au serveur
    servInteract(blob.data);
}

function servInteract(OGGBlob){
    // Envoie le blob au serveur
    var formData = new FormData();
    formData.append('userSession', userSession);
    formData.append('hashedPass', hashedPass);
    formData.append('clientDB', clientDB);
    
    formaData.append('action', 'recognize_spoken_word');

    formData.append('audioBlob', OGGBlob);
    formData.append('audioType', 'ogg');

    var req = new XMLHttpRequest();
    req.open('POST', SERVERURL, true);
    req.onstatechange = function(e){
        if (req.readyStatus === 4){
            if (req.status == 200){
                wordResponse(req.responseXML);         
            }
        }
    }
    req.send()

}

function wordResponse(respXML){
    if (respXML.getElementsByTagName().length()){
        var responseWord = respXML.getElementsByTagName('respWord');
    }
    else{
        var responseWord = "Error :'(";
    }
    var responseElement = document.getElementById('responseWord');
    responseElement.innerHTML = responseWord;

}

function changeLogoBG(color){
    /* Change la couleur d'arrière-plan du logo microphone */
    if (!color){
        color = 'white';
    }
    document.getElementById("microphone").style.backgroundColor = color;
    return color;
}
