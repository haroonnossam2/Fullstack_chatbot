import React from "react";


export default function AgentActivity({
  activity,
  agent,
}) {

  return (
    <details className="activity">

      <summary>
        Agent activity ·{" "}
        {agent}
      </summary>

      <div className="activity-list">

        {activity.map(
          (item, index) => (

            <div
              className="activity-item"
              key={index}
            >

              <span className="activity-dot">
                ●
              </span>

              <span>
                {item}
              </span>

            </div>

          )
        )}

      </div>

    </details>
  );
}