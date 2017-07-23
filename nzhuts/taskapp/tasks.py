import logging
import requests

from celery import Celery
from celery.decorators import task

from django.conf import settings

from nzhuts.core.models import HutPage, HutIndexPage
app = Celery('nzhuts')


@app.task(name="fetch_huts")
def fetch_huts():
    huts_index = HutIndexPage.objects.first()
    url = settings.API_HUTS_BASE_URL
    headers = {'x-api-key': settings.API_KEY}
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.exception(str(e))
    if r.status_code == 200:
        for h in r.json():
            try:
                rh = requests.get('%s/%s/detail' % (url, h['assetId']), headers=headers)
            except requests.exceptions.RequestException as e:
                logger.exception(str(e))
            else:
                if r.status_code == 200:
                    rh_json = rh.json()
                    try:
                        hut = HutPage.objects.get(asset_id=rh_json['assetId'])
                    except HutPage.DoesNotExist:
                        hut = HutPage(title=rh_json['name'], seo_title=rh_json['name'], asset_id=rh_json['assetId'])
                    for key, value in HutPage.API_FIELDS_MAPPING.items():
                        setattr(obj, value, rh_json[key])
                    huts_index.add_child(hut)
                    print(hut)
                else:
                    logger.error("Failed hut details request with status %s, %s", str(r.status_code), r.json()['message'])
    else:
        logger.error("Failed huts request with status %s, %s", str(r.status_code), r.json()['message'])
