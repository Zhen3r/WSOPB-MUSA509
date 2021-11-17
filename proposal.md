# Proposal

## Authors

Ziyuan Cai, Zhenzhao Xu

## Abstract

As the COVID-19 stretched into end of 2020, people in Philadelphia began to flock to outdoor green spaces in and around the city. A report from the [Trust for Public Land](https://www.tpl.org/city/philadelphia-pennsylvania) finds that although green spaces in Philadelphia is accessible to most citizens, **the amont of green spaces varies greatly based on income and race**. And according to [Inquirer](https://www.inquirer.com/science/climate/philadelphia-heat-island-climate-change-hunting-park-20190724.html), some Philly neighborhoods can be up to 20°F (6.7°C) hotter than others during the summer months due to Urban Heat Island Effect. Besides, the drainage problem of the flood has almost become a worrying problem in Philadelphia. Moreover, Philadelphia Parks and Recreation budget was cut by 20% during the last fiscal year, equating to about $12.5 million, which means that **the budget on new green spaces is limited**.

Therefore, it is particularly important for planners of Philadelphia Parks and Recreation to determine the best locations for new green spaces effectively so that green spaces can be more equitable and also do some goods to the city environment. This project is a toolkit built for this scenario that helps planners to answer following questuions: Is the location of current green spaces reasonable? If we want to build a new park, where is our best location? How do the pubilc involves in it?

In this project, three aspects of current situations are discussed and rational locations of green spaces are predicted by algorithm.

1. **Equality**

    Whether there is a correlation between race, income and current city green spaces accessiblity. How does race or income factors affect area of green spaces? Are there any spatial relationships in them?
        
1. **Ecology**

    Is the effect of Urban Heat Island obvious? to what extent? Is there a relationship between green spaces and 
    
    The green vegetation coverage of the green spaces can improve the situation.

1. **Economy**

    If a park is to be built, what is the current use of this land? Will it be expensive to build a park on it? What is the land value? Is it the best location financially? 

## Stakeholders

* City planners who want to improve people’s lives and increase greenery in Philadelphia.
* (To be discussed) Neighborhoods that has a great demand for parks but cannot be satisfied.

## Data

| Category |     Source     |            Name            |                                                                                                                                                                                              Url                                                                                                                                                                                               | Geometry Type | Size | Update Frequency |
| :------: | :------------: | :------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-----------: | :--: | :--------------: |
| Equality |      ACS       | Race/Income by block group |                                                                                                                                                           [ACS2019](https://www.census.gov/data/developers/data-sets/acs-5year.html)                                                                                                                                                           |    Polygon    |      |     as need      |
| Equality | OpendataPhilly |       Park Boundary        |                                                                                                            [OpenDataPhilly](https://www.opendataphilly.org/dataset/ppr-properties), [Api Endpoint](https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson)                                                                                                            |    Polygon    |      |      weekly      |
| Ecology  | OpendataPhilly |           Flood            | [100y](https://metadata.phila.gov/#home/representationdetails/56ccbad74d934cea1ef05c20/), [500y](https://metadata.phila.gov/#home/representationdetails/56ccbb1df041bd4d03549350/), [contours](https://www.opendataphilly.org/dataset/topographic-contours), [Flood Hazard Zone](https://www.opendataphilly.org/dataset/flood-hazard-zone-lines/resource/85d4503f-ecfc-4c26-ba45-2506755cab53) |    Polygon    |      |     one time     |
| Ecology  |      USGS      |    Surface Temperature     |                                                                                                                  [USGS](https://www.usgs.gov/core-science-systems/nli/landsat/landsat-data-access?qt-science_support_page_related_con=0#qt-science_support_page_related_con)                                                                                                                   |    Raster     |      |      yearly      |
| Economy  | OpendataPhilly |         Land Value         |                                                                                                                                                             [OPA](https://www.opendataphilly.org/dataset/opa-property-assessments)                                                                                                                                                             |    Polygon    |      |      yearly      |
| Economy  | OpendataPhilly |         Buildings          |                                                                                                                                                               [OpendataPhilly](https://www.opendataphilly.org/dataset/buildings)                                                                                                                                                               |    Polygon    |      |      yearly      |
| Economy  | OpendataPhilly |         Land Cover         |                                                                                                                                                   [Land Cover Raster](https://www.opendataphilly.org/dataset/philadelphia-land-cover-raster)                                                                                                                                                   |    Polygon    |      |      yearly      |

## Wireframes 

* [Sketches](https://docs.google.com/presentation/d/1Y0M4FNZb5tpQm4QnBYiDKPy0F1HD9FtDx_t1gVQYYJY/edit#slide=id.g10178e42f57_0_16)

## Related Links

- https://eos.org/features/growing-equity-in-city-green-space
- https://www.phillymag.com/news/2021/05/27/parks-philadelphia-equity-report/
- https://www.inquirer.com/opinion/commentary/philadelphia-parks-and-rec-budget-cuts-20210323.html
- https://www.tpl.org/city/philadelphia-pennsylvania