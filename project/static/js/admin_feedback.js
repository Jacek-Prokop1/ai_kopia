document.addEventListener("DOMContentLoaded", function() {
  // przełączanie sekcji Do oceny / Historia
  const toReviewBtn = document.getElementById("show-to-review");
  const historyBtn = document.getElementById("show-history");
  const toReviewDiv = document.getElementById("to-review");
  const historyDiv = document.getElementById("history");

  toReviewBtn.addEventListener("click", () => {
    toReviewDiv.style.display = "block";
    historyDiv.style.display = "none";
  });

  historyBtn.addEventListener("click", () => {
    toReviewDiv.style.display = "none";
    historyDiv.style.display = "block";
  });

  // toggle szczegóły feedbacku
  document.querySelectorAll(".feedback-item > strong").forEach(summary => {
    summary.addEventListener("click", function() {
      const fbId = this.parentElement.dataset.fbid;
      const details = this.parentElement.querySelector(".feedback-details");
      details.style.display = (details.style.display === "block") ? "none" : "block";
    });
  });

  // przyciski zatwierdź/odrzuć
  document.querySelectorAll(".btn-confirm, .btn-reject").forEach(button => {
    button.addEventListener("click", function(e) {
      e.stopPropagation(); // nie zamykaj szczegółów
      const fbId = this.dataset.fbid;
      const confirmed = this.classList.contains("btn-confirm");

      fetch("/admin/feedbacks/confirm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feedback_id: fbId, confirmed: confirmed })
      })
      .then(res => res.json())
      .then(res => {
        if(res.success) {
          // przenieś rekord do historii
          const item = document.getElementById("fb-" + fbId);
          if(item) {
            item.classList.remove("feedback-item");
            item.classList.add("feedback-item");
            item.classList.remove("confirmed","rejected");
            item.classList.add(res.admin_confirmed ? "confirmed" : "rejected");
            // usuń z do oceny
            if(item.parentElement.id === "to-review") item.remove();
            // dodaj do historii
            historyDiv.prepend(item);
          }
        } else {
          alert("Błąd: " + JSON.stringify(res));
        }
      })
      .catch(err => {
        console.error(err);
        alert("Wystąpił błąd podczas komunikacji z serwerem");
      });
    });
  });
});
