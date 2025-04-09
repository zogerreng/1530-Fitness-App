const validUsers = [
    { username: "nicholas", password: "pass" },
    { username: "michael", password: "pass" },
    { username: "roger", password: "pass" },
    { username: "devansh", password: "pass" },
    { username: "maggie", password: "pass" } 
  ];
  
  document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const user = document.getElementById("username").value.trim();
    const pass = document.getElementById("password").value.trim();
    const isValid = validUsers.some(u => u.username === user && u.password === pass);
  
    if (isValid) {
      window.location.href = "dashboard.html";
    } else {
      document.getElementById("errorMsg").textContent = "Invalid credentials. Try again.";
    }
  });
  