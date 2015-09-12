/**
 * Created by tyler on 06.07.15.
 */
$(document).ready(function () {


    var csrftoken= $.cookie('csrftoken');

    function csrvSafeMethod(method){
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))

    };

    $.ajaxSetup({
        beforeSend:function(xhr,settings){
            if(!csrvSafeMethod(settings.type) && !this.crossDomain){
                xhr.setRequestHeader('X-CSRFToken',csrftoken)};
            loading()
        },
        complete:stopLoading
    });


    $('#birth_date').datepicker({
        dateFormat: 'yy-mm-dd'
    });

    $('#edit_form').submit(function (eve) {
        eve.preventDefault();
        var form = $.toJSON($(this).serializeArray());
        imageloader(function(image){
            var image_data = $.toJSON(image);
            sender(form,image_data);
        });
    });

    $('#cancel').on('click',function(eve){
        eve.preventDefault();
        history.back(1);
    });

function sender (form,image){
    $.post('/edit/',{form:form,image:image},function(data){
        $('#status').text(data).fadeIn('fast');
        console.log(data);
    });
};

function imageloader(callBack){
    var input = $('#photo');
    var file = input.prop('files')[0];
    console.log(file)
    var reader = new FileReader();
    reader.onload = function(){
        $('#image_picture').attr('src', reader.result);
        $('#image_picture').fadeIn('fast');
        callBack(reader.result);
        
    };
    if (file != null) {
        reader.readAsDataURL(file);
        }
    else{
        callBack(null)
    }
};


function loading(){
    $('input:enabled').prop('disabled',true);
    $('textarea:enabled').prop('disabled',true);
    $('#edit_wrapper').fadeIn('fast',function(){
        $('#loader').css('display','block')    
    });
};
function stopLoading(){
    $('input:disabled').prop('disabled',false);
    $('textarea:disabled').prop('disabled',false);
    $('#edit_wrapper').fadeOut('fast',function(){
        $('#loader').css('display','none')
    })    
};



});

