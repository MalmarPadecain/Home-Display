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
    number = Column(String(16))

    @classmethod
    def create(cls, type: str, datestr: str, number: str) -> PhoneCall:
        return PhoneCall(type=Type.from_str(type), time=datetime.strptime(datestr, "%d.%m.%y %H:%M"), number=number)
