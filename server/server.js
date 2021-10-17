const http = require('http')
const server = http.createServer() 

const socketio = require('socket.io')

const io = socketio(server, {
    cors : {
        origin : 'http://127.0.0.1:8000',
        methods : ["GET", "POST"]
    }
})

var usersInRoom = {}

io.on('connection', socket=> {
    // console.log('connected')
    // console.log(socket.id)
    let room = ''

    socket.on('joinDetails', details=>{
        room = details['roomCode']
        socket.join(room)
        socket.username = details['userName']
        // console.log(socket.username)

        if(!usersInRoom.hasOwnProperty(details['roomCode'])) {
            usersInRoom[room] = [] 
        }

        usersInRoom[room].push(details['userName'])

        // Broadcast welcome to other users. 
        socket.to(room).emit('welcome', details['userName']+' entered the chat')
        io.in(room).emit('roomdetails',usersInRoom[room])
    })

    // Enter message in chat
    socket.on('message', msg=>{
        // console.log(msg)
        socket.broadcast.to(room).emit('messageToClients', msg)
    })

    // Broadcast data about the canvas
    socket.on('drawing', (diagram)=>{
        socket.broadcast.to(room).emit('drawing', diagram);
    })

    // Broadcast leave message .
    socket.on('disconnect',()=>{
        userName = socket.username
        if(!usersInRoom.hasOwnProperty(room)) {
            return
        }
        const index = usersInRoom[room].indexOf(userName);
        if (index > -1) {
            usersInRoom[room].splice(index, 1);
        }
        io.to(room).emit('roomdetails',usersInRoom[room])
        io.to(room).emit('leave', 'user left the chat')
    })
})

server.listen(8000, ()=> console.log('listening on port 8000'))
