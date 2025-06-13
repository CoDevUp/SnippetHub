
document.getElementById("snippet-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const form = e.target;

  const snippet = {
    title: form.title.value,
    language: form.language.value,
    content: form.content.value,
  };

  const msg = document.getElementById("create-msg");
  msg.textContent = "";

  try {
    const res = await apiRequest("/snippets/", "POST", snippet, true);
    msg.style.color = "green";
    msg.textContent = "Snippet creado exitosamente.";
    form.reset();
  } catch (err) {
    msg.style.color = "red";
    msg.textContent = err.message;
  }
});
