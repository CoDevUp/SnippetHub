

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const form = e.target;
  const username = form.username.value;
  const password = form.password.value;

  const errorMsg = document.getElementById("error-msg");
  errorMsg.textContent = "";

  try {
    const response = await fetch("http://127.0.0.1:8000/auth/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Credenciales incorrectas");
    }

    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
    window.location.href = "index.html";
  } catch (err) {
    errorMsg.textContent = err.message;
  }
});
