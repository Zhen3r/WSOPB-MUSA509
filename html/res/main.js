var map01 = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "width": "container",
    "height": "container",
    "data": {
        "url": "https://vega.github.io/vega-lite/examples/data/us-10m.json",
        "format": {
            "type": "topojson",
            "feature": "counties"
        }
    },
    "transform": [{
        "lookup": "id",
        "from": {
            "data": {
                "url": "https://vega.github.io/vega-lite/examples/data/unemployment.tsv"
            },
            "key": "id",
            "fields": ["rate"]
        }
    }],
    "projection": {
        "type": "albersUsa"
    },
    "mark": "geoshape",
    "encoding": {
        "color": {
            "field": "rate",
            "type": "quantitative"
        }
    }
};

// Embed the visualization in the container with id `vis`
vegaEmbed('#map01', map01, { "actions": false });
vegaEmbed('#map02', map01, { "actions": false });