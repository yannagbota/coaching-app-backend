"""Calcul des besoins nutritionnels de base à partir du profil (formule de Mifflin-St Jeor).

Ces calculs donnent une estimation, pas une prescription médicale : ils sont
présentés à l'utilisateur comme un point de départ ajustable.
"""

FACTEUR_ACTIVITE = {
    "sedentaire": 1.2,
    "modere": 1.45,
    "actif": 1.65,
    "tres_actif": 1.85,
}


def calculer_besoins(profil) -> dict:
    if profil.sexe == "homme":
        bmr = 10 * profil.poids_kg + 6.25 * profil.taille_cm - 5 * profil.age + 5
    else:
        bmr = 10 * profil.poids_kg + 6.25 * profil.taille_cm - 5 * profil.age - 161

    facteur = FACTEUR_ACTIVITE.get(profil.niveau_activite, 1.4)
    tdee = bmr * facteur

    objectifs_types = {o["type"] for o in profil.objectifs}
    if "perte_poids" in objectifs_types:
        kcal_cible = tdee * 0.85
    elif "force" in objectifs_types or "esthetique" in objectifs_types:
        kcal_cible = tdee * 1.05
    else:
        kcal_cible = tdee

    proteines_g = profil.poids_kg * 1.8
    lipides_g = profil.poids_kg * 0.9
    kcal_restantes = kcal_cible - (proteines_g * 4 + lipides_g * 9)
    glucides_g = max(kcal_restantes / 4, 0)

    return {
        "kcal_cible": round(kcal_cible),
        "proteines_g": round(proteines_g),
        "glucides_g": round(glucides_g),
        "lipides_g": round(lipides_g),
    }
