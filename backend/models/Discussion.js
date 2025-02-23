const mongoose = require("mongoose");

const discussionSchema = new mongoose.Schema({
  agent: { type: String, required: true },
  message: { type: String, required: true },
});

const summarySchema = new mongoose.Schema({
  summary: { type: String, required: true },
});

const Discussion = mongoose.model("Discussion", discussionSchema);
const Summary = mongoose.model("Summary", summarySchema);

module.exports = { Discussion, Summary };