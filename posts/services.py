from .models import LikeAnalytics
import datetime


def format_date(date_str: str) -> datetime.date:
    """The function for formatting date for API filter"""
    date = tuple(map(int, date_str.split('-')))
    date = datetime.date(*date)
    return date


def date_generator(date_from, date_to):
    """The function for generate date range"""
    while date_to >= date_from:
        yield date_from
        date_from = date_from + datetime.timedelta(days=1)


def is_liked(post, user):
    if LikeAnalytics.objects.filter(user=user, post=post).first():
        return True
    return False
