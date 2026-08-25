import React, {
  useState,
} from "react";

import ChatWindow
  from "./components/ChatWindow";

import ChatInput
  from "./components/ChatInput";

import {
  sendMessage,
} from "./api/chatApi";


export default function App() {

  const [
    messages,
    setMessages,
  ] = useState([]);


  const [
    input,
    setInput,
  ] = useState("");


  const [
    loading,
    setLoading,
  ] = useState(false);


  async function handleSend() {

    const message =
      input.trim();


    if (
      !message ||
      loading
    ) {

      return;

    }


    setMessages(
      current => [
        ...current,

        {
          role: "user",
          content: message,
        },
      ]
    );


    setInput("");

    setLoading(true);


    try {

      const result =
        await sendMessage(
          message,
          "demo-conversation"
        );


      setMessages(
        current => [
          ...current,

          {
            role: "assistant",

            content:
              result.response,

            agent:
              result.agent,

            activity:
              result.activity,
          },
        ]
      );

    }

    catch (error) {

      setMessages(
        current => [
          ...current,

          {
            role: "assistant",

            content:
              "Sorry, something went wrong: " +
              error.message,
          },
        ]
      );

    }

    finally {

      setLoading(false);

    }

  }


  return (
    <div className="app">

      <header className="header">

        <div>

          <h1>
            AI Customer Support
          </h1>

          <p>
            LangGraph Multi-Agent System
          </p>

        </div>


        <div className="online">

          <span>
            ●
          </span>

          Online

        </div>

      </header>


      <ChatWindow
        messages={messages}
        loading={loading}
      />


      <footer>

        <ChatInput
          value={input}
          onChange={setInput}
          onSend={handleSend}
          disabled={loading}
        />

        <div className="hint">
          Enter to send · Shift+Enter
          for a new line
        </div>

      </footer>

    </div>
  );
}