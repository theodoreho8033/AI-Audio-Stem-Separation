
var files;

function handleFiles3(event) {
  var files = event.target.files;
  var fd = new FormData();
  fd.append('file', files[0], "audio.mp3" /*, optional filename */)

  var req = jQuery.ajax({
    url: 'https://demucsproxy4gb1cpu-wfccdzqdja-uw.a.run.app/upload',
    method: 'POST',
    data: fd, // sends fields with filename mimetype etc
    // data: aFiles[0], // optional just sends the binary
    processData: false, // don't let jquery process the data
    contentType: false // let xhr set the content type
  });
  req.then(function (response) {
    console.log(response)
  }, function (xhr) {
    console.error('failed to fetch xhr', xhr)
  })
  //var files = event.target.files;
  //$("#src").attr("src", URL.createObjectURL(files[0]));
  //document.getElementById("audio").load();
}
function handleFiles2(event) {
  var files = event.target.files;
  $("#src").attr("src", URL.createObjectURL(files[0]));
  document.getElementById("audio").load();
}

function submit_audio() {
  $("#main").html("<p>File submitted, server processing this will take a couple minutes</p>");
  var fd = new FormData();
  fd.append('file', files[0], "audio.mp3" /*, optional filename */)
  console.log("test")
  var req = fetch('/upload',{
    
    method: 'POST',
    body: fd, // sends fields with filename mimetype etc
    // data: aFiles[0], // optional just sends the binary
    processData: false, // don't let jquery process the data
    contentType: false // let xhr set the content type
  });
  req.then(response => response.arrayBuffer()).then(data => {
    $("#main").html(' <p>successfully separated vocals, refresh to run again.</p> <audio id="audio" controls><source src="" id="src" /></audio>');
    const audioBlob = new Blob([data], { type: 'audio/mpeg' });
    const audioUrl = URL.createObjectURL(audioBlob);
    const audioElement = document.getElementById('audio');

    // Set the src attribute to the Blob URL
    audioElement.src = audioUrl;
    audioElement.load()
  })

}
function pre(event) {
  files = event.target.files;
}

window.onload = function () {
  document.getElementById("upload").addEventListener("change", pre, false);
}
