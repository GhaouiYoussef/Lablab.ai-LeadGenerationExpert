const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose
  .connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("Error connecting to MongoDB:", err));

// API Endpoint to Fetch Discussion
app.get("/api/agents-discussion", async (req, res) => {
  try {
    //print
    console.log("fetching discussion history");
    // Fetch discussion history and summary

    console.log(discussions);
    console.log(summary);
    // Respond with the discussion history

    res.json({ history: discussions, summary: summary ? summary.summary : "" });
  } catch (err) {
    res.status(500).json({ error: "Error fetching discussion" });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});