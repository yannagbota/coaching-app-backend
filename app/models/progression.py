"""Mesures corporelles et performances suivies dans le temps."""
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.database import Base


class MesureCorporelle(Base):
    __tablename__ = "mesures_corporelles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    poids_kg = Column(Float, nullable=True)
    mensurations = Column(JSON, nullable=True)  # {"tour_taille": .., "tour_bras": ..}

    user = relationship("User", backref="mesures")


class PerformanceLog(Base):
    __tablename__ = "performance_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    exercice = Column(JSON, nullable=False)  # {"nom":.., "charge":.., "reps":.., "duree":..}

    user = relationship("User", backref="performances")
