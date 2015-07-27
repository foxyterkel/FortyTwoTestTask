$(document).ready(function () {
    spy()
});
function spy(){
  setInterval(function(){
      $.get('/updater/', function (data) {
          $('#spy').text(data)
      })
  },3000)
};