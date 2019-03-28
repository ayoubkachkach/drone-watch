from .models import Article
from .models import DateEntity
from .models import InjuredEntity
from .models import KilledEntity
from .models import LocationEntity
from .models import PerpetratorEntity
from .models import Source
from django.contrib import admin

admin.site.register(Article)
admin.site.register(DateEntity)
admin.site.register(LocationEntity)
admin.site.register(KilledEntity)
admin.site.register(InjuredEntity)
admin.site.register(PerpetratorEntity)
admin.site.register(Source)
