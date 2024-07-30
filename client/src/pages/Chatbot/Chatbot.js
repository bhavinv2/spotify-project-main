import React, { useState, useEffect } from 'react';
import './Chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [accessToken, setAccessToken] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('spotifyAuthToken');
    if (token) {
      setAccessToken(token);
    }
  }, []);

  const handleSend = async () => {
    if (input.trim()) {
      const newMessages = [...messages, { text: input, user: true }];
      setMessages(newMessages);
      setInput('');

      try {
        const response = await fetch('http://localhost:5000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
          },
          body: JSON.stringify({ query: input }),
        });

        const data = await response.json();
        setMessages([...newMessages, { text: data.response, user: false }]);
      } catch (error) {
        console.error('Error fetching chatbot response:', error);
        setMessages([...newMessages, { text: 'Sorry, something went wrong.', user: false }]);
      }
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