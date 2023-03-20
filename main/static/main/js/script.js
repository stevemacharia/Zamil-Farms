///start of slider
$(document).ready(function () {
  $('#carouselExampleIndicators').find('.carousel-item').first().addClass('active');
});

$(document).ready(function(){
  $(".owl-carousel").owlCarousel(
      {
    "loop":true,
    "margin":10,
    "nav":true,
        "autoWidth":true,
    "items":4,
    "responsive":{
        0:{
            "items":1
        },
        600:{
            "items":3
        },
        1000:{
            "items":3
        }
    }
}
  );
});

///////end of slider


function change_image(image){

  var container = document.getElementById("main-image");

  container.src = image.src;
  }



  document.addEventListener("DOMContentLoaded", function(event) {


  });
