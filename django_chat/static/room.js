const chatLog = document.querySelector('#chat-log')
const roomName = JSON.parse(document.getElementById('room-name').textContent);

if (!chatLog.hasChildNodes()) {
    const emptyText = document.createElement('h3')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'No Messages'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}
const ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';

const chatSocket = new WebSocket(
    ws_scheme
    + '://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageElement = document.createElement('div')
    const userId = data['user']['id']
    const loggedInUserId = JSON.parse(document.getElementById('user_id').textContent)
    
    // Create the avatar image element
    const avatarElement = document.createElement('img');
    avatarElement.src = data['user']['avatar'];
    avatarElement.alt = `${data['user']['username']}'s avatar`;
    avatarElement.classList.add('avatar');

    // Create the username strong element
    const usernameElement = document.createElement('strong');
    usernameElement.innerText = data['user']['username'];

    // Create the message content span
    const messageContentElement = document.createElement('span');
    messageContentElement.innerText = `: ${data.message}`;

    // Append the avatar, username, and message content to the message element
    messageElement.appendChild(avatarElement);
    messageElement.appendChild(usernameElement);
    messageElement.appendChild(messageContentElement);

    if (userId === loggedInUserId) {
        messageElement.classList.add('message', 'sender')
    } else {
        messageElement.classList.add('message', 'receiver')
    }

    chatLog.appendChild(messageElement)

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }
};

chatSocket.onclose = function(e) {
    console.log(e)
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};