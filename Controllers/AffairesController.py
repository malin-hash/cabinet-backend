from Models import Affaire

class AffaireController:
    @staticmethod
    def get_aff_all():
        affaires = Affaire.query.order_by(Affaire.title.asc()).all()
        data = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
            } for t in affaires
        ]
        return data 