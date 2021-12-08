// const { default: GeoRasterLayer } = require("georaster-layer-for-leaflet");

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

classifyValueByBreaks = function (breaks, value) {
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
var chart02Options = $.extend({}, chart01Options)
chart02Options.xaxis.title.text = "Average Median Household Income"
var chart01 = new ApexCharts(document.querySelector("#chart01"), chart01Options);
chart01.render();
var chart02 = new ApexCharts(document.querySelector("#chart02"), chart02Options);
chart02.render();
let mapLayers = [];

// Load Map00 data
$.getJSON("res/park.geojson", function (geojson) {
    let map00Data = L.geoJSON(geojson, {
        style: { color: "green", weight: .8 }
    });
    mapLayers[0] = map00Data;
    map00Data.addTo(map01);
})

// Load Map01 data
$.getJSON('res/resSection1.geojson', function (geojson) {
    let w_quan = getQuantileBreaks(geojson, "pct_white", 6);
    let p_quan = getQuantileBreaks(geojson, "pct_park", 6);
    let map01Data = L.geoJSON(geojson, {
        style: (feature) => {
            let pct_white = feature.properties["pct_white"];
            let pct_park = feature.properties["pct_park"];
            let q_w = classifyValueByBreaks(w_quan, pct_white);
            let q_p = classifyValueByBreaks(p_quan, pct_park);
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
    mapLayers[1] = map01Data;
    // map01Data.addTo(map01);
    let chartData = geojson.features.map((blockgroup) => {
        return [blockgroup.properties.pct_white, Math.log(0.001 + blockgroup.properties.pct_park)]
    })
    chart01.updateSeries([{
        name: 'Sales',
        data: chartData,
    }])
})
// Map01 legend
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

// Load Map02 data
$.getJSON('res/resSection1.geojson', function (geojson) {
    let w_quan = getQuantileBreaks(geojson, "medinc", 6);
    let p_quan = getQuantileBreaks(geojson, "pct_park", 6);
    let map02Data = L.geoJSON(geojson, {
        style: (feature) => {
            let pct_white = feature.properties["medinc"];
            let pct_park = feature.properties["pct_park"];
            let q_w = classifyValueByBreaks(w_quan, pct_white);
            let q_p = classifyValueByBreaks(p_quan, pct_park);
            let colors = ["#14299e", "#a51313"];
            let c = chroma.average(colors, "lab", [q_w + 1, q_p + 1]);
            c = c.luminance((q_w + q_p) / 12 * .7);
            c = c.saturate(.5);
            return {
                color: c,
                weight: .8,
                opacity: 1,
            };
        },
        onEachFeature: function (feature, layer) {
            let medinc = feature.properties.medinc;
            medinc = medinc === null ? 0 : medinc;
            let pct_park = feature.properties.pct_park;
            pct_park = pct_park > 1 ? 1 : pct_park;
            layer.bindPopup(
                generatePopup("Median House Hold Income", (medinc).toFixed(2) + "%") +
                generatePopup("Park Area Percentage", (pct_park * 100).toFixed(2) + "%")
            );
        }
    });

    mapLayers[2] = map02Data;
    let chartData = geojson.features.map((blockgroup) => {
        return [blockgroup.properties.medinc, Math.log(0.001 + blockgroup.properties.pct_park)]
    })
    chart02.updateSeries([{
        name: 'correlations',
        data: chartData,
    }])
})

// Load temp data
var url_to_geotiff_file = "res/temperature.tif";
let rasterLayer;
// var parse_georaster = require("georaster");
// var GeoRasterLayer = require("georaster-layer-for-leaflet");
$(() => {
    fetch(url_to_geotiff_file)
        .then(response => response.arrayBuffer())
        .then(arrayBuffer => {
            parseGeoraster(arrayBuffer).then(georaster => {
                let values = georaster.values.flat().map(x => Array.from(x)).flat().filter(x => x > 0);
                let tempQuanBreaks = chroma.limits(values, "q", 6);
                let tempColorMap = chroma.scale("RdYlBu").domain([5, 4, 3, 2, 1, 0]);
                rasterLayer = new GeoRasterLayer({
                    georaster: georaster,
                    opacity: 0.7,
                    pixelValuesToColorFn: values => {
                        if (values == 0) { return null }
                        values = classifyValueByBreaks(tempQuanBreaks, values);
                        return tempColorMap(values)
                    },
                    resolution: 64,
                });
                mapLayers[3] = rasterLayer;
            });
        });
})

let topOffset = -$(window).height() * 1;
let mapTops = $(".map-change").toArray().map((div) => { return $(div).offset().top + topOffset })
let mapStatus = 0; // no map
console.log(mapTops);

let clearMap = function (map) {
    map.eachLayer(function (layer) {
        if (layer != basemap02) {
            map.removeLayer(layer);
        }
    });
}

let addDataToMap = function (map, layer) {
    clearMap(map);
    layer.addTo(map);
}

$(window).on('scroll', function () {
    var yScrollPos = window.pageYOffset;
    let currentMapStatus = classifyValueByBreaks(mapTops, yScrollPos);
    // console.log(currentMapStatus);
    if (currentMapStatus != mapStatus && currentMapStatus >= 0) {
        mapStatus = currentMapStatus;
        console.log("adding map", mapStatus);
        addDataToMap(map01, mapLayers[currentMapStatus]);
    }
});