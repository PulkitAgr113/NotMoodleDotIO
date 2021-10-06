const http = require('http')
const server = http.createServer() 

const socketio = require('socket.io')

const io = socketio(server, {
    cors : {
        origin : 'http://127.0.0.1:8000',
        methods : ["GET", "POST"]
    }
})

const room = 'testRoom'

io.on('connection', socket=> {
    console.log('connected')
    console.log(socket.id)

    socket.join(room)

    // Broadcast welcome to other users. 
    socket.broadcast.emit('welcome', 'A new user entered the chat')

    // Enter message in chat
    socket.on('message', msg=>{
        console.log(msg)
        io.to(room).emit('messageToClients', msg)
    })

    // Broadcast leave message .
    socket.on('disconnect',()=>{
        io.to(room).emit('leave', 'user left the chat')
    })
})

server.listen(8000, ()=> console.log('listening on port 8000'))
