from django.contrib.auth.models import User, Group,Permission
from rest_framework import serializers
from quickstart.models import Typesteps,Mission,Envoye,Regime,Config_blocage,Config_rapport,Rapport,Bloque,Bank,Cheque,Justifs,Paiement,Actions,Service, Employe,Montant_zone,Bareme,Bareme_detail,Processus,Stepprocess,Pole,Entite,TypeProjet,Projet, Country, Worldcities, Categorie, Bareme_envoye,Notifications,Zone, Bareme_envoye
from django.db import models
import ast
from django.conf import settings
from datetime import date, datetime, timedelta
from rest_framework.response import Response
from django.db.models import Sum







class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['pk','url', 'name']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    
class EnvoyeSerializer(serializers.ModelSerializer):
    hebergement = serializers.SerializerMethodField()
    perdiem = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    url_photo = serializers.SerializerMethodField()
    Paye =serializers.SerializerMethodField()
    Receptionner= serializers.SerializerMethodField()
    userid= serializers.SerializerMethodField()
    justif = serializers.SerializerMethodField()
    Montant = serializers.SerializerMethodField()
    rapport = serializers.SerializerMethodField()
    rapport_state = serializers.SerializerMethodField()
    rapport_config = serializers.SerializerMethodField()
   
    
    def get_justif(self, obj):
        justif = Justifs.objects.filter(id_envoye_id_id  = obj.id_envoye).exists()
        if justif:
            justif = list(Justifs.objects.filter(id_envoye_id_id  = obj.id_envoye).values())
            
            return  justif
        return None
    
    def get_userid(self, obj):
        
        return obj.id_employe.id_user_id
    def get_Paye(self, obj):
        pay=False
        paiement = Paiement.objects.filter(id_envoye_id  = obj.id_envoye).exists()
        if paiement:
           pay=True
        return pay

    def get_Receptionner(self, obj):
        Receptionner=False
        paiement = Paiement.objects.filter(id_envoye_id  = obj.id_envoye).exists()
        if paiement :
            paie=Paiement.objects.filter(id_envoye_id  = obj.id_envoye).values('date_reception')
            if paie[0]['date_reception']!=None:
                Receptionner=True
        return Receptionner


    def get_url_photo(self, obj):
        photo = Employe.objects.filter(nom_employe  = obj.nom_employe).values('photo')
        image= photo[0]['photo']
        if photo:
            image= '/static/'+image
        else:
            image= '/static/photo/user.png'
        return image
    
    def get_hebergement(self, obj):
        bareme_envoye = Bareme_envoye.objects.filter(id_envoye_id_id  = obj.id_envoye).values('hebergement')
        print("kakakakak")
        print( len(bareme_envoye))
        hebergement=0
        if len(bareme_envoye)>0:
            hebergement= bareme_envoye[0]['hebergement']
        return hebergement

    def get_perdiem(self, obj):
        bareme_envoye = Bareme_envoye.objects.filter(id_envoye_id_id  = obj.id_envoye).values('perdiem')
        perdiem=0
        if(len(bareme_envoye)>0):
            perdiem= bareme_envoye[0]['perdiem']
        return perdiem
    
    def get_total(self, obj):
        bareme_envoye = Bareme_envoye.objects.filter(id_envoye_id_id  = obj.id_envoye).values('hebergement','perdiem')
        hebergement=0
        perdiem=0
        if(len(bareme_envoye)>0 and len(bareme_envoye)):
            hebergement= bareme_envoye[0]['hebergement']
            perdiem= bareme_envoye[0]['perdiem']
        return hebergement+perdiem

    def get_Montant(self,obj):
        montant=0
        miss = Mission.objects.filter(id_mission = obj.id_mission_id).values('frais_extra')
        bareme_envoye = Bareme_envoye.objects.filter(id_envoye_id_id  = obj.id_envoye).exists()
        hebergement=0
        perdiem=0
        sold_des_justif=0
        justif= Justifs.objects.filter(id_envoye_id_id = obj.id_envoye).exists()
        montant1={}
        if obj.role == 'chef de delegation':
           
          
           if(bareme_envoye):
                bareme_envoye1 = Bareme_envoye.objects.filter(id_envoye_id_id  = obj.id_envoye).values('hebergement','perdiem')
                hebergement= bareme_envoye1[0]['hebergement']
                perdiem= bareme_envoye1[0]['perdiem']
           montant=int(hebergement) +int(miss[0]['frais_extra'])
        else:
            if(bareme_envoye):
                bareme_envoye1 = Bareme_envoye.objects.filter(id_envoye_id_id  = obj.id_envoye).values('hebergement','perdiem')
                hebergement= bareme_envoye1[0]['hebergement']
                perdiem= bareme_envoye1[0]['perdiem']
            montant=hebergement
        if (justif):
            sum= Justifs.objects.filter(id_envoye_id_id  = obj.id_envoye).aggregate(Sum('Montant')) 
            print('kkk')
            print(sum)
            sold_des_justif = sum['Montant__sum']  
        montant1['montant_a_justifier']=montant
        montant1['rest_a_justifier']=montant-sold_des_justif
        montant1['sold_des_justif']=sold_des_justif
        return montant1

    def get_rapport(self, obj):
        rapp=False
        mission = obj.id_mission.type_processus.id_process
        print(obj.id_envoye)
        print(obj.id_mission)
        print(obj.id_mission.type_processus.id_process)

        rapport1=Config_rapport.objects.filter(id_process_id=mission).exists()
        print(obj.role)
        if rapport1:
            
            rapport= Config_rapport.objects.filter(id_process_id=mission).values()
            print(rapport[0]['acteur'])
            if rapport[0]['acteur']=="C" and obj.role=="chef de delegation":
                rapp= True
                
                
            elif rapport[0]['acteur']=="T":
                rapp= True
    
        print(rapp)
        return rapp
    def get_rapport_config(self, obj):
        mission = obj.id_mission.type_processus.id_process
        
        rapport= Config_rapport.objects.filter(id_process_id=mission).values()
        id=rapport[0]['id_config_rapport']
        return id

    
    def get_rapport_state(self, obj):
        sub= False
        valid = False
        rep={}
        rapport = Rapport.objects.filter(id_envoye1_id=obj.id_envoye).exists()
        if rapport:
            rapp= Rapport.objects.filter(id_envoye1=obj.id_envoye).values()
            sub= True
            if rapp[0]['validation']!= None and rapp[0]['id_validateur_id']!= None:
                valid= True
        rep['Submitted']= sub
        rep['Validated']= valid

        return rep

    def get_rapport_config(self, obj):
        rap=1
        mission=Mission.objects.filter(id_mission=obj.id_mission.id_mission).values()
        print(mission)
        processus= int(mission[0]['type_processus_id'])
        config_rapport= Config_rapport.objects.filter( id_process_id=processus).exists()
        c_rapport= Config_rapport.objects.filter( id_process_id=processus).values()
        if config_rapport:
           rap= c_rapport[0]['id_config_rapport']
 
        return rap

    
    
    class Meta:
        model = Envoye
        fields = ['id_envoye', 'id_mission','userid', 'id_employe','nom_employe','prenom_employe','role','billet_avion','statut_des_justifs','hebergement','perdiem','total','Montant','Paye','Receptionner','justifier','validation_justier','url_photo','justif','rapport','rapport_state','rapport_config']

        extra_kwargs = {'id_mission_id': {'read_only': False}}


