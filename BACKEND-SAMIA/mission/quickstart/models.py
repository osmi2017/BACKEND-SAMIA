from multiprocessing.dummy import Process
from typing import Type
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

# Create your models here.
class Rights(models.Model):
            
    class Meta:
        
        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model. 
                
        default_permissions = () # disable "add", "change", "delete"
                                 # and "view" default permissions

        permissions = (
            ("billets", "peut actribuer un billet d'avion"),
            ("validation", "peut faire une validation"),
            ("numero", "peut attribuer le numero"),
            ("forfait", "peut changer le forfait"),
            ("paiement", "peut faire un paiement"),
            ("justification", "peut valider des justificatifs"),
            ("traite_mission", "peut traiter des missions"),
            ("valide_rapport", "peut valider les rapports"),
            
            
        )

class Pole(models.Model):
    id_pole = models.AutoField(primary_key=True)
    nom_pole = models.CharField(max_length=50)
   

class Entite(models.Model):
    id_entite = models.AutoField(primary_key=True)
    id_pole_id = models.ForeignKey(Pole, on_delete=models.CASCADE)
    nom_entite = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo')

class TypeProjet(models.Model):
    id_typeprojet= models.AutoField(primary_key=True)
    nom_typeprojet = models.CharField(max_length=50)


class Projet(models.Model):
    id_projet = models.AutoField(primary_key=True)
    nom_projet= models.CharField(max_length=50)
    date_debut =models.DateField()
    date_fin = models.DateField()
    id_entite= models.ForeignKey(Entite, on_delete=models.RESTRICT)
    type_projet = models.ForeignKey(TypeProjet, on_delete=models.RESTRICT)

class Processus(models.Model):
    typeprocess = (
        ('NO','Normal'),
        ('PO','Pôle'),       
        ('PR','Projet'),
        
    )
    id_process = models.AutoField(primary_key=True)
    type_process=models.CharField(max_length=5, choices=typeprocess)
    id_relatated=models.IntegerField()
    nom_processus = models.CharField(max_length=50)

class Typesteps(models.Model):
    id_typesteps=models.AutoField(primary_key=True)
    nom_typesteps = models.CharField(max_length=50)


class Stepprocess(models.Model):
    
    id_stepprocess=models.AutoField(primary_key=True)
    id_process=models.ForeignKey(Processus, on_delete=models.RESTRICT)
    cible=models.ForeignKey(Group, on_delete=models.RESTRICT)
    type_steps= models.ForeignKey(Typesteps, on_delete=models.RESTRICT)
    order_steps=models.IntegerField()

class Categorie(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    nom_categorie = models.CharField(max_length=50)

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    nom_service = models.CharField(max_length=50)
    date_creation = models.DateTimeField()



class Employe(models.Model):
    id_employe = models.AutoField(primary_key=True)
    nom_employe = models.CharField(max_length=50)
    prenoms_employe = models.CharField(max_length=50)
    date_naiss_employe = models.DateField()
    matricule_employe = models.CharField(max_length=50)
    email_employe = models.CharField(max_length=50)
    tel_employe = models.CharField(max_length=50)
    fonction_employe = models.CharField(max_length=100)
    login_employe = models.CharField(max_length=255)
    password_employe = models.CharField(max_length=50)
    compte_actif = models.BooleanField()
    verrou_employe = models.BooleanField()
    photo = models.ImageField(upload_to='photo', default='photo/user.png')
    id_entite = models.ForeignKey(Entite, on_delete=models.CASCADE)
    id_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
   
    id_createur = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='createur',on_delete=models.CASCADE)
    id_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user',on_delete=models.CASCADE)
    date_creation = models.DateTimeField()

    id_service = models.ForeignKey(Service, on_delete=models.CASCADE)

class Regime(models.Model):
    id_regime = models.AutoField(primary_key=True)
    nom_regime = models.CharField(max_length=50)

class Bareme(models.Model):
    id_bareme = models.AutoField(primary_key=True)
    id_processus = models.ForeignKey(Processus, on_delete=models.CASCADE)
    id_regime =  models.ForeignKey(Regime, on_delete=models.CASCADE)
    jour_max = models.IntegerField()
    jour_min = models.IntegerField()

class Bareme_detail(models.Model):
    id_bareme_detail = models.AutoField(primary_key=True)
    id_categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    id_bareme = models.ForeignKey(Bareme, on_delete=models.CASCADE)

class Zone(models.Model):
    id_zone = models.AutoField(primary_key=True)
    nom_zone = models.CharField(max_length=50)

