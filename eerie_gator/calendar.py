import icalendar
import logging
from urllib2 import urlopen


class CalendarCacheError(Exception):
    pass


def get_calendar(config):
    logging.debug("Loading cached calendar from %s", config["cache"])
    vcalendar_txt = open(config["cache"]).read()
    return icalendar.Calendar.from_ical(vcalendar_txt)


def cache_calendar(config):
    calendar_url = config["url"]
    cache_filename = config["cache"]
    max_size = config["max size"]
    logging.debug("Downloading calendar from %s", calendar_url)
    response = urlopen(calendar_url)
    if response.getcode() != 200:
        message = "Unable to retrieve %s: %r" % (calendar_url, response)
        logging.error(message)
        raise CalendarCacheError(message)
    logging.debug("Downloading %d bytes of calendar", max_size)
    vcalendar = response.read(max_size)
    logging.debug("Downloaded %d bytes of calendar", len(vcalendar))
    if vcalendar.endswith(b"END:VCALENDAR\r\n"):
        logging.debug("Caching calendar in %s", cache_filename)
        with open(cache_filename, "wb") as cache:
            cache.write(vcalendar)
    else:
        message = "%s unexpected ending %r; probably exceeds %d bytes" % (
            calendar_url,
            vcalendar[-15:],
            max_size,
            )
        logging.error(message)
        raise CalendarCacheError(message)
