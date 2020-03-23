"""NSW Transport Service Incidents feed entry."""
import pytz
import calendar
from datetime import datetime
from time import strptime
 
import logging
import re
from typing import Optional, Tuple
from aio_geojson_client.feed_entry import FeedEntry
from geojson import Feature

from .consts import ATTR_TITLE, ATTRIBUTION, ATTR_CATEGORY, \
    ATTR_GUID, ATTR_PUB_DATE, ATTR_DESCRIPTION, \
    ATTR_ADVICEA, ATTR_ADVICEB, ATTR_ISMAJOR, ATTR_INCIDENT_KIND,\
    ATTR_ADVICE_OTHER, ATTR_INCIDENT_SUBCAT, CUSTOM_ATTRIBUTE,\
    ATTR_ISNEW, ATTR_IMPACTNETWORK,  ATTR_ISENDED, ATTE_DIVERSIONS,\
    ATTR_DURATION, ATTR_OTHERADVICE, ATTR_PUBLIC_TRANSPORT, ATTR_FEATURE_TYPE,\
    ATTR_ROADS

_LOGGER = logging.getLogger(__name__)


class NswTransportServiceIncidentsFeedEntry(FeedEntry):
    """NSW Transport Service Incidents feed entry."""

    def __init__(self,
                 home_coordinates: Tuple[float, float],
                 feature: Feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def attribution(self) -> Optional[str]:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def title(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties(ATTR_TITLE)

    @property
    def category(self) -> str:
        """Return the category of this entry."""
        return self._search_in_properties(ATTR_CATEGORY)

    @property
    def external_id(self) -> str:
        """Return the external id of this entry."""
        return self._search_in_feature(ATTR_GUID)

    @property
    def feature_type(self) -> str:
        """Return the feature_type of this entry."""
        return self._search_in_feature(ATTR_FEATURE_TYPE)

    @property
    def publication_date(self) -> datetime:
        """Return the publication date of this entry."""
        publication_date = self._search_in_properties(ATTR_PUB_DATE)
        if publication_date:         
            publication_date = datetime.fromtimestamp(int(publication_date)/1000)
        return publication_date

    @property
    def description(self) -> str:
        """Return the description of this entry. A one line summary ofthe hazard, including its type, location and other high level details. 
        The headline text of major hazards appears in the yellow “Major Incident Ticker” above the map in Map View."""
        return self._search_in_properties(ATTR_DESCRIPTION)

    @property
    def otherAdvice(self) -> str:
        """Return a Free form text containing advice to motorists, to supplement thestandard advice 
        conveyed in the adviceAand adviceBproperties. This text may contain HTML markup."""
        return self._search_in_properties(ATTR_OTHERADVICE)
        
    @property
    def publicTransport(self) -> str:
        """Return a Free form text containing information about the public transport impact of 
        this hazard. This text may contain HTML markup.."""
        return self._search_in_properties(ATTR_PUBLIC_TRANSPORT)

    @property
    def adviceA(self) -> str:
        """Return the first advice of this entry.
        The first standard piece of advice to motorists. At the present time, the following values are possible:
        * Allow extra traveltime 
        * Avoid the area 
        * Check signage 
        * Delay journey 
        * Exercise caution 
        * Expect delays 
        * Police directing traffic 
        * Reduce speed 
        * Reduced speed limit 
        * Snow chains required 
        * Stay away 
        * Turn around, go back 
        * Use alternative route 
        * Use diversions 
        * Use public transport"""
        return self._search_in_properties(ATTR_ADVICEA)

    @property
    def adviceB(self) -> str:
        """Return the second advice of this entry."""
        return self._search_in_properties(ATTR_ADVICEB)

    @property
    def adviceOther(self) -> str:
        """Return the other advice of this entry."""
        return self._search_in_properties(ATTR_ADVICE_OTHER)

    @property
    def isMajor(self) -> bool:
        """Return  true is the incident is major for this entry."""
        return self._search_in_properties(ATTR_ISMAJOR) == True

    @property
    def isEnded(self) -> bool:
        """
        Return  true if the hazard has ended, otherwise false. Once ended, the hazard’s 
        record in our internal tracking system is closed and further modification
        becomes impossible unless the record is later re-opened. This 
        property is a counterpart to the createdproperty. When true, the 
        lastUpdatedproperty of the hazard will be the date/time when 
        the hazard’s record  in the tracking system was closed.
        """
        return self._search_in_properties(ATTR_ISENDED) == True

    @property
    def isNew(self) -> bool:
        """Return  true if the incident is new for this entry."""
        return self._search_in_properties(ATTR_ISNEW) == True

    @property
    def isImpactNetwork(self) -> bool:
        """Return  true if the hazard is currently having some impact on traffic on the road network."""
        return self._search_in_properties(ATTR_IMPACTNETWORK) == True

    @property
    def diversions(self) -> str:
        """Return the Summary of any traffic diversions in place. The text may contain HTML markup.."""
        return self._search_in_properties(ATTE_DIVERSIONS)

    @property
    def type(self) -> str:
        """Return the type of incident of this entry. (Planned or Unplanned) A Planned hazard must have the properties: startand end. And optionally the properties: durationand periods. An Unplanned hazard will not contain these properties."""
        return self._search_in_properties(ATTR_INCIDENT_KIND)
    
    @property
    def subCategory(self) -> str:
        """Return the sub-category of incident of this entry."""
        return self._search_in_properties(ATTR_INCIDENT_SUBCAT)

    @property
    def duration(self) -> str:
        """Return the Planned duration of the hazard. This property is rarely used."""
        return self._search_in_properties(ATTR_DURATION)
      

    @property
    def council_area(self) -> str:
        """Return the council area of this entry."""
        return self._search_in_properties(ATTR_ROADS)[0]["suburb"]

    @property
    def road(self) -> str:
        """Return the council area of this entry."""
        return self._search_in_properties(ATTR_ROADS)[0]["mainStreet"]
