function registerUser() {
    const data = {
        name: document.getElementById("reg-name").value,
        email: document.getElementById("reg-email").value,
        password: document.getElementById("reg-password").value
    };

    fetch("http://127.0.0.1:5000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => alert(data.message || data.error));
}
function loginUser() {
    const data = {
        email: document.getElementById("log-email").value,
        password: document.getElementById("log-password").value
    };

    fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert("Welcome " + data.name);
            window.location.href = "dashboard.html";
        } else {
            alert(data.error);
        }
    });
}

fetch("http://127.0.0.1:5000/api/user")
  .then(res => res.json())
  .then(data => {
      if (!data.logged_in) {
          window.location.href = "login.html";
      }
  });

  function logout() {
    fetch("http://127.0.0.1:5000/api/logout")
    .then(() => window.location.href = "index.html");
}

