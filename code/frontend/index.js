window.onload = function() {
  var image_element = document.getElementById('image-container')
  var pin_size_ratio = 0.027
  var x;
  var y;
   
  image_element.addEventListener('click', function (e) {
    if (e.target !== this)
        return;
    x = (e.pageX - this.offsetLeft) / this.clientWidth
    y = (e.pageY - this.offsetTop) / this.clientHeight

    document.getElementById("x").innerHTML="x: " + x; 
    document.getElementById("y").innerHTML="y: " + y; 
    console.log(e)
    updatePinLocation()
  });

  window.addEventListener('resize', function(e) {
    updatePinLocation();
  });

  function updatePinLocation() {
    var pin_size = pin_size_ratio * image_element.clientWidth
    var pin_x = x * image_element.clientWidth - pin_size / 2
    var pin_y = y * image_element.clientHeight - pin_size
    
    document.getElementById('pin')
      .setAttribute("style","width:" + pin_size + "px; height:" + pin_size + "px; display:block;top: " + pin_y + "px; left:" + pin_x + "px;");
  }

  new Clipboard('#copy', {
      text: function(trigger) {
          return x + "," + y
      }
  });
}
