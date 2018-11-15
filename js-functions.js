  'use strict' 

//import os 

forvo_key = os.environ["forvo_key"]
key = forvo_key


// Don't be terrified you can write this!! 
   // var url = 'http://apifree.forvo.com//XXXXXXXXXXXXXXXX/format/json/callback/pronounce/action/standard-pronunciation/word/'+encodeURI(word)+'/language/zh';

    function getAudio() {
    var url="https://apifree.forvo.com/key/"+`${key}`+ "/format/json/callback/pronounce/action/word-pronunciations/word/"+ encodeURI(word)+"/language/fa"
    $.ajax({
        url: url,
        jsonpCallback: "pronounce",
        dataType: "json",
        type: "json",
        method: "GET",
        success: function (json) {
            if (json.items["langname"] === "Persian"){
                var mp3 = json.items[0].pathmp3 ;
            } else {
                error = function(){
                console.log("error")};
}
} 
});
$('#audio').on ("click", getAudio);