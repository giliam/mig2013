/* HTML5Script 
An audio recorder for the speech recognition project
of the mig2013 SE team */


// cross-browser shortcuts
navigator.getUserMedia = (navigator.getUserMedia || 
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia);
window.AudioContext = window.AudioContext || window.webkitAudioContext;
window.URL = window.URL || window.webkitURL || window.mozURL;


mediaRecorder = null //Object MediaRecorder
audioElement = document.getElementById('audio'); //L'object audio pour le direct play
mediaStream = null; //Le flux LocalMediaStream pour moz browsers

webkit-audioContext = null;
webkit-recorder = null;


var recording = false;
var nav = null; //Enregistre le type de navigateur: moz ou webkit


var user = "demo";
var hashedPass = "8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762";
var clientDB = "demo"


onload = function(){
    /* Au chargement, si l'API MediaRecorder est supportée, 
    on initialise l'entrée audio avec l'API getUserMedia */
    if (navigator.getUserMedia){
        if (typeof MediaRecorder === 'undefined'{
            if (navigator.getUserMedia && window.AudioContext && window.URL){
                nav = 'webkit';
                audio_context = new AudioContext;

            }
            else{
                alert("Votre navigateur ne nous supporte pas :°(");
            }
        } 
        else{
            nav = 'moz';
            console.log('moz compatibilty mode running ...')
        }
    }

    if (nav){
        navigator.getUserMedia({audio: true},
                initRecording,
                function(err) {
		            console.log("The following error occured: " + err);
		        }
            );
        console.log(nav + ' compatibilty mode running ...');

    }
};  


function initRecording(localMediaStream){
    if (nav == 'moz'){
        moz-initRecording(localMediaStream)
    }
    else if (nav == 'webkit'){
        webkit-initRecording(localMediaStream)
    }
}


function main(){
    /* Decide quelle action lancer lorsque le bouton est togglé */
    var microphone = document.getElementById('microphone');
    if (!recording){
        try{
            microphone.className = "wobble animated";
            microphone.style.border = '5px solid #003173';
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
            microphone.style.border = '5px solid white';
        }
        catch (e){
            console.log("Recording stop issue\n" + e);
        }
    }

}


function startRecord(){
    /* Lance un enregistrement */
    navSwitch(mediaRecorder.start(), webkit-startRecorder);
    console.log('recording');
}

function stopRecord(){
    /* Stopper et clore un enregistrement */
    navSwitch(moz-stopRecorder, webkit-stopRecoder); 
}


function navSwitch(moz-action, webkit-action){
    if (nav == 'moz'){
        moz-action();
    }
    else if (nav == 'webkit'){
        webkit-action()
    }
}


function preInteract(audioBlob, blobType){
    var url = windows.URL.createObjectURL(audioBlob.data);
    showDlLink(url):


    //Log dans la console
    console.log("Data available !!!");
    console.log(audioBlob);

    //Envoie à la console une adresse de téléchargement de l'échantillon
    console.log(url);

    //Communique les data au serveur
    servInteract(blob.data, blobType);

}

function showDlLink(url){
    console.log(url);
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

function moz-initRecording(localMediaStream){
    /* Initialise l'enregistrement */
    mediaRecorder = new MediaRecorder(localMediaStream);
    mediaRecorder.ondataavailable = moz-mediaOnDataAvailable;
    mediaStream = localMediaStream;

    console.log('getUserMedia initialised');  
}  


function moz-startRecorder(){
    mediaRecorder.start();
    var audioElement = document.getElementById('audio');
    audioElement.src = window.URL.createObjectURL(mediaStream);
}


function moz-stopRecorder(){
    if (mediaStream){
		console.log('stopRecord');
        var audioElement = document.getElementById('audio');
        audioElement.src = '';
    }
}


function moz-mediaOnDataAvailable(blob){
    /* A la fin de l'enregistrement, récupère le blob dans data 
       et lance le traitement                                       */

    preInteract(blob, 'ogg');
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

function webkit-initRecording(localMediaStream){
    var input = webkit-audio_context.createMediaStreamSource(localMediaStream);
    input.connect(webkit-audio_context.destination);
    webkit-recorder = new Recorder(input);

}


function webkit-startRecorder(){
    webkit-recorder && webkit-recorder.record();
}


function webkit-stopRecorder(){
    webkit-recorder && webkit-recorder.stop();

    webkit-recorder && webkit-recorder.exportWAV(function(audioBlob) {
          preInteract(audioBlob, 'wav');
        });

    webkit-recorder.clear()
}

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

function servInteract(OGGBlob, blobType){
    // Envoie le blob au serveur
    var formData = new FormData();
    formData.append('userSession', userSession);
    formData.append('hashedPass', hashedPass);
    formData.append('clientDB', clientDB);
    
    formaData.append('action', 'recognize_spoken_word');

    formData.append('audioBlob', OGGBlob);
    formData.append('audioType', blobType);

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
