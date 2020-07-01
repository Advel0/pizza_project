

document.addEventListener('DOMContentLoaded', ()=>{
  dish_images = document.querySelectorAll('.dish_img');
  dish_images.forEach((dish_image)=>{
    dish_image.src=`/static/pizza/images/${dish_image.alt}.jpg`

  })

});