class StepprocessSerializer(serializers.ModelSerializer):
    pagination_class = None
    class Meta:
        model = Stepprocess
        fields = ['id_stepprocess','cible','type_steps','order_steps','id_process']


class Montant_zoneSerializer(serializers.ModelSerializer):
    pagination_class = None
    class Meta:
        model = Montant_zone
        fields = ['id_montant_zone','perdiem','hebergement','id_bareme_detail','id_zone']
        

class ProcessusSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Processus
        fields = ['id_process','type_process','id_relatated','nom_processus']

class RegimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Regime
        fields = ['id_regime', 'nom_regime']



class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = '__all__'


class TypestepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typesteps
        fields = ['id_typesteps','nom_typesteps']


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id_categorie','nom_categorie']

class ServiceSerializer(serializers.ModelSerializer):
     class Meta:
         model = Service
         fields = ['id_service','nom_service']

class EmployeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    url_photo = serializers.SerializerMethodField()
    def get_url_photo(self, obj):
        image=''
        if obj.photo:
            image= '/static'+obj.photo.url
        else:
            image= '/static/photo/user.png'
        return image

    def get_full_name(self, obj):
        return '{} {}'.format(obj.nom_employe, obj.prenoms_employe)
    class Meta:
        model = Employe
        fields = ['id_employe', 'full_name','nom_employe','prenoms_employe','date_naiss_employe','email_employe','matricule_employe','tel_employe','fonction_employe','login_employe','password_employe','compte_actif','verrou_employe','id_createur','id_user','date_creation','id_categorie','id_entite','id_service','photo','url_photo']

