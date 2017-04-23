var History = require("../models/history.js");

function createJSON(name, data){
    return(
        {
            "chart": {
                "caption": String(name),
                "subCaption": "40-Day Prices",
                "xAxisName": "Day",
                "yAxisName": "Price (USD)",
                "anchorRadius": "1",
				"drawAnchors": "1",
                "showValues": "0",
				"borderThickness": "3",
				"yAxisMinValue": getMinValue(data) - 5,
				"yAxisMaxValue": getMinValue(data) + 100,
				"canvasbgColor": "#252830",
				"bgColor": "#252830",
				"bgAlpha": 100,
				"captionFontColor": "#ffffff",
				"subcaptionFontColor": "#ffffff",
				"labelFontColor": "#ffffff",
				"xAxisNameFontColor": "#ffffff",
				"yAxisNameFontColor": "#ffffff",
				"baseFontColor": "#41a5f5",
				"showBorder": 0,
                "theme": "fint"
            },
            "data": data.reverse(),
        }
    );
}

var getHistory = function(req,res,next){
 
    var data = [];
	History.findOne({"Symbol": String(req.params.sym)}, function(err, foundHistory){
		if(foundHistory){
			(foundHistory.Historical).forEach(function(day){
				data.push({
					"label": day.Date,
					"value": day.Close,
					"color": "#41a5f5"
				});
			});
			res.json(createJSON(foundHistory.Name, data));
			next();
		}
		else{
			next();
		}
	});	
};

function getMinValue(data)
{
	var min = Number.MAX_SAFE_INTEGER;
	for(var i = 0; i < data.length; i++) {
		if(data[i].value < min) min = data[i].value;
	}
	return min;
}

module.exports = getHistory;