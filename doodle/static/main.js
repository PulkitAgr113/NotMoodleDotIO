
const socket = io('http://localhost:8000')

const alertBox = document.getElementById('alert-box')
const messageBox = document.getElementById('messages-box')
const messageInput = document.getElementById('message-input')
const sendBtn = document.getElementById('send-btn')

const handleAlert = (msg, type) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
    setTimeout(() => {
        alertBox.innerHTML = ""
    }, 5000);
}

const roomCode = 10 ;
const userName = document.getElementById('username').value

socket.emit('joinDetails', {
    'roomCode': roomCode ,
    'userName': userName ,
})

socket.on('welcome', msg=>{
    handleAlert(msg, 'primary')
})

socket.on('leave', msg=>{
    handleAlert(msg, 'danger')
})

sendBtn.addEventListener('click',()=>{
   
    const message = messageInput.value
    if(messageInput.value == "") return
    messageInput.value = ""
    console.log(message)
    msg = {
        'message':message ,
        'username':userName ,
    }
    messageBox.innerHTML = `<div class="row justify-content-end" style="margin-bottom: 10px;">
                            <div class="col-4 msg-self">
                            <b>${userName}</b><br>
                            ${message}
                            </div></div>` + messageBox.innerHTML 
    socket.emit('message', msg)
})

socket.on('messageToClients', msg=>{
    // console.log('msg from server'+msg)
    messageBox.innerHTML = `<div class="row justify-content-start" style="margin-bottom: 10px;">
                            <div class="msg-other">
                            <b>${msg['username']}</b><br>
                            ${msg['message']}
                            </div></div>` + messageBox.innerHTML
})