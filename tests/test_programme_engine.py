"""Tests de base du moteur de génération de programme."""
from types import SimpleNamespace

from app.services.programme_engine import generer_semaine


def _profil_test(**overrides):
    base = dict(
        environnements=["maison"],
        materiel_disponible=[],
        objectifs=[{"type": "force", "poids": 1.0}],
        niveau_global="debutant",
        douleurs_actuelles=[],
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def test_genere_au_moins_une_seance():
    semaine = generer_semaine(_profil_test())
    assert len(semaine) >= 3


def test_exclut_le_materiel_indisponible():
    profil = _profil_test(environnements=["salle"], materiel_disponible=[])
    semaine = generer_semaine(profil)
    ids_utilises = {ex["exercice_id"] for seance in semaine for ex in seance["exercices"]}
    assert "developpe_couche" not in ids_utilises


def test_evite_le_groupe_touche_par_une_douleur():
    profil = _profil_test(environnements=["maison", "salle", "street"], douleurs_actuelles=["genou"])
    semaine = generer_semaine(profil)
    for seance in semaine:
        for ex in seance["exercices"]:
            assert ex["exercice_id"] not in {"squat_air", "fentes", "hip_thrust"}
