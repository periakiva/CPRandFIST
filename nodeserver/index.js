var express = require('express');

const MongoClient = require('mongodb').MongoClient;

var app = express();

app.use(function(req, res, next) {
	res.header('Access-Control-Allow-Origin', "*");
	res.header('Access-Control-Allow-Methods', 'GET,POST');
	res.header('Access-Control-Allow-Headers', 'Content-Type');
	next();
})

app.get('/:collection', function(req, res) {
	var url = 'mongodb://localhost/stocks';
	var beststocks = [{
	"_id" : "58fc10db421aa95182fe6cd4",
	"Rating" : 100,
	"Name" : "American Electric Power Company",
	"Symbol" : "AEP",
	"Suggestion" : "BUY",
	"Volatility" : 2.844734677769793
},
{
	"_id" : "58fc10dc421aa95182fe6d30",
	"Rating" : 100,
	"Name" : "Baker Hughes Incorporated",
	"Symbol" : "BHI",
	"Suggestion" : "BUY",
	"Volatility" : 4.720238572735198
},
{
	"_id" : "58fc10dc421aa95182fe6d60",
	"Rating" : 100,
	"Name" : "Chesapeake Energy Corporation",
	"Symbol" : "CHK",
	"Suggestion" : "BUY",
	"Volatility" : 1.958972638910506
},
{
	"_id" : "58fc10dc421aa95182fe6d68",
	"Rating" : 100,
	"Name" : "Colgate-Palmolive Company",
	"Symbol" : "CL",
	"Suggestion" : "BUY",
	"Volatility" : 1.3925594889169872
},
{
	"_id" : "58fc10dc421aa95182fe6d76",
	"Rating" : 100,
	"Name" : "CMS Energy Corporation",
	"Symbol" : "CMS",
	"Suggestion" : "BUY",
	"Volatility" : 1.5992577286439058
},
{
	"_id" : "58fc10dc421aa95182fe6d7a",
	"Rating" : 100,
	"Name" : "CenterPoint Energy, Inc (Holdin",
	"Symbol" : "CNP",
	"Suggestion" : "BUY",
	"Volatility" : 0.8656089866483399
},
{
	"_id" : "58fc10dc421aa95182fe6d84",
	"Rating" : 100,
	"Name" : "ConocoPhillips",
	"Symbol" : "COP",
	"Suggestion" : "BUY",
	"Volatility" : 9.52574090544249
},
{
	"_id" : "58fc10dc421aa95182fe6dae",
	"Rating" : 100,
	"Name" : "D.R. Horton, Inc.",
	"Symbol" : "DHI",
	"Suggestion" : "BUY",
	"Volatility" : 1.4611621274097644
},
{
	"_id" : "58fc10dc421aa95182fe6dca",
	"Rating" : 100,
	"Name" : "DTE Energy Company",
	"Symbol" : "DTE",
	"Suggestion" : "BUY",
	"Volatility" : 4.947259915981647
},
{
	"_id" : "58fc10dc421aa95182fe6dd4",
	"Rating" : 100,
	"Name" : "eBay Inc.",
	"Symbol" : "EBAY",
	"Suggestion" : "BUY",
	"Volatility" : 2.3833279618515633
}];

	res.end(JSON.stringify(beststocks));


	if (false) {
		MongoClient.connect(url).then(function(db) {
			if (req.params.collection === 'beststocks') {
				var collec = db.collection('beststocks');
				collec.find({}).toArray().then(function(docs) {
					res.end(JSON.stringify(docs));
				});
			} else if (req.params.collection === 'bestvol') {
				var collec = db.collection('bestvol');
				collec.find({}).toArray().then(function(docs) {
					res.end(JSON.stringify(docs));
				});
			} else if (req.params.collection === 'volatile') {
				var collec = db.collection('volatile');
				collec.find({}).toArray().then(function(docs) {
					res.end(JSON.stringify(docs));
				});
			}
		});
	}
});

app.listen(3000, function() {
	console.log("listening");
});


