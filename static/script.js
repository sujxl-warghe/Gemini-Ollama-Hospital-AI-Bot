const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");

const addMessage = (msg, cls) => {
  const div = document.createElement("div");
  div.className = `msg ${cls}`;
  div.innerHTML = msg;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
};

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user-msg");
  userInput.value = "";

  const formData = new FormData();
  formData.append("user_query", text);

  const res = await fetch("/chat", { method: "POST", body: formData });
  const data = await res.json();

  addMessage(data.response, "bot-msg");
});
