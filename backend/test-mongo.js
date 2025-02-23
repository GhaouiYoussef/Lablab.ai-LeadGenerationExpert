const mongoose = require("mongoose");
require("dotenv").config();

// Define the Mongoose models
const DiscussionSchema = new mongoose.Schema({
  agent: String,
  message: String,
  timestamp: { type: Date, default: Date.now },
});

const SummarySchema = new mongoose.Schema({
  summary: String,
  timestamp: { type: Date, default: Date.now },
});

const Discussion = mongoose.model("Discussion", DiscussionSchema);
const Summary = mongoose.model("Summary", SummarySchema);

// Connect to MongoDB
mongoose
  .connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("Error connecting to MongoDB:", err));

// Function to insert example data
const insertExampleData = async () => {
  try {
    // Insert example discussion history
    const discussions = await Discussion.insertMany([
      { agent: "Agent1", message: "Hello, how can I help you?" },
      { agent: "Agent2", message: "I need assistance with my account." },
    ]);

    console.log("Inserted discussions:", discussions);

    // Insert example summary
    const summary = await Summary.create({
      summary: "This is a test summary of the discussion.",
    });

    console.log("Inserted summary:", summary);

    console.log("Example data inserted successfully!");
  } catch (err) {
    console.error("Error inserting example data:", err);
  } finally {
    // Close the connection
    mongoose.connection.close();
  }
};

// Run the function
insertExampleData();