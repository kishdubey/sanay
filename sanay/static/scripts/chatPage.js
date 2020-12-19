document.addEventListener('DOMContentLoaded', () => {
  // enter submit message
  let msg = document.querySelector('#user-message');
  msg.addEventListener('keyup', event => {
    event.preventDefault();
    if (event.keyCode == 13) {
      document.querySelector('#send-message').click();
    }
  })
})
