"""NSW Transport Service Incidents feed."""
import logging
from typing import List, Optional, Tuple, Dict
from datetime import datetime
 
import asyncio
from aio_geojson_client.feed import GeoJsonFeed
from aio_geojson_client.consts import (DEFAULT_REQUEST_TIMEOUT, UPDATE_ERROR, UPDATE_OK,
                     UPDATE_OK_NO_DATA)
from aiohttp import ClientSession
from geojson import FeatureCollection

from json import JSONDecodeError

import aiohttp
import geojson
from aiohttp import ClientSession, client_exceptions
from geojson import FeatureCollection




from .consts import URL_BASE
from .feed_entry import NswTransportServiceIncidentsFeedEntry

_LOGGER = logging.getLogger(__name__)


class NswTransportServiceIncidentsFeed(
        GeoJsonFeed[NswTransportServiceIncidentsFeedEntry]):
    """NSW Transport Services Incidents feed."""

    def __init__(self,
                 websession: ClientSession,
                 home_coordinates: Tuple[float, float],
                 filter_radius: float = None,
                 hazard: str = None,
                 filter_categories: str = None):
        """Initialise this service."""
        if(hazard is None):
            hazard = "incident-open"
        URL = f"{URL_BASE+hazard.lower()}.json"
        super().__init__(websession,
                         home_coordinates,
                         URL,
                         filter_radius=filter_radius)
        self._filter_categories = filter_categories

    def __repr__(self):
        """Return string representation of this feed."""
        return '<{}(home={}, url={}, radius={}, categories={})>'.format(
            self.__class__.__name__, self._home_coordinates, self._url,
            self._filter_radius, self._filter_categories)

    def _new_entry(self, home_coordinates: Tuple[float, float], feature,
                   global_data: Dict) -> NswTransportServiceIncidentsFeedEntry:
        """Generate a new entry."""
        return NswTransportServiceIncidentsFeedEntry(home_coordinates, feature)

    def _filter_entries(self,
                        entries: List[NswTransportServiceIncidentsFeedEntry]) \
            -> List[NswTransportServiceIncidentsFeedEntry]:
        """Filter the provided entries."""
        filtered_entries = super()._filter_entries(entries)
        if self._filter_categories:
            filtered_entries = list(filter(lambda entry:
                                    entry.category in self._filter_categories,
                                    filtered_entries))
        return filtered_entries

    def _extract_last_timestamp(
            self,
            feed_entries: List[NswTransportServiceIncidentsFeedEntry]) \
            -> Optional[datetime]:
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(filter(
                None, [entry.publication_date for entry in feed_entries]),
                reverse=True)
            return dates[0]
        return None

    def _extract_from_feed(self, feed: FeatureCollection) -> Optional[Dict]:
        """Extract global metadata from feed."""
        return None


    async def _fetch(self,
                     method: str = "GET",
                     headers=None,
                     params=None) -> Tuple[str, Optional[FeatureCollection]]:
        """Fetch GeoJSON data from external source. and overwrite the POINT geometry issue"""
        try:
            timeout = aiohttp.ClientTimeout(
                total=self._client_session_timeout())
            async with self._websession.request(
                    method, self._url, headers=headers, params=params,
                    timeout=timeout
            ) as response:
                try:
                    response.raise_for_status()
                    text = await response.text()
                    # ARCGIS generates files with all upper case features, which is not valid for the geoJson standards
                    feature_collection = geojson.loads(text.replace('POINT','Point'))                    
                    return UPDATE_OK, feature_collection
                except client_exceptions.ClientError as client_error:
                    _LOGGER.warning("Fetching data from %s failed with %s",
                                    self._url, client_error)
                    return UPDATE_ERROR, None
                except JSONDecodeError as decode_ex:
                    _LOGGER.warning("Unable to parse JSON from %s: %s",
                                    self._url, decode_ex)
                    return UPDATE_ERROR, None
        except client_exceptions.ClientError as client_error:
            _LOGGER.warning("Requesting data from %s failed with "
                            "client error: %s",
                            self._url, client_error)
            return UPDATE_ERROR, None
        except asyncio.TimeoutError:
            _LOGGER.warning("Requesting data from %s failed with "
                            "timeout error", self._url)
            return UPDATE_ERROR, None
