import logging
import requests

from celery import Celery
from celery.decorators import task

from django.conf import settings

from nzhuts.core.models import HutPage, HutIndexPage
app = Celery('nzhuts')

logger = logging.getLogger(__name__)


@app.task(name="nzhuts.taskapp.tasks.fetch_all_huts")
# , expires=3600, retry=True, retry_policy={'max_retries': 3, 'interval_start': 30})
def fetch_all_huts():
    headers = {'x-api-key': settings.API_KEY}
    try:
        r = requests.get(settings.API_HUTS_BASE_URL, headers=headers, timeout=settings.API_TIMEOUT)
    except requests.exceptions.RequestException as e:
        logger.exception(str(e))
    if r.status_code == 200:
        for h in r.json():
            # fetch_hut(h['assetId'])
            fetch_hut.delay(h['assetId'])
    else:
        logger.error("Failed huts request with status %s, %s", str(r.status_code), r.json()['message'])
    return


@app.task(name="nzhuts.taskapp.tasks.fetch_hut")
# , expires=300, retry=True, retry_policy={'max_retries': 5, 'interval_start': 10})
def fetch_hut(hut_id):
    assert hut_id
    headers = {'x-api-key': settings.API_KEY}
    huts_index = HutIndexPage.objects.first()
    try:
        rh = requests.get('%s/%s/detail' % (settings.API_HUTS_BASE_URL, hut_id), headers=headers, timeout=settings.API_TIMEOUT)
    except requests.exceptions.RequestException as e:
        logger.exception(str(e))
    else:
        if rh.status_code == 200:
            rh_json = rh.json()
            try:
                hut = HutPage.objects.get(asset_id=rh_json['assetId'])
            except HutPage.DoesNotExist:
                hut = HutPage(title=rh_json['name'], seo_title=rh_json['name'], asset_id=rh_json['assetId'])
            for key, value in HutPage.API_FIELDS_MAPPING.items():
                setattr(hut, value, rh_json[key])
            if hut.pk is None:
                huts_index.add_child(instance=hut)
            else:
                hut.save()
            logger.debug(str(hut))
        else:
            logger.error("Failed hut details request with status %s, %s", str(rh.status_code), rh.json()['message'])
