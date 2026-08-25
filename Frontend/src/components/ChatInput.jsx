import React from "react";


export default function ChatInput({
  value,
  onChange,
  onSend,
  disabled,
}) {

  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      onSend();

    }

  }


  return (
    <div className="chat-input-container">

      <textarea
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        disabled={disabled}
        rows={1}
      />

      <button
        onClick={onSend}
        disabled={
          disabled ||
          !value.trim()
        }
      >
        Send
      </button>

    </div>
  );
}