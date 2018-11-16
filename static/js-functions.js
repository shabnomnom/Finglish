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

$('#test').on("click", ()=>alert("hello"));




//url,.. error are keys 
//  "this" would refer to the element that triggered the call
// you can refer to it by its id whic is defined on the html side of the audio botton 
// 'audio' is referring to the tag 
// #audio reffering to the id 
// .class reffere to the class of elements wit the 



function getPronouciation(){
    $.get('/pronouciation/<farsi_word>',

    (results) => { 
        var elm = farsi_word;
        var audio = document.getElementById('audio');

        var source = document.getElementById('audioSource');
        source.src = elm.getAttribute('results');

  audio.load(); //call this to just preload the audio without playing
  audio.play(); //call this to play the song right away
});






$("audio").on("click", getPronouciation);


























