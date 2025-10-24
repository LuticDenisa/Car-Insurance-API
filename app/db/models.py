from datetime import date, datetime, timezone
from decimal import Decimal
from sqlalchemy import DateTime, String, Integer, Date, Numeric, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str | None] = mapped_column(String(200))

    cars: Mapped[list["Car"]] = relationship(back_populates="owner", cascade="all, delete", passive_deletes=True)


class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vin: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    make: Mapped[str | None] = mapped_column(String(100))
    model: Mapped[str | None] = mapped_column(String(100))
    year_of_manufacture: Mapped[int | None] = mapped_column(Integer)

    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id", ondelete="RESTRICT"), nullable=False)

    owner: Mapped[Owner] = relationship(back_populates="cars")
    policies: Mapped[list["InsurancePolicy"]] = relationship(back_populates="car", cascade="all, delete", passive_deletes=True)
    claims: Mapped[list["Claim"]] = relationship(back_populates="car", cascade="all, delete", passive_deletes=True)


class InsurancePolicy(Base):
    __tablename__ = "insurance_policy"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"), nullable=False)

    provider: Mapped[str | None] = mapped_column(String(100))
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    logged_expiry_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    car: Mapped["Car"] = relationship(back_populates="policies")

    __table_args__ = (Index("ix_policy_car_start_end", "car_id", "start_date", "end_date"),)


class Claim(Base):
    __tablename__ = "claim"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"), nullable=False)

    claim_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    car: Mapped["Car"] = relationship(back_populates="claims")
    
    __table_args__ = (Index("ix_claim_car_date", "car_id", "claim_date"),)