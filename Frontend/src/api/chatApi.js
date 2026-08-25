const API_URL =
  "http://localhost:8000/api/chat";


export async function sendMessage(
  message,
  conversationId = "default"
) {

  const response = await fetch(
    API_URL,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({
        message,
        conversation_id:
          conversationId,
      }),
    }
  );


  const data =
    await response.json();


  if (!response.ok) {

    throw new Error(
      data.detail ||
      "Request failed"
    );

  }


  return data;
}