window.onload = function () {
  let toggle = document.querySelector(".toggle");

  let navigation = document.querySelector(".navigation");
  let main = document.querySelector(".main");
  let img = document.querySelector(".img");

  toggle.onclick = function () {
    navigation.classList.toggle("active");
    main.classList.toggle("active");
    img.element.toggle("active");
  };


 

};
