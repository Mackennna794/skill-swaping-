import { useState, useEffect } from 'react';
import { Star, Heart, Video, MessageCircle, LogOut, Medal, XCircle, Send } from 'lucide-react';

interface User {
  id: string;
  name: string;
  offers: string;
  wants: string;
  score: number;
  maxScore: number;
  badges: string[];
}

interface ChatMessage {
  text: string;
  sender: string;
}

// --- MOCK DATA ---
const MOCK_USERS: User[] = [
  { id: '1', name: 'Buddy Bear', offers: 'Drawing', wants: 'Math', score: 85, maxScore: 100, badges: ['🎨', '🌟'] },
  { id: '2', name: 'Smarty Fox', offers: 'Coding', wants: 'Reading', score: 60, maxScore: 100, badges: ['💻'] },
  { id: '3', name: 'Math Wizard', offers: 'Math', wants: 'Drawing', score: 95, maxScore: 100, badges: ['🔢', '🏆'] },
];

const QUOTES = [
  "You are a star learner! ⭐",
  "Sharing is Caring! 💖",
  "Every expert was once a beginner! 🚀",
  "Yay for learning new things! 🎉"
];

// --- JITSI MAGIC CALL COMPONENT ---
function MagicCall({ roomName, onEnd }: { roomName: string; onEnd: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="bg-white rounded-[2rem] shadow-xl overflow-hidden border-8 border-[#BFFCC6] w-full max-w-4xl h-[80vh] flex flex-col">
        <div className="bg-[#BFFCC6] p-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">✨ Magic Video Call ✨</h2>
          <button 
            onClick={onEnd}
            className="p-2 bg-[#F1CBFF] text-gray-800 rounded-full shadow-[0_4px_0_#d8a8ea] active:shadow-[0_0px_0_#d8a8ea] active:translate-y-[4px] transition-all"
          >
            <XCircle size={32} />
          </button>
        </div>
        <div className="flex-1 bg-gray-100">
          <iframe
            src={`https://meet.jit.si/${roomName}`}
            allow="camera; microphone; fullscreen; display-capture"
            className="w-full h-full border-0"
          />
        </div>
      </div>
    </div>
  );
}

