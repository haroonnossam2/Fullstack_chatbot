import React from "react";

import AgentActivity
  from "./AgentActivity";


export default function Message({
  message,
}) {

  const isUser =
    message.role === "user";


  return (
    <div
      className={
        "message-row " +
        (isUser
          ? "user-row"
          : "assistant-row")
      }
    >

      <div
        className={
          "message-bubble " +
          (isUser
            ? "user-bubble"
            : "assistant-bubble")
        }
      >

        <div>
          {message.content}
        </div>


        {!isUser &&
          message.activity &&
          message.activity.length > 0 && (

            <AgentActivity
              activity={
                message.activity
              }
              agent={
                message.agent
              }
            />

          )}

      </div>

    </div>
  );
}