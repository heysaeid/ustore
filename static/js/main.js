jQuery(document).ready(function($){
    const data_id = $('.product-favorite p').attr('data-id'), cookie = getCookie('wishlist');
    let pmess = $('.st-message')
    if(getCookie(`review-${data_id}`) == 1){
        $('.submit-review').remove()
        pmess.show()
        pmess.text('You have already rated this post')
    }
    if(cookie.indexOf(data_id) != -1){
        $('.product-favorite p').text('Remove from favorites')
    }
    // jQuery sticky Menu
    
	$(".mainmenu-area").sticky({topSpacing:0});
    
    
    $('.product-carousel').owlCarousel({
        loop:true,
        nav:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:3,
            },
            1000:{
                items:5,
            }
        }
    });  
    
    $('.related-products-carousel').owlCarousel({
        loop:true,
        nav:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:2,
            },
            1000:{
                items:2,
            },
            1200:{
                items:3,
            }
        }
    });  
    
    $('.brand-list').owlCarousel({
        loop:true,
        nav:true,
        margin:20,
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:3,
            },
            1000:{
                items:4,
            }
        }
    });    
    
    
    // Bootstrap Mobile Menu fix
    $(".navbar-nav li a").click(function(){
        $(".navbar-collapse").removeClass('in');
    });    
    
    // jQuery Scroll effect
    $('.navbar-nav li a, .scroll-to-up').bind('click', function(event) {
        var $anchor = $(this);
        var headerH = $('.header-area').outerHeight();
        $('html, body').stop().animate({
            scrollTop : $($anchor.attr('href')).offset().top - headerH + "px"
        }, 1200, 'easeInOutExpo');

        event.preventDefault();
    });    
    
    /* 1. Visualizing things on Hover - See next part for action on click */
  $('#stars li').on('mouseover', function(){
    var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on
   
    // Now highlight all the stars that's not after the current hovered star
    $(this).parent().children('li.star').each(function(e){
      if (e < onStar) {
        $(this).addClass('hover');
      }
      else {
        $(this).removeClass('hover');
      }
    });
    
  }).on('mouseout', function(){
    $(this).parent().children('li.star').each(function(e){
      $(this).removeClass('hover');
    });
  });
  
  
  /* 2. Action to perform on click */
  $('#stars li').on('click', function(){
    var onStar = parseInt($(this).data('value'), 10); // The star currently selected
    var stars = $(this).parent().children('li.star');
    
    for (i = 0; i < stars.length; i++) {
      $(stars[i]).removeClass('selected');
    }
    
    for (i = 0; i < onStar; i++) {
      $(stars[i]).addClass('selected');
    }
    
    // JUST RESPONSE (Not needed)
    var ratingValue = parseInt($('#stars li.selected').last().data('value'), 10);
    $('#id_rating').val(ratingValue)
    
  });

    // Bootstrap ScrollPSY
    $('body').scrollspy({ 
        target: '.navbar-collapse',
        offset: 95
    })      
});

  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-10146041-21', 'auto');
  ga('send', 'pageview');

    function setCookie(name,value,days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }

  $('#form-review').submit(function(e){
      e.preventDefault()
      const data_id = $('.product-favorite p').attr('data-id')
      let pmess = $('.st-message') 
      $.ajax({
          type:'POST',
          data: $(this).serialize(),
          success: function(response){
              console.log(response)
              pmess.css('display', 'block')
              if(response.status == 'ok'){
                pmess.css('color', 'green')
                pmess.text('Your comment was successfully submitted')
                setCookie(`review-${data_id}`, 1, 5)
                $('.submit-review').remove()
              }else{
                  pmess.css('color', 'red')
                  pmess.text(response.error)
              }
          },
          error: function(error){
              console.log(error)
          },
      })
  })

$('.product-favorite p').click(function(){
    let cookie = getCookie('wishlist')
    let msg = 'This product was added to favorites', txt = 'Remove from favorites'
    const data_id = $(this).attr('data-id')
    if(cookie == null){
        setCookie('wishlist', [data_id], 5)
    }else if(cookie.indexOf(data_id) == -1){
        setCookie('wishlist', cookie + data_id, 5)
    }else{
        msg = 'This product was removed from favorites'
        txt = 'Add to favorites'
        setCookie('wishlist', cookie.replace(data_id, ''), 5)
    }
    $(this).text(txt)
    alert(msg)
})

$('.button_added').click(function(){
    const action = $(this).attr('data-action')
    let input = $(this).parent().find('.qty'), quantity = parseInt(input.val())
    if(action=='plus' && quantity < 10){
        input.val(quantity+1)
    }else if(action=='minus' && quantity > 1){
        input.val(quantity-1)
    }
})

$('input[name=update_cart]').click(function(e){
    e.preventDefault()
    let data = $('#form_update_cart').serialize()
    const action = $('#form_update_cart').attr('action')
    $.ajax({
        type: 'POST',
        url: action,
        data: data,
        success: function(response){
            if(response.status=='ok'){
                alert('Cart was updated')
            }else{
                alert(response.error)
            }
        },
        error: function(error){
            console.log(error)
        }
    })
})