/*

#Volatile


{
	"_id" : "58fc10dc421aa95182fe6d73",
	"Rating" : 66,
	"Name" : "Chipotle Mexican Grill, Inc.",
	"Symbol" : "CMG",
	"Suggestion" : "SELL",
	"Volatility" : 109.4129632596979
}
{
	"_id" : "58fc10db421aa95182fe6cff",
	"Rating" : 66,
	"Name" : "Amazon.com, Inc.",
	"Symbol" : "AMZN",
	"Suggestion" : "SELL",
	"Volatility" : 105.51032392217803
}
{
	"_id" : "58fc10dd421aa95182fe6e8b",
	"Rating" : 66,
	"Name" : "Intuitive Surgical, Inc.",
	"Symbol" : "ISRG",
	"Suggestion" : "SELL",
	"Volatility" : 85.01975345568849
}
{
	"_id" : "58fc10dc421aa95182fe6d1b",
	"Rating" : 33,
	"Name" : "Acuity Brands Inc (Holding Comp",
	"Symbol" : "AYI",
	"Suggestion" : "SELL",
	"Volatility" : 67.52409050371102
}
{
	"_id" : "58fc10dd421aa95182fe6e47",
	"Rating" : 34,
	"Name" : "W.W. Grainger, Inc.",
	"Symbol" : "GWW",
	"Suggestion" : "SELL",
	"Volatility" : 65.21939515468199
}
{
	"_id" : "58fc10de421aa95182fe6f63",
	"Rating" : 84,
	"Name" : "The Priceline Group Inc.",
	"Symbol" : "PCLN",
	"Suggestion" : "HOLD",
	"Volatility" : 64.63764867401187
}
{
	"_id" : "58fc10dc421aa95182fe6d1d",
	"Rating" : 33,
	"Name" : "AutoZone, Inc.",
	"Symbol" : "AZO",
	"Suggestion" : "SELL",
	"Volatility" : 58.1413725311495
}
{
	"_id" : "58fc10df421aa95182fe6ffd",
	"Rating" : 49,
	"Name" : "Transdigm Group Incorporated Tr",
	"Symbol" : "TDG",
	"Suggestion" : "SELL",
	"Volatility" : 49.56182920472929
}
{
	"_id" : "58fc10df421aa95182fe704d",
	"Rating" : 66,
	"Name" : "Vertex Pharmaceuticals Incorpor",
	"Symbol" : "VRTX",
	"Suggestion" : "SELL",
	"Volatility" : 48.50536010739843
}
{
	"_id" : "58fc10dd421aa95182fe6e43",
	"Rating" : 67,
	"Name" : "Goldman Sachs Group, Inc. (The)",
	"Symbol" : "GS",
	"Suggestion" : "SELL",
	"Volatility" : 41.34223380532097
}





# Best volatile


{
	"_id" : "58fc10de421aa95182fe6f63",
	"Rating" : 84,
	"Name" : "The Priceline Group Inc.",
	"Symbol" : "PCLN",
	"Suggestion" : "HOLD",
	"Volatility" : 64.63764867401187
}
{
	"_id" : "58fc10dd421aa95182fe6e43",
	"Rating" : 67,
	"Name" : "Goldman Sachs Group, Inc. (The)",
	"Symbol" : "GS",
	"Suggestion" : "SELL",
	"Volatility" : 41.34223380532097
}
{
	"_id" : "58fc10dc421aa95182fe6d73",
	"Rating" : 66,
	"Name" : "Chipotle Mexican Grill, Inc.",
	"Symbol" : "CMG",
	"Suggestion" : "SELL",
	"Volatility" : 109.4129632596979
}
{
	"_id" : "58fc10db421aa95182fe6cff",
	"Rating" : 66,
	"Name" : "Amazon.com, Inc.",
	"Symbol" : "AMZN",
	"Suggestion" : "SELL",
	"Volatility" : 105.51032392217803
}
{
	"_id" : "58fc10dd421aa95182fe6e8b",
	"Rating" : 66,
	"Name" : "Intuitive Surgical, Inc.",
	"Symbol" : "ISRG",
	"Suggestion" : "SELL",
	"Volatility" : 85.01975345568849
}
{
	"_id" : "58fc10df421aa95182fe704d",
	"Rating" : 66,
	"Name" : "Vertex Pharmaceuticals Incorpor",
	"Symbol" : "VRTX",
	"Suggestion" : "SELL",
	"Volatility" : 48.50536010739843
}
{
	"_id" : "58fc10df421aa95182fe6ffd",
	"Rating" : 49,
	"Name" : "Transdigm Group Incorporated Tr",
	"Symbol" : "TDG",
	"Suggestion" : "SELL",
	"Volatility" : 49.56182920472929
}
{
	"_id" : "58fc10dd421aa95182fe6e47",
	"Rating" : 34,
	"Name" : "W.W. Grainger, Inc.",
	"Symbol" : "GWW",
	"Suggestion" : "SELL",
	"Volatility" : 65.21939515468199
}
{
	"_id" : "58fc10dc421aa95182fe6d1b",
	"Rating" : 33,
	"Name" : "Acuity Brands Inc (Holding Comp",
	"Symbol" : "AYI",
	"Suggestion" : "SELL",
	"Volatility" : 67.52409050371102
}
{
	"_id" : "58fc10dc421aa95182fe6d1d",
	"Rating" : 33,
	"Name" : "AutoZone, Inc.",
	"Symbol" : "AZO",
	"Suggestion" : "SELL",
	"Volatility" : 58.1413725311495
}
*/