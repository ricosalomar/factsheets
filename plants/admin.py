from django.contrib import admin
from plants.models import Plant, Category,CommonName, Cultivar, PlantImage, OldUrl
from django.forms import CheckboxSelectMultiple


# class CategoryInline(admin.TabularInline):
#     model = Plant.category.through
#     extra = 0
class CategoryAdmin(admin.ModelAdmin):
    fields = ['category']

class FlowerColorAdmin(admin.ModelAdmin):
    fields = ['search_flower_color']

class LeafColorAdmin(admin.ModelAdmin):
    fields = ['search_leaf_color']

class LightAdmin(admin.ModelAdmin):
    fields = ['search_light']

class CommonNameInline(admin.TabularInline):
    model = CommonName
    extra = 0

class CultivarInline(admin.TabularInline):
    model = Cultivar
    extra = 0

class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 0

class OldUrlInline(admin.TabularInline):
    model = OldUrl
    extra = 0

class PlantAdmin(admin.ModelAdmin):
    fields = ['scientific_name',
                'genus',
                'species',
                'category',
                'comment',
                'description',
                'search_flower_color',
                'search_leaf_color',
                'search_light',
                'search_season',
                'attracts',
                'drought_tolerant',
                'update_time',
                'tags',
                'season',
                'light',
                'color',
                'height',
                'width',
                'space',
                'flowering_period',
                'flower_color',
                'depth',
                'usage',
                'organ',
                'hardiness',
                'zones',
                'habit',
                # 'rate',
                'size',
                'texture',
                'form',
                'propagation',
                'exposure',
                'fruit',
                'soil',
                'inflorescence',
                'regions',
                'family',
                'origin',
                'distribution',
                'found',
                'mode',
                'edibility',
                'severity',
                'sub_type',
                'fragrance',
                'growth_rate',
                'climbing_method',
                'life_cycle',
                'foliage',
                'flower',
                'fronds',
                'site',
                'leaf',
                'storage',
                'poison_part',
                'symptoms',
                'toxic_principle',
                'internal_comment', ]
    ordering = ('scientific_name',)
    readonly_fields = ['update_time', 'update_by', OldUrlInline]
    inlines = [ CommonNameInline, CultivarInline, PlantImageInline, OldUrlInline,]
    list_display = ('scientific_name','common_names', 'categories','update_time', 'internal_comment')
    list_filter = ['category','updated','update_time']

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'search_flower_color' or db_field.name == 'search_leaf_color' or db_field.name == 'category' or db_field.name == 'search_light' or db_field.name == 'search_season' or db_field.name == 'attracts':
            kwargs['widget'] = CheckboxSelectMultiple()
            kwargs['help_text'] = ''

        return db_field.formfield(**kwargs)

    class Media:
        js = (
            '/static/plants/js/tiny_mce/tiny_mce.js',
            '/static/plants/js/tiny_mce/textareas.js',
        )

        css = {
            'all': ('/static/plants/css/admin/admin.css',)
        }

# class CategoryAdmin(admin.ModelAdmin):
#     fields = ['category']


admin.site.register(Plant, PlantAdmin)
# admin.site.register(Category, CategoryAdmin)
