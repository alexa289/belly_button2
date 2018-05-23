// Create the dropdown for samples
function buildDropdown() {
    var selDataset = document.getElementById("selDataset");
    //point to names route
    Plotly.d3.json('/names', function (error, data) {
        if (error) return console.warn(error)
        // loop through samples for dropdown
        for (i = 0; i < data.length; i++) {
            
            var option = document.createElement("option");
            option.text = data[i]
            option.value = data[i]
            
            selDataset.appendChild(option);
        }
        //getData(data[0], buildDropdown);
    }
    )
}

//Call the function
buildDropdown()




// generate a random color function. Copied from https://stackoverflow.com/questions/30143082/how-to-get-color-value-from-gradient-by-percentage-with-javascript/30144587
function pickHex(color1, color2, weight) {
    var w1 = weight;
    var w2 = 1 - w1;
    var rgb = [Math.round(color1[0] * w1 + color2[0] * w2),
    Math.round(color1[1] * w1 + color2[1] * w2),
    Math.round(color1[2] * w1 + color2[2] * w2)];
    return rgb;
}

//Initialize the chart with default "BB_940"
function getPieChart(data) {
    console.log(data.samples)
    if (data.samples.length > 10) {
        endListRange = 9
    }
    else endListRange = data.samples.length - 1

    top10_Samples = []
    top10_OTUIds = []
    for (i = 0; i < endListRange; i++) {
        top10_Samples.push(+data.samples[i])
        top10_OTUids.push(+data.otu_id[i])
    };


    pieData = [{
        "labels": top10_OTUids,
        "values": top10_Samples,
        "type": "pie"
    }];

    return pieData

};


function buildPie(sampleID) {
    url = '/samples/' + sampleID;
    Plotly.d3.json(url, function (error, data) {
        if (error) return console.warn(error);

        var pielayout = {
            title: "Pie Chart for Samples"
        }
        var pieChart = document.getElementById('pie');

        var pietrace = getPieChart(data)

        Plotly.plot(pieChart, pietrace, pielayout);
    })
}

buildPie('BB_940')


function updatePieChart(sampledata) {
    url = '/samples/' + sampledata;
    Plotly.d3.json(url, function (error, data) {
        if (error) return console.warn(error);

        var pieChart = document.getElementById('pie');

        var pietrace = getPieChart(data)

        console.log(pietrace)
        console.log(pietrace[0].labels)
        console.log(pietrace[0].values)

        Plotly.restyle(pieChart, "labels", [pietrace[0].labels]);
        Plotly.restyle(pieChart, "values", [pietrace[0].values]);
    })
}


// get value 
function getValue() {
    value = document.querySelector("select").value;
    getDataPie(value);

}

    // call back function to get data on the onChange in the select tag 
    function getDataPie(sample_id) {
        var url = "/samples/" + sample_id;
        Plotly.d3.json(url, function (error, pie_data) {
            if (error) return console.warn(error)

            var update = {
                values: [Object.values(pie_data.sample_values)],
                labels: [Object.values(pie_data.otu_ids)]
            };

            restylePlotly(update);
        });
    };
function optionChanged(sampleID) {


    buildPie(sampleID)

}
