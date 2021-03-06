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

// defining reuseable geojson objects
let park;

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
var chart01Options = { series: [], chart: { height: 250, type: 'scatter', zoom: { enabled: true, type: 'xy' } }, xaxis: { tickAmount: 10, labels: { formatter: function (val) { return parseFloat(val).toFixed(1) } }, title: { text: "White Percentage of Blockgroups" } }, yaxis: { tickAmount: 7, labels: { formatter: function (val) { return parseFloat(val).toFixed(2) } }, title: { text: "log(ParkAreaPct)" } }, noData: { text: 'Loading...' }, markers: { size: 2 }, };
var chart02Options = { series: [], chart: { height: 250, type: 'scatter', zoom: { enabled: true, type: 'xy' } }, xaxis: { tickAmount: 10, labels: { formatter: function (val) { return parseFloat(val).toFixed(1) } }, title: { text: "Average Median Household Income" } }, yaxis: { tickAmount: 7, labels: { formatter: function (val) { return parseFloat(val).toFixed(2) } }, title: { text: "log(ParkAreaPct)" } }, noData: { text: 'Loading...' }, markers: { size: 2 }, };
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
    park = geojson;
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
    if (i >= 36) i -= 36;
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
                generatePopup("Median House Hold Income", (medinc).toFixed(2)) +
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

$.getJSON('res/flood.geojson', function (geojson) {
    let mapData = L.geoJSON(geojson, {
        style: (feature) => {
            let score = 1 - feature.properties.score;
            let c = chroma.scale("viridis")(score);
            return {
                color: c,
                weight: .8,
                opacity: 1,
            };
        },
        onEachFeature: function (feature, layer) {
            let score = feature.properties.score;
            let description = feature.properties.description;
            layer.bindPopup(
                generatePopup("score", (score).toFixed(2)) +
                generatePopup("description", description)
            );
        }
    });
    mapLayers[4] = [mapData];
})

let cost;
let getCostLayer = function (layerIndex) {
    let layer = ['score', 'land_use_score', 'land_value_score', 'building_score'][layerIndex]
    let mapData = L.geoJSON(cost, {
        style: (feature) => {
            let score = feature.properties[layer];

            let c = chroma.scale("viridis")(score);
            return {
                color: c,
                weight: .95,
                opacity: 1,
            };
        },
        onEachFeature: function (feature, layer) {
            let score = feature.properties.score;
            let land_value_score = feature.properties.land_value_score;
            let building_score = feature.properties.building_score;
            let land_use_score = feature.properties.land_use_score;
            layer.bindPopup(
                generatePopup("Overall Cost", (score).toFixed(2)) +
                generatePopup("Land Use Cost", (land_use_score).toFixed(2)) +
                generatePopup("Land Value Cost", (land_value_score).toFixed(2)) +
                generatePopup("Demolition Cost", (building_score).toFixed(2))
            );
        }
    });
    return (mapData)
}

$.getJSON('res/cost.geojson', function (geojson) {
    cost = geojson;
    mapData = getCostLayer(0);
    mapLayers[5] = [mapData];
})

let feasibility;
let coef = { a1: 1, a2: 1, a3: 1, a4: 1, a5: 1, a6: 1 };
let changeFeaLayer = function () {
    let park, cost, race, income, flood, heat, score;
    console.log(coef)
    let mapData = L.geoJSON(feasibility, {
        style: (feature) => {
            park = feature.properties.park;
            cost = feature.properties.cost;
            race = feature.properties.race;
            income = feature.properties.income;
            flood = feature.properties.flood;
            heat = feature.properties.income;
            let a1 = coef['a1'], a2 = coef['a2'], a3 = coef['a3'], a4 = coef['a4'], a5 = coef['a5'], a6 = coef['a6'];
            score = a1 * race + a2 * income - a3 * cost - a4 * park + a5 * flood + a6 * heat;
            // standardize the score
            score = score / Math.abs(a1 + a2 - a3 - a4 + a5 + a6)
            // console.log('score', score)
            let c = chroma.scale("viridis").domain([-0.5, 1])(score);
            return {
                color: c,
                weight: .95,
                opacity: 1,
            };
        },
        onEachFeature: function (feature, layer) {
            layer.bindPopup(
                generatePopup("Overall Feasibility Index", (score).toFixed(2)) +
                generatePopup("Park Area Index", (park).toFixed(2)) +
                generatePopup("Cost Index", (cost).toFixed(2)) +
                generatePopup("Race Index", (race).toFixed(2)) +
                generatePopup("Income Index", (income).toFixed(2)) +
                generatePopup("Flood Index", (flood).toFixed(2)) +
                generatePopup("Heat Index", (heat).toFixed(2))
            );
        }
    });
    mapLayers[6] = mapData;
}
$.getJSON('res/feasibility.geojson', function (geojson) {
    feasibility = geojson;
    changeFeaLayer();
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
    if (layer instanceof Array) {
        layer.forEach(l => l.addTo(map))
    } else layer.addTo(map)
}
let drawCostLayer = function (layerIndex) {
    mapData = getCostLayer(layerIndex);
    mapLayers[5] = [mapData];
    addDataToMap(map01, mapLayers[5]);
}

$(".cost-btn").each((i, element) => {
    $(element).on("click", () => {
        drawCostLayer(i);

    })
})
$('.fea-btn').on('click', () => {
    changeFeaLayer();
    addDataToMap(map01, mapLayers[6]);
})
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


$('input').on('input change', function () {
    let s = $(this);
    let id = s.attr("id");
    let v = s.val();
    v = Number(v);
    coef[id] = v;
    s.parent().find('.value').text(v.toFixed(2))
})