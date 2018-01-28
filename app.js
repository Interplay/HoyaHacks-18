$(document).ready(function() {
    $('.dropdown-button').dropdown('open');
    $('.dropdown-button').on('change', function() {
      if ( this.value == '1')
      {
        $("#jacob").show();
      }
      else
      {
        $("#jacob").hide();
      }
    });
});