class Montant_zone(models.Model):
    id_montant_zone =  models.AutoField(primary_key=True)
    id_bareme_detail = models.ForeignKey(Bareme_detail, on_delete=models.CASCADE)
    perdiem = models.IntegerField()
    hebergement = models.IntegerField()
    id_zone = models.ForeignKey(Zone, on_delete=models.CASCADE)


class Mission(models.Model):
   
    avion = (
        ('True','OUI'),
        ('False','NON'),
        
    )
    
    id_mission = models.AutoField(primary_key=True)
    date_demande = models.DateTimeField()   
    objet_mission = models.CharField(max_length=500)
    depart_mission = models.DateField()
    retour_mission = models.DateField()
    lieu_mission = models.CharField(max_length=500)
    statut_mission = models.CharField(max_length=100)
    numero_mission = models.CharField(max_length=20)
    destination_mission = models.CharField(max_length=50)
    contexte_mission = models.CharField(max_length=2000)
    objectifs_mission = models.CharField(max_length=2000)
    frais_extra = models.CharField(max_length=20)
    chg_extra = models.CharField(max_length=20)
    frais_changes = models.CharField(max_length=50)
    current_step = models.IntegerField()
    relance_cible = models.CharField(max_length=50)
    regime = models.ForeignKey(Regime, on_delete=models.CASCADE)
    type_processus =  models.ForeignKey(Processus, on_delete=models.CASCADE)
    avion=models.CharField(max_length=5, choices=avion)
    id_demandeur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    

class Envoye(models.Model):
    id_envoye = models.AutoField(primary_key=True)
    id_mission = models.ForeignKey(Mission,related_name='envoye', on_delete=models.CASCADE)
    id_employe = models.ForeignKey(Employe,related_name='employe', on_delete=models.CASCADE)
    nom_employe=models.CharField(max_length=20)
    prenom_employe=models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    billet_avion = models.CharField(max_length=20)
    statut_des_justifs = models.CharField(max_length=20)
    justifier = models.BooleanField(default=False)
    validation_justier = models.BooleanField(default=False)

class Bareme_envoye(models.Model):
    id_bareme_envoye = models.AutoField(primary_key=True)
    hebergement = models.IntegerField()
    perdiem = models.IntegerField()
    total_cout = models.IntegerField()
    id_envoye_id = models.ForeignKey(Envoye,related_name='envoye', on_delete=models.CASCADE)
    id_montant_zone_id = models.ForeignKey(Montant_zone, on_delete=models.CASCADE)
    id_bareme_detail_id = models.ForeignKey(Bareme_detail, on_delete=models.CASCADE)
    id_bareme_id = models.ForeignKey(Bareme, on_delete=models.CASCADE)
    id_mission_id = models.ForeignKey(Mission, on_delete=models.CASCADE)


class Country(models.Model):
    continents = (
        ('Africa','Africa'),
        ('Asia','Asia'),
        ('Europe','Europe'),
        ('North America','North America'),
        ('South America','South America'),
        ('Oceania','Oceania'),
        ('Antarctica','Antarctica'),
        
    )
    Code = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=52)
    Continent = models.CharField(max_length=52,choices=continents)
    Region = models.CharField(max_length=52)
    SurfaceArea = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    IndepYear = models.IntegerField()
    Population = models.IntegerField()
    LifeExpectancy = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    GNP = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    GNPOld = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    LocalName = models.CharField(max_length=52)
    GovernmentForm = models.CharField(max_length=52)
    HeadOfState = models.CharField(max_length=52)
    Capital = models.IntegerField()
    Code2 = models.CharField(max_length=2)

class Worldcities(models.Model):
    city = models.CharField(max_length=255)
    city_ascii = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    longi = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iso2 = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=255)
    admin_name = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)
    population = models.CharField(max_length=255)
    zipe = models.CharField(max_length=255)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

class Notifications(models.Model):
    id_notifications = models.AutoField(primary_key=True)
    A = models.CharField(max_length=255)
    cc = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    prochaine_action = models.CharField(max_length=50)
    sent = models.CharField(max_length=20)
    auteur = models.CharField(max_length=200)

class Bank(models.Model):
    id_bank = models.AutoField(primary_key=True)
    sigle = models.CharField(max_length=20)
    nom_bank = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logo')

class Cheque(models.Model):
    id_cheque = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=20)
    id_bank_id = models.ForeignKey(Bank,on_delete=models.CASCADE)

