import hashlib
import json
import logging
import os
from datetime import datetime

from dateutil import parser
from webapp.api import get


def truncate_chars(value, max_length):
    length = len(value)
    if length > max_length:
        truncated = value[:max_length]
        if not length == (max_length + 1) and value[max_length + 1] != " ":
            truncated = truncated[: truncated.rfind(" ")]
        return truncated + "&hellip;"
    return value


def format_date(date):
    date_formatted = parser.parse(date)
    return date_formatted.strftime("%-d %B %Y")


def replace_admin(url):
    return url.replace("admin.insights.ubuntu.com", "blog.ubuntu.com")


def versioned_static(filename):
    """
    Template function for generating URLs to static assets:
    Given the path for a static file, output a url path
    with a hex hash as a query string for versioning
    """

    filepath = os.path.join("static", filename)
    url = "/" + filepath

    if not os.path.isfile(filepath):
        # Could not find static file
        return url

    # Use MD5 as we care about speed a lot
    # and not security in this case
    file_hash = hashlib.md5()
    with open(filepath, "rb") as file_contents:
        for chunk in iter(lambda: file_contents.read(4096), b""):
            file_hash.update(chunk)

    return url + "?v=" + file_hash.hexdigest()[:7]


def get_year():
    return datetime.now().year


def get_json_feed_content(url, offset=0, limit=None):
    """
    Get the entries in a JSON feed
    """

    logger = logging.getLogger(__name__)
    end = limit + offset if limit is not None else None

    response = get(url)

    try:
        content = json.loads(response.text)
    except Exception as parse_error:
        logger.warning(
            "Failed to parse feed from {}: {}".format(url, str(parse_error))
        )
        return []

    return content[offset:end]
