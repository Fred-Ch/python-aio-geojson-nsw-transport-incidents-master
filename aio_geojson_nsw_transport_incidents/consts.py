"""NSW Transport Service Incidents constants."""

ATTR_CATEGORY = "mainCategory" 
ATTR_DESCRIPTION = "headline"
ATTR_OTHERADVICE = "otherAdvice"
ATTR_GUID = "id"
ATTR_PUB_DATE = "created"
ATTR_TITLE = "displayName"

ATTR_PUBLIC_TRANSPORT = "publicTransport"
ATTR_FEATURE_TYPE = "type"
ATTR_ROADS= "roads"

ATTR_ADVICEA = "adviceA"
ATTR_ADVICEB = "adviceB"
ATTR_ADVICE_OTHER = "otherAdvice"
ATTR_ISMAJOR = "isMajor"
ATTR_INCIDENT_KIND = "incidentKind"
ATTR_INCIDENT_SUBCAT ="subCategoryA"
ATTR_ISNEW = "isNewIncident"
ATTR_IMPACTNETWORK = "impactingNetwork"
ATTR_ISENDED = "ended"

ATTE_DIVERSIONS = "diversions"
ATTR_DURATION = "duration"

ATTR_COUNCIL_AREA = "roads.0.suburb" # to verify

ATTRIBUTION = "State of New South Wales (NSW Transport Service)"

CUSTOM_ATTRIBUTE = "custom_attribute"

# REGEXP_ATTR_COUNCIL_AREA = "COUNCIL AREA: (?P<{}>[^<]+) <br"\
#     .format(CUSTOM_ATTRIBUTE)
# REGEXP_ATTR_FIRE = "FIRE: (?P<{}>[^<]+) <br".format(CUSTOM_ATTRIBUTE)
# REGEXP_ATTR_LOCATION = "LOCATION: (?P<{}>[^<]+) <br".format(CUSTOM_ATTRIBUTE)
# REGEXP_ATTR_RESPONSIBLE_AGENCY = "RESPONSIBLE AGENCY: (?P<{}>[^<]+) <br"\
#     .format(CUSTOM_ATTRIBUTE
# )
# REGEXP_ATTR_SIZE = "SIZE: (?P<{}>[^<]+) <br".format(CUSTOM_ATTRIBUTE)
# REGEXP_ATTR_STATUS = "STATUS: (?P<{}>[^<]+) <br".format(CUSTOM_ATTRIBUTE)
# REGEXP_ATTR_TYPE = "TYPE: (?P<{}>[^<]+) <br".format(CUSTOM_ATTRIBUTE)

URL = "http://data.livetraffic.com/traffic/hazards/flood-open.json"
URL_BASE = "http://data.livetraffic.com/traffic/hazards/"

VALID_CATEGORIES = [
    "Emergency Warning",
    "Watch and Act",
    "Advice",
    "Not Applicable"
]
VALID_HAZARDSS = [
    "Incidents",
    "Fire",
    "Flood",
    "Alpine",
    "conditions",
    "Major Events",
    "Roadworks"
]
