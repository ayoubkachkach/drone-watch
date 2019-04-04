from .models import Article
from .models import DateEntity
from .models import CasualtyEntity
from .models import VictimEntity
from .models import LocationEntity
from .models import PerpetratorEntity
from .models import Source
from django.contrib import admin

admin.site.register(Article)
admin.site.register(DateEntity)
admin.site.register(LocationEntity)
admin.site.register(CasualtyEntity)
admin.site.register(VictimEntity)
admin.site.register(PerpetratorEntity)
admin.site.register(Source)
