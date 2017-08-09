from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres import fields
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import RegexValidator
from django.db import models
from django.utils.functional import cached_property

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from .mixins import ApiHutMixin, ApiCampsiteMixin
from .utils import validate_only_one_instance


class HomePage(Page):
    def clean(self):
        validate_only_one_instance(self)

    class Meta:
        verbose_name = "NZ Huts Home"


class Alert(models.Model):
    """
        Hut and Campsite alerts. Example of result:

        {
          "assetId": 100043757, # id of the hut/campsite
          "name": "Anapai Bay Campsite",
          "alerts": [
            {
              "displayDate": "01 October 2016",
              "heading": "Abel Tasman National Park, pest control operation",
              "detail": "<p>DOC and Project Janszoon completed an aerial application of 1080 pesticide in the Northern Abel Tasman National Park on 9&nbsp;September 2016 to control possums. The treatment area was from the northern side of the Awaroa estuary north to Separation Point. All huts, camp sites and beaches were excluded from the treatment area. Tracks and roads in the area have been cleared of bait but park users should be aware that baits can get caught up in trees and can be dislodged through wind action many days after the operation. Do not touch these baits.&nbsp;</p>\r\n<p>Dogs are particularly susceptible to this poison. Dogs are only allowed in the park by permit, but people with dogs in areas adjoining the park including Awaroa and Wainui Bay, need to keep their dogs under control to avoid contact with carcasses. For further information contact the DOC Motueka Office, phone +64 3 528 1810.</p>"
            }
          ]
        }
    """
    API_FIELDS_MAPPING = {
        'assetId': 'asset_id',
        'name': 'name',
    }

    name = models.CharField(max_length=200, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    asset_id = models.CharField(max_length=9, unique=True, validators=[RegexValidator(r'^\d{1,9}$')])
    content_object = GenericForeignKey('content_type', 'asset_id')

    @cached_property
    def messages(self):
        return self.alert_message.all()


class AlertMessage(models.Model):
    """
    Detail alert message belonging to an Alert
    """
    API_FIELDS_MAPPING = {
        'date': 'date',
        'heading': 'heading',
        'detail': 'detail'
    }

    date = models.DateField(null=True)
    heading = models.CharField(max_length=400, blank=True)
    detail = models.TextField(max_length=3000, blank=True)
    alert = models.ForeignKey('Alert', on_delete=models.CASCADE, related_name='alert_message')


class HutPageFacility(TaggedItemBase):
    content_object = ParentalKey('HutPage', related_name='hut_facilities')


class HutPage(Page, ApiHutMixin):
    subpage_types = []
    parent_page_types = ['HutIndexPage']
    alerts = GenericRelation(Alert)

    facilities = ClusterTaggableManager(through=HutPageFacility, blank=True, related_name='facility_huts')

    content_panels = Page.content_panels + [
        FieldPanel('facilities'),
    ]
    api_panels = [
        # common fields
        FieldPanel('asset_id'),
        FieldPanel('name'),
        FieldPanel('location'),
        FieldPanel('raw_facilities'),
        FieldPanel('intro'),
        FieldPanel('intro_thumbnail'),
        FieldPanel('link_url'),
        FieldPanel('region'),
        FieldPanel('place'),
        FieldPanel('x'),
        FieldPanel('y'),
        # hut specific fields
        FieldPanel('bunks'),
        FieldPanel('category'),
        FieldPanel('proximity'),
        FieldPanel('bookable'),
        FieldPanel('status'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(api_panels, heading='API fields'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    class Meta:
        verbose_name = "Hut Page"


class CampsitePageFacility(TaggedItemBase):
    content_object = ParentalKey('HutPage', related_name='campsite_facilities')


class CampsitePageLandscape(TaggedItemBase):
    content_object = ParentalKey('HutPage', related_name='campsite_landscapes')


class CampsitePageActivity(TaggedItemBase):
    content_object = ParentalKey('HutPage', related_name='campsite_activities')


class CampsitePage(Page, ApiCampsiteMixin):
    subpage_types = []
    parent_page_types = ['CampsiteIndexPage']
    alerts = GenericRelation(Alert)

    facilities = ClusterTaggableManager(through=CampsitePageFacility, blank=True, related_name='facility_campsites')
    landscapes = ClusterTaggableManager(through=CampsitePageLandscape, blank=True, related_name='landscape_campsites')
    activities = ClusterTaggableManager(through=CampsitePageActivity, blank=True, related_name='activity_campsites')

    promote_panels = Page.promote_panels + [
        FieldPanel('facilities'),
        FieldPanel('landscapes'),
        FieldPanel('activities'),
    ]

    class Meta:
        verbose_name = "Campsite Page"


class HutIndexPage(Page):
    subpage_types = ['HutPage']
    parent_page_types = ['HomePage']

    def get_context(self, request):
        context = super(HutIndexPage, self).get_context(request)
        page = request.GET.get('page')
        tag = request.GET.get('tag')
        pages = HutPage.objects.child_of(self).live()
        if tag:
            pages = pages.filter(facilities__slug__iexact=tag)
            context['tag'] = Tag.objects.get(slug__iexact=tag)
        paginator = Paginator(pages, 10)  # Show 10 huts per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        context['children'] = pages
        return context

    class Meta:
        verbose_name = "All Hut Pages"


class CampsiteIndexPage(Page):
    subpage_types = ['CampsitePage']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = "All Campsite Pages"
