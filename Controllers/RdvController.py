from Models import Rdv
from Extensions import db 
from datetime import datetime, date, time, timedelta
import locale

class RdvController:
    @staticmethod
    def advAdd(data):
        if  data["nom"] and data["prenom"] and data["email"] and data["date"] and data["heureDebut"] and data["affaire_id"] and data["subject"]:
            try: 
                timeRdv = datetime.strptime(data['heureDebut'], "%H:%M")
            except ValueError:
                return {"message": "Ce format de l'heure pas pris en charge", "status": 400}
                
            try: 
                date = datetime.fromisoformat(data['date'])
            except ValueError:
                return {"message": "Ce format de date pas pris en charge", "status": 400}
             
            # Vérification si la date n'est pas passée
            today = datetime.utcnow().date()
            if date.date() < today:
                return {"message": "Cette date est déjà passée choisissez une date valide", "status": 400}
                
            # Verification si les heures sont valable qu'elle sont dans les heures autorisées
            # Pour les rendez-vous
            heure_min = time(8, 0)
            heure_max = time(17, 0)
            
            if not (heure_min <= timeRdv.time() < heure_max):
                return {"message": "Ces heures ne sont pas convenables pour un rendez-vous. (entre 8h et 17h Uniquement)", "status": 400}
            
            som = timeRdv + timedelta(hours=1, minutes=00)
            timer = som.time()
            rdvs = Rdv.query.filter_by(date=date).all()
            for rdv in rdvs:
                if rdv.heureDebut <= timeRdv.time() <= rdv.heureFin or rdv.heureDebut < timer <= rdv.heureFin: 
                    return {"message": "Cette heure est déjà prise", "status": 400}
                    
            new_rdv = Rdv(
               nom = data['nom'], 
               prenom = data['prenom'], 
               email = data['email'],
               date = date,
               heureDebut = timeRdv,
               heureFin = timer,
               subject = data['subject'],
               affaire_id = data['affaire_id'],
            )
            
            db.session.add(new_rdv)
            db.session.commit()
            return {'message':'Votre rendevez-vous est prit avec succès', 'statut':201}
        else:
            return {"message": "Veuillez renseigner tous les champs", "status": 400}
            
    @staticmethod
    def get_rdv_all():
        locale.setlocale(locale.LC_TIME, "fr_FR")
        try:
            rdvs = Rdv.query.order_by(Rdv.date.asc(), Rdv.heureDebut.asc()).filter_by(statut=False).all()
        except:
            return {"message": 'Aucun rendez-vous en cours ...', "status": 401}
        data = [
            {
                "id": t.id,
                "nom": t.nom,
                "prenom": t.prenom,
                "heureDebut": t.heureDebut.strftime("%H:%M").replace(':', 'H') if t.heureDebut else None,
                "heureFin": t.heureFin.strftime("%H:%M").replace(':', 'H') if t.heureFin else None,
                "date": t.date.strftime("%d %B %Y"),
                "statut": t.statut
            } for t in rdvs
        ]
        return data 
    @staticmethod
    def get_number_rdv():
        try:
            rdvs = Rdv.query.filter_by(statut=False).count()
        except:
            return {"message": 'Aucune donnnée trouvée', "status": 401}
        
        return {
            "rdvs": rdvs
        }
        
    @staticmethod
    def delete_rdv(id):
        try:
            rdv = Rdv.query.filter_by(id=id).first()
        except:
            return {"message": 'Aucun rendez-vous trouvé', "status": 401}
        
        db.session.delete(rdv)
        db.session.commit()
        return {"message": 'rendez-vous supprimé avec succès', "status": 201}
        
    @staticmethod
    def update_rdv(id):
        try:
            rdv = Rdv.query.filter_by(id=id).first()
        except:
            return {"message": 'Aucun rendez-vous trouvé', "status": 401}
        
        rdv.statut = True
        db.session.commit()
        return {"message": 'rendez-vous honoré avec succès', "status": 201}
       