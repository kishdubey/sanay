document.addEventListener('DOMContentLoaded', () => {
  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', () => {
    socket.send('Connected!');
  });

  socket.on('message', data => {
    console.log(`Message recieved: ${data}`);
  });

})
