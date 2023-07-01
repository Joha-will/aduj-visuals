// Update button Js

$(document).ready(function(){
  $(".update-button").click(function(e){
    e.preventDefault();
    var form = $(this).prev('.update-form');
    form.submit();
  });
});