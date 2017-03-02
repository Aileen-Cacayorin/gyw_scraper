$(function() {
      $('button#find').bind('click', function() {
        $.getJSON('/results', {

        }, function(data) {
          $("#message").text(data.message);
        });

      });
    });