import React, { useState } from 'react';
import './Chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, user: true }]);
      setInput('');
      // Placeholder for sending input to the backend and getting a response
      setMessages([...messages, { text: input, user: true }, { text: 'This is a response', user: false }]);
    }
  };

  return (
    <div className="chatbot">
      <h2>Chat with Your Stats</h2>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.user ? 'user' : 'bot'}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Type a message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default Chatbot;