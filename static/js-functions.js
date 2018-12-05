  'use strict' 




// Don't be terrified you can write this!! 
   // var url = 'http://apifree.forvo.com//XXXXXXXXXXXXXXXX/format/json/callback/pronounce/action/standard-pronunciation/word/'+encodeURI(word)+'/language/zh';

// function getAudio() {
//     // this.id
//     var url = `https://apifree.forvo.com/key/XXXXXXXXXXXXXXXX/format/json/action/word-pronunciations/word/${this.id}/language/fa`;

//     $.ajax({
//         url: url,
//         dataType: "json",
//         type: "json",
//         method: "GET",
//         success: function(json) {
//             if (json.items["langname"] === "Persian") {
//                 var mp3 = json.items[0].pathmp3;
//             }
//         },
//         error : function(){
//             console.log("error")
//         }
//     })
// }

//$('#test').on("click", ()=>alert("hello"));




//url,.. error are keys 
//  "this" would refer to the element that triggered the call
// you can refer to it by its id whic is defined on the html side of the audio botton 
// 'audio' is referring to the tag 
// #audio reffering to the id 
// .class reffere to the class of elements wit the 



function getPronouciation(){
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

$("#word").click(function(){
    console.log("I've been clicked!");
    let wordId = this.getAttribute("data-word-id");
    console.log(this.getAttribute("data-word-id"));
    $.ajax({url: "/update_seen_count/" + wordId,
        success: function(result){
        $("#div1").html(result);
    }});
});

$("#lesson").click(function(){
    console.log("I've been clicked!");
    let userId = this.getAttribute("data-user-id");
    console.log(this.getAttribute("data-user-id"));
    $.ajax({url: "/request_new_lesson/" + userId,
        success: function(result){
            window.location.href = "/users/" + userId;
    }});
});













