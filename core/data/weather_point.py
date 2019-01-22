from __future__ import annotations

from sqlalchemy import Column, String, DateTime, Float
from datetime import datetime

from core import db


class WeatherPoint(db.Base):
    __tablename__ = 'weather_points'

    zip = Column(String(10), primary_key=True)
    time = Column(DateTime, primary_key=True)
    temp = Column(Float)
    rain = Column(Float)
    description = (String(256))

    @classmethod
    def create(cls, zip: str, time: str, date: str, temp: float, rain: float, description: str) -> WeatherPoint:
        datetime_str = date + " " + time
        dtm = datetime.strptime(datetime_str, "%d.%m.%Y %H:%M")
        return WeatherPoint(zip=zip, time=dtm, temp=temp, rain=rain, description=description)
