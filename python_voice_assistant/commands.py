import datetime
import os
import sys

import psutil  # for cpu usage
from newsapi import NewsApiClient  # pip install newsapi-python

from .engine import Engine


class CommandHandler:
    def __init__(self):
        self.engine = Engine()
        self.commands = {
            "time": self.time,
            "date": self.date,
            "greeting": self.greeting,
            "news": self.news,
            "clear": self.clear,
            "cpu": self.cpu,
            "battery": self.battery,
            "exit": self.exit,
            "where are the turtles": self.the_office,
        }

    def time(self):
        time = datetime.datetime.now().strftime(
            "%I:%M"
        )  # %I is hour %M minute %S is second
        self.engine.speak("The current time is " + time)

    def date(self):
        date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )  # %d is day %B is month in name %Y is year
        self.engine.speak("today is " + date)

    def cpu(self):
        usage = str(psutil.cpu_percent())
        self.engine.speak(usage)
        print(usage)

    def battery(self):
        battery = psutil.sensors_battery()
        self.engine.speak(f"Battery is at {str(battery.percent)}")

    def greeting(self, gender: str, name: str):
        if gender.lower() == "male":
            title = "Sir"
        elif gender.lower == "female":
            title = "Ma'am"
        else:
            title = ""

        hour = datetime.datetime.now().hour
        if hour >= 6 and hour < 12:
            now = "Morning"
        elif hour >= 12 and hour < 18:
            now = "Afternoon"
        elif hour >= 18 and hour < 24:
            now = "Evening"
        else:
            now = "Night"
        self.engine.speak(f"Good {now} {title} {name}! How can I help you today?")

    def news(self):
        api_key = os.getenv("NEWS_API_KEY")
        newsapi = NewsApiClient(api_key=api_key)

        self.engine.speak("Please specify a topic")
        topic = self.engine.mic_to_text()
        data = newsapi.get_top_headlines(q=topic, language="en", page_size=5)
        newsdata = data["articles"]
        if not newsdata:
            self.engine.speak("No news on this topic")
            return

        for x, y in enumerate(newsdata):
            print(f'{x} {y["description"]}')
            self.engine.speak(f'{x} {y["description"]}')
        self.engine.speak("You're now fully updated on the news")

    def the_office(self):
        # Say something typical that Michael Scott would say
        self.engine.speak("That's what she said")

    def clear(self):
        os.system("cls")

    def exit(self):
        self.engine.speak("Goodbye")
        sys.exit(1)
