

document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const form = e.target;

  const data = {
    username: form.username.value,
    email: form.email.value,
    password: form.password.value,
    disable: form.disable.checked
  };

  const msg = document.getElementById("register-msg");
  msg.textContent = "";

  try {
    const res = await apiRequest("/users/register", "POST", data);
    msg.style.color = "green";
    msg.textContent = "Registro exitoso. Ahora puedes iniciar sesión.";
    form.reset();
  } catch (err) {
    msg.style.color = "red";
    msg.textContent = err.message;
  }
});
