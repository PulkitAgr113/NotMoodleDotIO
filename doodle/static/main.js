
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

socket.on('welcome', msg=>{
    handleAlert(msg, 'primary')
})

socket.on('leave', msg=>{
    handleAlert(msg, 'danger')
})

sendBtn.addEventListener('click',()=>{
    // messageInput.value = ""
    const message = messageInput.value
    console.log(message)
    socket.emit('message', message)
})

socket.on('messageToClients', msg=>{
    messageBox.innerHTML += `<b>${msg}</b><br>` 
})