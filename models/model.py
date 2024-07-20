from db.db import db

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey, TypeDecorator, Date
from sqlalchemy.ext.hybrid import hybrid_property

import enum
from datetime import datetime
from typing import List


class Role(enum.Enum):
    INFLUENCER = 'influencer'
    SPONSOR = 'sponsor'
    ADMIN = 'admin'


class Industry(enum.Enum):
    TECH = 1
    FASHION = 2
    EDUCATIONAL = 3
    TRANSPORTATION = 4
    HEALTHCARE = 5
    GAMING = 6
    OTHER = 4


class SqliteEnum(TypeDecorator):
    impl = db.String

    def __init__(self, enumtype, *args, **kwargs):
        self.enumtype = enumtype
        super(SqliteEnum, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        return value.value if value else None

    def process_result_value(self, value, dialect):
        return self.enumtype(value) if value else None


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    role: Mapped[Role] = mapped_column(Enum("Influencer", "Sponsor", name="role"))


class Influence(db.Model):
    # id: Mapped[int] = mapped_column(primary_key=True)
    # user_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.username"), primary_key=True)
    name: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    niche: Mapped[str] = mapped_column()
    channel: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()


# class Admin(db.Model):
#     pass


class Sponsor(db.Model):
    user_id: Mapped[str] = mapped_column(ForeignKey("user.username"), primary_key=True)
    full_name: Mapped[str] = mapped_column()
    phone_number: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column()
    company_name: Mapped[str] = mapped_column()
    company_website: Mapped[str] = mapped_column()
    industry: Mapped[Industry] = mapped_column(Enum(Industry, name="industry"), nullable=False) # SqliteEnum
    active_campaigns: Mapped[int] = mapped_column(default=0)
    campaigns: Mapped[List['Campaign']] = relationship('Campaign', backref='sponsor', lazy=True)


class Campaign(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    start_date: Mapped[datetime] = mapped_column(Date(), name="start_date")
    end_date: Mapped[datetime] = mapped_column(Date(), name="end_date")
    description: Mapped[str] = mapped_column()
    budget: Mapped[str] = mapped_column()
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.user_id'), nullable=False)

    @hybrid_property
    def get_date(self):
        return datetime.strftime(self.start_date, "%Y-%m-%d")
