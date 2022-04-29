from django.contrib import admin
from .models import Mission,Employe,Envoye,Entite,Pole,Config_rapport,Rapport_droit,Rapport,Config_blocage,Bloque,Fiches, Service,Actions,Justifs,Paiement,Cheque,Bank,Notifications, Processus, Stepprocess, Country, Worldcities, Regime, Zone, Montant_zone, Bareme_detail, Bareme, Categorie, Notifications,Bareme_envoye, Typesteps, Projet, TypeProjet, Bank, Paiement, Cheque, Actions

admin.site.site_header= 'SAMIA administration'
admin.site.register(Mission)
admin.site.register(Employe)
admin.site.register(Envoye)
admin.site.register(Entite)
admin.site.register(Pole)
admin.site.register(Processus)
admin.site.register(Stepprocess)
admin.site.register(Country)
admin.site.register(Worldcities)
admin.site.register(Regime)
admin.site.register(Zone)
admin.site.register(Montant_zone)
admin.site.register(Bareme_detail)
admin.site.register(Bareme)
admin.site.register(Categorie)
admin.site.register(Notifications)
admin.site.register(Bareme_envoye)
admin.site.register(Typesteps)
admin.site.register(Projet)
admin.site.register(TypeProjet)
admin.site.register(Service)
admin.site.register(Bank)
admin.site.register(Paiement)
admin.site.register(Cheque)
admin.site.register(Actions)
admin.site.register(Justifs)
admin.site.register(Config_rapport)
admin.site.register(Rapport_droit)
admin.site.register(Rapport)
admin.site.register(Config_blocage)
admin.site.register(Bloque)
admin.site.register(Fiches)



# Register your models here.
