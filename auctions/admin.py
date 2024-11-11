from django.contrib import admin
from .models import Auctions, Comments, Bids

# Register your models here.
admin.site.register(Auctions)
admin.site.register(Comments)
admin.site.register(Bids)