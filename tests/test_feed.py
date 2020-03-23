"""Test for the NSW Transport Service Incidents GeoJSON feed."""
import datetime
import pytz

import aiohttp
import pytest

from aio_geojson_client.consts import UPDATE_OK

from aio_geojson_nsw_transport_incidents.consts import ATTRIBUTION
from aio_geojson_nsw_transport_incidents.feed import NswTransportServiceIncidentsFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        'data.livetraffic.com',
        '/traffic/hazards/flood-open.json',
        'get',
        aresponses.Response(text=load_fixture('flood-open.json'),
                            status=200),
        match_querystring=True,
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        timezone = pytz.timezone("UTC")
        feed = NswTransportServiceIncidentsFeed(websession, home_coordinates,hazard="flood-open")
        assert repr(feed) == "<NswTransportServiceIncidentsFeed(" \
                             "home=(-31.0, 151.0), " \
                             "url=http://data.livetraffic.com" \
                             "/traffic/hazards/flood-open.json, " \
                             "radius=None, categories=None)>"
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 5

        feed_entry = entries[0]
        assert feed_entry.title == "FLOODING"
        assert feed_entry.category == "Flooding"
        assert feed_entry.external_id == 53718
        assert feed_entry.coordinates == (-32.212312, 148.211304)
        assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 417.9
        assert repr(feed_entry) == "<NswTransportServiceIncidents" \
                                   "FeedEntry(id=53718)>"

        # assert timezone.localize(feed_entry.publication_date) \
        #     == datetime.datetime(2020, 3, 4, 2, 27, 31, 513000 , pytz.UTC)
        assert feed_entry.type == "Unplanned"
        assert feed_entry.attribution == ATTRIBUTION

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.title == "FLOODING"
        assert feed_entry.category == "Flooding"
        # assert not feed_entry.fire

        feed_entry = entries[2]
        assert feed_entry.title == "FLOODING"
        assert feed_entry.category  == "Flooding"

        feed_entry = entries[3]
        assert feed_entry.title == "FLOODING"
        assert feed_entry.geometries is not None
        assert len(feed_entry.geometries) == 1
        assert round(abs(feed_entry.distance_to_home - 578.5), 1) == 163.7


@pytest.mark.asyncio
async def test_update_ok_with_categories(aresponses, event_loop):
    """Test updating feed is ok, filtered by category."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        'data.livetraffic.com',
        '/traffic/hazards/flood-open.json',
        'get',
        aresponses.Response(text=load_fixture('flood-open.json'),
                            status=200),
        match_querystring=True,
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = NswTransportServiceIncidentsFeed(
            websession, home_coordinates, hazard="flood-open", filter_categories=['Flooding'])
        assert repr(feed) == "<NswTransportServiceIncidentsFeed(" \
                             "home=(-31.0, 151.0), " \
                             "url=http://data.livetraffic.com/traffic/hazards/flood-open.json, " \
                             "radius=None, categories=['Flooding'])>"
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 5

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "FLOODING"
        assert feed_entry.category == "Flooding"
        assert repr(feed_entry) == "<NswTransportServiceIncidents" \
                                   "FeedEntry(id=53718)>"


@pytest.mark.asyncio
async def test_empty_feed(aresponses, event_loop):
    """Test updating feed is ok when feed does not contain any entries."""
    home_coordinates = (-41.2, 174.7)
    aresponses.add(
        'data.livetraffic.com',
        '/traffic/hazards/incident-open.json',
        'get',
        aresponses.Response(text=load_fixture('incidents-2.json'),
                            status=200),
        match_querystring=True,
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = NswTransportServiceIncidentsFeed(websession, home_coordinates)
        assert repr(feed) == "<NswTransportServiceIncidentsFeed(" \
                             "home=(-41.2, 174.7), " \
                             "url=http://data.livetraffic.com" \
                             "/traffic/hazards/incident-open.json, " \
                             "radius=None, categories=None)>"
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
        assert feed.last_timestamp is None
