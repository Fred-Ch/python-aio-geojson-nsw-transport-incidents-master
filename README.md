# python-aio-geojson-nsw-transport-incidents
 
[![Build Status](https://travis-ci.org/Fred-Ch/python-aio-geojson-nsw-transport-incidents-master.svg)](https://travis-ci.org/Fred-Ch/python-aio-geojson-nsw-transport-incidents-master)
[![PyPi](https://img.shields.io/pypi/v/aio-geojson-nsw-transport-incidents.svg)](https://pypi.python.org/pypi/aio-geojson-nsw-transport-incidents)
[![Version](https://img.shields.io/pypi/pyversions/aio-geojson-nsw-transport-incidents.svg)](https://pypi.python.org/pypi/aio-geojson-nsw-transport-incidents)

This library provides convenient async access to the [NSW Transport Service Live traffic status](https://opendata.transport.nsw.gov.au/dataset/live-traffic-site-status) incidents feed. 
The feed can be seen online on (https://www.livetraffic.com/)
 
## Installation
`pip install aio-geojson-nsw-transport-incidents`

## Usage
See below for examples of how this library can be used. After instantiating a 
particular class - feed or feed manager - and supply the required parameters, 
you can call `update` to retrieve the feed data. The return value 
will be a tuple of a status code and the actual data in the form of a list of 
feed entries specific to the selected feed.

Status Codes
* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

**Parameters**

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |
| `feature`          | Type of Hazard to retreive                |

Traffic Hazards are divided into six basic types:
* Incidents (`incident-open` `incident-closed` `incident`)
* Fire  (`fire-open` `fire-closed` `fire`)
* Flood (`flood-open` `flood-closed` `flood`)
* Alpine conditions (`alpine-open` `alpine-closed` `alpine`)
* Major Events (`majorevent-open` `majorevent-closed` `majorevent`)
* Roadworks (`roadwork-open` `roadwork-closed` `roadwork`)

Hazards can be open, closed (or both can be retreived). Refer to the [Live Traffic Data Developer Guide](https://opendata.transport.nsw.gov.au/sites/default/files/Live_Traffic_Data_Developer_Guide.pdf)

**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. |

**Example**
```python
import asyncio
from aiohttp import ClientSession
from aio_geojson_nsw_transport_incidents import NswTransportServiceIncidentsFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: -33.0, Longitude: 150.0
        # Filter radius: 50 km
        # Filter categories: 'Scheduled roadwork'
        # Hazard type : 'roadworks-open'
        feed = NswTransportServiceIncidentsFeed(websession, 
                                                (-33.0, 150.0), 
                                                filter_radius=50, 
                                                filter_categories=['Scheduled roadwork'],
                                                hazard="roadwork-open")
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```

## Feed entry properties
Each feed entry is populated with the following properties:

| Name               | Description                                                                                         | Feed attribute |
|--------------------|-----------------------------------------------------------------------------------------------------|----------------|
| geometry           | All geometry details of this entry.                                                                 | `geometry`     |
| coordinates        | Best coordinates (latitude, longitude) of this entry.                                               | `geometry`     |
| external_id        | The unique public identifier for this incident.                                                     | `guid`         |
| title              | Title of this entry.                                                                                | `title`        |
| attribution        | Attribution of the feed.                                                                            | n/a            |
| distance_to_home   | Distance in km of this entry to the home coordinates.                                               | n/a            |
| category           | The broad hazard category description assigned to the hazard by TMC Communications. Used internally by TMCCommunications for reporting hazard statistics.Please note the values used by this property are subject to change and should not be relied upon.                                 | `mainCategory`     |
| publication_date   | The publication date of the incidents.                                                              | `created`      |
| description        | The description of the incident.                                                                    | `headline`  |
| council_area       | Council are this incident falls into.                                                               | `roads` -> `suburb`        |
| road               | Council are this incident falls into.                                                               | `roads` -> `mainStreet`        |
| type               | Type of the incident (e.g. Bush Fire, Grass Fire, Hazard Reduction).                                | `type`         |
| publicTransport    | The publication date of this entry                                                                  | `publicTransport`        |
| adviceA            | The first advice of this entry. The first standard piece of advice to motorists. At the present time | `adviceA`       |
| adviceB            | Turn the second advice of this entry                                                                | `adviceB`        |
| adviceOther        | The other advice of this entry                                                                      | `adviceOther`        |
| isMajor            | True is the incident is major for this entry                                                        | `isMajor`        |
| isEnded            | True if the hazard has ended, otherwise false. Once ended, the hazard’s record in our internal tracking system is closed and further modification becomes impossible unless the record is later re-opened. This  property is a counterpart to the createdproperty. When true, the  lastUpdatedproperty of the hazard will be the date/time when  the hazard’s record  in the tracking system was closed.                                                                    | `isEnded`        |
| isNew              | True if the incident is new for this entry.                                                         | `isNew`        |
| isImpactNetwork    | True if the hazard is currently having some impact on traffic on the road network.                  | `isImpactNetwork`        |
| diversions         | The Summary of any traffic diversions in place. The text may contain HTML markup..                  | `diversions`        |
| subCategory        | The sub-category of incident of this entry.                                                         | `subCategory`        |
| duration           | The Planned duration of the hazard. This property is rarely used.                                   | `duration`        |


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest 
  timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.


## Attribution and motivation
This is a fork of [exxamalte/python-aio-geojson-nsw-rfs-incidents](https://github.com/exxamalte/python-aio-geojson-nsw-rfs-incidents). 
It deferes mainly as the geoJSON feeds generated by NSW Transport using QGis.  QGis generates files that don't match exactly geojson format (geometry types : `POINT` instead of `Point`)

This library has been created for [Home Assistant component](https://github.com/Fred-Ch/core/tree/dev/homeassistant/components/nsw_transport_incident_service_feed).