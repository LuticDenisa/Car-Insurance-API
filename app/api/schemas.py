from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date as DateType
from decimal import Decimal


class OwnerOut(BaseModel):
    id: int
    name: str
    email: str | None = None


class CarOut(BaseModel):
    id: int
    vin: str
    make: str | None = None
    model: str | None = None
    yearOfManufacture: int | None = Field(None, alias="year_of_manufacture")
    owner: OwnerOut

    class Config:
        populate_by_name = True


class PolicyIn(BaseModel):
    provider: str | None = None
    startDate: DateType = Field(alias="start_date")
    endDate: DateType = Field(alias="end_date")

    class Config:
        populate_by_name = True

    @field_validator("startDate", "endDate")
    @classmethod
    def check_dates(cls, v: DateType) -> DateType:
        if not (1900 <= v.year <= 2100):
            raise ValueError("Year must be between 1900 and 2100")
        return v


class ValidityQuery(BaseModel):
    date: DateType

    @field_validator("date")
    @classmethod
    def check_date(cls, value: DateType) -> DateType:
        if not (1900 <= value.year <= 2100):
            raise ValueError("date out of allowed range [1900..2100]")
        return value
    

class ClaimIn(BaseModel):
    claimDate: DateType = Field(alias="claim_date")
    description: str
    amount: Decimal

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("claimDate")
    @classmethod
    def check_claim_date(cls, value: DateType) -> DateType:
        if not (1900 <= value.year <= 2100):
            raise ValueError("claim_date out of allowed range [1900..2100]")
        return value
    
    @field_validator("description")
    @classmethod
    def check_description(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("description cannot be empty")
        return value.strip()
    
    @field_validator("amount")
    @classmethod
    def check_amount(cls, value: Decimal) -> Decimal:
        if value is None or value <= 0:
            raise ValueError("amount must be a positive number")
        return value