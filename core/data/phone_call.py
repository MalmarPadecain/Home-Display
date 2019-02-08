from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Sequence, Enum

import enum

from core import db


class Type(enum.Enum):
    OUTGOING = enum.auto()
    INCOMING = enum.auto()
    MISSED = enum.auto()
    REJECTED = enum.auto()

    def __str__(self):
        if self is Type.OUTGOING:
            return "outgoing"
        if self is Type.INCOMING:
            return "incoming"
        if self is Type.MISSED:
            return "missed"
        if self is Type.REJECTED:
            return "rejected"

    @classmethod
    def from_str(cls, string: str):
        if string == "call_out":
            return Type.OUTGOING
        elif string == "call_in":
            return Type.INCOMING
        elif string == "call_in_fail":
            return Type.MISSED
        elif string == "call_rejected":
            return Type.REJECTED
        else:
            raise ValueError


class PhoneCall(db.Base):
    __tablename__ = 'phone_calls'

    id = Column(Integer, Sequence('phone_call_id_seq'), primary_key=True)
    type = Column(Enum(Type))
    time = Column(DateTime)
    number = Column(String(64))

    def __str__(self):
        return f"{self.time}: {self.type} {self.number}"

    @classmethod
    def create(cls, type: str, datestr: str, number: str) -> PhoneCall:
        return PhoneCall(type=Type.from_str(type), time=datetime.strptime(datestr, "%d.%m.%y %H:%M"), number=number)


class CallStreamer:
    def __init__(self):
        self.session = db.Session()
        self.pos = 0
        self._last_call = None

    def get_next_n_calls(self, n):
        print(self.pos)
        if n < 0:
            self.pos += 2*n
            n = abs(n)
        if self.pos < 0:
            self.pos = 0
        calls = self.session.query(PhoneCall).order_by(PhoneCall.time.desc()).offset(self.pos).limit(n).all()
        if calls:
            self.pos += n
        return calls
