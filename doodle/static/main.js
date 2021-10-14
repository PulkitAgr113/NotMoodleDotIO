const socket = io('http://localhost:8000')

// Chatbox and Messaging

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

// Canvas and Drawings

const canvas = document.getElementsByClassName('whiteboard')[0];
const colors = document.getElementsByClassName('color');
const context = canvas.getContext('2d');
var rect = canvas.getBoundingClientRect();
// Stores current brush color
var current = {
    color: 'black'
};
// Whether pen is down or not
var drawing = false;

// Canvas events
canvas.addEventListener('mousedown', onMouseDown);
canvas.addEventListener('mouseup', onMouseUp);
canvas.addEventListener('mouseout', onMouseUp);
canvas.addEventListener('mousemove', throttle(onMouseMove, 10));

// Color button events
for (var i = 0; i < colors.length; i++){
    colors[i].addEventListener('click', onColorUpdate);
}

// Receiving broadcast
socket.on('drawing', onDrawingEvent);

// If window is resized
window.addEventListener('resize', onResize, false);
onResize();

// Utility Function
function drawLine(x0, y0, x1, y1, color, emit){
    // Drawing a line
    context.beginPath();
    context.moveTo(x0-rect.left, y0-rect.top);
    context.lineTo(x1-rect.left, y1-rect.top);
    context.strokeStyle = color;
    context.lineWidth = 2;
    context.stroke();
    context.closePath();

    if (!emit) { return; }
    var w = canvas.width;
    var h = canvas.height;

    // Sending ratios because height and width could vary
    socket.emit('drawing', {
      x0: x0 / w,
      y0: y0 / h,
      x1: x1 / w,
      y1: y1 / h,
      color: color
    });
}

// Position when down
function onMouseDown(e){
    drawing = true;
    current.x = e.clientX||e.touches[0].clientX;
    current.y = e.clientY||e.touches[0].clientY;
}

// Draw once the mouseUp event happens
function onMouseUp(e){
    if (!drawing) { return; }
    drawing = false;
    drawLine(current.x, current.y, e.clientX||e.touches[0].clientX, e.clientY||e.touches[0].clientY, current.color, true);
}

// Draw once the mouse moves
function onMouseMove(e){
    if (!drawing) { return; }
    drawLine(current.x, current.y, e.clientX||e.touches[0].clientX, e.clientY||e.touches[0].clientY, current.color, true);
    current.x = e.clientX||e.touches[0].clientX;
    current.y = e.clientY||e.touches[0].clientY;
}

// Colour change
function onColorUpdate(e){
    current.color = e.target.className.split(' ')[1];
}

// Drawing received from other sockets 
function onDrawingEvent(data){
    var w = canvas.width;
    var h = canvas.height;
    drawLine(data.x0 * w, data.y0 * h, data.x1 * w, data.y1 * h, data.color);
}

// limit the number of events per second
function throttle(callback, delay) {
    var previousCall = new Date().getTime();
    return function() {
        var time = new Date().getTime();

        if ((time - previousCall) >= delay) {
            previousCall = time;
            callback.apply(null, arguments);
        }
    };
}

// Making the canvas fill its encloser
function onResize() {
    canvas.width = window.innerWidth*0.50;
    canvas.height = window.innerWidth*0.50;
    rect = canvas.getBoundingClientRect();
}