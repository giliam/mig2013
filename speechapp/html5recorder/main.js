var recording = false;
var audio = document.getElementById('audio');
var mediaStream;

onload = function (){
    initAudio();
};

function initAudio() {
    /* Initialisation des flux audios */
    console.log("Init");
    try{
        navigator.getMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);

    }
    catch (e){
        console.log("erreur d'initialisation des flux audios ! \n" + e);
    }
}

function main(){
    /* Fonction principale, déclenche ou stoppe l'enregistrement */
    if (!recording){
        /* Lance l'enregistrement */
		try{
			record();
			recording = true;
			changeLogoBG('green');
		}
		catch (e){
			console.log("Erreur d'enregistrement");
		}
        
    }
    else{
        /* Arrête l'enregistrement */
		try{
			stopRecord();
			recording = false;
			changeLogoBG('white');
		}
		catch (e){
			console.log("Erreur à l'arrêt de l'enregistrement");
		}
    }
}

function record() {
	if (!mediaStream){
		/* Si l'enregistrement n'est pas initialisé */
		navigator.getMedia({audio: true}, 
			function(localMediaStream) {
				mediaStream = localMediaStream;
				var audio = document.getElementById('audio');

				audio.src = window.URL.createObjectURL(localMediaStream);
				console.log(audio.src);
			},
			function(err) {
				console.log("The following error occured: " + err);
			}
		)
	}
	else{
		var audio = document.getElementById('audio');

		audio.src = window.URL.createObjectURL(mediaStream);
	}
}

function stopRecord(){
	if (mediaStream){
		/* Si on enregistre */
		console.log('stopRecord');
		var audio = document.getElementById('audio');

		audio.src = '';
		//mediaStream.stop();	//detruit le LocalMediaStream
	}
    
}    

function changeLogoBG(color){
    /* Change la couleur d'arrière-plan du logo microphone */
    if (!color){
        color = 'white';
    }
    document.getElementById("microphone").style.backgroundColor = color;
    return color;
}