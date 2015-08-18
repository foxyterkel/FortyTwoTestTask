$(document).ready(function () {

    var isFocus;
    window.onblur = function () {isFocus = false;};
    window.onfocus = function () {isFocus = true;};
    console.log(isFocus)
    start();


function start(){
    setInterval(function(){
        console.log(isFocus)
        if (isFocus == false){
                  $.get('/updater-unactive/', function (data) {
                      document.title = '('+(data)+') new request';
                  });}
        if (isFocus == true) {
            $.get('/updater-active/', function (data) {
              if (parseInt(data.number) > 0) {
                $.each(data.requests, function(index, el) {
                    if ($('#request_container div.panel').length == 10){
                        $('#request_container div.panel:last').remove()
                    }
                    $('#request_container').prepend('<div class="panel panel-default">\
                        <div class="panel-heading"> At '+el[1]+'</div>\
                        <div class="panel-body">'+el[0]+'</div></div>');
                    });
              };
              document.title = '(0) new request';
            });
        }   
    },2000);
}


});

