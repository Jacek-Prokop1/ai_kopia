document.addEventListener("DOMContentLoaded", () => {
  const thumbUp = document.getElementById("thumb-up");
  const thumbDown = document.getElementById("thumb-down");
  const feedbackContainer = document.getElementById("feedback-container");

  function sendFeedback(rating) {
    if (!window.currentFeedbackId) {
      console.warn("Feedback niedostępny - poczekaj na odpowiedź AI");
      return;
    }

    fetch("/feedback/rate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        feedback_id: window.currentFeedbackId,
        rating: rating
      })
    })
    .then(res => res.json())
    .then(res => {
      if(res.success) {
        console.log("Feedback zapisany:", rating);
        // ukryj kontener po kliknięciu
        feedbackContainer.style.display = "none";
      } else {
        console.error("Błąd zapisu feedbacku:", res);
      }
    });
  }

  [thumbUp, thumbDown].forEach((thumb) => {
    thumb.addEventListener("click", () => {
      // jeśli już ukryto kontener, ignorujemy kliknięcie
      if (feedbackContainer.style.display === "none") return;

      // usuwa zaznaczenie z obu
      thumbUp.classList.remove("selected", "up");
      thumbDown.classList.remove("selected", "down");

      // dodaje zaznaczenie do klikniętej ikony
      thumb.classList.add("selected");
      const rating = thumb.id === "thumb-up" ? "up" : "down";
      thumb.classList.add(rating);

      sendFeedback(rating);
    });
  });
});
