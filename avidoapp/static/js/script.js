$(document).ready(function() {
  $('.advert-image').click(function() {
    var imageUrl = $(this).data('image-url');
    $('.main-image img').attr('src', imageUrl);
  });
});