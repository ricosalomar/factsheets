from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import render_to_response
from plants.models import Plant, Category
from urlobject import URLObject
from django.core.cache import cache
from hashlib import sha1
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection
import re

class PlantDetailView(DetailView):
    """
    The plant detail view: returns a plant and a category (for navigation)
    """
    context_object_name='plant'
    template_name='plants/detail.html'
    model = Plant

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(PlantDetailView, self).get_context_data(**kwargs)
        if self.kwargs['cat'] and self.kwargs['cat'] != 'all':
            category = Category.objects.get(slug=self.kwargs['cat'])
        else:
            category = ''
        if 'Poisonous Plants' in [c.category for c in self.object.category.all()]:
            context['poison'] = True
        context['category']= category
        context['plant_url'] = self.request.get_host()+context['plant'].get_absolute_url()
        return context


class PlantCatListView(ListView):
    """
    This view will return a set of all the categories
    """
    context_object_name = 'plant_cat_list'
    template_name = 'plants/index2.html'
    cat_model = Category

    def get_queryset(self):
        return self.cat_model.objects.all().order_by('category')


class CustomPlantListView(TemplateView):
    """
    This is the abstract parent class of the category view and search view. Since the two views have different SQL queries,
    those are in the respective child classes.
    If the view is a Category view, there will be a kwarg['cat'].
    get_query_cache is the method that attempts to retrieve the sql result from the cache, or store a new one.
    The get_context_data method is pretty complex, because it builds the layered navigation on the left side.
    """

    def dispatch(self, request, *args,**kwargs):
        self.query = URLObject(request.get_full_path()).query.dict
        self.full_query_dict = self.query
        self.sort = request.GET.get('s','scientific_name')
        self.sort_direction = request.GET.get('d','asc').upper()
        self.cursor = connection.cursor()
        self.cat = kwargs.get('cat', 'all')
        self.sql = ''
        self.params = ()
        self.request = request

        return super(CustomPlantListView, self).dispatch(request, *args, **kwargs)


    def get_query_cache(self, sql, params):
        """
        cache results of the raw query
        return a list of dict items (rows)
        """
        key = sha1(self.sql).hexdigest()
        if cache.get(key):
            rows = cache.get(key)
        else:
            rows = sqltodict(self.sql,self.params)

            for s in rows:
                m = re.search('[0-9]+ (in.|ft.)', s.get('height', None))
                if m:
                    v = m.group(0).split(' ')
                    if v[1] == 'in.':
                        h = 12 / float(v[0])
                    else:
                        h = int(v[0])

                    if h <= 1:
                        height = '1 ft. or less'
                    elif h <= 3:
                        height = '1-3 ft.'
                    elif h <= 6:
                        height = '3-6 ft.'
                    elif h <= 9:
                        height = '6-9 ft.'
                    elif h <= 20:
                        height = '9-20 ft.'
                    elif h > 20:
                        height = 'greater than 20 ft.'

                    s.update({'search_height': height})
                else:
                    s.update({'search_height': None})

            cache.set(key, rows, 300)

        return rows


    def get_context_data(self, **kwargs):

        NAV_DICT = {
            'category': 'search_categories',
            'light': 'light',
            'flower_color': 'flower_colors',
            'leaf_color': 'leaf_colors',
            'season': 'seasons',
            'attracts': 'attracts',
            'height':'search_height'
        }

        plant_nav = {}
        nav_count = {}

        sql_result_dict_list = self.get_query_cache(self.sql, self.params)

        #
        # This is the section that loops over all the left nav categories (NAV_DICT), and returns a copy of the sql
        # result that has been cleaned of those items that DO NOT contain the NAV facets chosen.
        #
        for key, idx in NAV_DICT.iteritems():
            plant_nav[key] = []
            nav_count[key] = {}
            sql_result_dict_list = self.remove_from_list(key, sql_result_dict_list, self.query, idx)

        #
        # The sql_result_dict_list now has only items chosen from left nav. We can now rebuild the left nav, and increment
        # the nav_count for each key[facet]
        #
        # Nav looks like this:
        #
        # Key
        #   facet(8)
        #   facet(2)
        # Key
        #   facet(n)
        #   ...

        for plant in sql_result_dict_list:
            for key, idx in NAV_DICT.iteritems():
                if plant[idx]:
                    nav_facets = [x.strip() for x in plant[idx].split(',')]
                    for facet in nav_facets:
                        nav_count[key][facet] = nav_count[key].get(facet,0)+1
                        if facet not in plant_nav[key]:
                            plant_nav[key].append(facet)


        # sort the nav facets
        for n in plant_nav.keys():
            plant_nav[n] = sorted(plant_nav[n])

        for key in NAV_DICT:
            # Build the actual HTML to display the list
            plant_nav[key] = self.make_nav_list(self.request, key, self.query, plant_nav[key], nav_count)

        plant_count = sql_result_dict_list.__len__()

        data = {}
        data['plant_count'] = plant_count
        data['plant_count_results'] = ': '+str(plant_count) +' '+ 'results' if plant_count > 1 else ': '+str(plant_count) +' '+ 'result'
        data['plant_nav'] = plant_nav

        data['category_slug'] = self.cat
        data['url_params'] = '?s=%s&d=%s' % (self.sort, self.sort_direction)
        data['query_params'] = URLObject(self.request.get_full_path()).query
        data['query_dict'] = self.query
        data['url'] = URLObject(self.request.get_full_path())
        data['link_address'] ='/plants/category/'+self.cat+'/'
        data['cat_count'] = nav_count

        if plant_count > 500:
            limit = 50
        else:
            limit = 25

        paginator = Paginator(sql_result_dict_list, limit)
        try:
            sql_result_dict_list = paginator.page(kwargs.get('page',1))
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            sql_result_dict_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range , go to first page
            sql_result_dict_list = paginator.page(1)

        data['plant_list'] = sql_result_dict_list

        return data


    def remove_from_list(self, nav_heading, dict_list, query, idx):
        """
        This actually returns a copy of the sql_result_dict_list, minus those items that
        don't match the navigation options chosen.
        Returns a list of dicts (plants).
        """
        ret = []
        if nav_heading in query:
            for plant in dict_list:
                if plant[idx]:
                    nav_list = [x.strip() for x in plant[idx].split(',')]
                    query_items = query[nav_heading].split(',')
                    q_set = set(query_items)
                    n_set = set(nav_list)
                    if q_set.issubset(n_set):
                        ret.append(plant)
        else:
            ret = dict_list

        return ret


    def make_nav_list(self, request, nav_heading, query, nav_heading_values, nav_count):
        """
        Builds the href and query string for the left navigation elements.
        Returns a list of html elements (checkboxes) for the left nav.
        nav_heading is the left nav category I'm checking against.
        nav_heading_values is the list of facets currently on display for the above category (nav_heading).
        E.g., if nav_heading is "category", then nav_heading_values[] might be [u'Annuals', u'Herbs', etc...]

        What I want to do here is:
        If the url query contains this definition ( e.g., category=), I want to do one of 2 things:
            1. If the selection and url query item are the same, then remove the query item. This is like a toggle.
            2. If the selection and url query are different, then add a comma to the query
                (we'll add the new query item later)
        """
        import urllib
        new_list = []

        if nav_heading in query:
            new_query = query.copy()
            old_query_item = new_query[nav_heading]+','
            del new_query[nav_heading]
        else:
            old_query_item = ''
            new_query = query.copy()

        for key, val in new_query.iteritems():
            new_list.append('%s=%s' % (key, val))
        new_query = '&'.join(new_list)

        if new_query:
            new_query = '?'+new_query+'&'
        else:
            new_query = '?'

        ret = []
        path = URLObject(request.get_full_path()).path

        # Now we have the old query built and patched up.
        # We are going to loop through the values for this nav_heading and create the html for each one.

        for el in nav_heading_values:
            if nav_heading in query:
                query_list = query[nav_heading].split(',')
                if el in query_list:
                    #
                    # Are you SURE Python doesn't need a switch?
                    #
                    query_list.remove(el)
                    new_q = (',').join(query_list)
                    if new_q:
                        ret.append('<label><input class="nav_checkbox checked" type="checkbox" checked '
                                   'onchange="window.location.href=\''+path+new_query+'%s=%s\'">%s (%d)</label>'
                                   % (nav_heading,new_q,el.title(), nav_count[nav_heading].get(el,0))
                        )
                    else:
                        ret.append('<label><input class="nav_checkbox checked" type="checkbox" checked '
                                   'onchange="window.location.href=\''+path+new_query[:-1]+'\'">%s (%d)</label>'
                                   % (el.title(),nav_count[nav_heading].get(el,0)))
                else:
                    ret.append('<label><input class="nav_checkbox" type="checkbox" '
                               'onchange="window.location.href=\''+path+new_query+'%s=%s\'">%s (%d)</label>'
                               % (nav_heading,old_query_item+el,el.title(), nav_count[nav_heading].get(el,0)))
            else:
                ret.append('<label><input class="nav_checkbox"  type="checkbox" '
                           'onchange="window.location.href=\'%s%s%s=%s\'">%s (%d)</label>'
                           % (path, str(new_query), nav_heading, el, el.title(), nav_count[nav_heading].get(el, 0)))

        return ret


    class Meta:
        abstract = True


    def render_to_response(self, context, **kwargs):
        return render_to_response('plants/plant_index.html', context)


