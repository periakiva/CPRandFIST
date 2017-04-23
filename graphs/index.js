var express = require("express");
    app = express();
    bodyParser = require("body-parser"),
    mongoose = require("mongoose"),
    passport = require("passport"),
    bodyParser = require("body-parser");
    History = require("./models/history.js");
    getHistory = require("./middleware/getHistory.js");

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static(__dirname));

mongoose.connect("mongodb://localhost/stocks");

//routes
app.get("/", function(req,res){
   res.render(__dirname + '/views/index.ejs');
});

app.get("/symbol=:sym", getHistory,function(req,res){
});

app.get("/symbol=/:sym1/:sym2/:sym3", function(req,res){
  var temp = {
    sym1: req.params.sym1,
    sym2: req.params.sym2,
    sym3: req.params.sym3
  };

  res.render(__dirname + "/views/index.ejs", {sym: temp});
});

app.post("/symbol", function(req,res){
  var sym1 = req.body.sym1,
      sym2 = req.body.sym2,
      sym3 = req.body.sym3;

  
  
  
if (sym1 === "AAPL" ||
	sym1 === "AXP" ||
	sym1 === "BA" ||
	sym1 === "CAT" ||
	sym1 === "CSCO" ||
	sym1 === "CVX" ||
	sym1 === "DD" ||
	sym1 === "DIS" ||
	sym1 === "GE" ||
	sym1 === "GS" ||
	sym1 === "HD" ||
	sym1 === "IBM" ||
	sym1 === "INTC" ||
	sym1 === "JNJ" ||
	sym1 === "JPM" ||
	sym1 === "KO" ||
	sym1 === "MCD" ||
	sym1 === "MMM" ||
	sym1 === "MRK" ||
	sym1 === "MSFT" ||
	sym1 === "NKE" ||
	sym1 === "PFE" ||
	sym1 === "PG" ||
	sym1 === "TRV" ||
	sym1 === "UNH" ||
	sym1 === "UTX" ||
	sym1 === "V" ||
	sym1 === "VZ" ||
	sym1 === "WMT" ||
	sym1 === "XOM"){
		sym3 = "DIA";
	}
else {
		sym3 = "^GSPC";
	}
	
if (sym1 === "AEP" || sym1 === "D" || sym1 === "DUK" ||
    sym1 === "EIX" || sym1 === "EXC" || sym1 === "NEE" ||
    sym1 === "PCG" || sym1 === "PPL" || sym1 === "SO" ||
    sym1 === "SRE"){
		sym2 = "IDU";
	} 

else if (sym1 === "AMZN" || sym1 === "CMCSA" || sym1 === "COST" ||
    sym1 === "CVS" || sym1 === "DIS" || sym1 === "HD" ||
    sym1 === "MCD" || sym1 === "PCLN" || sym1 === "SBUX" ||
    sym1 === "WMT"){
		sym2 = "IYC";
	}

else if (sym1 === "APC" || sym1 === "COP" || sym1 === "CVX" ||
    sym1 === "EOG" || sym1 === "HAL" || sym1 === "KMI" ||
    sym1 === "OXY" || sym1 === "PSX" || sym1 === "SLB" ||
    sym1 === "XOM"){
		sym2 = "IYE";
	}
	
else if (sym1 === "BAC" || sym1 === "BRKB" || sym1 === "C" ||
    sym1 === "GS" || sym1 === "JPM" || sym1 === "MA" ||
    sym1 === "MS" || sym1 === "PNC" || sym1 === "USB" ||
    sym1 === "V" || sym1 === "WFC"){
		sym2 = "IYG";
	}
	
else if (sym1 === "ABBV" || sym1 === "AMGN" || sym1 === "BMY" ||
    sym1 === "CELG" || sym1 === "GILD" || sym1 === "JNJ" ||
    sym1 === "MDT" || sym1 === "MRK" || sym1 === "PFE" ||
    sym1 === "UNH"){
		sym2 = "IYH";
	}
	
else if (sym1 === "ACN" || sym1 === "BA" || sym1 === "CAT" ||
    sym1 === "GE" || sym1 === "HON" || sym1 === "LMT" ||
    sym1 === "MMM" || sym1 === "UNP" || sym1 === "UPS" ||
    sym1 === "UTX"){
		sym2 = "IYJ";
	}
	
else if (sym1 === "CL" || sym1 === "GM" || sym1 === "KHC" ||
    sym1 === "KO" || sym1 === "MDLZ" || sym1 === "MO" ||
    sym1 === "NKE" || sym1 === "PEP" || sym1 === "PG" ||
    sym1 === "PM"){
		sym2 = "IYK";
	}
	
else if (sym1 === "APD" || sym1 === "DD" || sym1 === "DOW" ||
    sym1 === "ECL" || sym1 === "LYB" || sym1 === "MON" ||
    sym1 === "NEM" || sym1 === "NUE" || sym1 === "PPG" ||
    sym1 === "PX"){
		sym2 = "IYM";
	}
	
else if (sym1 === "AMT" || sym1 === "AVB" || sym1 === "CCI" ||
    sym1 === "EQIX" || sym1 === "EQR" || sym1 === "HCN" ||
    sym1 === "PLD" || sym1 === "PSA" || sym1 === "SPG" ||
    sym1 === "WY"){
		sym2 = "IYR";
	}
	
else if (sym1 === "ALK" || sym1 === "FDX" || sym1 === "JBHT" ||
    sym1 === "KSU" || sym1 === "LSTR" || sym1 === "NSC" ||
    sym1 === "R" || sym1 === "UAL" || sym1 === "UNP" ||
    sym1 === "UPS"){
		sym2 = "IYT";
	}
	
else if (sym1 === "AAPL" || sym1 === "AVGO" || sym1 === "CSCO" ||
    sym1 === "FB" || sym1 === "GOOGL" || sym1 === "IBM" ||
    sym1 === "INTC" || sym1 === "MSFT" || sym1 === "ORCL"){
		sym2 = "IYW";
	}
	
else if (sym1 === "CTL" || sym1 === "GSAT" || sym1 === "LVLT" ||
    sym1 === "S" || sym1 === "SBAC" || sym1 === "T" ||
    sym1 === "TDS" || sym1 === "TMUS" || sym1 === "VZ" ||
    sym1 === "WIN"){
		sym2 = "IYZ";
	}
	
else {
	sym2 = "IYY";
}

  res.redirect("/symbol=/"+sym1+"/"+ sym2 + "/" + sym3);
});

app.listen(8000,function(){
  console.log("Server Has Started");
});
