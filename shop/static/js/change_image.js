var b_image = document.getElementById("b_image");
var s_image = document.getElementById("s_image").getElementsByTagName("img");

for (var i = 0; i < s_image.length; i++) {
  s_image[i].addEventListener("click", full_image);
}

function full_image() {
  var ImageSRC = this.getAttribute("src");
  b_image.innerHTML = "<img width='400' height='400' src=" + ImageSRC + ">";
}