class User1Serializer(serializers.ModelSerializer):
    mission = MissionSerializer(many=True, read_only=True)
    employe = EmployeSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups','mission','employe','employe']

class PoleSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Pole
        fields = ['id_pole', 'nom_pole']

class EntiteSerializer(serializers.ModelSerializer):
    url_logo = serializers.SerializerMethodField()
    nom_pole=serializers.SerializerMethodField()
    def get_url_logo(self, obj):
        image=''
        if obj.logo:
            image= '/static'+obj.logo.url
        else:
            image= '/static/logo/logo_default.png'
        return image

    
    class Meta:
        model = Entite
        fields = ['id_entite', 'id_pole_id','nom_pole','nom_entite','logo','url_logo']
        extra_kwargs = {'logo': {'required': False}}

    def get_nom_pole(self, obj):
         print(getattr(obj.id_pole_id,'id_pole'))
         id=getattr(obj.id_pole_id,'id_pole')
         pole= Pole.objects.filter(id_pole=id).values('nom_pole')
         return pole[0]['nom_pole']

class TypeProjetSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = TypeProjet
        fields = ['id_typeprojet', 'nom_typeprojet']

class ProjetSerializer(serializers.ModelSerializer):
    # date_debut=serializers.SerializerMethodField()
    # date_fin=serializers.SerializerMethodField()

    # def get_date_debut(self, obj):
    #     print(obj)
    #     print(obj.date_debut)
    #     return datetime.strptime(obj.date_debut, '%Y-%m-%d').date()

    # def get_date_fin(self, obj):
    #     print(obj.date_fin)
    #     return datetime.strptime(obj.date_fin, '%Y-%m-%d').date()

    class Meta:
        model = Projet
        fields = ['id_projet', 'nom_projet','date_debut','date_fin','id_entite','type_projet']

class CountrySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Country
        fields = ['Code','Name']

class ZoneSerializer(serializers.ModelSerializer):
    pagination_class = None
    class Meta:
        model = Zone
        fields = ['id_zone','nom_zone']

class WorldcitiesSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Worldcities
        fields = ['id','city','iso3','country','zone_id']

class BankSerializer(serializers.ModelSerializer):

    url_logo = serializers.SerializerMethodField()
    def get_url_logo(self, obj):
        image=''
        if obj.logo:
            image= '/static'+obj.logo.url
        else:
            image= '/static/logo/bank.png'
        return image
    class Meta:
        model = Bank
        fields = ['id_bank','sigle','nom_bank','logo', 'url_logo' ]

class ChequeSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Cheque
        fields = ['id_cheque','numero','id_bank_id']

class PaiementSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Paiement
        fields = ['id_paiement','id_tresorier','cheque','id_cheque_id','date_paiement','date_reception','montant','id_envoye_id']

class ActionsSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Actions
        fields = ['id_actions','libelle_action','id_mission_id','id_cheque_id','id_user_id']


