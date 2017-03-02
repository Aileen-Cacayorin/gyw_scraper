 $(function() {
    var submit_form = function(e) {
      $.getJSON('/_results', {
        brand_name: $('input[name="inputBrand"]').val()
      }, function(data) {
          if (data.color == "red") {
              $('#red-message').text(data.message);
          } else {
              $('#green-message').text(data.message);
          }
        $('#results').show();
        $('#brand-form').hide();
      });
      return false;
    };
    $('button#find').bind('click', submit_form);
    $('input[type=text]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });
  });
