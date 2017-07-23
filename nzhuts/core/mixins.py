from django.contrib.postgres import fields
from django.contrib.gis.geos import Point
from django.db import models
from django.core.validators import RegexValidator


API_HUT_STATUS = (
    ('OPEN', 'OPEN'),
    ('CLOSED', 'CLOSED'),
)
API_HUT_CATEGORIES = (
    ('Standard', 'Standard'),
    ('Basic/Bivvies', 'Basic/Bivvies'),
    ('Serviced', 'Serviced'),
    ('Great Walks', 'Great Walks'),
    ('Scenic', 'Scenic'),
    ('Serviced Alpine', 'Serviced Alpine'),
)
API_CAMPSITE_STATUS = (
    ('OPEN', 'OPEN'),
    ('CLOSED', 'CLOSED'),
)
API_CAMPSITE_CATEGORIES = (
    ('Backcountry', 'Backcountry'),
    ('Basic', 'Basic'),
    ('Serviced', 'Serviced'),
    ('Great Walk', 'Great Walk'),
    ('Scenic', 'Scenic'),
    ('Standard', 'Standard'),
)


class ApiCommonMixin(models.Model):
    """
    Common fields for Hut and Campsite instances
    """
    asset_id = models.CharField(max_length=9, unique=True, validators=[RegexValidator(r'^\d{1,9}$')])
    name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=400, blank=True)
    raw_facilities = fields.ArrayField(models.CharField(max_length=100, blank=True), blank=True)
    intro = models.TextField(max_length=3000, blank=True)
    intro_thumbnail = models.URLField(blank=True)
    link_url = models.URLField(blank=True)
    region = models.CharField(max_length=200, blank=True)
    place = models.CharField(max_length=400, blank=True)
    x = models.IntegerField(null=True)  # X coordinate in NZTM2000 projection
    y = models.IntegerField(null=True)  # Y coordinate in NZTM2000 projection

    def get_point():
        return Point(x, y, srid=2193)  # NZTM2000 projection

    class Meta:
        abstract = True


class ApiHutMixin(ApiCommonMixin):
    """
        Example of response data from /huts/100072002/detail

        {
          "assetId": 100072002,
          "name": "Poutaki Hut",
          "locationString": "Located in Ruahine Forest Park",
          "numberOfBunks": 4,
          "facilities": [
            "Heating"
          ],
          "hutCategory": "Basic/bivvies",
          "proximityToRoadEnd": null,
          "bookable": false,
          "introduction": "This is a basic four-bunk hut in the Hawke's Bay region.",
          "introductionThumbnail": "http://www.doc.govt.nz/images/no-photo-220x140.jpg",
          "staticLink": "http://www.doc.govt.nz/link/43d5f6b8ce4241bfb877ba7fdd6f8786.aspx",
          "region": "Hawke's Bay",
          "place": "Ruahine Forest Park",
          "status": "OPEN",
          "x": 1884086,
          "y": 5597140
        }
    """
    API_FIELDS_MAPPING = {
        'assetId': 'asset_id',
        'name': 'name',
        'locationString': 'location',
        'numberOfBunks': 'bunks',
        'facilities': 'raw_facilities',
        'hutCategory': 'category',
        'proximityToRoadEnd': 'proximity',
        'bookable': 'bookable',
        'introduction': 'intro',
        'introductionThumbnail': 'intro_thumbnail',
        'staticLink': 'link_url',
        'region': 'region',
        'place': 'place',
        'status': 'status',
        'x': 'x',
        'y': 'y',
    }

    bunks = models.PositiveIntegerField(blank=True)
    category = models.CharField(max_length=200, choices=API_HUT_CATEGORIES, blank=True)
    proximity = models.CharField(max_length=200, blank=True)
    bookable = models.BooleanField(blank=True)
    status = models.CharField(max_length=200, choices=API_HUT_STATUS)

    class Meta:
        abstract = True

class ApiCampsiteMixin(ApiCommonMixin):
    """
        Example of response data from /campsites/100044048/detail

        {
          "assetId": 100044048,
          "campsiteCategory": "Basic",
          "dogsAllowed": "Dogs on a leash only",
          "facilities": [
            [
              "Non-powered/tent sites",
              "Water from stream",
              "Water from tap"
            ]
          ],
          "free": false,
          "landscape": [
            [
              "Rivers and lakes",
              "Alpine"
            ]
          ],
          "locationString": "Located in Abel Tasman National Park",
          "numberOfPoweredSites": 0,
          "numberOfUnpoweredSites": 6,
          "name": "Anapai Bay Campsite",
          "introduction": "Walk-in or boat-in to this beachside campsite on the Waiharakeke to Whariwharangi section of the Abel Tasman Coast Track.",
          "introductionThumbnail": "/thumbs/large/pagefiles/29491/anapai223.jpg",
          "activities": [
            [
              "Caving",
              "Picnicking",
              "Walking and tramping"
            ]
          ],
          "staticLink": "http://www.doc.govt.nz/link/6b8984ad28c74b25b54780661cf0676a.aspx",
          "region": "Nelson/Tasman",
          "place": "Abel Tasman National Park",
          "status": "OPEN",
          "x": 1600360,
          "y": 5483142
        }
    """
    API_FIELDS_MAPPING = {
        'assetId': 'asset_id',
        'campsiteCategory': 'category',
        'dogsAllowed': 'dogs_allowed',
        'facilities': 'raw_facilities',
        'is_free': 'free',
        'landscape': 'raw_landscape',
        'locationString': 'location',
        'numberOfPoweredSites': 'powered_sites',
        'numberOfUnpoweredSites': 'unpowered_sites',
        'name': 'name',
        'introduction': 'intro',
        'introductionThumbnail': 'intro_thumbnail',
        'activities': 'raw_activities',
        'staticLink': 'link_url',
        'region': 'region',
        'place': 'place',
        'status': 'status',
        'x': 'x',
        'y': 'y',
    }

    dogs_allowed = models.BooleanField(blank=True)
    is_free = models.BooleanField(blank=True)
    raw_landscape = fields.ArrayField(models.CharField(max_length=100, blank=True), blank=True)
    powered_sites = models.PositiveIntegerField(blank=True)
    unpowered_sites = models.PositiveIntegerField(blank=True)
    raw_activities = fields.ArrayField(models.CharField(max_length=100, blank=True), blank=True)

    class Meta:
        abstract = True
