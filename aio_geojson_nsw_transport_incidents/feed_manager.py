"""Feed Manager for NSW Transport Service Incidents feed."""
from typing import List, Tuple, Callable, Awaitable

from aio_geojson_client.feed_manager import FeedManagerBase
from aio_geojson_client.status_update import StatusUpdate
from aiohttp import ClientSession
 
from .feed import NswTransportServiceIncidentsFeed


class NswTransportServiceIncidentsFeedManager(FeedManagerBase):
    """Feed Manager for NSW Transport Services Incidents feed."""

    def __init__(self,
                 websession: ClientSession,
                 generate_callback: Callable[[str], Awaitable[None]],
                 update_callback: Callable[[str], Awaitable[None]],
                 remove_callback: Callable[[str], Awaitable[None]],
                 coordinates: Tuple[float, float],
                 filter_radius: float = None,
                 filter_categories: List[str] = None,
                 hazard: str = None,
                 status_callback: Callable[[StatusUpdate],
                                           Awaitable[None]] = None):
        """Initialize the NSW Transport Services Feed Manager."""
        feed = NswTransportServiceIncidentsFeed(
            websession,
            coordinates,
            filter_radius=filter_radius,
            hazard=hazard,
            filter_categories=filter_categories)
        super().__init__(feed,
                         generate_callback,
                         update_callback,
                         remove_callback,
                         status_async_callback=status_callback)
