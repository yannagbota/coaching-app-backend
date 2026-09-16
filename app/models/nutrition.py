"""Journal alimentaire et objectifs nutritionnels."""
from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class NutritionEntry(Base):
    __tablename__ = "nutrition_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(String, nullable=False, default="manuel")  # manuel | code_barre | photo_ia
    aliments = Column(JSON, nullable=False, default=list)  # [{"nom":..,"kcal":..,"proteines":..,...}]
    kcal_total = Column(Float, nullable=False, default=0)
    confiance_ia = Column(Float, nullable=True)  # taux de confiance si source = photo_ia

    user = relationship("User", backref="nutrition_entries")
