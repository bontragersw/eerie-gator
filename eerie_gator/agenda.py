import icalendar
from dateutil import rrule
from datetime import datetime
import pytz


def get_rrule(vevent):
    """Parse an icalendar.VEvent into a dateutil.rrule

    Returns None if the event is non-recurring.
    """
    recur = vevent.get("RRULE")
    if recur is None:
        return None
    dtstart = vevent["DTSTART"].dt
    wkst = [getattr(rrule, day) for day in recur.get("WKST", [])]
    return rrule.rrule(
        getattr(rrule, recur["FREQ"][0]),
        dtstart=dtstart,
        interval=recur.get("INTERVAL", 1),
        wkst=wkst[0] if wkst else None,
        count=recur.get("COUNT"),
        #byyear=recur.get("BYYEAR"),
        byyearday=recur.get("BYYEARDAY"),
        bymonth=recur.get("BYMONTH"),
        bymonthday=recur.get("BYMONTHDAY"),
        byweekno=recur.get("BYWEEKNO"),
        byweekday=[getattr(rrule, day) for day in recur.get("BYDAY", [])],
        byhour=recur.get("BYHOUR"),
        byminute=recur.get("BYMINUTE"),
        bysecond=recur.get("BYSECOND"),
        )


def next_event(vcalendar, summaries=None):
    """Find the current or next event occurrance on the calendar.

    Assumes non-overlapping events, as appropriate for a sprinkler system
    where only one zone should be turned on at a time.
    """
    if summaries is None:
        summaries = {
            vevent["SUMMARY"].lower()
            for vevent in vcalendar.walk("VEVENT")
            }
    agenda = []
    for vevent in vcalendar.walk("VEVENT"):
        if vevent["SUMMARY"].lower() not in summaries: continue
        vevent = next_occurrence(vevent)
        if vevent is not None:
            agenda.append((vevent["DTSTART"].dt, vevent))
    if not agenda:
        return None
    agenda.sort()
    return agenda[0][1]


def next_occurrence(vevent):
    """Find the current or next occurrance of an event.

    If the event is recurring, return the next occurrance of it.
    If the event is non-recurring, return the event.
    Returns None if the last occurrance of the event has already past.
    """
    recur = get_rrule(vevent)
    now = datetime.now(tz=pytz.UTC)
    dtstart = vevent["DTSTART"].dt
    if recur is None:
        if dtstart >= now:
            return vevent
    else:
        rstart = recur.after(now)
        copy_vevent = vevent.copy()
        del copy_vevent["RRULE"]
        copy_vevent["DTSTART"].dt = rstart
        dtend = vevent["DTEND"].dt
        dt = dtend - dtstart
        copy_vevent["DTEND"].dt = rstart + dt
        return copy_vevent
