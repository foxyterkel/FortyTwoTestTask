$(document).ready(function () {
    spy()
});
function spy(){
  setInterval(function(){
      $.get('/updater/', function (data) {
          $('#spy').text(data)
          document.title = '('+(data)+') new request'
      })
  },3000)
};