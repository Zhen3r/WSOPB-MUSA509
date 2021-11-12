1. Authors — list the names of everyone part of producing the project.

    Ziyuan Cai, Zhenzhao Xu

1. Abstract — a paragraph description of the problem/situation/domain/etc. The Abstract should clearly state the types of decisions that your dashboard is going to help facilitate.

    **Why is it important?**

    1. Inequality
        https://eos.org/features/growing-equity-in-city-green-space, 
        https://www.phillymag.com/news/2021/05/27/parks-philadelphia-equity-report/,
        https://www.inquirer.com/opinion/commentary/philadelphia-parks-and-rec-budget-cuts-20210323.html,
        https://www.tpl.org/city/philadelphia-pennsylvania

        > "In most studies there’s a demonstrated pattern between income and urban forest cover; that is, higher income is associated with more urban forest cover"
        
    1. Climate

        > Some Philly neighborhoods can be up to 20 degrees hotter than others during the summer months, thanks to a lack of tree canopy coverage, or what’s known as the “urban heat island” effect.

    1. Underfunded

        The Parks and Recreation budget was cut by 20% during the last fiscal year, equating to about $12.5 million, and more cuts are being considered over the coming weeks during the next budget cycle.

    1. Difficulty of planning

    **Types of decisions that out dashboard is going to help facilitate.**



1. List of data sources you intend to use for this project. For each data source, please list:

    1. Where you can get access to the dataset (e.g., a URL, government agency, third-party API, BigQuery public dataset, etc.)

    1. Size of dataset (if applicable)

    1. Whether you currently have access to this data

    **data sources**

    | Category |     Source     |        Name         |                                                                                                                                                                                              Url                                                                                                                                                                                               | Geometry Type | Size  | Update Frequency |
    | :------: | :------------: | :-----------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------: | :---: | :--------------: |
    | Equality |      ACS       |     Race/Income     |                                                                                                                                                           [ACS2019](https://www.census.gov/data/developers/data-sets/acs-5year.html)                                                                                                                                                           |    Polygon    |       |     as need      |
    | Equality | OpendataPhilly |    Park Boundary    |                                                                                                            [OpenDataPhilly](https://www.opendataphilly.org/dataset/ppr-properties), [Api Endpoint](https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson)                                                                                                            |    Polygon    |       |                  |
    | Ecology  | OpendataPhilly |        Flood        | [100y](https://metadata.phila.gov/#home/representationdetails/56ccbad74d934cea1ef05c20/), [500y](https://metadata.phila.gov/#home/representationdetails/56ccbb1df041bd4d03549350/), [contours](https://www.opendataphilly.org/dataset/topographic-contours), [Flood Hazard Zone](https://www.opendataphilly.org/dataset/flood-hazard-zone-lines/resource/85d4503f-ecfc-4c26-ba45-2506755cab53) |    Polygon    |       |                  |
    | Ecology  |      USGS      | Surface Temperature |                                                                                                                  [USGS](https://www.usgs.gov/core-science-systems/nli/landsat/landsat-data-access?qt-science_support_page_related_con=0#qt-science_support_page_related_con )                                                                                                                  |    Polygon    |       |                  |
    | Economy  | OpendataPhilly |     Land Value      |                                                                                                                                                             [OPA](https://www.opendataphilly.org/dataset/opa-property-assessments)                                                                                                                                                             |    Polygon    |       |                  |
    | Economy  | OpendataPhilly |      Buildings      |                                                                                                                                                               [OpendataPhilly](https://www.opendataphilly.org/dataset/buildings)                                                                                                                                                               |    Polygon    |       |                  |
    | Economy  | OpendataPhilly |     Land Cover      |                                                                                                                                                   [Land Cover Raster](https://www.opendataphilly.org/dataset/philadelphia-land-cover-raster)                                                                                                                                                   |    Polygon    |       |                  |

dvrpc, 
telemetry,
usgs,
guray.erus@pennmedicine.upenn.edu

1. Wireframes of the webpage(s) for your project. This of a wireframe as an outline for an interactive project. It allows you to quickly communicate the general makeup and organization of the dashboard content. See this page for guidance on creating wireframes. Hand-drawn or digital are both acceptable, but please scan or take pictures of the hand-drawn ones for inclusion in the repo. Link the images in the proposal markdown. Interactive wireframes are acceptable too. Many free and paid tools exist for creating wireframes (Adobe Wireframe XD, MockFlow, Figma, etc.)


