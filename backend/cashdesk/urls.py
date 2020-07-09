"""cashdesk URL Configuration"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import routers
from accounts.views import AccountViewSet, TransactionViewSet
from items.views import ItemViewSet
from items.fetch_images import fetch

index_view = never_cache(TemplateView.as_view(template_name="index.html"))

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet, basename="Accounts")
router.register('items', ItemViewSet, basename="Items")
router.register('transactions', TransactionViewSet, basename="Transactions")

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/', include(router.urls)),
    re_path(r'', index_view, name="index")
]

fetch()
