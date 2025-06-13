
document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("snippets-container");

  try {
    const snippets = await apiRequest("/snippets/");

    snippets.forEach(snippet => {
      const div = document.createElement("div");
      div.classList.add("snippet");

      div.innerHTML = `
        <h3>${snippet.title}</h3>
        <p><strong>Lenguaje:</strong> ${snippet.language}</p>
        <pre>${snippet.content}</pre>
        <p><em>Autor:</em> ${snippet.author} - ${new Date(snippet.created_at).toLocaleString()}</p>
        <hr>
      `;

      container.appendChild(div);
    });
  } catch (err) {
    container.innerHTML = `<p style="color:red;">Error al cargar snippets: ${err.message}</p>`;
  }
});
