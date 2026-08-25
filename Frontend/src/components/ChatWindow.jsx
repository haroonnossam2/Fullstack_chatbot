import React, {
  useEffect,
  useRef,
} from "react";

import Message from "./Message";


export default function ChatWindow({
  messages,
  loading,
}) {

  const bottomRef =
    useRef(null);


  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, loading]);


  return (
    <main className="chat-window">

      {messages.length === 0 && (

        <div className="welcome">

          <div className="welcome-icon">
            AI
          </div>

          <h2>
            How can we help?
          </h2>

          <p>
            Ask about orders,
            payments, refunds,
            delivery, or support.
          </p>

          <div className="examples">

            <div>
              Where is my order 12345?
            </div>

            <div>
              I was charged twice.
            </div>

            <div>
              What is your return policy?
            </div>

          </div>

        </div>

      )}


      {messages.map(
        (message, index) => (

          <Message
            key={index}
            message={message}
          />

        )
      )}


      {loading && (

        <div className="message-row assistant-row">

          <div className="message-bubble assistant-bubble">

            <div className="typing">

              <span></span>
              <span></span>
              <span></span>

            </div>

          </div>

        </div>

      )}


      <div ref={bottomRef} />

    </main>
  );
}