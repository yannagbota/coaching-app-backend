"""Suivi de la progression sur les figures de street workout."""
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class FigureProgress(Base):
    __tablename__ = "figure_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    figure_id = Column(String, nullable=False)  # ex: "hand_stand", "drapeau"
    etape_actuelle = Column(String, nullable=False)
    meilleure_performance = Column(Float, nullable=True)  # secondes ou répétitions selon la figure
    mise_a_jour_le = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="figures_progress")
