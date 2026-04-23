const express = require('express');
const session = require('express-session');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

// --- BACKEND LOGIC ---

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
// Using standard sessions for a straightforward, presentation-friendly login flow
app.use(session({ secret: 'skill-swap-secret', resave: false, saveUninitialized: true }));

// In-memory mock database
const users = {}; 
let interactionsCount = 0;

// Authentication Route
app.post('/api/login', (req, res) => {
    const { username } = req.body;
    if (!users[username]) {
        users[username] = { 
            username, 
            onboarded: false, 
            hobbies: '', 
            teachSkill: '', 
            learnSkill: '',
            interactions: 0,
            reviews: [],
            requests: []
        };
    }
    req.session.username = username;
    res.json({ success: true, user: users[username] });
});

// Profile Setup Route
app.post('/api/profile', (req, res) => {
    const { hobbies, teachSkill, learnSkill } = req.body;
    const username = req.session.username;
    if (username && users[username]) {
        users[username].hobbies = hobbies;
        users[username].teachSkill = teachSkill;
        users[username].learnSkill = learnSkill;
        users[username].onboarded = true;
        res.json({ success: true, user: users[username] });
    } else {
        res.status(401).json({ error: 'Not logged in' });
    }
});

// Get Dashboard Data
app.get('/api/dashboard', (req, res) => {
    const username = req.session.username;
    if (!username) return res.status(401).json({ error: 'Not logged in' });
    
    const otherUsers = Object.values(users).filter(u => u.username !== username && u.onboarded);
    res.json({ currentUser: users[username], peers: otherUsers });
});

// Complete Session Route (Increases stats and adds review)
app.post('/api/review', (req, res) => {
    const { peerName, reviewText } = req.body;
    const username = req.session.username;
    if (username && users[peerName]) {
        users[username].interactions += 1;
        users[peerName].interactions += 1;
        users[peerName].reviews.push(`Review from ${username}: ${reviewText}`);
        res.json({ success: true, currentUser: users[username] });
    }
});

// Real-time Socket & Bot Logic
io.on('connection', (socket) => {
    // Basic Support Bot Logic
    socket.on('bot-message', (msg) => {
        let reply = "Support Bot: I'm here to help! If you have connection issues, try refreshing. How else can I assist?";
        if (msg.toLowerCase().includes('secure')) {
            reply = "Support Bot: All interactions here are routed safely through our standard server connections.";
        }
        socket.emit('bot-reply', reply);
    });

    // WebRTC Signaling for Video Calling
    socket.on('join-room', (roomId) => {
        socket.join(roomId);
        socket.to(roomId).emit('user-connected', socket.id);
    });
    socket.on('offer', (offer, roomId) => socket.to(roomId).emit('offer', offer));
    socket.on('answer', (answer, roomId) => socket.to(roomId).emit('answer', answer));
    socket.on('ice-candidate', (candidate, roomId) => socket.to(roomId).emit('ice-candidate', candidate));
});

