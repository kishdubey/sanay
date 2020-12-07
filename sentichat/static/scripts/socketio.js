document.addEventListener('DOMContentLoaded', () => {
  var socket = io;
  socket.on('connect', function() {
    socket.send('Connected!');
  });

  socket.on('message', data => {
    // const p = document.createElement('p');
    // const br = document.createElement('br');
    // p.innerHTML = data;
    //document.querySelector('#display-message-section').append(p);
    console.log(`Message recieved: ${data}`);

  });

  socket.on('some-event', data => {
    console.log(data)
  });

  document.querySelector('#send-message').onclick = () => {
    socket.send(document.querySelector('#user-message').value);
  }

})
