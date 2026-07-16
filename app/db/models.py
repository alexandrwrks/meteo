from datetime import datetime

from sqlalchemy import func, ForeignKey, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class Cities(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    latitude: Mapped[float] = mapped_column(nullable=False, index=True)
    longitude: Mapped[float] = mapped_column(nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    forecasts = relationship(
        "WeatherHourlyForecast",
        back_populates="city",
        cascade="all, delete, delete-orphan",
    )

class WeatherHourlyForecast(Base):
    __tablename__ = 'weather_forecast'
    id: Mapped[int] = mapped_column(primary_key=True)

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
    )

    forecast_time: Mapped[datetime] = mapped_column(index=True)

    temperature: Mapped[float]

    humidity: Mapped[float]

    wind_speed: Mapped[float]

    precipitation: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(default=func.now())

    city = relationship(
        "Cities",
        back_populates="forecasts",
    )