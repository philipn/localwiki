from django import template
from tags.models import slugify
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def filtered_tags(region_slug, list, keywords):
    list = list or []
    keywords = keywords or []
    unused = set(list)
    filtered = []
    for word in keywords:
        for tag in unused:
            if word.lower() in tag.lower():
                filtered.append(tag)
                unused.remove(tag)
                break
    if not filtered:
        return ''
    tags = [{'name': t, 'slug': slugify(t), 'region': {'slug': region_slug}} for t in filtered]
    return render_to_string('tags/tag_list_snippet.html', {'tag_list': tags})
