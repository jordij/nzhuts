import logging
import requests
import metadata_parser
from bs4 import BeautifulSoup
from io import BytesIO

from celery import shared_task
from celery import group

from django.conf import settings
from django.core.files.images import ImageFile

from wagtail.wagtailimages.models import Image

from nzhuts.core.models import HutPage, HutIndexPage

logger = logging.getLogger(__name__)


@shared_task(name="nzhuts.taskapp.tasks.fetch_all_huts", expires=3600, retry=True, retry_policy={'max_retries': 3, 'interval_start': 30})
def fetch_all_huts():
    headers = {'x-api-key': settings.API_KEY}
    subtasks = []
    try:
        r = requests.get(settings.API_HUTS_BASE_URL, headers=headers, timeout=settings.API_TIMEOUT)
    except requests.exceptions.RequestException as e:
        logger.exception(str(e))
    if r.status_code == 200:
        for h in r.json():
            subtasks.append(fetch_hut.s(h['assetId']))
    else:
        logger.error("Failed huts request with status %s, %s", str(r.status_code), r.json()['message'])
    results = group(subtasks)()  # in parallel
    results.get()


@shared_task(name="nzhuts.taskapp.tasks.fetch_hut", expires=300, retry=True, retry_policy={'max_retries': 5, 'interval_start': 10})
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
        else:
            logger.error("Failed hut details request with status %s, %s", str(rh.status_code), rh.json()['message'])


@shared_task(name="nzhuts.taskapp.tasks.fetch_hut_images", expires=300, retry=True, retry_policy={'max_retries': 5, 'interval_start': 10})
def fetch_hut_images():
    for hpage in HutPage.objects.all():
        if hpage.link_url:
            try:
                r = requests.get(hpage.link_url, timeout=settings.API_TIMEOUT)
            except requests.exceptions.RequestException as e:
                logger.exception(str(e))
            else:
                soup = BeautifulSoup(r.content, 'html5lib')
                a_tag = soup.find_all("a", {"class": "fancybox-gallery"})
                if a_tag:
                    img_tag = a_tag[0].find_all("img")
                    if img_tag:
                        img_url = 'http://www.doc.govt.nz/%s' % img_tag[0].get('src')
                        logger.debug("Hut %s using img %s from HTML body.", str(hpage.pk), img_url)
                else:
                    page = metadata_parser.MetadataParser(url=hpage.link_url)
                    img_url = page.get_metadata_link('image')
                    logger.debug("Hut %s using img %s from HTML meta", str(hpage.pk), img_url)
                if img_url:
                    try:
                        response = requests.get(img_url, timeout=settings.API_TIMEOUT)
                    except requests.exceptions.RequestException as e:
                        logger.exception(str(e))
                    image = Image(title=hpage.title, file=ImageFile(BytesIO(response.content), name=img_url.split('/')[-1]))
                    image.save()
                    hpage.meta_image = image
                    hpage.save()
                else:
                    logger.debug("No img found for hut %s", str(hpage.pk))
