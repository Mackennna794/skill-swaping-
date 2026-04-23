import { useState, useEffect } from 'react';
import { Send, MessageCircle, LogOut, User, Home, Mail } from 'lucide-react';
import './App.css';

interface SkillUser {
  id: number;
  name: string;
  email: string;
  skills_offered: string;
  skills_wanted: string;
  bio: string;
}

interface ChatMessage {
  text: string;
  sender: string;
  timestamp: string;
}


// Sample data
const SAMPLE_USERS: SkillUser[] = [
  {
    id: 1,
    name: 'Alice Smith',
    email: 'alice@example.com',
    skills_offered: 'JavaScript, React',
    skills_wanted: 'Python, Design',
    bio: 'Full-stack developer passionate about learning'
  },
  {
    id: 2,
    name: 'Bob Johnson',
    email: 'bob@example.com',
    skills_offered: 'Python, Machine Learning',
    skills_wanted: 'Web Design, UX',
    bio: 'AI enthusiast and data scientist'
  },
  {
    id: 3,
    name: 'Carol Davis',
    email: 'carol@example.com',
    skills_offered: 'UI/UX Design, Figma',
    skills_wanted: 'JavaScript, Node.js',
    bio: 'Creative designer with 5+ years experience'
  }
];

export default function App() {
  const [page, setPage] = useState<'login' | 'register' | 'dashboard' | 'profile' | 'messages'>('login');
  const [currentUser, setCurrentUser] = useState<SkillUser | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [selectedUser, setSelectedUser] = useState<SkillUser | null>(null);
  const [messageText, setMessageText] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && password) {
      setCurrentUser({
        id: 999,
        name: 'You',
        email,
        skills_offered: 'JavaScript, Design',
        skills_wanted: 'Python, Music',
        bio: 'Learner and skill sharer'
      });
      setPage('dashboard');
    }
  };

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === confirmPassword && name) {
      setCurrentUser({
        id: 999,
        name,
        email,
        skills_offered: '',
        skills_wanted: '',
        bio: ''
      });
      setPage('dashboard');
    }
  };

  const sendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (messageText.trim()) {
      setMessages([...messages, {
        text: messageText,
        sender: 'You',
        timestamp: new Date().toLocaleTimeString()
      }]);
      setMessageText('');
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setPage('login');
    setEmail('');
    setPassword('');
    setMessages([]);
    setSelectedUser(null);
  };

  return (
    <div className="app-container">
      <div className="gradient-background"></div>

      {/* Navigation */}
      {currentUser && (
        <nav className="navigation">
          <div className="nav-content">
            <h1 className="app-logo">🔄 SkillSwap</h1>
            <div className="nav-links">
              <button
                className={`nav-link ${page === 'dashboard' ? 'active' : ''}`}
                onClick={() => setPage('dashboard')}
              >
                <Home size={20} /> Dashboard
              </button>
              <button
                className={`nav-link ${page === 'profile' ? 'active' : ''}`}
                onClick={() => setPage('profile')}
              >
                <User size={20} /> Profile
              </button>
              <button
                className={`nav-link ${page === 'messages' ? 'active' : ''}`}
                onClick={() => setPage('messages')}
              >
                <Mail size={20} /> Messages
              </button>
              <button className="nav-link logout" onClick={handleLogout}>
                <LogOut size={20} /> Logout
              </button>
            </div>
          </div>
        </nav>
      )}

      {/* Main Content */}
      <main className="main-content">
        {/* LOGIN PAGE */}
        {page === 'login' && !currentUser && (
          <div className="auth-container">
            <div className="auth-card">
              <div className="auth-header">
                <h2>Welcome to SkillSwap 👋</h2>
                <p>Exchange skills, learn together</p>
              </div>
              <form onSubmit={handleLogin} className="auth-form">
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button type="submit" className="btn-primary">
                  Login
                </button>
              </form>
              <p className="auth-switch">
                Don't have an account?{' '}
                <button onClick={() => setPage('register')} className="link-btn">
                  Sign up here
                </button>
              </p>
            </div>
          </div>
        )}

        {/* REGISTER PAGE */}
        {page === 'register' && !currentUser && (
          <div className="auth-container">
            <div className="auth-card">
              <div className="auth-header">
                <h2>Join SkillSwap ✨</h2>
                <p>Start sharing your skills today</p>
              </div>
              <form onSubmit={handleRegister} className="auth-form">
                <input
                  type="text"
                  placeholder="Full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
                <input
                  type="email"
                  placeholder="Email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Create password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Confirm password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
                <button type="submit" className="btn-primary">
                  Register
                </button>
              </form>
              <p className="auth-switch">
                Already have an account?{' '}
                <button onClick={() => setPage('login')} className="link-btn">
                  Login here
                </button>
              </p>
            </div>
          </div>
        )}

        {/* DASHBOARD */}
        {page === 'dashboard' && currentUser && (
          <div className="dashboard">
            <div className="hero-section">
              <h2>👥 Find Your Skill Match</h2>
              <p>Discover users and exchange your skills</p>
            </div>

            <div className="user-grid">
              {SAMPLE_USERS.map((user) => (
                <div key={user.id} className="user-card">
                  <div className="card-avatar">
                    <span className="avatar-emoji">👤</span>
                  </div>
                  <h3 className="card-name">{user.name}</h3>
                  <div className="card-skills">
                    <div className="skill-tag offers">
                      <span className="skill-emoji">🎓</span>
                      <span>{user.skills_offered}</span>
                    </div>
                    <div className="skill-tag wants">
                      <span className="skill-emoji">📚</span>
                      <span>{user.skills_wanted}</span>
                    </div>
                  </div>
                  {user.bio && <p className="card-bio">{user.bio}</p>}
                  <button
                    className="btn-message"
                    onClick={() => {
                      setSelectedUser(user);
                      setMessages([]);
                    }}
                  >
                    <MessageCircle size={18} /> Message
                  </button>
                </div>
              ))}
            </div>

            {/* Chat Modal */}
            {selectedUser && (
              <div className="modal-overlay">
                <div className="modal-card">
                  <div className="modal-header">
                    <h3>Message {selectedUser.name}</h3>
                    <button
                      className="modal-close"
                      onClick={() => setSelectedUser(null)}
                    >
                      ✕
                    </button>
                  </div>
                  <div className="chat-area">
                    {messages.map((msg, idx) => (
                      <div key={idx} className={`message ${msg.sender === 'You' ? 'sent' : 'received'}`}>
                        <p>{msg.text}</p>
                        <span className="msg-time">{msg.timestamp}</span>
                      </div>
                    ))}
                  </div>
                  <form onSubmit={sendMessage} className="message-form">
                    <input
                      type="text"
                      placeholder="Type your message..."
                      value={messageText}
                      onChange={(e) => setMessageText(e.target.value)}
                    />
                    <button type="submit" className="btn-send">
                      <Send size={20} />
                    </button>
                  </form>
                </div>
              </div>
            )}
          </div>
        )}

        {/* PROFILE */}
        {page === 'profile' && currentUser && (
          <div className="profile-page">
            <div className="profile-card">
              <div className="profile-header">
                <div className="profile-avatar">👤</div>
                <h2>{currentUser.name}</h2>
              </div>
              <div className="profile-info">
                <div className="info-item">
                  <label>Email</label>
                  <p>{currentUser.email}</p>
                </div>
                <div className="info-item">
                  <label>Skills Offered</label>
                  <p>{currentUser.skills_offered || 'Not set'}</p>
                </div>
                <div className="info-item">
                  <label>Skills Wanted</label>
                  <p>{currentUser.skills_wanted || 'Not set'}</p>
                </div>
                <div className="info-item">
                  <label>Bio</label>
                  <p>{currentUser.bio || 'No bio added'}</p>
                </div>
              </div>
              <button className="btn-primary">Edit Profile</button>
            </div>
          </div>
        )}

        {/* MESSAGES */}
        {page === 'messages' && currentUser && (
          <div className="messages-page">
            <h2>📬 Your Messages</h2>
            <div className="messages-list">
              {messages.length === 0 ? (
                <p className="no-messages">No messages yet. Start a conversation!</p>
              ) : (
                messages.map((msg, idx) => (
                  <div key={idx} className="message-item">
                    <strong>{msg.sender}</strong>
                    <p>{msg.text}</p>
                    <span className="msg-timestamp">{msg.timestamp}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
