// Return window width or return 0
function getBrowserWidth(){
    if (window.innerWidth){
        return window.innerWidth;}
    else if (document.documentElement && document.documentElement.clientWidth != 0){
        return document.documentElement.clientWidth;    }
    else if (document.body){return document.body.clientWidth;}
    return 0;
};

// Responsive design logic
function dynamicLayout(){
    var browserWidth = getBrowserWidth();
    if ( 640 > browserWidth){
        $(".tiny_able").addClass("tiny");
        $(".thinable").removeClass("thin");
        $(".wide_able").removeClass("wide");

//        $('link').attr('href', '/static/yap/css/yap_mobile.css');
        $('#logo').text("y");
        $('#download_icon_container').text("Download App");
    }
    else if ( 640 < browserWidth && browserWidth < 1280){
//        if ($("#slideshow_container").next().attr('id') == 'player_container') {
//            $("#slideshow_container").insertAfter("#player_container");
//        }
        $(".thinable").addClass("thin");
        $(".tiny_able").removeClass("tiny");
        $(".wide_able").removeClass("wide");

//        $('link').attr('href', '/static/yap/css/yap_thin.css');
        $('#logo').text("yapster");
        $('#download_icon_container').text("");
    }
    //Load Wide CSS Rules
    else if (1776 >= browserWidth  && browserWidth >= 1280){
//        if ($("#player_container").next().attr('id') == 'slideshow_container') {
//            $("#player_container").insertAfter("#slideshow_container");
//        }
        $(".thinable").removeClass("thin");
        $(".tiny_able").removeClass("tiny");
        $(".wide_able").removeClass("wide");

//        $('link').attr('href', '/static/yap/css/yap_wide.css');
        $('#logo').text("yapster");
        $('#download_icon_container').text("");
    }
    //Load Wider CSS Rules
    else if (browserWidth > 1776){
//        if ($("#player_container").next().attr('id') == 'slideshow_container') {
//            $("#player_container").insertAfter("#slideshow_container");
//        }
        $(".thinable").removeClass("thin");
        $(".tiny_able").removeClass("tiny");
        $(".wide_able").addClass("wide");

//        $('link').attr('href', '/static/yap/css/yap_wide.css');
        $('#header_text2').text("yapster");
        $('#download_icon_container').text("");
    }
}

// Event: size window changed
function addEvent( obj, type, fn ){
    if (obj.addEventListener){
        obj.addEventListener( type, fn, false );
    }
    else if (obj.attachEvent){
        obj["e"+type+fn] = fn;
        obj[type+fn] = function(){ obj["e"+type+fn]( window.event ); }
        obj.attachEvent( "on"+type, obj[type+fn] );
    }
} //Run dynamicLayout function when page loads and when it resizes.
addEvent(window, 'load', dynamicLayout);
addEvent(window, 'resize', dynamicLayout);


// Check if tiny
function if_mobile()
{
    if( navigator.userAgent.match(/Android/i)
        || navigator.userAgent.match(/webOS/i)
        || navigator.userAgent.match(/iPhone/i)
        || navigator.userAgent.match(/iPad/i)
        || navigator.userAgent.match(/iPod/i)
        || navigator.userAgent.match(/BlackBerry/i)
        || navigator.userAgent.match(/Windows Phone/i)
        )
    {
        return true;
    }
    else
    {

        return false;
    }
}

$(document).ready(function(){
    // Slideshow
    var i = 1;
    setInterval(function() {
        $('#slideshow_image' + i.toString()).hide();
        i = i + 1;
        if (i == 5)
        {
            i = 1;
        }

        $('#slideshow_image' + i.toString()).show();
    }, 10000);



    $("#jquery_jplayer_1").jPlayer({
        swfPath: "http://jplayer.org/latest/js",
        supplied: 'm4a',
        ready: function () {
            $(this).jPlayer("setMedia", {
                m4a: $('#yap_audio_url').val()
            });
        }

    });

// Rotation picture Yap
//    var yap_picture = $("#yap_picture")[0]; // Get my yap_picture elem
//    var yap_picture_width, yap_picture_height;
//    $("<img/>") // Make in memory copy of image to avoid css issues
//        .attr("src", $(yap_picture).attr("src"))
//        .load(function() {
//            yap_picture_width = this.width;   // Note: $(this).width() will not
//            yap_picture_height = this.height; // work for in memory images.
//            if (yap_picture_width > yap_picture_height) {
//                $("#yap_picture_container").addClass("rotated_yap_picture");
//                var yap_picture_container = $('#yap_picture_container')[0];
//                $("#yap_picture").addClass("rotated_yap_picture");
//            }
//        });
});