class CustomCatView(CustomPlantListView):
    """
    This class produces a list of all plants in a given category, e.g., 'annuals'
    """

    def get_context_data(self, **kwargs):

        # full_query_dict = self.query
        if self.sort == 'common_name':
            self.sql = """ SELECT p.scientific_name, p.slug, CONCAT('<a href="/plants/all/',p.slug,'">',n.common_name,'</a>') as common_names,
            GROUP_CONCAT( DISTINCT CONCAT('<a href="/plants/category/',c2.slug,'">',c2.category,'</a>') SEPARATOR ', ') as categories,
            GROUP_CONCAT( DISTINCT c2.category SEPARATOR ', ') as search_categories,
            GROUP_CONCAT( DISTINCT clr.color SEPARATOR ', ') as flower_colors,
            GROUP_CONCAT( DISTINCT clr2.color SEPARATOR ', ') as leaf_colors,
            GROUP_CONCAT( DISTINCT l.light SEPARATOR ', ') as light,
            GROUP_CONCAT( DISTINCT s.season SEPARATOR ', ') as seasons,
            GROUP_CONCAT( DISTINCT a.attracts SEPARATOR ', ') as attracts,
            (SELECT img_url FROM plants_plantimage images WHERE images.plant_id = p.id LIMIT 1 ) AS img
            , p.height
            FROM plants_commonname n
            LEFT JOIN plants_plant p ON p.id = n.plant_id
            LEFT JOIN plants_plant_category pc ON pc.plant_id = p.id
            LEFT JOIN plants_category c ON c.id = pc.category_id
            LEFT JOIN plants_plant_category pc2 ON pc2.plant_id = p.id
            LEFT JOIN plants_category c2 ON pc2.category_id = c2.id
            LEFT JOIN plants_plant_search_flower_color fc ON fc.plant_id = p.id
            LEFT JOIN plants_color clr ON clr.id = fc.color_id
            LEFT JOIN plants_plant_search_leaf_color lc ON lc.plant_id = p.id
            LEFT JOIN plants_color clr2 ON clr2.id = lc.color_id
            LEFT JOIN plants_plant_search_light sl ON sl.plant_id = p.id
            LEFT JOIN plants_light l ON l.id = sl.light_id
            LEFT JOIN plants_plant_search_season ss ON ss.plant_id = p.id
            LEFT JOIN plants_season s ON s.id = ss.season_id
            LEFT JOIN plants_plant_attracts pa ON pa.plant_id = p.id
            LEFT JOIN plants_attracts a ON pa.attracts_id = a.id """

            if self.cat != 'all':
                self.sql += """WHERE c.slug = '%s' """ % (self.cat)

            self.sql += """GROUP BY n.common_name ORDER BY n.common_name """
        else:
            self.sql = """ SELECT p.scientific_name, p.slug, GROUP_CONCAT( DISTINCT n.common_name SEPARATOR ', ') as common_names,
            GROUP_CONCAT( DISTINCT CONCAT('<a href="/plants/category/',c2.slug,'">',c2.category,'</a>') SEPARATOR ', ') as categories,
            GROUP_CONCAT( DISTINCT c2.category SEPARATOR ', ') as search_categories,
            GROUP_CONCAT( DISTINCT clr.color SEPARATOR ', ') as flower_colors,
            GROUP_CONCAT( DISTINCT clr2.color SEPARATOR ', ') as leaf_colors,
            GROUP_CONCAT( DISTINCT l.light SEPARATOR ', ') as light,
            GROUP_CONCAT( DISTINCT s.season SEPARATOR ', ') as seasons,
            GROUP_CONCAT( DISTINCT a.attracts SEPARATOR ', ') as attracts,
            (SELECT img_url FROM plants_plantimage images WHERE images.plant_id = p.id LIMIT 1 ) AS img
            , p.height
            FROM plants_plant_category pc
            LEFT JOIN plants_category c ON c.id = pc.category_id
            LEFT JOIN plants_plant p ON p.id = pc.plant_id
            LEFT JOIN plants_plant_category pc2 ON pc2.plant_id = p.id
            LEFT JOIN plants_category c2 ON pc2.category_id = c2.id
            LEFT JOIN plants_commonname n ON p.id = n.plant_id
            LEFT JOIN plants_plant_search_flower_color fc ON fc.plant_id = p.id
            LEFT JOIN plants_color clr ON clr.id = fc.color_id
            LEFT JOIN plants_plant_search_leaf_color lc ON lc.plant_id = p.id
            LEFT JOIN plants_color clr2 ON clr2.id = lc.color_id
            LEFT JOIN plants_plant_search_light sl ON sl.plant_id = p.id
            LEFT JOIN plants_light l ON l.id = sl.light_id
            LEFT JOIN plants_plant_search_season ss ON ss.plant_id = p.id
            LEFT JOIN plants_season s ON s.id = ss.season_id
            LEFT JOIN plants_plant_attracts pa ON pa.plant_id = p.id
            LEFT JOIN plants_attracts a ON pa.attracts_id = a.id """

            if self.cat != 'all':
                self.sql += """WHERE c.slug = '%s' """ % (self.cat)

            self.sql += """GROUP BY p.id ORDER BY p.scientific_name """

        self.params = ()

        data = super(CustomCatView, self).get_context_data(**kwargs)
        if self.cat != 'all':
            data['category'] = Category.objects.get(slug=self.cat)
        else:
            data['category'] = 'All Plants'

        return data


