function hide_or_show_div(div) {
  var x = document.getElementById(div);
  if (x.style.display === "none") {
    x.style.display = "inline-block";
  } else {
    x.style.display = "none";
  }
}