// --- MAIN APP COMPONENT ---
export default function App() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [quoteIndex, setQuoteIndex] = useState(0);
  const [activeCall, setActiveCall] = useState<string | null>(null);
  const [activeChat, setActiveChat] = useState<User | null>(null);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [messageInput, setMessageInput] = useState('');

  // My Personal Profile (Mocked)
  const myProfile: User = {
    id: 'me',
    name: 'You!',
    offers: 'Reading',
    wants: 'Coding',
    score: 450,
    maxScore: 500,
    badges: ['⭐', '🚀', '📚']
  };

  // Rotating Quote Timer
  useEffect(() => {
    const interval = setInterval(() => {
      setQuoteIndex((prev) => (prev + 1) % QUOTES.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Simple Mock Login
  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F1CBFF] p-4 font-sans">
        <div className="bg-white p-10 rounded-[2rem] shadow-xl text-center max-w-md w-full border-4 border-[#BFFCC6]">
          <Star className="w-20 h-20 mx-auto text-yellow-400 mb-6" fill="currentColor" />
          <h1 className="text-4xl font-black text-gray-800 mb-2">SkillShare Friends</h1>
          <p className="text-xl text-gray-600 mb-8">Play, Share, and Learn together!</p>
          <button 
            onClick={() => setCurrentUser(myProfile)}
            className="w-full py-4 bg-[#A7BED3] text-white text-2xl font-bold rounded-[2rem] shadow-[0_6px_0_#7a9bb8] active:shadow-[0_0px_0_#7a9bb8] active:translate-y-[6px] transition-all"
          >
            Come Play!
          </button>
        </div>
      </div>
    );
  }

  // Matching Logic: Find users who offer what I want, OR want what I offer
  const friendMatches = MOCK_USERS.filter(user => 
    user.offers === currentUser.wants || user.wants === currentUser.offers
  );

  const sendMessage = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!messageInput.trim()) return;
    setChatMessages([...chatMessages, { text: messageInput, sender: 'me' }]);
    setMessageInput('');
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-20 font-sans">
      {/* Header */}
      <header className="bg-[#BFFCC6] p-6 rounded-b-[2rem] shadow-md flex flex-col md:flex-row justify-between items-center mb-8 border-b-4 border-[#9ae8a2]">
        <div className="flex items-center gap-3">
          <Heart className="w-10 h-10 text-pink-400" fill="currentColor" />
          <h1 className="text-3xl font-black text-gray-800">SkillShare Friends</h1>
        </div>
        
        <div className="bg-white px-6 py-2 rounded-full shadow-inner my-4 md:my-0 border-2 border-dashed border-gray-300">
          <span className="text-xl font-bold text-gray-600 animate-pulse">
            {QUOTES[quoteIndex]}
          </span>
        </div>

        <button 
          onClick={() => setCurrentUser(null)}
          className="flex items-center gap-2 px-6 py-3 bg-[#F1CBFF] text-gray-800 font-bold rounded-[2rem] shadow-[0_4px_0_#d8a8ea] active:shadow-[0_0px_0_#d8a8ea] active:translate-y-[4px] transition-all"
        >
          <LogOut size={20} /> Bye Bye!
        </button>
      </header>

      <main className="max-w-6xl mx-auto px-4 space-y-8">
        
        {/* Profile Section */}
        <section className="bg-[#A7BED3] p-6 rounded-[2rem] shadow-lg border-4 border-white">
          <h2 className="text-3xl font-bold text-white mb-4 flex items-center gap-2">
            <Medal className="text-yellow-300" fill="currentColor" /> My Report Card
          </h2>
          <div className="bg-white p-6 rounded-[2rem]">
            <p className="text-xl font-bold mb-2 text-gray-700">Skill Score: {currentUser.score} / {currentUser.maxScore}</p>
            <div className="w-full bg-gray-200 rounded-full h-8 mb-4 overflow-hidden border-2 border-gray-300">
              <div className="bg-[#BFFCC6] h-8 rounded-full" style={{ width: `${(currentUser.score/currentUser.maxScore)*100}%` }}></div>
            </div>
            <div className="flex items-center gap-4 text-2xl font-bold text-gray-600">
              <span>My Badges:</span>
              <span className="text-4xl">⭐ 🚀 📚</span>
            </div>
            <div className="mt-4 flex gap-4 text-lg">
              <span className="bg-[#BFFCC6] px-4 py-2 rounded-full font-bold">I can teach: {currentUser.offers}</span>
              <span className="bg-[#F1CBFF] px-4 py-2 rounded-full font-bold">I want to learn: {currentUser.wants}</span>
            </div>
          </div>
        </section>

        {/* Matches Section */}
        <section>
          <h2 className="text-3xl font-bold text-gray-800 mb-6 pl-4">Friend Matches! 🧩</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {friendMatches.map(match => (
              <div key={match.id} className="bg-white p-6 rounded-[2rem] shadow-md border-4 border-[#F1CBFF] flex flex-col items-center text-center">
                <div className="w-24 h-24 bg-[#BFFCC6] rounded-full mb-4 flex items-center justify-center text-4xl border-4 border-white shadow-sm">
                  😊
                </div>
                <h3 className="text-2xl font-black text-gray-800 mb-2">{match.name}</h3>
                <div className="text-lg text-gray-600 mb-6 bg-gray-50 p-4 rounded-xl w-full">
                  <p>Has: <strong className="text-[#A7BED3]">{match.offers}</strong></p>
                  <p>Wants: <strong className="text-pink-400">{match.wants}</strong></p>
                </div>
                
                <div className="flex gap-4 w-full mt-auto">
                  <button 
                    onClick={() => setActiveChat(match)}
                    className="flex-1 py-3 bg-[#BFFCC6] text-gray-800 font-bold rounded-[2rem] shadow-[0_4px_0_#9ae8a2] active:shadow-[0_0px_0_#9ae8a2] active:translate-y-[4px] transition-all flex items-center justify-center gap-2"
                  >
                    <MessageCircle size={20} /> Chat
                  </button>
                  <button 
                    onClick={() => setActiveCall(`SkillShare-${match.id}-${currentUser.id}`)}
                    className="flex-1 py-3 bg-[#A7BED3] text-white font-bold rounded-[2rem] shadow-[0_4px_0_#7a9bb8] active:shadow-[0_0px_0_#7a9bb8] active:translate-y-[4px] transition-all flex items-center justify-center gap-2"
                  >
                    <Video size={20} /> Call
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Active Call Overlay */}
      {activeCall && (
        <MagicCall roomName={activeCall} onEnd={() => setActiveCall(null)} />
      )}

      {/* Chat Overlay */}
      {activeChat && (
        <div className="fixed bottom-4 right-4 w-80 bg-white rounded-[2rem] shadow-2xl border-4 border-[#BFFCC6] overflow-hidden flex flex-col h-96 z-40">
          <div className="bg-[#BFFCC6] p-4 flex justify-between items-center">
            <h3 className="font-bold text-gray-800">Chat with {activeChat.name}</h3>
            <button onClick={() => setActiveChat(null)} className="text-gray-600 hover:text-black">
              <XCircle size={24} />
            </button>
          </div>
          <div className="flex-1 p-4 bg-gray-50 overflow-y-auto flex flex-col gap-2">
            <div className="bg-gray-200 self-start p-3 rounded-2xl rounded-tl-none">Hi! Want to swap skills?</div>
            {chatMessages.map((msg, idx) => (
              <div key={idx} className="bg-[#A7BED3] text-white self-end p-3 rounded-2xl rounded-tr-none">
                {msg.text}
              </div>
            ))}
          </div>
          <form onSubmit={sendMessage} className="p-3 bg-white border-t flex gap-2">
            <input 
              type="text" 
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              placeholder="Say hello..." 
              className="flex-1 bg-gray-100 rounded-full px-4 outline-none"
            />
            <button type="submit" className="bg-[#F1CBFF] p-3 rounded-full shadow-[0_2px_0_#d8a8ea] active:translate-y-[2px] active:shadow-none">
              <Send size={18} />
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
