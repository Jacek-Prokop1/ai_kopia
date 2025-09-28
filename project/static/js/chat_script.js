const chatContainer = document.getElementById('chat-container');
const textarea = document.getElementById('question');
const form = document.getElementById('chat-form');
const loading = document.getElementById('loading');

window.currentFeedbackId = null;
window.setFeedbackId = function(id) {
  window.currentFeedbackId = id;
};

function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
});

textarea.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event('submit'));
  }
});

form.addEventListener("submit", function(e) {
  e.preventDefault();
  const formData = new FormData(form);

  // pokaż feedback i nie resetujemy historii
  window.currentFeedbackId = window.currentFeedbackId || null;
  document.getElementById("feedback-container").style.display = "flex";

  const userDiv = document.createElement("div");
  userDiv.className = "message user";
  userDiv.innerHTML = "<strong>Ty:</strong><br>" + textarea.value;
  chatContainer.appendChild(userDiv);

  const aiDiv = document.createElement("div");
  aiDiv.className = "message assistant streaming";
  aiDiv.innerHTML = `<strong>AI:</strong><br><span class="ai-text"></span>`;
  chatContainer.appendChild(aiDiv);
  scrollToBottom();
  textarea.value = "";
  loading.style.display = "block";

  fetch("/stream", { method: "POST", body: formData })
    .then(response => {
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      function read() {
        reader.read().then(({ done, value }) => {
          if (done) {
            loading.style.display = "none";
            aiDiv.classList.remove("streaming");
            scrollToBottom();
            return;
          }

          const chunk = decoder.decode(value, { stream: true });

          chunk.split("\n\n").forEach(line => {
            if (line.startsWith("data:__FEEDBACK_ID__:")) {
              const id = line.replace("data:__FEEDBACK_ID__:", "").trim();
              window.setFeedbackId(id);
            } else if (line.startsWith("data:")) {
              const text = line.replace("data:", "");
              aiDiv.querySelector(".ai-text").textContent += text;
              scrollToBottom();
            }
          });
          read();
        });
      }
      read();
    });
});