class CustomSearchView(CustomPlantListView):
    """
    This class produces a list of plants filtered on url parameter q.
    """

    def dispatch(self, request, *args,**kwargs):
        self.cat = 'all'
        self.search_query = request.GET['q'].split(',')

        return super(CustomSearchView, self).dispatch(request, *args, **kwargs)

    def get_query_cache(self, sql, params):
        # Cache the results of the raw query
        key = sha1(sql + (',').join(params)).hexdigest()
        if cache.get(key):
            rows = cache.get(key)
        else:
            rows = sqltodict(self.sql,self.params)

            for s in rows:
                m = re.search('[0-9]+ (in.|ft.)', s.get('height', None))
                if m:
                    v = m.group(0).split(' ')
                    if v[1] == 'in.':
                        h = 12 / float(v[0])
                    else:
                        h = int(v[0])

                    if h <= 1:
                        height = '1 ft. or less'
                    elif h <= 3:
                        height = '1-3 ft.'
                    elif h <= 6:
                        height = '3-6 ft.'
                    elif h <= 9:
                        height = '6-9 ft.'
                    elif h <= 20:
                        height = '9-20 ft.'
                    elif h > 20:
                        height = 'greater than 20 ft.'

                    s.update({'search_height': height})
                else:
                    s.update({'search_height': None})

            cache.set(key, rows, 300)

        return rows


    def get_context_data(self, **kwargs):

        search_query = self.search_query
        sort_direction = self.sort_direction
        sort = self.sort

        sql=[]
        params=()
        for q in search_query:
            q = q.strip()
            if sort == 'common_name':
                self.sort_stmt = 'ORDER BY n.common_name '+sort_direction+';'
                sql.append(""" SELECT p.scientific_name
                , p.slug
                , CONCAT('<a href="/plants/all/',p.slug,'">',n.common_name,'</a>')  as common_names
                , GROUP_CONCAT( DISTINCT CONCAT('<a href="/plants/category/',c2.slug,'">',c2.category,'</a>') SEPARATOR ', ') as categories
                , GROUP_CONCAT( DISTINCT c2.category SEPARATOR ', ') as search_categories
                , GROUP_CONCAT( DISTINCT clr.color SEPARATOR ', ') as flower_colors
                , GROUP_CONCAT( DISTINCT clr2.color SEPARATOR ', ') as leaf_colors
                , GROUP_CONCAT( DISTINCT l.light SEPARATOR ', ') as light
                , GROUP_CONCAT( DISTINCT s.season SEPARATOR ', ') as seasons,
                GROUP_CONCAT( DISTINCT a.attracts SEPARATOR ', ') as attracts,
                (SELECT img_url FROM plants_plantimage images WHERE images.plant_id = p.id LIMIT 1 ) AS img
                , p.height
                FROM plants_commonname n
                LEFT JOIN plants_plant p ON p.id = n.plant_id
                LEFT JOIN plants_plant_category pc ON pc.plant_id = p.id
                LEFT JOIN plants_category c ON c.id = pc.category_id
                LEFT JOIN plants_plant_category pc2 ON pc2.plant_id = p.id
                LEFT JOIN plants_category c2 ON pc2.category_id = c2.id
                LEFT JOIN plants_plant_search_flower_color fc ON fc.plant_id = p.id
                LEFT JOIN plants_color clr ON clr.id = fc.color_id
                LEFT JOIN plants_plant_search_leaf_color lc ON lc.plant_id = p.id
                LEFT JOIN plants_color clr2 ON clr2.id = lc.color_id
                LEFT JOIN plants_plant_search_light sl ON sl.plant_id = p.id
                LEFT JOIN plants_light l ON l.id = sl.light_id
                LEFT JOIN plants_plant_search_season ss ON ss.plant_id = p.id
                LEFT JOIN plants_season s ON s.id = ss.season_id
                LEFT JOIN plants_plant_attracts pa ON pa.plant_id = p.id
                LEFT JOIN plants_attracts a ON pa.attracts_id = a.id
                LEFT OUTER JOIN plants_cultivar cv ON (p.`id` = cv.`plant_id`)
                LEFT OUTER JOIN taggit_taggeditem ti ON (p.`id` = ti.`object_id`)
                LEFT OUTER JOIN taggit_tag t ON (ti.`tag_id` = t.`id`)
                LEFT OUTER JOIN `django_content_type` ON (ti.`content_type_id` = `django_content_type`.`id`)
                WHERE (p.`scientific_name` REGEXP %s = 1 OR p.`comment` REGEXP %s = 1 OR n.`common_name` REGEXP %s = 1
                OR cv.`cultivar` REGEXP %s = 1
                OR (t.`name` REGEXP %s = 1 AND `django_content_type`.`id` = 12 ) OR p.`color` REGEXP %s = 1
                OR p.`flower_color` REGEXP %s = 1
                OR p.`flower` REGEXP %s = 1
                OR p.`foliage` REGEXP %s = 1
                OR p.`season` REGEXP %s = 1
                OR c.`category` REGEXP %s = 1  )
                GROUP BY scientific_name, n.common_name """)
            else:
                self.sort_stmt = 'ORDER BY scientific_name '+sort_direction+';'
                sql.append(""" SELECT
                p.scientific_name
                , p.slug
                , GROUP_CONCAT( DISTINCT CONCAT('<a href="/plants/all/',p.slug,'">',n.common_name,'</a>') SEPARATOR ', ') as common_names
                , GROUP_CONCAT( DISTINCT CONCAT('<a href="/plants/category/',c2.slug,'">',c2.category,'</a>') SEPARATOR ', ') as categories
                , GROUP_CONCAT( DISTINCT c2.category SEPARATOR ', ') as search_categories
                , GROUP_CONCAT( DISTINCT clr.color SEPARATOR ', ') as flower_colors
                , GROUP_CONCAT( DISTINCT clr2.color SEPARATOR ', ') as leaf_colors
                , GROUP_CONCAT( DISTINCT l.light SEPARATOR ', ') as light
                , GROUP_CONCAT( DISTINCT s.season SEPARATOR ', ') as seasons,
                GROUP_CONCAT( DISTINCT a.attracts SEPARATOR ', ') as attracts,
                (SELECT img_url FROM plants_plantimage images WHERE images.plant_id = p.id LIMIT 1 ) AS img
                , p.height
                FROM plants_plant_category pc
                LEFT JOIN plants_category c ON c.id = pc.category_id
                LEFT JOIN plants_plant p ON p.id = pc.plant_id
                LEFT JOIN plants_plant_category pc2 ON pc2.plant_id = p.id
                LEFT JOIN plants_category c2 ON pc2.category_id = c2.id
                LEFT JOIN plants_commonname n ON p.id = n.plant_id
                LEFT JOIN plants_plant_search_flower_color fc ON fc.plant_id = p.id
                LEFT JOIN plants_color clr ON clr.id = fc.color_id
                LEFT JOIN plants_plant_search_leaf_color lc ON lc.plant_id = p.id
                LEFT JOIN plants_color clr2 ON clr2.id = lc.color_id
                LEFT JOIN plants_plant_search_light sl ON sl.plant_id = p.id
                LEFT JOIN plants_light l ON l.id = sl.light_id
                LEFT JOIN plants_plant_search_season ss ON ss.plant_id = p.id
                LEFT JOIN plants_season s ON s.id = ss.season_id
                LEFT JOIN plants_plant_attracts pa ON pa.plant_id = p.id
                LEFT JOIN plants_attracts a ON pa.attracts_id = a.id
                LEFT OUTER JOIN plants_cultivar cv ON (p.`id` = cv.`plant_id`)
                LEFT OUTER JOIN taggit_taggeditem ti ON (p.`id` = ti.`object_id`)
                LEFT OUTER JOIN taggit_tag t ON (ti.`tag_id` = t.`id`)
                LEFT OUTER JOIN `django_content_type` ON (ti.`content_type_id` = `django_content_type`.`id`)
                WHERE (p.`scientific_name` REGEXP %s = 1
                OR p.`comment` REGEXP %s = 1
                OR n.`common_name` REGEXP %s = 1
                OR cv.`cultivar` REGEXP %s = 1
                OR (t.`name` REGEXP %s = 1 AND `django_content_type`.`id` = 12 )
                OR p.`color` REGEXP %s = 1
                OR p.`flower_color` REGEXP %s = 1
                OR p.`flower` REGEXP %s = 1
                OR p.`foliage` REGEXP %s = 1
                OR p.`season` REGEXP %s = 1
                OR c.`category` REGEXP %s = 1  )
                GROUP BY scientific_name """)

            for x in range(0,11):
                params = params+('[[:<:]]' + q + '[[:>:]]',)

        self.params = params
        self.sql = (" UNION").join(sql)


        data = super(CustomSearchView, self).get_context_data(**kwargs)
        data['category'] = None
        data['category_slug'] = 'all'
        data['link_address'] = '/plants/search/'
        data['search'] = True
        data['search_query'] = (',').join(self.search_query)

        return data


def sqltodict(query,param):
    """
    http://djangosnippets.org/snippets/1383/
    """
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(query,param)
    fieldnames = [name[0] for name in cursor.description]
    result = []
    for row in cursor.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result


