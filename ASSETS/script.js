// ✅ Retrieve the stored JWT token from localStorage
function getToken() {
  return localStorage.getItem("token");
}

// ✅ Return headers with Authorization token
function getHeaders() {
  return {
    "Authorization": `Bearer ${getToken()}`, // Add Bearer prefix for standard JWT auth
    "Content-Type": "application/json"
  };
}

// ✅ Logout user by clearing token and redirecting to login page
function logout() {
  localStorage.clear();
  window.location.href = "login.html";  // Redirect to login page
}
