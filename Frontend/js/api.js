
const API_BASE_URL = "http://127.0.0.1:8000"; 

// Función para hacer peticiones con/ sin token
async function apiRequest(endpoint, method = "GET", body = null, auth = false) {
  const headers = {
    "Content-Type": "application/json"
  };

  if (auth) {
    const token = localStorage.getItem("access_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Error desconocido");
  }

  return await response.json();
}