class Bareme_envoyeSerializer(serializers.ModelSerializer):
    id_envoye_id_id = serializers.IntegerField(read_only=False) 
    id_bareme_detail_id_id = serializers.IntegerField(read_only=False) 
    id_bareme_id_id = serializers.IntegerField(read_only=False)
    id_mission_id_id = serializers.IntegerField(read_only=False)
    id_montant_zone_id_id = serializers.IntegerField(read_only=False)
    class Meta:
        model = Bareme_envoye
        fields = ['id_envoye_id_id','hebergement','perdiem','total_cout','id_bareme_detail_id_id','id_bareme_id_id','id_mission_id_id','id_montant_zone_id_id']
       
class BaremeSerializer(serializers.ModelSerializer):
    Bareme=serializers.SerializerMethodField()
    class Meta:
        model = Bareme
        fields = ['id_bareme','jour_max','jour_min','id_processus','id_regime','Bareme']

    def get_Bareme(self, obj):
        Barem= Bareme.objects.filter(id_bareme=obj.id_bareme).values('id_processus_id','id_regime_id')
        Process= Processus.objects.filter(id_process=int(Barem[0]['id_processus_id'])).values('nom_processus')
        Regim = Regime.objects.filter(id_regime =int(Barem[0]['id_regime_id'])).values('nom_regime')
        bar={}    
        if Barem:
            print('kakakakooooo')
            print(Barem[0]['id_regime_id'])
            nom_Process= str(Process[0]['nom_processus'])
            nom_Regim= str(Regim[0]['nom_regime'])
            bar['Processus'] =nom_Process
            bar['Regime']  =    nom_Regim  

            return bar
        return None

class Bareme_detailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bareme_detail
        fields = ['id_bareme_detail','id_bareme','id_categorie'] 



class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = ['id_notifications','A','cc','message','prochaine_action','sent','auteur']

class JustifsSerializer(serializers.ModelSerializer):
    url_piece = serializers.SerializerMethodField()
    def get_url_piece(self, obj):
        justif = Justifs.objects.filter(id_justif = obj.id_justif).values('piece')
        piece= justif[0]['piece']
        if piece:
            piece= '/static/'+piece
        
        return piece
    class Meta:
        model = Justifs
        fields = ['id_justif','id_envoye_id','id_comptable','piece','url_piece','Type_piece','Libelle','Montant','commentaire']

class BloqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bloque
        fields = ['id_bloque','id_envoye_id','step_process']


class Config_blocageSerializer(serializers.ModelSerializer):
    debut=serializers.SerializerMethodField()
    fin=serializers.SerializerMethodField()

    def get_debut(self, obj):
        data={}
        step= obj.step_debut.type_steps_id
        stepproce = Typesteps.objects.filter(id_typesteps=step).values('id_typesteps','nom_typesteps')
        grp= Group.objects.filter(pk=int(obj.step_debut.cible_id)).values('name')
        data[obj.step_debut.id_stepprocess]=str(stepproce[0]['nom_typesteps'])+" du( de l'/ de la/ des) "+str(grp[0]['name'])
      
        return data
    def get_fin(self, obj):
        data={}
        step= obj.step_fin.type_steps_id
        stepproce = Typesteps.objects.filter(id_typesteps=step).values('id_typesteps','nom_typesteps')
        grp= Group.objects.filter(pk=int(obj.step_fin.cible_id)).values('name')
        data[obj.step_debut.id_stepprocess]=str(stepproce[0]['nom_typesteps'])+" du( de l'/ de la/ des) "+str(grp[0]['name'])
        return data

    class Meta:
        model = Config_blocage
        fields = ['id_config_blocage','id_process_id','step_debut','step_fin','debut','fin']

class Config_rapportSerializer(serializers.ModelSerializer):
    class Meta:
        model= Config_rapport
        fields = ['id_config_rapport','expression','acteur','id_process_id','Validateur']

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rapport
        fields = ['fichier','id_rapport','resultats_attendu','recommendations','date_creation','id_createur','date_derniere_modification','validation','id_validateur','id_envoye1','rapport_config']





