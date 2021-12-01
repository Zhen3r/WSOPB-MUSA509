// define basemap
let basemap01 = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
})

let basemap02 = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">Carto</a>'
})

getQuantileBreaks = function (geojson, propertyName, breakNum) {
    let classData = [];
    geojson.features.forEach(feature => {
        classData.push(feature.properties[propertyName]);
    });
    return chroma.limits(classData, "q", breakNum);
}

getQuantileLevel = function (breaks, value) {
    for (let i = 0; i < breaks.length; i++) {
        const b = breaks[i];
        if (value < b) { return i - 1; }
    }
    return breaks.length - 1;
}

generatePopup = function (name, value) {
    return "<p><strong>" + name + "</strong>:" + value + "</p>"
}

// map01
var map01 = L.map('map01', { zoomSnap: 0.2, scrollWheelZoom: false }).setView([40.0, -75.26], 11.6)
basemap02.addTo(map01);
//chart
var chart01Options = {
    series: [],
    chart: {
        height: 250,
        type: 'scatter',
        zoom: {
            enabled: true,
            type: 'xy'
        }
    },
    xaxis: {
        tickAmount: 10,
        labels: {
            formatter: function (val) {
                return parseFloat(val).toFixed(1)
            }
        },
        title: { text: "White Percentage of Blockgroups" }
    },
    yaxis: {
        tickAmount: 7,
        labels: {
            formatter: function (val) {
                return parseFloat(val).toFixed(2)
            }
        },
        title: { text: "log(ParkAreaPct)" }
    },
    noData: {
        text: 'Loading...'
    },
    markers: {
        size: 2
    },
};
var chart01 = new ApexCharts(document.querySelector("#chart01"), chart01Options);
chart01.render();
let map01Data;


// Add roads
$.getJSON('res/resSection1.geojson', function (geojson) {
    let w_quan = getQuantileBreaks(geojson, "pct_white", 6);
    let p_quan = getQuantileBreaks(geojson, "pct_park", 6);
    map01Data = L.geoJSON(geojson, {
        style: (feature) => {
            let pct_white = feature.properties["pct_white"];
            let pct_park = feature.properties["pct_park"];
            let q_w = getQuantileLevel(w_quan, pct_white);
            let q_p = getQuantileLevel(p_quan, pct_park);
            let colors = ["#14299e", "#a51313"];
            let c = chroma.average(colors, "lab", [q_w + 1, q_p + 1]);
            c = c.luminance((q_w + q_p) / 12 * .7);
            c = c.saturate(.5);
            let o = pct_park;
            return {
                color: c,
                weight: .8,
                opacity: 1,
            };
        },
        onEachFeature: function (feature, layer) {
            let pct_white = feature.properties.pct_white;
            let pct_park = feature.properties.pct_park;
            pct_park = pct_park > 1 ? 1 : pct_park;
            layer.bindPopup(
                generatePopup("GEOID", feature.properties.geoid) +
                generatePopup("Percentage White", (pct_white * 100).toFixed(2) + "%") +
                generatePopup("Park Area Percentage", (pct_park * 100).toFixed(2) + "%")
            );
        }
    });
    // map01Data.addTo(map01);
    let chartData = geojson.features.map((blockgroup) => {
        return [blockgroup.properties.pct_white, Math.log(0.001 + blockgroup.properties.pct_park)]
    })
    chart01.updateSeries([{
        name: 'Sales',
        data: chartData,
    }])
})
//legend
legendNum = 6;
for (let i = 0; i < legendNum ** 2; i++) {
    $("<div class='box-legend-square'></div>").appendTo(".box-legend")
}
let boxes = $(".box-legend-square").each(function (i, box) {
    let x = Math.floor(i / legendNum);
    let y = legendNum - 1 - i % legendNum;
    let colors = ["#14299e", "#a51313"];
    let c = chroma.average(colors, "lab", [1 + x, 1 + y]);
    c = c.luminance((x + y) / 10 * .7 + .15);
    c = c.saturate(.5);
    $(box).css("background-color", c);
    $(box).text("" + x + ", " + y);
})


let scroll_pos_test = 2400;             // set to whatever you want it to be
let mapStatus = 0;
$(window).on('scroll', function () {
    var y_scroll_pos = window.pageYOffset;
    console.log(y_scroll_pos, scroll_pos_test)
    if (y_scroll_pos > scroll_pos_test) {
        if (mapStatus == 0) {
            map01Data.addTo(map01);
            mapStatus = 1;
        }
    }
});