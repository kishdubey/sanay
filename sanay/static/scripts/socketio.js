document.addEventListener('DOMContentLoaded', () => {
  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('message', data => {
    const p = document.createElement('p');
    const span_username = document.createElement('span');
    const span_timestamp = document.createElement('span');
    const br = document.createElement('br');
    span_username.innerHTML = data.username;
    span_timestamp.innerHTML = data.time_stamp;
    p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
    document.querySelector('#display-message-section').append(p);
  });

  socket.on('some-event', data => {
    console.log(data);
  });

  // Send Message
  document.querySelector('#send-message').onclick = () => {
    socket.send({'msg': document.querySelector('#user-message').value,
                'username': username });
  }
})
