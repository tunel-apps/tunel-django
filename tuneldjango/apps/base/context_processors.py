from django.conf import settings


def domain_processor(request):
    return {
        "domain": settings.DOMAIN_NAME,
        "TITLE": settings.TITLE,
        "AUTHOR": settings.AUTHOR,
        "KEYWORDS": settings.KEYWORDS,
    }


def social_processor(request):
    return {
        "TWITTER_USERNAME": settings.TWITTER_USERNAME,
        "FACEBOOK_USERNAME": settings.FACEBOOK_USERNAME,
        "INSTAGRAM_USERNAME": settings.INSTAGRAM_USERNAME,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
        "GITHUB_REPOSITORY": settings.GITHUB_REPOSITORY,
    }