class Paiement(models.Model):
    id_paiement = models.AutoField(primary_key=True)
    id_tresorier =models.ForeignKey(settings.AUTH_USER_MODEL,related_name='id_tresorier',default=1,on_delete=models.CASCADE)
    cheque = models.BooleanField(default=False)
    id_cheque_id = models.ForeignKey(Cheque,  blank=True,null=True,on_delete=models.CASCADE)
    date_paiement = models.DateField(blank=True,null=True)
    date_reception = models.DateField(blank=True,null=True)
    montant = models.IntegerField()
    id_envoye_id= models.ForeignKey(Envoye,default=1,on_delete=models.CASCADE)
    


class Justifs(models.Model):
    id_justif = models.AutoField(primary_key=True)
    id_envoye_id= models.ForeignKey(Envoye,on_delete=models.CASCADE)
    id_comptable =models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True,related_name='id_comptable',default=1,on_delete=models.CASCADE)
    piece = models.FileField(upload_to='justifs',default='justifs/img.png')
    Type_piece = models.CharField(max_length=50)
    Libelle = models.CharField(max_length=250)
    Montant = models.IntegerField()
    commentaire = models.CharField(blank=True,null=True,max_length=250)


 
   
    

class Actions(models.Model):
    id_actions = models.AutoField(primary_key=True)
    libelle_action = models.CharField(max_length=255)
    id_mission_id = models.ForeignKey(Mission, on_delete=models.CASCADE)
    id_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user_id',on_delete=models.CASCADE)

class Config_rapport(models.Model):
    express = (
        ('ET','AND'),
        ('OU','OR'),       
        
        
    )
    act = (
        ('C','Chef de mission'),
        ('T','tout le monde'),       
        
        
    )
    id_config_rapport = models.AutoField(primary_key=True)
    id_process_id= models.ForeignKey(Processus,on_delete=models.RESTRICT)
    expression = models.CharField(max_length=10, choices= express)
    acteur = models.CharField(max_length=10, choices= act)
    Validateur=models.ForeignKey(Group,blank=True,null=True, on_delete=models.RESTRICT)


class Rapport_droit(models.Model):
    id_rapport_droit = models.AutoField(primary_key=True)
    id_config_rapport = models.ForeignKey(Config_rapport, on_delete=models.CASCADE)
    validation_rapport=models.ForeignKey(Group,related_name='validation_rapport', on_delete=models.RESTRICT)
    consultation_rapport=models.ForeignKey(Group,related_name='consultation_rapport', on_delete=models.RESTRICT)
    suppression_rapport=models.ForeignKey(Group,related_name='suppression_rapport', on_delete=models.RESTRICT)

class Rapport(models.Model):
    id_rapport= models.AutoField(primary_key=True)
    resultats_attendu = models.CharField(max_length=500)
    recommendations = models.CharField(max_length=500)
    date_creation =models.DateField()
    id_createur = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='id_createur',on_delete=models.CASCADE)
    date_derniere_modification =models.DateField()
    validation=models.DateField(blank=True,null=True)
    id_validateur = models.ForeignKey(settings.AUTH_USER_MODEL,blank=True,null=True,related_name='id_validateur',on_delete=models.CASCADE)
    id_envoye1 = models.ForeignKey(Envoye,default=1,related_name='env', on_delete=models.CASCADE)
    fichier =models.FileField(upload_to='rapport')
    rapport_config= models.ForeignKey(Config_rapport,default=1, on_delete=models.CASCADE)

class Config_blocage(models.Model):
    id_config_blocage= models.AutoField(primary_key=True)
    id_process_id = models.ForeignKey(Processus, on_delete=models.CASCADE)
    step_debut = models.ForeignKey(Stepprocess,related_name='step_debut', on_delete=models.CASCADE)
    step_fin = models.ForeignKey(Stepprocess,related_name='step_fin', on_delete=models.CASCADE)

class Bloque(models.Model):
    id_bloque= models.AutoField(primary_key=True)
    id_envoye_id = models.ForeignKey(Envoye,related_name='envoye1', on_delete=models.CASCADE)
    step_process = models.ForeignKey(Typesteps,related_name='process1', on_delete=models.CASCADE)

class Fiches(models.Model):
    id_fiches= models.AutoField(primary_key=True)
    id_process_id = models.ForeignKey(Processus, on_delete=models.CASCADE)
    fiche_de_mission = models.ForeignKey(Stepprocess,related_name='fiche_de_mission', on_delete=models.CASCADE)
    ordre_de_mission = models.ForeignKey(Stepprocess,related_name='ordre_de_mission', on_delete=models.CASCADE)


    





