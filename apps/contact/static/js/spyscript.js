$(document).ready(function () {

    var isFocus = true;
    window.onblur = function () {spy_unactive()};
    window.onfocus = function () {spy_active()};
    
});



function spy_unactive () {
  isFocus = false;  
  var intId = setInterval(function(){
    if (isFocus == false){
      $.get('/updater-unactive/', function (data) {
          document.title = '('+(data)+') new request';
      });}
    else {
        clearInterval(intId);
    }
  },2000);
}


function spy_active () {
  isFocus = true;  
  var intId = setInterval(function(){
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
    else {
        clearInterval(intId);
    }
  },2000);
};
