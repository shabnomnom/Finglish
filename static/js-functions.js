  'use strict' 
//url,.. error are keys 
//  "this" would refer to the element that triggered the call
// you can refer to it by its id whic is defined on the html side of the audio botton 
// 'audio' is referring to the tag 
// #audio reffering to the id 
// .class reffere to the class of elements wit the 



function getPronouciation(e){
    e.stopPropagation();
    $.get(`/pronouciation/${this.id}`,

    (results) => { 
        //console.log(results)
        console.log(results);
        console.log(this.id);

        let audio = document.getElementById(this.id);
        console.log("AUDIO");
        console.log(audio);

        let source = document.getElementById("audio_src_" + this.id);
        console.log("SOURCE");
        console.log(source);
        source.src = results.url;

        audio.load(); //call this to just preload the audio without playing
  
        var playPromise = audio.play(); //call this to play the song right away

        if (playPromise !== undefined) {

            playPromise.then(_ => {
                console.log("Playback is starting");
            })
            .catch(error => {
                console.log("Derp. There was an error in loading the audio")        
            });
        }
    }
)};

$("audio").on("click", getPronouciation);

// $('#playButton').on('click', (evt) => {
//     evt.preventDefault();

//     word = this.id

//     $.get(`/pronouciation/${}`,
//         (mp3Url) => {
//             let song = new Audio(mp3Url);
//             song.play();
//         }
//     )
// });

$("#lesson").click(function(){
    console.log("I've been clicked!");
    let userId = this.getAttribute("data-user-id");
    console.log(this.getAttribute("data-user-id"));
    $.ajax({url: "/request_new_lesson/" + userId,
        success: function(result){
            window.location.href = "/users/" + userId;
    }});
});


$(".flip-card").click(function() {
    const self = this;   //do this to have access to the element in the call back function 
    $(self).toggleClass("hover");
    console.log("I've been clicked!");
    let wordId = self.getAttribute("data-word-id");
    console.log(self.getAttribute("data-word-id"));
    if (!$(self).hasClass('hasBeenRecorded')) {
        $.ajax({url: "/update_seen_count/" + wordId,
            success: function() {
                $(self).addClass('hasBeenRecorded');
            }
        });
    }
});
//added click handler on clip card class to toggle (add and 
//remove) hover 
// getting the data attribute fro the farsi word from html
// check to see if the hasbeencrecorded class is already 
// in the .flip-card class, otherwise make an ajax call 
//in success call back we add the hasbeenrecorded to the flipcard
//class












