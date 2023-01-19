You must provide one dataset for listed buildings.

Format
------

We recommend you [provide each dataset as a CSV](../how-to-provide-data.html)

If your data includes geospatial information (a point or geometry field), CSV is still preferred but alternatively you can provide it in one of these open data formats:

-   [GeoJSON](https://digital-land.github.io/specification/specification/article-4-direction/#GeoJSON-format)
-   OGC [GML](https://digital-land.github.io/specification/specification/article-4-direction/#GML-format)
-   OGC [Geopackage](https://digital-land.github.io/specification/specification/article-4-direction/#geopackage-format)
-   OGC Keyhole Markup Language [KML](https://digital-land.github.io/specification/specification/article-4-direction/#KML-format)

Listed buildings dataset
------------------------

This dataset is about buildings listed on the National Heritage List for England because of their historical or architectural importance.

The dataset must contain at least one entry (row) for each listed building.

It must containing the following fields (columns):

### reference

A reference or ID for each listed building that is: 

-   unique within your dataset
-   permanent - it doesn't change when the dataset is updated

If you don't use a reference already, you will need to create one. It can be the Historic England reference used in the [register of listed buildings](https://historicengland.org.uk/listing/the-list/), or a short set of letters or numbers. 

Example: `LB1`

### name

The name of the listed building, as listed in the [register of listed buildings](https://historicengland.org.uk/listing/the-list/).

Example: `10 and 12, Lower Clapton Road E5`

### geometry

The outline of the listed building as a single polygon or multipolygon value. Points must be in the WGS84 coordinate reference system.

This should be in GeoJSON format.

Example: `MULTIPOLYGON (((1.188829 51.23478,1.188376 51.234909,1.188381 51.234917,1.187912 51.235022...`

### listed-building

The Historic England listed building reference for the listed building. This is recorded in the [register of listed buildings](https://historicengland.org.uk/listing/the-list/) as "List Entry Number".

Example: `1480524`

### listed-building-grade

The Historic England listed-building-grade value for the listed building: I, II or II*.

### notes

Optional text on how this data was made or produced, or how it can be interpreted.

### start-date

The date from which the building was listed, written in `YYYY-MM-DD` format.

Example: `1984-03-28`

### end-date

If applicable, the date from which the building was no longer listed, written in `YYYY-MM-DD` format. If it's still listed, leave the cell blank.

Example: `1999-01-20`

### entry-date

The date this dataset was created or last updated, written in `YYYY-MM-DD` format.

Example: `2022-12-20`
