document.addEventListener('DOMContentLoaded', () => {
  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  let room = "Coding";
  joinRoom("Coding");

  // Incoming message
  socket.on('message', data => {
    const p = document.createElement('p');
    const span_username = document.createElement('span');
    const span_timestamp = document.createElement('span');
    const predict = document.createElement('span')
    const br = document.createElement('br');

    if (data.username) {
      span_username.innerHTML = data.username;
      span_timestamp.innerHTML = data.time_stamp;
      predict.innerHTML = "";

      // setting prediction color
      let color = "black";
      if (data.prediction > 0){
        color = "green";
        predict.innerHTML = data.prediction+"%";

      }
      else if (data.prediction < 0){
        color = "red";
        predict.innerHTML = data.prediction*-1+"%";
      }

      predict.style.color = color;
      p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML + br.outerHTML + predict.outerHTML;
      document.querySelector('#display-message-section').append(p);
    }
    else {
      printSysMsg(data.msg);
    }

  });

  // Send Message
  document.querySelector('#send-message').onclick = () => {
    socket.send({'msg': document.querySelector('#user-message').value,
            'username': username, 'room': room});

    // Clear input after sending
    document.querySelector('#user-message').value = '';
  }

  // Room Selection
  document.querySelectorAll('.select-room').forEach(p => {
    p.onclick = () => {
      let newRoom = p.innerHTML;
      if (newRoom == room) {
        msg = `You are already in ${room} room.`;
        printSysMsg(msg);
      }
      else {
        leaveRoom(room);
        joinRoom(newRoom);
        room = newRoom;
      }
    }
  });

  // Leave room
  function leaveRoom(room) {
    socket.emit('leave', {'username': username, 'room': room});
  }

  // Join Room
  function joinRoom(room) {
    socket.emit('join', {'username': username, 'room': room});
    // clearing messages
    document.querySelector('#display-message-section').innerHTML = ''
  }
  // Print System Msg
  function printSysMsg(msg) {
    const p = document.createElement('p');
    p.innerHTML = msg;
    document.querySelector('#display-message-section').append(p);

  }


})
