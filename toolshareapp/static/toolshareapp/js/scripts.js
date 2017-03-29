$(document).ready(function()
{
    /*confirmation and error messages*/
    $('div.messages').slideDown().animate().animate();
    
    setTimeout(function() { $('div.messages').slideUp() }, 3000);
    $('div.messages').click(function() { $('div.messages').slideUp() });
});

formValidationArguments = {
    errorPlacement: function(error, element) {
        $(element).before(error);
    }
}

inlineFormValidationArguments = {
    errorPlacement: function(error, element) {
        $(element).next().after(error);
    }
}


