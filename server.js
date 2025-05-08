const express = require("express");
const cors = require("cors");
const path = require("path");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");

const app = express();
const PORT = 5000;


app.use(cors());
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

/*...................................................... Route ....................................................*/
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/viewdetails", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "LoginDetails.html"));
});

app.get("/ChatPage", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index2.html"));
});

app.get("/SignUP", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "SignUPPage.html"));
});

app.get("/nextpage", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html")); // You can change this to another page if needed
});

// API: Test Message
app.get("/api/message", (req, res) => {
  res.json({ message: "API is working!" });
});

/*..................................................... SignUp Route ................................................*/
app.post("/api/register", (req, res) => {
  const { name, email, password } = req.body;

  const nameValid = /^[A-Za-z\s]+$/.test(name);
  const emailValid = /^[a-zA-Z0-9._%+-]+@gmail\.com$/.test(email);

  if (!nameValid) {
    return res.status(400).json({ message: "Invalid name format." });
  }

  if (!emailValid) {
    return res.status(400).json({ message: "Invalid Gmail address." });
  }

  const python = spawn("python", ["SignUp.py", name, email, password]);

  python.stdout.on("data", (data) => {
    console.log(`Python Output: ${data}`);
  });

  python.stderr.on("data", (data) => {
    console.error(`Python Error: ${data}`);
  });

  python.on("close", (code) => {
    if (code === 0) {
      res.json({ message: "✅ You are registered!" });
    } else {
      res.status(500).json({ message: "❌ Failed to store user in DB." });
    }
  });
});
/*..................................................... SignUp Route ................................................*/

/*......................................................... Login Route ....................................................*/
app.post("/api/login", (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: "Email and password are required!" });
  }

  const python = spawn("python", ["LoginCheck.py", email, password]);

  python.stdout.on("data", (data) => {
    const output = data.toString().trim();
    console.log(`Python Output: ${output}`);
    if (output === "valid") {
      res.json({ message: "Login successful!", redirect: "/index2" });
    } else {
      res.status(400).json({ message: "Invalid credentials." });
    }
  });

  python.stderr.on("data", (data) => {
    console.error(`Python Error: ${data}`);
  });

  python.on("close", (code) => {
    console.log(`Python script exited with code ${code}`);
  });
});

app.get("/index2", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index2.html"));
});
/*-------------------------- Login Route ---------------------------*/

/*-------------------------- Start Server ---------------------------*/
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
