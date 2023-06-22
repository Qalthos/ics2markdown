from pathlib import Path
import re
import sys

import html2markdown
import icalendar


def parse_event(event: icalendar.Event) -> str:
    summary = event.get("summary")
    start = event.get("dtstart").dt.timestamp()
    end = event.get("dtend").dt.timestamp()

    details = event.get("description")
    if details:
        details = html2markdown.convert(details)
        details = re.sub("</?span>", "", details)
        details = re.sub("&nbsp;", "", details)
    else:
        details = ""

    post = f"""{summary}
<t:{int(start)}:t>–<t:{int(end)}:t>
{html2markdown.convert(details)}"""
    return post


def main():
    cal_file = Path("calendar.ics")
    if not cal_file.exists():
        print("Could not find calendar.ics")
        sys.exit(1)

    with open(cal_file) as open_cal:
        cal = icalendar.Calendar.from_ical(open_cal.read())

    for element in sorted(cal.walk(name="VEVENT"), key=lambda e: e.get("dtstart").dt):
        parsed = parse_event(element)

        print(parsed)
        print("\n###########################\n")


if __name__ == "__main__":
    main()
