1. Authors — list the names of everyone part of producing the project.

    Ziyuan Cai, Zhenzhao Xu

1. Abstract — a paragraph description of the problem/situation/domain/etc. The Abstract should clearly state the types of decisions that your dashboard is going to help facilitate.

    **Why is it important?**

    1. Inequality
        https://eos.org/features/growing-equity-in-city-green-space

        > "In most studies there’s a demonstrated pattern between income and urban forest cover; that is, higher income is associated with more urban forest cover"
        
    1. Climate

        > Some Philly neighborhoods can be up to 20 degrees hotter than others during the summer months, thanks to a lack of tree canopy coverage, or what’s known as the “urban heat island” effect.

    1. Underfunded

        The Parks and Recreation budget was cut by 20% during the last fiscal year, equating to about $12.5 million, and more cuts are being considered over the coming weeks during the next budget cycle.
        
    1. Hard to 

    **Types of decisions that out dashboard is going to help facilitate.**



1. List of data sources you intend to use for this project. For each data source, please list:

    1. Where you can get access to the dataset (e.g., a URL, government agency, third-party API, BigQuery public dataset, etc.)

    1. Size of dataset (if applicable)

    1. Whether you currently have access to this data

    **data sources**

    - Park boundaries of Philly (Link)[https://www.opendataphilly.org/dataset/ppr-properties] (Api Endpoint)[https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson]

    - Euqality: 
    
        - Race, Income: ACS block group

        - Accessibility: Transportation (bus, subway, bike)

    - Ecology:

        - Temperature : (Heat Island) Landsat data - NDVI & temperature 

        - Flood: Flood plain (100y Link)[https://metadata.phila.gov/#home/representationdetails/56ccbad74d934cea1ef05c20/], (500y)[https://metadata.phila.gov/#home/representationdetails/56ccbb1df041bd4d03549350/], (contours)[https://www.opendataphilly.org/dataset/topographic-contours], (Flood Hazard Zone)[https://www.opendataphilly.org/dataset/flood-hazard-zone-lines/resource/85d4503f-ecfc-4c26-ba45-2506755cab53]

        - (?) Pollution (Air/water)

    - Economy:

        - cost: (Zoning)[], (Land Cover Raster)[https://www.opendataphilly.org/dataset/philadelphia-land-cover-raster] - relevant to the construction cost of park?




1. Wireframes of the webpage(s) for your project. This of a wireframe as an outline for an interactive project. It allows you to quickly communicate the general makeup and organization of the dashboard content. See this page for guidance on creating wireframes. Hand-drawn or digital are both acceptable, but please scan or take pictures of the hand-drawn ones for inclusion in the repo. Link the images in the proposal markdown. Interactive wireframes are acceptable too. Many free and paid tools exist for creating wireframes (Adobe Wireframe XD, MockFlow, Figma, etc.)