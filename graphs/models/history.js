var mongoose = require("mongoose");

var historySchema = new mongoose.Schema({
    Symbol: String,
    Name: String,
    Historical: [{
        Volume: String,
        Symbol: String,
        Adj_Close: String,
        High: String,
        Low: String,
        Date: String,
        Close: String,
        Open: String
    }]
});

module.exports = mongoose.model("history", historySchema);