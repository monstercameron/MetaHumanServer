import React, { useState, useEffect } from 'react';
import style from './index.module.css';

const Index = (props) => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/data')
      .then(response => response.json())
      .then(data => setMessages(data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className={`container ${style.main}`}>
      <div className='row'>
        <div className="col-12">
          {messages.map((message, index) => (
            <div key={index}>
              {message.user}: {message.text}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Index;
