from django.db import models
# from model_utils.managers import InheritanceManager
from django.http import HttpRequest
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager

class Category(models.Model):
    category = models.CharField(max_length=128)
    slug = models.SlugField(editable=False)

    def __unicode__(self):
        return self.category

    class Meta:
        ordering = ('category',)
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.category)

        super(Category, self).save(*args, **kwargs)


class Color(models.Model):
    color = models.CharField(max_length=64)

    def __unicode__(self):
        return self.color

    class Meta:
        ordering = ('color',)

class Light(models.Model):
    light=models.CharField(max_length=64)

    def __unicode__(self):
        return self.light

class Season(models.Model):
    season=models.CharField(max_length=16)

    def __unicode__(self):
        return self.season

class Attracts(models.Model):
    attracts=models.CharField(max_length=64)

    def __unicode__(self):
        return self.attracts


class Plant(models.Model):

    scientific_name = models.CharField(max_length=128, unique=True)
    update_time = models.DateTimeField(auto_now=True)
    update_by = models.CharField(max_length=128)
    comment = models.TextField(blank=True)
    internal_comment = models.TextField(blank=True)
    slug = models.SlugField(blank=True,editable=False)
    tags = TaggableManager(blank=True)

    updated = models.BooleanField(default=False)
    drought_tolerant = models.BooleanField(default=False)

    search_flower_color = models.ManyToManyField(Color, related_name='plant_flower_color', blank=True)
    search_leaf_color = models.ManyToManyField(Color, related_name='plant_leaf_color', blank=True)
    search_light = models.ManyToManyField(Light, blank=True)
    search_season = models.ManyToManyField(Season, blank=True)
    attracts = models.ManyToManyField(Attracts, blank=True)
    category = models.ManyToManyField(Category)

    height = models.CharField(max_length=128, blank=True)
    width = models.CharField(max_length=128, blank=True)
    size = models.CharField(max_length=128, blank=True)
    depth = models.CharField(max_length=128, blank=True)
    space = models.CharField(max_length=128, blank=True)
    growth_rate = models.CharField(max_length=128, blank=True)
    climbing_method = models.CharField(max_length=128, blank=True)
    life_cycle = models.CharField(max_length=128, blank=True)

    site = models.CharField(max_length=128, blank=True)
    light = models.CharField(max_length=128, blank=True)
    soil = models.CharField(max_length=128, blank=True)
    exposure = models.CharField(max_length=128, blank=True)
    hardiness = models.CharField(max_length=128, blank=True)
    propagation = models.CharField(max_length=128, blank=True)

    regions = models.CharField(max_length=128, blank=True)
    zones = models.CharField(max_length=128, blank=True)
    habit = models.CharField(max_length=128, blank=True)

    organ = models.CharField(max_length=128, blank=True)
    fruit = models.CharField(max_length=128, blank=True)
    leaf = models.CharField(max_length=256, blank=True)
    foliage = models.CharField(max_length=256, blank=True)
    flower = models.CharField(max_length=256, blank=True)
    flower_color = models.CharField(max_length=128, blank=True)
    color = models.CharField(max_length=128, blank=True)
    fronds = models.CharField(max_length=256, blank=True)
    texture = models.CharField(max_length=256, blank=True)
    form = models.CharField(max_length=128, blank=True)
    sub_type = models.CharField(max_length=128, blank=True)
    fragrance = models.CharField(max_length=128, blank=True)
    inflorescence = models.CharField(max_length=128, blank=True)

    season = models.CharField(max_length=128, blank=True)
    flowering_period = models.CharField(max_length=128, blank=True)
    storage = models.TextField(blank=True)
    usage = models.CharField(max_length=128, blank=True)

    # poison
    family = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)
    origin = models.CharField(max_length=128, blank=True)
    distribution = models.CharField(max_length=128, blank=True)
    found = models.CharField(max_length=128, blank=True)
    mode = models.CharField(max_length=128, blank=True)
    poison_part = models.TextField(blank=True)
    symptoms = models.TextField(blank=True)
    edibility = models.CharField(max_length=128, blank=True)
    toxic_principle = models.TextField(blank=True)
    severity = models.CharField(max_length=128, blank=True)


    # objects = InheritanceManager()

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            if self.scientific_name.__len__() > 49:
                sci_name = self.scientific_name[:49]
            else:
                sci_name = self.scientific_name
            self.slug = slugify(sci_name)

        self.updated = True

        super(Plant, self).save(*args, **kwargs)


    def common_names(self):
        return ', '.join([c.common_name for c in self.commonname_set.all()])

    def cultivars(self):
        return ', '.join([c.cultivar for c in self.cultivar_set.all()])

    def categories(self):
        return ', '.join([c.category for c in self.category.all()])

    def old_urls(self):
        return ', '.join([c.old_url for c in self.oldurl_set.all()])

    def category_links(self):
        urls = []
        for c in self.category.all():
            urls.append('<a href="/plants/category/%s"/>%s</a>' % (c.category, c.category))
        return ', '.join(urls)

    def images(self):
        imgs = ' /><img src="'.join([i.img_url for i in self.plantimage_set.all()])
        return '<img src="'+imgs+' />'

    def get_fields(self):
        # return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
        fields=[('Common Name(s)', self.common_names()),
                ('Cultivar(s)', self.cultivars()),
                ('Categories', self.categories()),
                ('Comment', self.comment),
                ('Description', self.description),
                ('Season', self.season),
                ('Light', self.light),
                ('Color', self.color),
                ('Height', self.height),
                ('Space', self.space),
                ('Flowering Period', self.flowering_period),
                ('Flower Color', self.flower_color),
                ('Depth', self.depth),
                ('Usage', self.usage),
                ('Organ', self.organ),
                ('Hardiness', self.hardiness),
                ('Storage', self.storage),
                ('Foliage', self.foliage),
                ('Flower', self.flower),
                ('Zones', self.zones),
                ('Habit', self.habit),
                ('Fronds', self.fronds),
                ('Site', self.site),
                # 'rate',
                ('Size', self.size),
                ('Texture', self.texture),
                ('Form', self.form),
                ('Propagation', self.propagation),
                ('Exposure', self.exposure),
                ('Fruit', self.fruit),
                ('Soil', self.soil),
                ('Inflorescence', self.inflorescence),
                ('Regions', self.regions),
                ('Family', self.family),
                ('Origin', self.origin),
                ('Distribution', self.distribution),
                ('Poison Part', self.poison_part),
                ('Poison Delivery Mode', self.mode),
                ('Symptoms', self.symptoms),
                ('Edibility', self.edibility),
                ('Toxic Principle', self.toxic_principle),
                ('Severity', self.severity),
                ('Found in', self.found),
                ('Type', self.sub_type),
                ('Fragrance', self.fragrance),
                ('Width', self.width),
                ('Growth Rate', self.growth_rate),
                ('Leaf', self.leaf),
                ('Climbing Method', self.climbing_method),
                ('Life Cycle', self.life_cycle),
                # ('Attracts Songbirds', self.attracts_songbirds),
                ('Tags', ', '.join([t.name for t in self.tags.all()])), ]

        if self.category.all().__len__() == 1:
            fields[2] = ('Category', self.categories())


        return fields

    def verbose_name(self):
        return self._meta.verbose_name

    def get_absolute_url(self):
        return '/plants/all/%s/' % (self.slug)

    def __unicode__(self):
        return self.scientific_name

class PlantImage(models.Model):
    plant = models.ForeignKey(Plant)
    img_url = models.URLField()
    alt_text = models.CharField(max_length=64)
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    thumbnail = models.BooleanField(default=False)
    def __unicode__(self):
        return self.img_url

class CommonName(models.Model):
    plant = models.ForeignKey(Plant)
    common_name = models.CharField(max_length=128, null=True)

    def __unicode__(self):
        return self.common_name

class OldUrl(models.Model):
    plant = models.ForeignKey(Plant)
    old_url = models.URLField(max_length=128, null=True)

    def __unicode__(self):
        return self.old_url

class Cultivar(models.Model):

    plant = models.ForeignKey(Plant)
    cultivar = models.CharField(max_length=128)

    def __unicode__(self):
        return self.cultivar