"""Programme d'entraînement généré pour un utilisateur, et son historique de séances."""
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Programme(Base):
    __tablename__ = "programmes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phase = Column(String, nullable=False)  # adaptation | developpement | intensification | deload
    semaine = Column(JSON, nullable=False)  # structure des séances de la semaine
    genere_le = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="programmes")


class SeanceLog(Base):
    __tablename__ = "seance_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    programme_id = Column(Integer, ForeignKey("programmes.id"), nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    exercices_realises = Column(JSON, nullable=False, default=list)
    ressenti = Column(String, nullable=True)  # facile | correct | difficile | douleur
    note = Column(String, nullable=True)

    user = relationship("User", backref="seance_logs")
