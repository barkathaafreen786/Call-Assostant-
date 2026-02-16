
import { useState, useEffect, useRef } from 'react';
import { Send, Zap, Shield, FileText, Info } from 'lucide-react';
import './App.css'; 

export default function App() {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: 'Hello! I am your BFSI Assistant. I can help with loans, EMIs, documentation, and banking policies.', 
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      source: 'system'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [health, setHealth] = useState({ status: 'unknown' });
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(() => setHealth({ status: 'offline' }));
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input, timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg.content })
      });
      
      const data = await res.json();
      
      const botMsg = { 
        role: 'assistant', 
        content: data.response, 
        source: data.source,
        confidence: data.confidence, 
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: "I'm unavailable right now. Please check if the backend is running.", isError: true, source: 'error' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div>
          <div className="logo-area">
            <div className="logo-icon">
              <Zap size={24} color="white" fill="white" />
            </div>
            <div>
              <h1 className="app-title">FinAssist AI</h1>
              <p className="app-subtitle">BFSI Support System</p>
            </div>
          </div>
          
          <div className="status-badge">
            <div className={`status-dot ${health.status === 'ok' ? 'online' : 'offline'}`} />
            <span>{health.status === 'ok' ? 'System Operational' : 'System Offline'}</span>
          </div>

          <div className="feature-list">
            <div className="feature-item">
              <FileText size={16} color="#4ade80" />
              <span>Dataset Knowledge (150+)</span>
            </div>
            <div className="feature-item">
              <Zap size={16} color="#facc15" />
              <span>Fine-Tuned SLM Engine</span>
            </div>
            <div className="feature-item">
              <Shield size={16} color="#a855f7" />
              <span>RAG Knowledge Base</span>
            </div>
          </div>
        </div>
        
        <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
          v1.0.0 • Local Secure Runtime
        </div>
      </aside>

      {/* Main Chat */}
      <main className="main-chat">
        <header className="chat-header">
           <div style={{display:'flex', alignItems:'center', gap:'10px'}}>
             <span style={{fontWeight:'600', fontSize:'0.9rem'}}>Current Session</span>
           </div>
           <Info size={20} color="#94a3b8" />
        </header>

        <div className="messages-area">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-row ${msg.role === 'user' ? 'user' : 'bot'}`}>
               {msg.role === 'assistant' && (
                 <div className="avatar">
                   <Zap size={16} color="#60a5fa" />
                 </div>
               )}
               
               <div>
                 <div className="message-bubble">
                   {msg.content}
                 </div>
                 
                 <div className="message-meta">
                   <span>{msg.timestamp}</span>
                   {msg.source && msg.source !== 'system' && (
                     <>
                       <span>•</span>
                       <span className={`source-tag ${msg.source}`}>
                         {msg.source.toUpperCase()}
                       </span>
                     </>
                   )}
                 </div>
               </div>
            </div>
          ))}
          
          {isLoading && (
             <div className="message-row bot">
               <div className="avatar"><Zap size={16} color="#60a5fa" /></div>
               <div className="typing-indicator" style={{ background: '#1e293b', padding: '12px 16px', borderRadius: '12px' }}>
                 <div className="status-dot" style={{ background: '#94a3b8', animation: 'typing 1.4s infinite -0.32s' }}></div>
                 <div className="status-dot" style={{ background: '#94a3b8', animation: 'typing 1.4s infinite -0.16s' }}></div>
                 <div className="status-dot" style={{ background: '#94a3b8', animation: 'typing 1.4s infinite' }}></div>
               </div>
             </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <div className="input-wrapper">
             <input 
               className="chat-input"
               placeholder="Ask about loans, interest rates, or policies..."
               value={input}
               onChange={(e) => setInput(e.target.value)}
               onKeyDown={(e) => e.key === 'Enter' && handleSend()}
               disabled={isLoading}
             />
             <button className="send-btn" onClick={handleSend} disabled={!input || isLoading}>
               <Send size={18} />
             </button>
          </div>
          <div style={{textAlign:'center', marginTop:'12px', fontSize:'0.7rem', color:'#64748b'}}>
            AI responses should be verified with official documents.
          </div>
        </div>
      </main>
    </div>
  );
}
