$(document).ready(function(){

    var csrftoken= $.cookie('csrftoken');

    function csrvSafeMethod(method){
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
    };


    $.ajaxSetup({
        beforeSend:function(xhr,settings){
            if(!csrvSafeMethod(settings.type) && !this.crossDomain){
                xhr.setRequestHeader('X-CSRFToken',csrftoken)};
        }
    });

    function priority_handler () {
        pk = $(this).data('name');
        direct = $(this).data('direct');
        $.post('/move-priority/', {pk: pk, direct: direct}, function(data){
            if (data == 'done') {
                    if (direct == 'up') {
                        $('#label_'+pk).text(function(){
                            var init = $('#label_'+pk).text();
                            var res = parseInt(init)+1;
                            return res;
                        })
                    }
                    else {
                        $('#label_'+pk).text(function(){
                            var init = $('#label_'+pk).text();
                            var res = parseInt(init)-1;
                            return res;
                        })
                    }
            }

        })

    }

    $(document).on('click','.move-btn', priority_handler)

});