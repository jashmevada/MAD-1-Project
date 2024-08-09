from db.db import db

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey, TypeDecorator, Date, Integer, String
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


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    role: Mapped[Role] = mapped_column(Enum("Influencer", "Sponsor", 'Admin', name="role"))


class Influencer(db.Model):
    user_id: Mapped[str] = mapped_column(ForeignKey("user.username"), primary_key=True)
    name: Mapped[str] = mapped_column()
    gender: Mapped[str] = mapped_column()
    niche: Mapped[str] = mapped_column()
    channel: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(ForeignKey("user.email"))
    image: Mapped[str] = mapped_column(String, nullable=True)
    ad_request: Mapped[List['AdRequest']] = relationship("AdRequest", backref="influencer", lazy=True)
    active_ad_request: Mapped[int] = mapped_column(default=0)
    follower: Mapped[int] = mapped_column(nullable=True)


class Sponsor(db.Model):
    user_id: Mapped[str] = mapped_column(ForeignKey("user.username"), primary_key=True)
    full_name: Mapped[str] = mapped_column()
    phone_number: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column()
    company_name: Mapped[str] = mapped_column()
    company_website: Mapped[str] = mapped_column()
    industry: Mapped[Industry] = mapped_column(Enum(Industry, name="industry"), nullable=False)  # SqliteEnum
    active_campaigns: Mapped[int] = mapped_column(default=0)

    campaigns: Mapped[List['Campaign']] = relationship('Campaign', backref='sponsor', lazy=True)
    ad_request: Mapped[List['AdRequest']] = relationship(lazy=True)


class Campaign(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    start_date: Mapped[datetime] = mapped_column(Date(), name="start_date")
    end_date: Mapped[datetime] = mapped_column(Date(), name="end_date")
    description: Mapped[str] = mapped_column(String)
    budget: Mapped[str] = mapped_column()
    visibility: Mapped[str] = mapped_column(Enum("private", "public"), name="visibility", default="public",
                                            nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    sponsor_id = db.Column(db.ForeignKey('sponsor.user_id'), nullable=False)

    ad_request: Mapped[List['AdRequest']] = relationship("AdRequest", backref="campaign", lazy=True)

    @hybrid_property
    def get_date(self):
        return datetime.strftime(self.start_date, "%Y-%m-%d")


class AdRequest(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey(Campaign.id ))
    influencer_id = db.Column(db.ForeignKey('influencer.user_id'), nullable=False)
    sponsor_id: Mapped[str] = mapped_column(ForeignKey(Sponsor.user_id, name="sponsor_id"),
                                            nullable=True)  # :TODO set here null to False
    message: Mapped[str] = mapped_column()
    requirement: Mapped[bool] = mapped_column(default=False)
    payment_amount: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    payment_done: Mapped[bool] = mapped_column(default=False)
    From: Mapped[str] = mapped_column(Enum("Influencer", "Sponsor", name="from"), nullable=True)
