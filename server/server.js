const http = require('http')
const server = http.createServer() 

const socketio = require('socket.io')

const io = socketio(server, {
    cors : {
        origin : 'http://127.0.0.1:8000',
        methods : ["GET", "POST"]
    }
})

var room = 'testRoom'

io.on('connection', socket=> {
    // console.log('connected')
    // console.log(socket.id)

    socket.on('joinDetails', details=>{
        room = details['roomCode']
        socket.join(details['roomCode'])

        // Broadcast welcome to other users. 
        socket.broadcast.to(room).emit('welcome', details['userName']+' entered the chat')
    })

    // Enter message in chat
    socket.on('message', msg=>{
        console.log(msg)
        socket.broadcast.to(room).emit('messageToClients', msg)
    })

    // Broadcast data about the canvas
    socket.on('drawing', (diagram)=>{
        socket.broadcast.emit('drawing', diagram);
    })

    // Broadcast leave message .
    socket.on('disconnect',()=>{
        io.to(room).emit('leave', 'user left the chat')
    })
})

server.listen(8000, ()=> console.log('listening on port 8000'))
