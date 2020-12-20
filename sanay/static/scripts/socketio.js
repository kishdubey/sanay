document.addEventListener('DOMContentLoaded', () => {
  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  const username = document.querySelector('#get-username').innerHTML;
  let room = "Coding"
  joinRoom("Coding");

  // Send messages
  document.querySelector('#send_message').onclick = () => {
      socket.emit('incoming-msg', {'msg': document.querySelector('#user-message').value,
        'username': username, 'room': room});

      // clear
      document.querySelector('#user-message').value = '';
  };

  // Incoming message
  socket.on('message', data => {
    if (data.msg) {
      const p = document.createElement('p');
      const span_username = document.createElement('span');
      const span_timestamp = document.createElement('span');
      const predict = document.createElement('span')
      const br = document.createElement('br')

      // this user message
      if (data.username == username) {
        p.setAttribute("class", "my-msg");

        span_username.setAttribute("class", "my-username");
        span_username.innerText = data.username;

        // Timestamp
        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = data.time_stamp;

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
        p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML + br.outerHTML + predict.outerHTML;

        document.querySelector('#display-message-section').append(p);
      }
      // Display other users' messages
      else if (typeof data.username !== 'undefined') {
        p.setAttribute("class", "others-msg");

        span_username.setAttribute("class", "other-username");
        span_username.innerText = data.username;

        // Timestamp
        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = data.time_stamp;

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
        p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML + br.outerHTML + predict.outerHTML;

        document.querySelector('#display-message-section').append(p);
      }
      else {
        printSysMsg(data.msg);
      }
    }
    scrollDownChatWindow();
  });

  // Room Selection
  document.querySelectorAll('.select-room').forEach(p => {
    p.onclick = () => {
      let newRoom = p.innerHTML;
      if (newRoom === room) {
        msg = `You are already in ${room} room.`;
        printSysMsg(msg);
      }
      else {
        leaveRoom(room);
        joinRoom(newRoom);
        room = newRoom;
      }
    };
  });

  // Logout
  document.querySelector("#logout-btn").onclick = () => {
      leaveRoom(room);
  };

  // Leave room
  function leaveRoom(room) {
      socket.emit('leave', {'username': username, 'room': room});

      document.querySelectorAll('.select-room').forEach(p => {
          p.style.color = "black";
      });
  }

  // Join Room
  function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});

        document.querySelector('#' + CSS.escape(room)).style.color = "#ffc107";
        document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "white";
        document.querySelector('#display-message-section').innerHTML = '';
        document.querySelector("#user-message").focus();
    }

  function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

  // Print System Msg
  function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        scrollDownChatWindow()

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
});
