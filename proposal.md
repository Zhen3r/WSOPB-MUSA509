# Proposal

## Authors

Ziyuan Cai, Zhenzhao Xu

## Abstract

Infrastructure has always been a heated topic of discussion among people. Citizens care about infrastructure because it is closely related to their lives, while, politicians and city managers, on the other hand care about infrastructure because it affects their political performance and support rate. Therefore, it is particularly significant to select the location of large-scale infrastructure such as parks that not only have social attributes but also environmental attributes. Is the address of the park at this stage reasonable? If we want to build a new park, where is our best location?

We will consider the location of the park from three aspects.
* Equality

    > In most studies there’s a demonstrated pattern between race and income and city green space. So race and income are the key points for us to consider equality.
        
* Ecology

    > Some Philly neighborhoods can be up to 20 degrees hotter than others during the summer months, thanks to the urban heat island effect. Besides, the drainage problem of the flood has almost become a regular issue in Philadelphia. The green vegetation coverage of the parks can improve the situation.

* Economy

    > The inevitable problem in the construction of a park is cost. We will calculate the land value in Philadelphia based on land use and give a rough cost range.

## Stakeholders

* City planners who want to improve people’s lives and increase greenery in Philadelphia.
* Neighborhoods that has a great demand for parks but cannot be satisfied.

## Data

    | Category |     Source     |            Name            |                             Url                              | Geometry Type | Size | Update Frequency |
    | :------: | :------------: | :------------------------: | :----------------------------------------------------------: | :-----------: | :--: | :--------------: |
    | Equality |      ACS       | Race/Income by block group | [ACS2019](https://www.census.gov/data/developers/data-sets/acs-5year.html) |    Polygon    |      |     as need      |
    | Equality | OpendataPhilly |       Park Boundary        | [OpenDataPhilly](https://www.opendataphilly.org/dataset/ppr-properties), [Api Endpoint](https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson) |    Polygon    |      |      weekly      |
    | Ecology  | OpendataPhilly |           Flood            | [100y](https://metadata.phila.gov/#home/representationdetails/56ccbad74d934cea1ef05c20/), [500y](https://metadata.phila.gov/#home/representationdetails/56ccbb1df041bd4d03549350/), [contours](https://www.opendataphilly.org/dataset/topographic-contours), [Flood Hazard Zone](https://www.opendataphilly.org/dataset/flood-hazard-zone-lines/resource/85d4503f-ecfc-4c26-ba45-2506755cab53) |    Polygon    |      |     one time     |
    | Ecology  |      USGS      |    Surface Temperature     | [USGS](https://www.usgs.gov/core-science-systems/nli/landsat/landsat-data-access?qt-science_support_page_related_con=0#qt-science_support_page_related_con) |    Polygon    |      |      yearly      |
    | Economy  | OpendataPhilly |         Land Value         | [OPA](https://www.opendataphilly.org/dataset/opa-property-assessments) |    Polygon    |      |      yearly      |
    | Economy  | OpendataPhilly |         Buildings          | [OpendataPhilly](https://www.opendataphilly.org/dataset/buildings) |    Polygon    |      |      yearly      |
    | Economy  | OpendataPhilly |         Land Cover         | [Land Cover Raster](https://www.opendataphilly.org/dataset/philadelphia-land-cover-raster) |    Polygon    |      |      yearly      |

## Wireframes 

* [Sketches](https://docs.google.com/presentation/d/1Y0M4FNZb5tpQm4QnBYiDKPy0F1HD9FtDx_t1gVQYYJY/edit#slide=id.g10178e42f57_0_16)

