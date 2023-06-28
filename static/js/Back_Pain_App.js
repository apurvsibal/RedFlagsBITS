function hide_or_show_div(div) {
  var x = document.getElementById(div);
  if (x.style.display === "none") {
    x.style.display = "inline-block";
  } else {
    x.style.display = "none";
  }
}

function Enable_Submit(id) {
  var x = document.getElementById(id);
  x.disabled = false;
}

function Toggle_Enable_Submit(id) {
  var x = document.getElementById(id);
  x.disabled = !x.disabled;
}

document.addEventListener('DOMContentLoaded', function() {
  var uploadButton = document.getElementById('upload-button');
  uploadButton.addEventListener('click', function() {
    var fileInput = document.createElement('input');
    fileInput.type = 'file';

    fileInput.click();
    fileInput.addEventListener('change', function() {
      // Handle file selection or upload logic here
      console.log('File selected:', fileInput.files[0]);
      // You can use AJAX or other methods to upload the file to the server
      // You may also redirect to another page or perform any other actions
      document.body.removeChild(fileInput);
    });
  });
});
