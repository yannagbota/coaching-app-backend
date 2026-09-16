"""Point d'intégration pour la reconnaissance alimentaire par photo.

En V1, aucune clé de fournisseur d'IA n'est configurée par défaut : le
service retombe sur un mode "mock" explicite plutôt que d'échouer
silencieusement, et le frontend affiche alors une confirmation manuelle
avant d'enregistrer. Pour activer une reconnaissance réelle, renseigner
FOOD_RECOGNITION_PROVIDER et FOOD_RECOGNITION_API_KEY dans .env, puis
implémenter l'appel au fournisseur choisi dans _appeler_fournisseur_ia.
"""
from app.config import settings


def _appeler_fournisseur_ia(image_bytes: bytes) -> list[dict]:
    """Point d'extension : brancher ici un vrai service de vision (ex: modèle de
    classification alimentaire hébergé). Doit retourner une liste d'aliments
    avec estimation calorique et macros.
    """
    raise NotImplementedError("Aucun fournisseur de reconnaissance alimentaire n'est configuré.")


def reconnaitre_aliments(image_bytes: bytes) -> dict:
    if settings.food_recognition_provider == "mock" or not settings.food_recognition_api_key:
        return {
            "aliments": [],
            "confiance": 0.0,
            "necessite_saisie_manuelle": True,
            "message": "Reconnaissance automatique non configurée : merci de confirmer ou saisir le repas manuellement.",
        }

    aliments = _appeler_fournisseur_ia(image_bytes)
    return {"aliments": aliments, "confiance": 0.75, "necessite_saisie_manuelle": False, "message": None}
