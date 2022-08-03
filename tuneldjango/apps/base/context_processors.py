from django.conf import settings


def domain_processor(request):
    return {
        "domain": settings.DOMAIN_NAME,
        "TITLE": settings.TITLE,
        "AUTHOR": settings.AUTHOR,
        "KEYWORDS": settings.KEYWORDS,
    }