// --- FRONTEND CODE (Served on /) ---
const HTML_VIEW = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkillSwap Platform</title>
    <style>
        :root { --primary: #4F46E5; --bg: #F3F4F6; --card: #FFFFFF; --text: #1F2937; }
        body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .card { background: var(--card); padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        h1, h2, h3 { margin-top: 0; }
        input, button, textarea { width: 100%; padding: 12px; margin: 8px 0; border-radius: 6px; border: 1px solid #D1D5DB; box-sizing: border-box; }
        button { background: var(--primary); color: white; border: none; font-weight: bold; cursor: pointer; }
        button:hover { opacity: 0.9; }
        .hidden { display: none; }
        .peer-card { border: 1px solid #E5E7EB; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
        .video-container { display: flex; gap: 10px; margin-top: 10px; }
        video { width: 100%; max-width: 280px; background: #000; border-radius: 8px; }
        #bot-box { border: 1px solid #ccc; padding: 10px; height: 100px; overflow-y: auto; background: #fafafa; font-size: 14px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        
        <div id="loginView" class="card">
            <h1>SkillSwap Login</h1>
            <p>Enter a username to join the platform.</p>
            <input type="text" id="usernameInput" placeholder="Username">
            <button onclick="login()">Login / Register</button>
        </div>

        <div id="profileView" class="card hidden">
            <h2>Complete Your Profile</h2>
            <p>You must fill this out before accessing the dashboard.</p>
            <input type="text" id="hobbies" placeholder="Your Hobbies">
            <input type="text" id="teachSkill" placeholder="Skill you can teach (e.g., Python, Guitar)">
            <input type="text" id="learnSkill" placeholder="Skill you want to learn (e.g., Spanish, UI Design)">
            <button onclick="saveProfile()">Save Profile & Enter</button>
        </div>

        <div id="dashboardView" class="card hidden">
            <h2>Welcome, <span id="dashName"></span>!</h2>
            <div style="display:flex; justify-content: space-between; background: #e0e7ff; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                <span><strong>Interactions:</strong> <span id="dashInteractions">0</span></span>
                <span><strong>Teaching:</strong> <span id="dashTeach"></span></span>
            </div>

            <h3>Available Peers</h3>
            <div id="peersList"></div>

            <hr style="margin: 20px 0;">
            <h3>Need Help? Ask the Bot</h3>
            <div id="bot-box"></div>
            <div style="display:flex; gap:10px;">
                <input type="text" id="botInput" placeholder="Ask a question...">
                <button onclick="sendBotMessage()" style="width: auto;">Ask</button>
            </div>
        </div>

        <div id="videoView" class="card hidden">
            <h2>Live Session with <span id="sessionPeer"></span></h2>
            <div class="video-container">
                <video id="localVideo" autoplay muted playsinline></video>
                <video id="remoteVideo" autoplay playsinline></video>
            </div>
            
            <h3 style="margin-top:20px;">End Session & Review</h3>
            <textarea id="reviewText" placeholder="Leave a review for your peer..."></textarea>
            <button onclick="endSession()">Submit Review & Return</button>
        </div>

    </div>

    <script src="/socket.io/socket.io.js"></script>
    <script>
        const socket = io();
        let currentUser = null;
        let currentPeer = null;

        // Views
        const show = (id) => { document.querySelectorAll('.card').forEach(c => c.classList.add('hidden')); document.getElementById(id).classList.remove('hidden'); };

        async function login() {
            const username = document.getElementById('usernameInput').value;
            if(!username) return alert('Enter a username');
            const res = await fetch('/api/login', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username}) });
            const data = await res.json();
            currentUser = data.user;
            if(!currentUser.onboarded) show('profileView');
            else loadDashboard();
        }

        async function saveProfile() {
            const hobbies = document.getElementById('hobbies').value;
            const teachSkill = document.getElementById('teachSkill').value;
            const learnSkill = document.getElementById('learnSkill').value;
            if(!hobbies || !teachSkill || !learnSkill) return alert('Fill all fields to proceed.');
            
            const res = await fetch('/api/profile', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({hobbies, teachSkill, learnSkill}) });
            currentUser = (await res.json()).user;
            loadDashboard();
        }

        async function loadDashboard() {
            show('dashboardView');
            const res = await fetch('/api/dashboard');
            const data = await res.json();
            currentUser = data.currentUser;
            
            document.getElementById('dashName').innerText = currentUser.username;
            document.getElementById('dashInteractions').innerText = currentUser.interactions;
            document.getElementById('dashTeach').innerText = currentUser.teachSkill;

            const list = document.getElementById('peersList');
            list.innerHTML = '';
            if(data.peers.length === 0) list.innerHTML = '<p>No other users online yet. Open another tab to simulate!</p>';
            
            data.peers.forEach(peer => {
                const div = document.createElement('div');
                div.className = 'peer-card';
                div.innerHTML = \`
                    <strong>\${peer.username}</strong><br>
                    <small>Teaches: \${peer.teachSkill} | Wants to learn: \${peer.learnSkill}</small><br>
                    <small>Hobbies: \${peer.hobbies} | Interactions: \${peer.interactions}</small><br>
                    <button style="margin-top: 10px; background: #10B981;" onclick="startSession('\${peer.username}')">Swap Skills & Connect</button>
                \`;
                list.appendChild(div);
            });
        }

        // --- Video & Session Logic (Simplified WebRTC Prototype) ---
        async function startSession(peerName) {
            currentPeer = peerName;
            document.getElementById('sessionPeer').innerText = peerName;
            show('videoView');
            
            // Mocking the video stream initialization for presentation
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false }); // Audio false to prevent echo in testing
                document.getElementById('localVideo').srcObject = stream;
                // In a full WebRTC setup, this stream is sent to the peer via RTCPeerConnection.
                // For this single-file prototype, we simulate connection readiness.
                socket.emit('join-room', 'demo-room');
            } catch (err) {
                console.log("No camera detected, simulating session.");
            }
        }

        async function endSession() {
            const reviewText = document.getElementById('reviewText').value;
            if(!reviewText) return alert("Please leave a review!");
            
            await fetch('/api/review', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify({peerName: currentPeer, reviewText}) 
            });
            
            // Stop local camera
            const stream = document.getElementById('localVideo').srcObject;
            if(stream) stream.getTracks().forEach(track => track.stop());
            
            document.getElementById('reviewText').value = '';
            loadDashboard(); // Returns to dashboard with updated stats
        }

        // --- Bot Logic ---
        function sendBotMessage() {
            const input = document.getElementById('botInput');
            const box = document.getElementById('bot-box');
            if(!input.value) return;
            box.innerHTML += \`<div><strong>You:</strong> \${input.value}</div>\`;
            socket.emit('bot-message', input.value);
            input.value = '';
        }
        
        socket.on('bot-reply', (msg) => {
            const box = document.getElementById('bot-box');
            box.innerHTML += \`<div style="color:var(--primary)">\${msg}</div>\`;
            box.scrollTop = box.scrollHeight;
        });

    </script>
</body>
</html>
`;

app.get('/', (req, res) => {
    res.send(HTML_VIEW);
});

// Start Server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(\`SkillSwap app running at http://localhost:\${PORT}\`);
});