// ===============================
// ARMOURMIND WORKING SERVER (FINAL)
// ===============================

const express = require("express");
const cors = require("cors");
const path = require("path");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Serve ALL static files from this folder
app.use(express.static(__dirname));

// Home route
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

// Chat API route
app.post("/api/chat", (req, res) => {

    const msg = req.body.message?.toLowerCase() || "";
    let reply = "Please contact our enterprise team for detailed assistance.";

    if (msg.includes("price")) {
        reply = "Pricing depends on enterprise scope. Would you like to schedule a demo?";
    } 
    else if (msg.includes("demo")) {
        reply = "You can request a demo directly from our Demo page.";
    } 
    else if (msg.includes("features")) {
        reply = "We provide autonomous recon, AI exploit simulation, and adaptive defense automation.";
    } 
    else if (msg.includes("hello") || msg.includes("hi")) {
        reply = "Hello. How can I assist you regarding ArmourMind?";
    }

    res.json({ reply });
});

// Start server
const PORT = 5000;

app.listen(PORT, () => {
    console.log("=================================");
    console.log("Server running at:");
    console.log(`http://localhost:${PORT}`);
    console.log("=================================");
});