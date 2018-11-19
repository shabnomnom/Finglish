'use strict';


$('#playButton').on('click', (evt) => {
    evt.preventDefault();

    let word;

    $.get(`http://localhost:5000/pronouciation/${word}`,
        (mp3Url) => {
            let song = new Audio(mp3Url);
            song.play();
        }
    )
});
