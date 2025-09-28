async function updateProgress() {
      try {
        let res = await fetch("{{ url_for('admin.progress') }}");
        let data = await res.json();

        if (data.total > 0) {
          let percent = (data.current / data.total) * 100;
          document.getElementById("progressBar").value = percent;
          document.getElementById("progressText").innerText =
            `${data.current} / ${data.total}`;
        }
      } catch (err) {
        console.error("Błąd pobierania progresu:", err);
      }
    }

setInterval(updateProgress, 1000);