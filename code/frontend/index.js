var urlParams;
(window.onpopstate = function () {
    var match,
        pl     = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
        query  = window.location.search.substring(1);

    urlParams = {};
    while (match = search.exec(query))
       urlParams[decode(match[1])] = decode(match[2]);
})();

window.onload = function() {
  var image_element = document.getElementById('image-container')
  var pin_element = document.getElementById('pin')
  var button_element = document.getElementById('update')
  var pin_size_ratio = 0.035
  var x;
  var y;
  var processingUpdate = false;
   
  alertify.parent(image_element);
  alertify.maxLogItems(1);

  window.addEventListener('resize', updatePinLocation);

  image_element.addEventListener('click', function (e) {
    if (e.target !== this && e.target !== pin_element)
        return;
    x = (e.pageX - this.offsetLeft) / this.clientWidth
    y = (e.pageY - this.offsetTop) / this.clientHeight
    updatePinLocation()
  });

  function updatePinLocation() {
    var pin_size = pin_size_ratio * image_element.clientWidth
    var pin_x = x * image_element.clientWidth - pin_size / 2
    var pin_y = y * image_element.clientHeight - pin_size
    pin_element.setAttribute("style","width:" + pin_size + "px; height:" + pin_size + "px; display:block;top: " + pin_y + "px; left:" + pin_x + "px;");
  }

  document.getElementById('update').addEventListener('click', function (e) {
    if (!processingUpdate) {
      setProcessing(true)
      var name = urlParams.entityname;
      var loadingMsg = '<i class="fa fa-circle-o-notch fa-spin fa-fw"></i> Updating location for "' + name + '"'
      var successMsg = '<i class="fa fa-check fa-fw"></i> Successfully updated location for "' + name + '"'
      var errorMsg = '<i class="fa fa-times fa-fw"></i> There was an error while updating location for "' + name + '"'

      alertify.closeLogOnClick(true).log(loadingMsg);

      var url = 'https://1aw7zewd9c.execute-api.us-east-1.amazonaws.com/prod/addToMapDb?name=' 
        + name + "&x=" + x + "&y=" + y;

      var script = document.createElement('script');
      script.setAttribute('src', url);
      script.addEventListener('error', function () {
        scriptLoaded(false)
      })
      script.addEventListener('load', function (e) { 
        scriptLoaded(result.success)
      });
      document.head.appendChild(script);

      function scriptLoaded(success) {
          if (success) {
            setTimeout(function(){
              alertify.delay(4000).closeLogOnClick(true).success(successMsg);
              setProcessing(false)
            }, 3000);
          } else {
            setTimeout(function(){
              alertify.delay(4000).closeLogOnClick(true).error(errorMsg);
              setProcessing(false)
            }, 3000);
          }
          script.parentNode.removeChild(script)
      }
    }
  });

  
  function setProcessing(value) {
    processingUpdate = value;
    if (processingUpdate) {
      button_element.classList.add('button-disabled');
    } else {
      button_element.classList.remove('button-disabled');
    }
  }
}
