document.addEventListener('DOMContentLoaded', () => {
  var socket = io();
  socket.on('connect', function() {
  socket.send('Connected!');
  });
  socket.on('message', data => {
    console.log(`Message Recieved: ${data}`)
  });
})
