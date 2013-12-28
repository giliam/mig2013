/* HTML5Script 
An audio recorder for the speech recognition project
of the mig2013 SE team */


// cross-browser shortcuts
navigator.getUserMedia = (navigator.getUserMedia || 
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia);
window.AudioContext = window.AudioContext || window.webkitAudioContext;
window.URL = window.URL || window.webkitURL || window.mozURL;


var mediaRecorder; //Object MediaRecorder
//var audioElement = document.getElementById('audio'); //L'object audio pour le direct play
var mediaStream; //Le flux LocalMediaStream pour moz browsers

var webkitaudio_context;
var webkitrecorder;


var recording = false;
var nav = null; //Enregistre le type de navigateur: moz ou webkit


var user = "demo";
var hashedPass = "8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762";
var clientDB = "demo";
var SERVERURL = 'localhost:8010';


onload = function(){
    /* Au chargement, si l'API MediaRecorder est supportée, 
    on initialise l'entrée audio avec l'API getUserMedia */
    if (navigator.getUserMedia){
        if (typeof MediaRecorder === 'undefined'){
            if (navigator.getUserMedia && window.AudioContext && window.URL){
                nav = 'webkit';
                webkitaudio_context = new AudioContext;

            }
            else{
                alert("Votre navigateur ne nous supporte pas :°(");
            }
        } 
        else{
            nav = 'moz';
        }
    }

    if (nav != null){
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
        mozinitRecording(localMediaStream);
    }
    else if (nav == 'webkit'){
        webkitinitRecording(localMediaStream);
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
    navSwitch(mozstartRecorder, webkitstartRecorder);
}

function stopRecord(){
    /* Stopper et clore un enregistrement */
    navSwitch(mozstopRecorder, webkitstopRecorder); 
}


function navSwitch(mozaction, webkitaction){
    console.log(nav);
    if (nav == 'moz'){
        mozaction();
    }
    else if (nav == 'webkit'){
        webkitaction();
    }
}


function preInteract(audioBlob, blobType){
    var url = window.URL.createObjectURL(audioBlob);
    //document.getElementById("recording").innerHTML += '<audio controls src="' + url + '">Sound</audio>'; 

    //Envoie à la console une adresse de téléchargement de l'échantillon
    console.log(url);

    //Communique les data au serveur
    servInteract(audioBlob, blobType);

}

/////////////////////////
/////////////////////////
/////////////////////////

function mozinitRecording(localMediaStream){
    /* Initialise l'enregistrement */
    mediaRecorder = new MediaRecorder(localMediaStream);
    mediaRecorder.ondataavailable = mozmediaOnDataAvailable;
    mediaStream = localMediaStream;

}  


function mozstartRecorder(){
    mediaRecorder.start();
    //var audioElement = document.getElementById('audio');
    //audioElement.src = window.URL.createObjectURL(mediaStream);
    //console.log(audioElement.src);
}


function mozstopRecorder(){
    if (mediaStream){
        mediaRecorder.stop();
        //var audioElement = document.getElementById('audio');
        //audioElement.src = '';
    }
}


function mozmediaOnDataAvailable(blob){
    /* A la fin de l'enregistrement, récupère le blob dans data 
       et lance le traitement                                       */
    preInteract(blob.data, 'ogg');
}

/////////////////////////
/////////////////////////

function webkitinitRecording(localMediaStream){
    var input = webkitaudio_context.createMediaStreamSource(localMediaStream);
    //input.connect(webkitaudio_context.destination);
    webkitrecorder = new Recorder(input);

}


function webkitstartRecorder(){
    webkitrecorder && webkitrecorder.record();
}


function webkitstopRecorder(){
    webkitrecorder && webkitrecorder.stop();

    webkitrecorder && webkitrecorder.exportWAV(function(audioBlob) {
          preInteract(audioBlob, 'wav');
        });

    webkitrecorder.clear();
}

/////////////////////////
/////////////////////////
/////////////////////////

function servInteract(audioBlob, blobType){
    // Envoie le blob au serveur
    var formData = new FormData();
    formData.append('user', user);
    formData.append('hashedPass', hashedPass);
    formData.append('clientDB', clientDB);
    
    formData.append('action', 'recognize_spoken_word');

    formData.append('audioBlob', audioBlob);
    formData.append('audioType', blobType);

    var req = new XMLHttpRequest();
    req.open('POST', 'handler', false);
    /*req.onstatechange = function(){
        console.log('ez');
        console.log(req.readyStatus);
        if (req.readyStatus === 4){
            console.log('4');
            if (req.status == 200){
                console.log(200);
                wordResponse(req.responseXML);         
            }
        }
    }*/
    //req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send(formData);
    resp = req.responseXML;
    wordResponse(resp);

}


function wordResponse(respXML){
    if (respXML.getElementsByTagName('respWord')){
        var responseWord = respXML.getElementsByTagName('respWord')[0].textContent;
    }
    else{
        var responseWord = "Error :'(";
    }
    var responseElement = document.getElementById('responseWord');
    console.log(responseWord);
    responseElement.innerHTML = responseWord;

}
