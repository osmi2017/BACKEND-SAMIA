from logging import raiseExceptions
from django.contrib.auth.models import User, Group
import io
from django.utils.datastructures import MultiValueDictKeyError

#from reportlab.pdfgen import canvas
from quickstart.models import Employe,Config_blocage,Rapport, Envoye,Regime,Bank,Justifs,Cheque,Mission,Employe,Config_rapport, Service,Stepprocess,Processus,Pole,Entite,TypeProjet,Projet,Country,Worldcities,Categorie, Bareme, Bareme_detail, Montant_zone,Notifications,Typesteps,Zone,Paiement,Bloque
from rest_framework import viewsets
from rest_framework import permissions
from quickstart.serializers import UserSerializer,TypestepsSerializer,RapportSerializer,Config_blocageSerializer,Config_rapportSerializer,BloqueSerializer,JustifsSerializer,ChequeSerializer,PaiementSerializer,BankSerializer,ServiceSerializer,Montant_zoneSerializer,EnvoyeSerializer,BaremeSerializer,Bareme_detailSerializer, GroupSerializer,MissiontSerializer,RegimeSerializer,ProcessusSerializer,StepprocessSerializer,User1Serializer,EmployeSerializer,PoleSerializer,TypeProjetSerializer,EntiteSerializer,ProjetSerializer,CountrySerializer,WorldcitiesSerializer, CategorieSerializer, Bareme_envoyeSerializer, NotificationSerializer,ZoneSerializer
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser,MultiPartParser, FormParser,FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.signals import request_finished
from mission.signals import send_mail_mission
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.renderers import JSONRenderer
from datetime import date, datetime, timedelta
from django.utils.formats import get_format
import json
import ast
import traceback
from django.db.models import Count
from django.shortcuts import render
from django.core.files import File
from django.core.serializers.json import DjangoJSONEncoder



from django.contrib.auth.models import Permission

def is_config_blocage(envo):
    envoye= Envoye.objects.filter(id_envoye=envo).values('id_mission','id_employe')
    mission=Mission.objects.filter(id_mission=int(envoye[0]['id_mission'])).values('type_processus','current_step')
    config_blocage=Config_blocage.objects.filter(id_process_id=int(mission[0]['type_processus'])).values('step_debut')
    if int(mission[0]['current_step'])>int(config_blocage[0]['step_debut']):
        obj = Employe.objects.get(id_employe=int(envoye[0]['id_employe']))
                
        obj.verrou_employe = True
        
        obj.save()
    bloque= Bloque.objects.filter(id_envoye_id=envo).exclude(step_process=10).exists()
    if not bloque:
       step_process= Stepprocess.objects.filter(order_steps=config_blocage[0]['step_fin']).values('')
       data={}
       data['id_envoye_id']=envo
       data['step_process']=step_process[0]['type_steps']
       serializer = BloqueSerializer(data=data)
        
       if serializer.is_valid():
            
            serializer.save()

def mission_to_envoye(mission):
    envoye= Envoye.objects.filter(id_mission=int(mission)).values()
    for env in envoye:
        is_config_blocage(env['id_envoye'])

def check_if_rapport_obligatoire(env):
    obl=False
    
    envoye= Envoye.objects.filter(id_envoye=int(env)).values()
    print(envoye)
    id_mission= envoye[0]['id_mission_id']
    mission = Mission.objects.filter(id_mission=int(id_mission)).values()
    id_process = mission[0]['type_processus_id']
    config_rapport = Config_rapport.objects.filter(id_process_id_id=int(id_process)).values()
    if config_rapport[0]['expression']=='ET':
       if config_rapport[0]['acteur']=='T': 
            obl=True
       elif config_rapport[0]['acteur']=='C' and envoye[0]['role']=='chef de delegation':
           obl=True
    
    return obl

def check_if_rapport_valide(env):
    valide=False
    rapport= Rapport.objects.filter(id_envoye1_id= int(env)).exists()
    if rapport:
        rapport= Rapport.objects.filter(id_envoye1_id= int(env)).values()
        print(env)
        print(rapport)
        if rapport[0]['validation']!= None:
            valide=True
            Bloque.objects.filter(id_envoye_id_id=int(env)).filter(step_process_id=10).delete()
    return valide

def check_if_envoye_bloque(env):
    bloque= True
    envoye= Envoye.objects.filter(id_envoye=int(env)).values()
    id_mission1= envoye[0]['id_mission_id']
    mission= Mission.objects.filter(id_mission=int(id_mission1)).values()
    currents_steps= mission[0]['current_step']
    process_id= mission[0]['type_processus_id']
    bloque_config= Config_blocage.objects.filter(id_process_id_id=int(process_id)).values()
    bloque_step= Stepprocess.objects.filter(id_stepprocess=bloque_config[0]['step_fin_id']).values()
    bloque_type_step= Typesteps.objects.filter(id_typesteps=bloque_step[0]['type_steps_id']).values()
    if currents_steps>bloque_step[0]['order_steps']:
        bloque=False
        
    elif bloque_type_step[0]['nom_typesteps']=='validation des justifications' or bloque_type_step[0]['nom_typesteps']=='justification':
        if envoye[0]['validation_justier']==True:
            bloque=False
    if bloque==False:
        Bloque.objects.filter(id_envoye_id_id=envoye[0]['id_envoye']).exclude(step_process_id=10).delete()
    step_process= Stepprocess.objects.filter(id_process_id=process_id).values().order_by('order_steps')
    final_step=len(step_process)
    print('ki0')
    print(currents_steps)
    print(env)
    #print(step_process.filter(order_steps=final_step).values())
    return bloque

def check_rapport_final(final):

   rapport= {}
   rapport_return=[]
   #rapport= final[0]
   for x in range(0,len(final)):
      print('femua')
      print(x)
      print(final[x]) 
      msg={}
      rapport= dict(rapport)
      msg=dict(msg) 
      rapport['id_envoye']=final[x]['id_envoye']
      envoye= Envoye.objects.filter(id_envoye=int(final[x]['id_envoye'])).values()
      mission= Mission.objects.filter(id_mission=envoye[0]['id_mission_id']).values()
      stepprocesss= Stepprocess.objects.filter(id_process_id =mission[0]['type_processus_id']).filter(order_steps=mission[0]['current_step']).values()
      type_process= Typesteps.objects.filter(id_typesteps = stepprocesss[0]['type_steps_id']).values()
      employe= Employe.objects.filter(id_employe=envoye[0]['id_employe_id']).values() 
      rapport['id_employe']=employe[0]['id_employe']
      rapport['nom_employe']=employe[0]['nom_employe']
      rapport['prenoms_employe']=employe[0]['prenoms_employe']
      msg['msg']= "L'employe numéro "+ str(employe[0]['id_employe'])+" nommé "+ str(employe[0]['nom_employe'])
      if final[x]['rapport_obligatoire']==True and final[x]['rapport_valide']==True:
          
          if final[x]['bloque']== False:
              msg['msg']=msg['msg']+ " est débloqué sur la mission "+str(mission[0]['numero_mission'])
              msg['statut']=True
              lst1=[]
              lst1.append(msg)
              rapport['msg']=lst1
          else:
              msg['msg']=msg['msg']+ " est bloqué sur la mission "+str(mission[0]['numero_mission'])+ " à l'étape "+type_process[0]['nom_typesteps']
              msg['statut']=False
              lst1=[]
              lst1.append(msg)
              rapport['msg']=lst1
      elif final[x]['rapport_obligatoire']==True and final[x]['rapport_valide']==False:
          msg['msg']=msg['msg']+ " est bloqué sur la mission pou rapport non validé "+str(mission[0]['numero_mission'])
          msg['statut']=False
          rapport['msg']=msg
          if final[x]['bloque']== True:
             msg['msg']=msg['msg']+ " est bloqué sur la mission "+str(mission[0]['numero_mission'])+ " à l'étape "+type_process[0]['nom_typesteps']
             msg['statut']=False
             lst1=[]
             lst1.append(msg)
             rapport['msg']=lst1
      else:
           if final[x]['bloque']== False:
              msg['msg']=msg['msg']+ " est débloqué sur la mission "+str(mission[0]['numero_mission'])
              msg['statut']=True
              lst1=[]
              lst1.append(msg)
              rapport['msg']=lst1 
           else:
              msg['msg']=msg['msg']+ " est bloqué sur la mission "+str(mission[0]['numero_mission'])+ " à l'étape "+type_process[0]['nom_typesteps']
              msg['statut']=False
              lst1=[]
              lst1.append(msg)
              rapport['msg']=lst1 

      rapport_return.append(rapport)
      print('femua')
      print(x)
      print(rapport_return) 

   return rapport_return

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
       # try:
            serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
        
            token, created = Token.objects.get_or_create(user=user)
        
            return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'username':user.username,
                    'name':user.first_name,
                    'lastname':user.last_name

            })
        #except:
            #return JsonResponse({'error':'Login ou mot de passe incorrecte'})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]




class MesMissionList(APIView):
    
    """
    Liste de mes missions, or create a new mission.
    """
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id=id,format=None):
        employe=Employe.objects.filter(id_user=id).values('id_employe')
        
        envoye=Envoye.objects.filter(id_employe__in= employe).values('id_envoye')
        ##print(envoye)
        mission = Mission.objects.filter(envoye__id_envoye__in=envoye).distinct()
        serializer = MissiontSerializer(mission,context={'request': request}, many=True)
        return Response(serializer.data)
        # if data:
        #     for mission in serializer.data:
        #         name = mission.pop("id_mission")
        #         modified_response[name] = mission
        # return Response(modified_response)

    def post(self, request, format=None):
        print('kokokokoko')
        print(request.data)
        a_email_list=[]
        cc_email_list=[]
        user_list=[]
        nom_destination=[]
        data1={}
        
        counter_mission=  Mission.objects.all().count()
        try:
            data1['date_demande'] = datetime.now()
            data1['objet_mission'] = request.data['objet']
            date_depart = request.data['date_depart']
            data1['depart_mission'] = datetime.strptime(date_depart, '%Y-%m-%d').date()
            retour_mission = request.data['date_retour']
            data1['retour_mission'] = datetime.strptime(retour_mission, '%Y-%m-%d').date()
            data1['lieu_mission'] = str(request.data['destinations'])
            data1['statut_mission'] = 'initie'
            data1['numero_mission'] = str(counter_mission)+'/DRH/SJA/AO/'+str(datetime.now().year)
            data1['destination_mission'] = str(request.data['destinations'])
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        for destination in ast.literal_eval(data1['destination_mission']):
            
            try:
                ville = Worldcities.objects.filter(id=destination).values('city')
                nom_destination.append(ville[0]['city'])
            except Exception as e:
                print(e)
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        try:
            data1['contexte_mission'] = request.data['contexte']
            data1['objectifs_mission'] = request.data['objectif']
            if request.data['divers']:
                data1['frais_extra'] = request.data['divers']
            else:
                data1['frais_extra'] = 0 #a ajouter
            data1['chg_extra'] ="0"
            data1['frais_changes'] = "0"
            zone_id = request.data['id_zone']
            data1['type_processus'] = request.data['processus'] #a ajouter
            
            data1['current_step'] =1
            if zone_id ==0:
               return Response("Acune zone ne correspond qu ville choisie", status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        try:
            cible_group= Stepprocess.objects.filter(id_process=int(request.data['processus']),order_steps=2).values('cible_id')

            
            data1['relance_cible'] = str(Group.objects.get(id=cible_group[0]['cible_id']))
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        try:
            users_in_group1 = Group.objects.get(id=int(cible_group[0]['cible_id'])).user_set.all()
            for user in users_in_group1:
                        
                        print(user.email)
                        cc_email_list.append('"'+user.email+'"')
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
       
        
        data1['regime']= request.data['regimebareme'] #a ajouter
        data1['avion'] = request.data['billet'] 
        data1['id_demandeur']= request.data['user'] #a ajouter

        try:
            dt = date(data1['retour_mission'].year,data1['retour_mission'].month,data1['retour_mission'].day) - date(data1['depart_mission'].year,data1['depart_mission'].month,data1['depart_mission'].day) 
        
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MissiontSerializer(data=data1)
        
        if serializer.is_valid():
            strerror=''
            serializer.save()
            print('okci')
            print(serializer.data)
            id_mision = Mission.objects.latest('id_mission')
            #print('kkkkkkkkkkkkkkkkkkk')
            #print(id_mision.id_mission)
            str_membre = ast.literal_eval(str(request.data['membres']))
            #print(str_membre)
            #str_membre=[1, 2, 3, 4]
            #print(type(str_membre))
            ##lst_membre = json.loads(str_membre)
            ##print(lst_membre)
            #print(len(lst_membre))
        
            for membre in str_membre:
             
                try:
                    emp = Employe.objects.filter(id_employe=int(membre)).values('id_employe','nom_employe','prenoms_employe','id_user_id')
                    print(emp[0]['nom_employe'])
                    if int(emp[0]['id_user_id']) not in user_list:
                        user_list.append(int(emp[0]['id_user_id']))
                    role = 'membre de délégation'
                    if int(request.data['chef_delegation'])== int(membre) :

                            role = 'chef de delegation'
                    data2={}
                    print(id_mision)
                    data2['id_mission']= id_mision.id_mission
                    print('kjkjkjkj')
                    print(data2['id_mission'])
                    data2['id_employe']=emp[0]['id_employe']
                    data2['nom_employe']=emp[0]['nom_employe']
                    data2['prenom_employe']=emp[0]['prenoms_employe']
                    data2['role']= role
                    data2['billet_avion']= '0'
                    data2['statut_des_justifs']= 'non déclaré'
                except Exception as e:
                        print(e)
                        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
                #print(data2)
                serializer1 = EnvoyeSerializer(data=data2)
                if serializer1.is_valid():
                    print(serializer1)
                    serializer1.save()
                    
                    try:
                        dt1=str(dt)
                        print(dt1)
                        dt2= dt1[0:2]
                        print(dt2)
                        data3={}
                        data3['id_mission_id_id'] = data2['id_mission']
                        
                        id_barem = Bareme.objects.filter(id_processus_id=int(data1['type_processus'])).filter(jour_max__gte=int(dt2)-1).filter(jour_min__lt=int(dt2)+1).values('id_bareme')
                        print("bbbbbbaaaaaa")
                        if dt2 and id_barem:
                            print(int(dt2))
                        else:
                            strerror='La durée de la mission ne correspond à aucun bareme:----->'
                        #print(id_barem)
                        id_barem1 = id_barem[0]
                        id_barem1 = id_barem1['id_bareme']
                        print(id_barem1)
                        data3['id_bareme_id_id'] = int(id_barem1)
                        categorie= Employe.objects.filter(id_employe=data2['id_employe']).values('id_categorie_id')
                        categorie1= categorie[0]['id_categorie_id']
                        id_barem_detail= Bareme_detail.objects.filter(id_bareme_id =int(id_barem1)).filter(id_categorie_id=int(categorie1)).values('id_bareme_detail')
                        print('bb')
                        print(data2['id_employe'])
                        print(categorie1)
                        if id_barem_detail:
                            id_barem_detail1=id_barem_detail[0]['id_bareme_detail']
                        else:
                            strerror="Aucun barème ne correspond à la catégorie de l'employé "+ str(data2['id_employe'])
                        data3['id_bareme_detail_id_id'] = int(id_barem_detail1)
                        montant_zone = Montant_zone.objects.filter(id_bareme_detail_id=int(id_barem_detail1)).filter(id_zone_id=int(zone_id)).values('perdiem','hebergement','id_montant_zone')
                        print("kkkkkkkkkkkkkkkkiiiiiiiiiiiiiiiiiiiooooooooooooooooo")
                        print(zone_id)
                        id_montant_zone = 	montant_zone[0]['id_montant_zone']
                        data3['id_montant_zone_id_id'] = int( id_montant_zone)
                        envoye = Envoye.objects.latest('id_envoye')
                        Id_envoye = envoye.id_envoye
                        data3['id_envoye_id_id'] = int(Id_envoye)
                        data3['perdiem'] = int(montant_zone[0]['perdiem'])*int(dt2)
                        data3['hebergement'] = int(montant_zone[0]['hebergement'])*int(dt2)
                        data3['total_cout'] = data3['perdiem'] + data3['hebergement']
                        print(data3)
                        serializer2 = Bareme_envoyeSerializer(data=data3)
                        print(serializer2)
                    except Exception as e:
                        print(e)
                        return Response(strerror+str(e), status=status.HTTP_400_BAD_REQUEST)
                    if serializer2.is_valid():
                    #print(serializer1)
                        serializer2.save()
                    else:
                        return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)


                else:
                    #print(serializer1)
                    return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
            print('group')
            data4 = {}
            print(data1['type_processus'])
            try:
                for user_id in user_list:
                    usermail= User.objects.filter(id=user_id).values('email')
                    a_email_list.append(usermail[0]['email'])
                group_mail = Stepprocess.objects.filter(id_process_id= int(data1['type_processus'])).values('cible_id')
                for group in group_mail:
                    #print(group['cible_id'])
                    users_in_group = Group.objects.get(id=int(group['cible_id'])).user_set.all()
                    for user in users_in_group:
                        print(user.email)
                        if user.email not in a_email_list:
                            cc_email_list.append(user.email)
                message = 'Demande de mission vers'
                for dest in nom_destination:
                    message = message+" "+dest+"," 
                message = message+" du "+data1['depart_mission'].strftime('%d/%m/%y')
                message = message+" au "+data1['retour_mission'].strftime('%d/%m/%y')
                step=int(data1['current_step']+1)
                next_step1='En attente du rapport'
                next_step2=0
                Group_cible1 = Group.objects.filter(id=cible_group[0]['cible_id']).values('name')
                try:
                    next_step= Stepprocess.objects.filter(id_process=int(request.data['processus']),order_steps=step).values('type_steps_id')
                    next_step2 = Typesteps.objects.filter(id_typesteps=int(next_step[0]['type_steps_id']) ).values('nom_typesteps')
                    next_step1=next_step2[0]['nom_typesteps']+' du '+Group_cible1[0]['name']

                except Exception as e:                
                        print('44444444444444444444')
                        trace_back = traceback.format_exc()
                        message = str(e)+ " " + str(trace_back)
                        print(message)
                prochaine_action = next_step1
                
                auteur = User.objects.filter(id=int(data1['id_demandeur'])).values('first_name','last_name')
                acteur= Group.objects.filter(id=cible_group[0]['cible_id']).values('name')
                data4['A'] =  ', '.join(map(str, a_email_list))
                data4['cc'] =  'ismael.soro@snedai.com'
                data4['message'] = message 
                data4['prochaine_action'] = prochaine_action
                data4['sent'] = 'no'
                data4['auteur'] = data1['id_demandeur']
            except Exception as e:
                print(e)
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            serializer3 = NotificationSerializer(data=data4)
            if serializer3.is_valid():
                    print(serializer3)
                    serializer3.save()
                    
            else:
                    return Response(serializer3.errors, status=status.HTTP_400_BAD_REQUEST)
            request_finished.connect(send_mail_mission)
            print('s<eet')
            Config_rappor= Config_rapport.objects.filter(id_process_id=int(data1['type_processus'])).values('expression','acteur')
            print(Config_rappor)
            if Config_rappor[0]['expression']=='ET':
                id_missio = Mission.objects.latest('id_mission')
                envoye= Envoye.objects.filter(id_mission=id_missio).values('id_envoye')
                for x in range(0,len(envoye)):
                    data5={}
                    data5['id_envoye_id']=envoye[x]['id_envoye']
                    data5['step_process']=10
                    serializer5 = BloqueSerializer(data=data5)
                    print(serializer5)
                    if serializer5.is_valid():
                        print('ok')
                        serializer5.save()
                    else:
                        print(serializer5.errors)
            

            return Response("Mission créée avec succès", status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class MesMissionTraitement(APIView):
    def get(self, request, id=id,format=None):
        list_group=[]
        list_processs=[]
        groupes=Group.objects.all()
        print(id)
        for group in groupes:
            
            if User.objects.filter(pk=id, groups__name=group.name).exists():
                
                list_group.append(group.id)
        print("iiiiiiiiiiiiiiiiiiiiikkkkkkkkkkkkkkkkkkkkkkkkkk")
        #print(list_group)
        step_process = Stepprocess.objects.filter(cible_id__in=list_group)
        for step in step_process:
            
            if step.id_process_id not in list_processs:
                list_processs.append(step.id_process_id)
                print(":]")
                print(step.id_process_id)    

        try:
            mission = Mission.objects.filter(id_demandeur_id=id).distinct().order_by('-id_mission') | Mission.objects.filter(type_processus_id__in=list_processs).distinct().order_by('-id_mission') 
        
        
            serializer = MissiontSerializer(mission,context={'request': request}, many=True) 

            return Response(serializer.data)
        except Mission.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)



class MesMissionDetail(APIView):
    """
    Retrieve, update or delete a mission instance.
    """
    #permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Mission.objects.get(pk=pk)
        except Mission.DoesNotExist:
            raise Http404
    def post(self, request, pk):
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk, format=None):
        mission = self.get_object(pk)
        serializer = MissiontSerializer(mission)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mission = self.get_object(pk)
        serializer = MissiontSerializer(mission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mission = self.get_object(pk)
        mission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EnvoyeList(generics.ListCreateAPIView):
    queryset = Envoye.objects.all()
    serializer_class = EnvoyeSerializer

class EnvoyeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Envoye.objects.all()
    serializer_class =  EnvoyeSerializer
    def put(self, request, pk, format=None):
        Envoy = Envoye.objects.filter(id_envoye=pk).update(justifier=True)
        
        return Response(Envoy, status=status.HTTP_201_CREATED)
        

class ProcessList(generics.ListCreateAPIView):
   
    queryset = Processus.objects.all()
    serializer_class = ProcessusSerializer
    paginator = None

    

class ProcessG(generics.ListCreateAPIView):
    def post(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        print(request.data)
        entite = request.data['entite']
        projet = Projet.objects.filter(id_entite_id = int(entite))
        idprojet = projet.values_list('id_projet', flat=True)
        list_idprojet = list(idprojet)
        queryset = Processus.objects.filter(type_process='NO',id_relatated= int(entite)) | Processus.objects.filter(type_process='PR').filter(id_relatated__in=list_idprojet)
        serializer = ProcessusSerializer(queryset, many=True)
        print(serializer)
        return Response(serializer.data)

class Processus_step(APIView):
    def get(self, request, id_process):
        id=id_process
        lst=[]
        type_st={}
        stepproces= Stepprocess.objects.filter(id_process_id=int(id)).values().order_by('order_steps')
        print(stepproces)
        for x in range(0, len(stepproces)):
            type_st=dict(type_st)
            tri=int(stepproces[x]['type_steps_id'])
            type_step= Typesteps.objects.filter(id_typesteps=tri).values('nom_typesteps')
            type_st['id']=stepproces[x]['cible_id']
            group= Group.objects.filter(pk=int(stepproces[x]['cible_id'])).values()
            type_st['nom']=str(type_step[0]['nom_typesteps'])+" ("+str(group[0]['name'])+")"
            lst.append(type_st)

        return Response(lst)


class ProcessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Processus.objects.all()
    serializer_class =  ProcessusSerializer

class StepprocessList(generics.ListCreateAPIView):
    queryset = Stepprocess.objects.all()
    serializer_class = StepprocessSerializer

    def post(self, request):
        print('oklklklkl')
        print(request.data)
        data={}
        data['cible']=request.data['cible']
        data['type_steps']=request.data['type_steps']
        data['order_steps']=request.data['order_steps']
        data['id_process']=request.data['id_process']

        serializer = StepprocessSerializer(data=data)
        if serializer.is_valid():
                    #print(serializer1)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        Stepprocess = self.get_object(pk)
        serializer = StepprocessSerializer(Stepprocess, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Stepprocess = self.get_object(pk)
        Stepprocess.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StepprocessDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stepprocess.objects.all()
    serializer_class =  StepprocessSerializer

class userList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class =  UserSerializer

   

class userDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class =  UserSerializer

class BankList(generics.ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class =  BankSerializer

   

class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.all()
    serializer_class =  UserSerializer


class employeList(generics.ListCreateAPIView):
     queryset = Employe.objects.all()
     serializer_class = EmployeSerializer

     def post(self, request):
         print('okkkiiiijjjjj')
         print(request.data)
         data={}
         data4={}
         data4['cc'] =  'ismael.soro@snedai.com'
         password =''
         data4['sent'] = 'no'
         data4['auteur'] = request.data['id_createur']
         
         
         data['nom_employe']= request.data['nom_employe']
         data['prenoms_employe']= request.data['prenoms_employe']
         dare_naiss=request.data['date_naissance_employe']
         data['date_naiss_employe']=  datetime.strptime(dare_naiss, '%Y-%m-%d').date()
         data['matricule_employe']= request.data['matricule_employe']
         data['email_employe']= request.data['email_employe']
         data['tel_employe']= request.data['telephone_employe']
         data['fonction_employe']= request.data['fonction_employe']
         data['login_employe']= request.data['email_employe']
         data['password_employe']= 'samia'
         data['compte_actif']= request.data['activer']
         data['verrou_employe']= False
         data['date_creation']= datetime.now() 
         data['id_createur']= request.data['id_createur']
         data['id_user']= request.data['id_user']
         data['id_categorie']= request.data['categorie_employe']
         data['id_entite']= request.data['filiale_employe']
         data['id_service']= request.data['id_service']

         if data['id_user']==0:
            
            
            password = User.objects.make_random_password()
            user = User.objects.create(
            username=request.data['email_employe'],
            email=request.data['email_employe'],
            first_name=request.data['nom_employe'],
            last_name=request.data['prenoms_employe']
            )
            
            user.set_password(password)
            user.save()
            data['id_user'] = User.objects.latest('id')
            data4['message'] = 'Votre a été crée le login est:'+str(request.data['email_employe'],)+' et le mot de passe est:'+str(password)
            data4['prochaine_action']= "connection et modification de mot de passe"
            data4['A'] =request.data['email_employe']
        
         else:

              utilisateur= User.objects.filter(pk=data['id_user']).values('email')
              data4['A'] = utilisateur[0]['email']
              data4['message'] = "L'employe avec le login:"+str(request.data['email_employe'],)+' à été rataché à votre compte'+str(password)
              data4['prochaine_action']= "connexion"


             
         serializer = EmployeSerializer(data=data)
         print("cuicui")
         print(serializer)
        
         if serializer.is_valid():
            
            serializer.save()       

            
            
         else:
            print(serializer.errors)

         serializer3 = NotificationSerializer(data=data4)
         if serializer3.is_valid():
                    print(serializer3)
                    serializer3.save()
                    try:
                        request_finished.connect(send_mail_mission)
                        print("caraib")
                    except Exception as e:
                        print(e)  
                        print("caraib111") 
                    
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
         
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class employeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employe.objects.all()
    serializer_class =  EmployeSerializer

class poleList(generics.ListCreateAPIView):
     queryset = Pole.objects.all()
     serializer_class = PoleSerializer

class poleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pole.objects.all()
    serializer_class =  PoleSerializer

    

     




class entiteList(generics.ListCreateAPIView):
     queryset = Entite.objects.all()
     serializer_class = EntiteSerializer

     

class entiteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entite.objects.all()
    serializer_class =  EntiteSerializer

class typeprojetList(generics.ListCreateAPIView):
     queryset = TypeProjet.objects.all()
     serializer_class = TypeProjetSerializer

class typeprojetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TypeProjet.objects.all()
    serializer_class =  TypeProjetSerializer
    
    
class projetList(generics.ListCreateAPIView):
     queryset = Projet.objects.all()
     serializer_class = ProjetSerializer

     def post(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        print(request.data)
        data1= {}

        data1['nom_projet'] = request.data['nom_projet']
        date_debut=request.data['date_debut']
        data1['date_debut'] = datetime.strptime(date_debut, '%Y-%m-%d').date()
        date_fin=request.data['date_fin']
        data1['date_fin'] = datetime.strptime(date_fin, '%Y-%m-%d').date()
        data1['id_entite'] = request.data['id_entite']
        data1['type_projet'] = request.data['type_projet']

        serializer = ProjetSerializer(data=data1)
        
        if serializer.is_valid():

            print('ok')
           
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class projetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projet.objects.all()
    serializer_class =  ProjetSerializer

class CountryList(generics.ListCreateAPIView):
     queryset = Country.objects.all()
     serializer_class = CountrySerializer

class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class =  CountrySerializer

class WorldcitiesList(generics.ListCreateAPIView):
     queryset = Worldcities.objects.all().order_by('city')
     serializer_class = WorldcitiesSerializer
     paginator = None

     def post(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        print(request)
        zone = request.data['zone']
        queryset = Worldcities.objects.filter(zone_id=int(zone)).order_by('city')
        serializer = WorldcitiesSerializer(queryset, many=True)
        return Response(serializer.data)

class WorldcitiesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worldcities.objects.all()
    serializer_class =  WorldcitiesSerializer

class RegimeList(generics.ListCreateAPIView):
     queryset = Regime.objects.all()
     serializer_class = RegimeSerializer
     

class RegimeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Regime.objects.all()
    serializer_class =  RegimeSerializer

class CategorieList(generics.ListCreateAPIView):
     queryset = Categorie.objects.all()
     serializer_class = CategorieSerializer
     

class CategorieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categorie.objects.all()
    serializer_class =  CategorieSerializer

class ZoneList(generics.ListCreateAPIView):
     queryset = Zone.objects.all()
     serializer_class = ZoneSerializer
     #paginator = None
     

class ZoneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class =  ZoneSerializer

class GroupList(generics.ListCreateAPIView):
     queryset = Group.objects.all()
     serializer_class = GroupSerializer
     

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Group.objects.all()
    serializer_class =  GroupSerializer

class TypestepsList(generics.ListCreateAPIView):
     queryset = Typesteps.objects.all().exclude(id_typesteps=9).exclude(id_typesteps=10)
     serializer_class = TypestepsSerializer
     

class TypestepsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Typesteps.objects.all()
    serializer_class =  TypestepsSerializer

class BaremeList(generics.ListCreateAPIView):
     queryset = Bareme.objects.all()
     serializer_class = BaremeSerializer
    #  def post(self, request, format=None):
    #     print(request.data)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
     

class BaremeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Bareme.objects.all()
    serializer_class =  BaremeSerializer

class Bareme_detailList(generics.ListCreateAPIView):
     queryset = Bareme_detail.objects.all()
     serializer_class = Bareme_detailSerializer
     

class Bareme_detailDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Bareme_detail.objects.all()
    serializer_class =  Bareme_detailSerializer

class Montant_zoneList(generics.ListCreateAPIView):
     queryset = Montant_zone.objects.all()
     serializer_class = Montant_zoneSerializer
     

class Montant_zoneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Montant_zone.objects.all()
    serializer_class =  Montant_zoneSerializer

class ServiceList(generics.ListCreateAPIView):
     queryset = Service.objects.all()
     serializer_class = ServiceSerializer
     

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Service.objects.all()
    serializer_class =  ServiceSerializer


class Validations(APIView):
    
    """
    Liste de mes missions, or create a new mission.
    """
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id=id,format=None):
       
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        print(request.data)
        try:
            idmission = request.data['id_mission']
            id_user = request.data['id_user']
            validation = request.data['validation']
            user = User.objects.get(pk=id_user)
            print(user)
            mission = Mission.objects.filter(id_mission=idmission).values('current_step','type_processus_id','numero_mission','avion')
            currentstep = mission[0]['current_step']
            processusid = mission[0]['type_processus_id'] 
            add=1
            stepprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep).values('cible_id','type_steps_id')
            nextprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep+add).values('cible_id','type_steps_id')
            currentnomsteps = Typesteps.objects.get(id_typesteps=int(stepprocess[0]['type_steps_id']))
            nextnomsteps = Typesteps.objects.get(id_typesteps=int(nextprocess[0]['type_steps_id']))
            groupe = Group.objects.filter(pk=int(nextprocess[0]['cible_id'])).values('id','name')
            print('kkkkkkkkkkkkkkkkid_user:{}'.format(id_user))
            print('groupe:{}'.format(groupe))
            groupid=[]
            groupemail=[user.email]
            currentsible = str(Group.objects.get(id=stepprocess[0]['cible_id']))
            relance_cible = str(Group.objects.get(id=nextprocess[0]['cible_id']))
            message = 'Validation de la mission numero '+mission[0]['numero_mission']+' par le '+ currentsible
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
                        
        try:    
            if mission[0]['avion']=='False' and nextnomsteps.nom_typesteps== 'Billet':
                add=1
                stepprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep).values('cible_id','type_steps_id')
                nextprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=int(currentstep)+add).values('id_stepprocess','order_steps','cible_id','type_steps_id')
                nextprocess1 = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=int(currentstep)+add+1).values('id_stepprocess','order_steps','cible_id','type_steps_id')
                currentnomsteps = Typesteps.objects.get(id_typesteps=int(stepprocess[0]['type_steps_id']))
                nextnomsteps = Typesteps.objects.get(id_typesteps=int(nextprocess[0]['type_steps_id']))
                groupe = Group.objects.all()
                gp=".user_set.all()"
                print('groupe:{}'.format(groupe))
                groupid=[]
                groupemail=[user.email]
                currentsible = str(Group.objects.get(id=nextprocess[0]['cible_id']))
                relance_cible = str(Group.objects.get(id=nextprocess1[0]['cible_id']))
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            print(stepprocess[0]['cible_id']) 
            print("zzzzzzzzzzzzzzzzmmmmmmmmmmmmmmmmmmmmmm")
            userlist = User.objects.filter(groups__name=groupe[0]['name'])
            
            for user1 in userlist:
                print('userid:{}'.format(userlist))
                groupid.append(user1.id)
                groupemail.append(user1.email)
                
            if user.has_perm('quickstart.validation'):
                print(":) yes")  
            else:
                print(":( no ")  
            if validation=='validation':
                print(":) yes1")  
                
            else:
                print(":( no1 ") 
                return Response("l' utilisateur  n'est pas autorisé à effectuer une validation ", status=status.HTTP_403_FORBIDDEN)
            if int(id_user) in groupid:
                print(":) yes2")  
            else:
                print("zzzzzzzzzzzzzzzzmmmmmmmmmmmmmmmmmmmmmm") 
                print('id_user:{}'.format(groupe[0]['name']))
                print('groupe:{}'.format(groupe))
                print(":( no2 ")
                return Response("l' utilisateur  n'est pas autorisé à effectuer cette action ", status=status.HTTP_403_FORBIDDEN)        
            data4={} 
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        try:       
            if user.has_perm('quickstart.validation') and validation=='validation' and int(id_user) in groupid:
                print("111") 
                obj = Mission.objects.get(pk=int(idmission))
                
                obj.current_step = currentstep+add
                obj.relance_cible = relance_cible
                obj.save()
                
                print(groupemail)
                data4['A'] = 'ismael.soro@snedai.com' ##', '.join(map(str, groupemail))
                data4['cc'] =  'joel.ziade@snedai.com'
                data4['message'] = message 
                data4['prochaine_action'] = nextnomsteps.nom_typesteps
                data4['sent'] = 'no'
                data4['auteur'] = id_user
                serializer3 = NotificationSerializer(data=data4)
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        try:
                if serializer3.is_valid():
                        print(serializer3)
                        serializer3.save()
                        request_finished.connect(send_mail_mission)
                        mission_to_envoye(int(idmission))
                        return Response("Validez avec succès",status=status.HTTP_201_CREATED)
                        
                else:
                        return Response(serializer3.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
              
            
            return JsonResponse("Vous n'êtes pas authorisé à faire cette action!!",status=status.HTTP_403_FORBIDDEN,content_type="application/json", safe=False)

class Billets(APIView):
    
    """
    Liste de mes missions, or create a new mission.
    """
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id=id,format=None):
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        print(request.data)
        try:
            id_envoye= request.data['id_envoye']
            is_config_blocage(int(id_envoye))
            envoyem=Envoye.objects.filter(id_envoye=int(id_envoye[0])).values('id_mission_id')
            idmission = envoyem[0]['id_mission_id']
            id_user = request.data['id_user']
            billet = request.data['billet']
            montant = request.data['montant']
            env={}
            i=0
            for x in range(0,len(id_envoye)):
                env[id_envoye[x]] = montant[x]
                i=i+1
            user = User.objects.get(pk=id_user)
            mission = Mission.objects.filter(id_mission=idmission).values('current_step','type_processus_id','numero_mission','avion')
            currentstep = mission[0]['current_step']
            processusid = mission[0]['type_processus_id']
            add=1 
            print(currentstep)
            print(currentstep)
            stepprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep).values('cible_id','type_steps_id')
            nextprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep+add).values('cible_id','type_steps_id')
            currentnomsteps = Typesteps.objects.get(id_typesteps=int(stepprocess[0]['type_steps_id']))
            nextnomsteps = Typesteps.objects.get(id_typesteps=int(nextprocess[0]['type_steps_id']))
            groupe = Group.objects.filter(pk=int(nextprocess[0]['cible_id'])).values('id','name')
            groupid=[]
            groupemail=[user.email]
            currentsible = str(Group.objects.get(id=stepprocess[0]['cible_id']))
            relance_cible = str(Group.objects.get(id=nextprocess[0]['cible_id']))
            message = "Attribution du montant du billet d'avion de la mission numéro "+mission[0]['numero_mission']+' par le '+ currentsible
            userlist = User.objects.filter(groups__name=groupe[0]['name'])
            print('userid:{}'.format(groupe[0]['name']))
            for user1 in userlist:
                print('userid:{}'.format(Mission))
                groupid.append(user1.id)
                groupemail.append(user1.email)  
                    
            data4={}
            
            if mission[0]['avion']=='False' and nextnomsteps.nom_typesteps== 'billet':
                
                add=2
                stepprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep).values('cible_id','type_steps_id')
                nextprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep+add).values('cible_id','type_steps_id')
                currentnomsteps = Typesteps.objects.get(id_typesteps=int(stepprocess[0]['type_steps_id']))
                nextnomsteps = Typesteps.objects.get(id_typesteps=int(nextprocess[0]['type_steps_id']))
                groupe = Group.objects.get(id=int(stepprocess[0]['cible_id'])).user_set.all()
                groupid=[]
                groupemail=[user.email]
                currentsible = str(Group.objects.get(id=stepprocess[0]['cible_id']))
                relance_cible = str(Group.objects.get(id=nextprocess[0]['cible_id']))
            print(groupid)
            if user.has_perm('quickstart.billets') and billet=='billet' and int(id_user) in groupid:
                print('11111111111')
                obj = Mission.objects.get(pk=int(idmission))
                
                obj.current_step = currentstep+add
                obj.relance_cible = relance_cible
                obj.save()
                
                for key,value in env.items():
                    envoye= Envoye.objects.get(id_envoye=int(key))
                    envoye.billet_avion = value
                    envoye.save()
                
                
                print(groupemail)
                data4['A'] = 'ismael.soro@snedai.com' ##', '.join(map(str, groupemail))
                data4['cc'] =  'joel.ziade@snedai.com'
                data4['message'] = message 
                data4['prochaine_action'] = nextnomsteps.nom_typesteps
                data4['sent'] = 'no'
                data4['auteur'] = id_user
                serializer3 = NotificationSerializer(data=data4)
                if serializer3.is_valid():
                        print(serializer3)
                        serializer3.save()
                        request_finished.connect(send_mail_mission)
                        return Response("Billet(s) d'avion enregistré(s)",status=status.HTTP_201_CREATED)
                        
                else:
                        return Response(serializer3.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print("cococococo")
            print(e)
            return Response(e,status=status.HTTP_204_NO_CONTENT)            

        return Response(status=status.HTTP_403_FORBIDDEN)

class forfait(APIView):
    
    """
    Liste de mes missions, or create a new mission.
    """
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id=id,format=None):
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        idmission = request.data['id_mission']
        id_user = request.data['id_user']
        action = request.data['action']
        forfait = request.data['forfait']

        user = User.objects.get(pk=id_user)
        mission = Mission.objects.filter(id_mission=idmission).values('current_step','type_processus_id','numero_mission','avion')
        currentstep = mission[0]['current_step']
        processusid = mission[0]['type_processus_id'] 
        add=1
        stepprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep).values('cible_id','type_steps_id')
        nextprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep+add).values('cible_id','type_steps_id')
        currentnomsteps = Typesteps.objects.get(id_typesteps=int(stepprocess[0]['type_steps_id']))
        nextnomsteps = Typesteps.objects.get(id_typesteps=int(nextprocess[0]['type_steps_id']))
        groupe = Group.objects.get(id=int(stepprocess[0]['cible_id'])).user_set.all()
        groupid=[]
        groupemail=[user.email]
        currentsible = str(Group.objects.get(id=stepprocess[0]['cible_id']))
        relance_cible = str(Group.objects.get(id=nextprocess[0]['cible_id']))
        message = 'Changement de forfait '+mission[0]['numero_mission']+' par le '+ currentsible
        
        if mission[0]['avion']=='False' and nextnomsteps.nom_typesteps== 'Billet':
            add=2
            stepprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep).values('cible_id','type_steps_id')
            nextprocess = Stepprocess.objects.filter(id_process_id =int(processusid) ).filter(order_steps=currentstep+add).values('cible_id','type_steps_id')
            currentnomsteps = Typesteps.objects.get(id_typesteps=int(stepprocess[0]['type_steps_id']))
            nextnomsteps = Typesteps.objects.get(id_typesteps=int(nextprocess[0]['type_steps_id']))
            groupe = Group.objects.get(id=int(stepprocess[0]['cible_id'])).user_set.all()
            groupid=[]
            groupemail=[user.email]
            currentsible = str(Group.objects.get(id=stepprocess[0]['cible_id']))
            relance_cible = str(Group.objects.get(id=nextprocess[0]['cible_id']))
        for user1 in groupe:
            groupid.append(user1.id)
            groupemail.append(user1.email)  
                  
        data4={}        
        if user.has_perm('quickstart.right.validation') and action=='forfait' and int(id_user) in groupid:
            obj = Mission.objects.get(pk=int(idmission))
            
            obj.current_step = currentstep+add
            obj.relance_cible = relance_cible
            obj.regime_id = forfait
            obj.save()
            
            print(groupemail)
            data4['A'] = 'ismael.soro@snedai.com' ##', '.join(map(str, groupemail))
            data4['cc'] =  'joel.ziade@snedai.com'
            data4['message'] = message 
            data4['prochaine_action'] = nextnomsteps.nom_typesteps
            data4['sent'] = 'no'
            data4['auteur'] = id_user
            serializer3 = NotificationSerializer(data=data4)
            if serializer3.is_valid():
                    print(serializer3)
                    serializer3.save()
                    request_finished.connect(send_mail_mission)
                    mission_to_envoye(int(idmission))
                    return Response(status=status.HTTP_201_CREATED)
                    
            else:
                    return Response(serializer3.errors, status=status.HTTP_400_BAD_REQUEST)

        
        return Response(status=status.HTTP_403_FORBIDDEN)


     



class NumeroDetail(APIView):
    def put(self, request,format=None):
        query1 = Mission.objects.filter(id_mission=request.data['id_mission'])
        query2 = query1.values('current_step','type_processus_id')
        currentstep = query2[0]['current_step']
        type_processus = query2[0]['type_processus_id']
        stepprocess= Stepprocess.objects.filter(order_steps=int(currentstep)+2,id_process_id=int(type_processus)).values('type_steps_id')
        typesteps=  Typesteps.objects.filter(id_typesteps=stepprocess[0]['type_steps_id']).values('nom_typesteps')
        query3 = query1.update(numero_mission=request.data['id_mission'],current_step=int(currentstep)+1,relance_cible=str(typesteps[0]['nom_typesteps'])) 
        mission_to_envoye(int(request.data['id_mission']))
        return Response("Numéro attribué", status=status.HTTP_202_ACCEPTED)
    

class paiement(APIView):
    
    """
    Liste de mes missions, or create a new mission.
    """
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id=id,format=None):
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, format=None):
        print(request.data)
        try:
            data={}
            data['id_tresorier']=int(request.data['user_paiement'])
            data['id_envoye_id']=int(request.data['id_envoye'])
            data['montant']=request.data['montant']
            data['cheque']=eval(request.data['cheque'])
            data['date_paiement']=date.today()
            if data['cheque']==True:
                data1={}
                data1['numero']=request.data['numero_cheque']
                data1['id_bank_id']=request.data['nom_banque']
                serializer1 = ChequeSerializer(data=data1)
            
                if serializer1.is_valid():
                        
                        serializer1.save()
                        cheq=Cheque.objects.latest('id_cheque')
                        
                        data['id_cheque_id']= cheq.id_cheque
            serializer = PaiementSerializer(data=data)
            #print(serializer)
            if serializer.is_valid():
                
                serializer.save()
                data2= Envoye.objects.filter(id_mission_id=request.data['id_mission'])
                serializer2 = EnvoyeSerializer(data2,context={'request': request}, many=True)
                is_config_blocage(int(request.data['id_envoye']))
                return Response(serializer2.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                
        except Exception as e:
                print(e)
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        

class reception_paiement(APIView):
    def put(self, request, format=None):
        try:
            close= 0
            id_envoye= request.data['id_envoye']
            query = Paiement.objects.filter(id_envoye_id_id=id_envoye).update(date_reception=date.today())
            id_mission=request.data['id_mission']
            mission=Mission.objects.filter(id_mission=id_mission).values('current_step')
            current_st=int(mission[0]['current_step'])+1
            envoye = Envoye.objects.filter(id_mission=id_mission).values('id_envoye')
            for envo in range(0,len(envoye)):
                paiement = Paiement.objects.filter(id_envoye_id_id=envoye[envo]['id_envoye']).values('date_reception')
                if paiement[0]['date_reception']==None:
                     close=close+1
                     print(envoye[envo]['id_envoye'])
            print(close)
            print('baia')
            print(current_st)
            if close==0:
               query1 = Mission.objects.filter(id_mission=id_mission).update(current_step=current_st)
               print(query1)     
            return Response("Reception du paiment éffectué avec succès", status=status.HTTP_201_CREATED)
        except Exception as e:
                print(e)
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class PaysList(APIView):

    def get(self, request):
        query= Worldcities.objects.values('country','iso3').order_by('country')
        return Response(query)

    def post(self, request,format=None):

        iso= request.data['country']
        id_zone=request.data['zone_id']
        query = Worldcities.objects.filter(country=iso).update(zone_id=id_zone)
        return Response(status=status.HTTP_201_CREATED)

class justification(APIView): 
        def post(self, request,format=None):
            print(request.data)
            return Response("AYIA!!!!!", status=status.HTTP_426_UPGRADE_REQUIRED) 

class justificationList(generics.ListCreateAPIView):
     queryset = Justifs.objects.all()
     serializer_class = JustifsSerializer
     def get(self, request,envoye,format=None):
            justificatifs=Justifs.objects.filter(id_envoye_id=envoye)
            serializer = JustifsSerializer(justificatifs,context={'request': request}, many=True) 

            return Response(serializer.data)
            


     def post(self, request,format=None):
            print(request.data)
            data={}
            data['id_envoye_id']= int(request.data['id_envoye_id'])
            
            data['piece']= request.data['piece']
            data['Type_piece']= request.data['Type_piece']
            data['Libelle']= request.data['Libelle']
            data['Montant']= request.data['Montant']
            data['commentaire']= request.data['commentaire']
            serializers= JustifsSerializer(data=data)
            if serializers.is_valid():
            
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED) 
            print(serializers.errors)
            return Response( serializers.errors, status=status.HTTP_400_BAD_REQUEST )

class justificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Justifs.objects.all()
    serializer_class =  JustifsSerializer 

class PaysDetail(APIView):
    def post(self, request):
        id_zone=request.data['zone_id']
        query= Worldcities.objects.filter(zone_id=id_zone).values('country','iso3').annotate(Count('zone_id'))
        #query=Worldcities.objects.values('country','iso3').annotate(count('zone_id'))
        return Response(query)

    def put(self, request):
        print(request.data)
        zone_id= request.data['zone_id']
        iso3= ast.literal_eval(str(request.data['country']))
        country=[]
        query = Worldcities.objects.filter(zone_id=zone_id).values('country').annotate(Count('zone_id'))
        query1=list(query)
        for quer in query1:
            country.append(quer['country'])
        
        for iso in iso3:
            print(iso)
            if iso not in country:
               print(iso)
               query2 = Worldcities.objects.filter(country=iso).update(zone_id=zone_id) 
        for quer in country:
            #print(quer)
            if quer not in iso3:
                query3 = Worldcities.objects.filter(country=quer).update(zone_id=999999)

        return Response(status=status.HTTP_201_CREATED)


class delais_bareme(APIView):
    
    """
    Liste de mes missions, or create a new mission.
    """
    #permission_classes = [permissions.IsAuthenticated]
    def get(self, request,format=None):
        jour_min=[{'jour':1,'enable':False},{'jour':2,'enable':False},{'jour':3,'enable':False},{'jour':4,'enable':False},{'jour':5,'enable':False},{'jour':6,'enable':False},{'jour':7,'enable':False},{'jour':8,'enable':False},{'jour':9,'enable':False},{'jour':10,'enable':False},{'jour':11,'enable':False},{'jour':12,'enable':False},{'jour':13,'enable':False},{'jour':14,'enable':False},{'jour':15,'enable':False},{'jour':16,'enable':False},{'jour':17,'enable':False},{'jour':18,'enable':False},{'jour':19,'enable':False},{'jour':20,'enable':False},{'jour':21,'enable':False},{'jour':22,'enable':False},{'jour':23,'enable':False},{'jour':24,'enable':False},{'jour':25,'enable':False},{'jour':26,'enable':False},{'jour':27,'enable':False},{'jour':28,'enable':False},{'jour':29,'enable':False},{'jour':30,'enable':False},{'jour':31,'enable':False}]
        jour_max=jour_min
        jour={}
        jour['jour_min']=jour_min
        jour['jour_max']=jour_min
        
        return Response(jour)

    def post(self, request, format=None):
        print(request.data)
        jour_min=[{'jour':1,'enable':False},{'jour':2,'enable':False},{'jour':3,'enable':False},{'jour':4,'enable':False},{'jour':5,'enable':False},{'jour':6,'enable':False},{'jour':7,'enable':False},{'jour':8,'enable':False},{'jour':9,'enable':False},{'jour':10,'enable':False},{'jour':11,'enable':False},{'jour':12,'enable':False},{'jour':13,'enable':False},{'jour':14,'enable':False},{'jour':15,'enable':False},{'jour':16,'enable':False},{'jour':17,'enable':False},{'jour':18,'enable':False},{'jour':19,'enable':False},{'jour':20,'enable':False},{'jour':21,'enable':False},{'jour':22,'enable':False},{'jour':23,'enable':False},{'jour':24,'enable':False},{'jour':25,'enable':False},{'jour':26,'enable':False},{'jour':27,'enable':False},{'jour':28,'enable':False},{'jour':29,'enable':False},{'jour':30,'enable':False},{'jour':31,'enable':False}]
        jour_max=jour_min
        jour={}
        barem= Bareme.objects.filter()
        jour['jour_min']=jour_min
        jour['jour_max']=jour_min
        if request.method == 'POST': 
            
            if 'id_processus' in request.POST and request.data['id_processus']!='null':
                id_processus_id=request.data['id_processus']
                barem= barem.filter(id_processus_id=id_processus_id)
                print("aaaaaaaaaaaaaaaaaaaa")
            if 'id_regime' in request.POST and request.data['id_regime']!='null':
                id_regime_id=request.data['id_regime']
                barem= barem.filter(id_regime_id=id_regime_id)
                print("wichi")

            if 'jour_max' in request.POST and request.data['jour_max']!='null':
                jourmax=request.data['jour_max']
                print("rrrrrrrrrrrrr")
              
            if 'jour_min' in request.POST and request.data['jour_min']!='null':
                jourmin=request.data['jour_min']
                print("111111111111111111111")
               
        
    
        for bare in barem:
            min_j=bare.jour_min
            max_j=bare.jour_max
            for x in range(0,len(jour_max)):
                for e in range (int(min_j),int(max_j)+1):
                    if jour_max[x]['jour']==e:
                        jour_max[x]['enable']=True
                        jour_min[x]['enable']=True

        jour['jour_min']=jour_min
        jour['jour_max']=jour_min
        return Response(jour)

class Finalisation(APIView):
    def post(self,request):
        debloque=''
        bloque=''
        envoye_rapport_obligatoire={}
        finalisation=[]
        id_mission= request.data['id_mission']
        mission= Mission.objects.filter(id_mission=int(id_mission)).values()
        step_process= Stepprocess.objects.filter(id_process_id=mission[0]['type_processus_id']).values().order_by('order_steps')
        final_step=len(step_process)
        #print(step_process.filter(order_steps=final_step).values())
        envoye = Envoye.objects.filter(id_mission=int(id_mission)).values()
        for x in range(len(envoye)):
            envoye_rapport_obligatoire = dict(envoye_rapport_obligatoire)
           
            rap_obl=check_if_rapport_obligatoire(envoye[x]['id_envoye'])
            rap_valid=check_if_rapport_valide(envoye[x]['id_envoye'])
            env_bloque= check_if_envoye_bloque(envoye[x]['id_envoye'])
            envoye_rapport_obligatoire['id_envoye']=envoye[x]['id_envoye']
            envoye_rapport_obligatoire['rapport_obligatoire']=rap_obl

            envoye_rapport_obligatoire['rapport_valide']=rap_valid
            envoye_rapport_obligatoire['bloque']=env_bloque
            
            finalisation.append(envoye_rapport_obligatoire)
        
        print(finalisation)
            
        rapport_final= check_rapport_final(finalisation)   

        return Response(rapport_final , status=status.HTTP_202_ACCEPTED )

class Config_blocageList(generics.ListCreateAPIView):
     queryset = Config_blocage.objects.all()
     serializer_class = Config_blocageSerializer
     

class Config_blocageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Config_blocage.objects.all()
    serializer_class =  Config_blocageSerializer

class RapportList(generics.ListCreateAPIView):
     """
    A view that can accept POST requests with JSON content.
    """
     
     queryset = Rapport.objects.all()
     serializer_class = RapportSerializer
     
     def get(self, request,format=None):
            Rapport1=Rapport.objects.all()
            serializer = RapportSerializer(Rapport1,context={'request': request}, many=True) 
            

            return Response(serializer.data)

     def post(self,request,format=None):
         print(request.data)
         data={}
        
         data['rapport_config']= request.data['rapport_config']
         data['fichier']= request.data['fichier']
         data['resultats_attendu']= str(request.data['resultats_attendu'])
         data['recommendations']= str(request.data['recommendations'])
         data['date_creation']= date.today()
         data['id_createur']= request.data['id_createur']
         data['date_derniere_modification']= date.today()
         #data['id_modificateur']= request.data['id_modificateur']
         #data['validation']= request.data['validation']
         #data['id_validateur']= request.data['id_validateur']
         data['id_envoye1']= int(request.data['id_envoye1'])
         
         serializers= RapportSerializer(data=data)
         print(serializers)
         if serializers.is_valid():
            
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED) 
         print(serializers.errors)
         return Response( serializers.errors, status=status.HTTP_400_BAD_REQUEST )
         

class RapportDetail(APIView):
    queryset =Rapport.objects.all()
    serializer_class =  RapportSerializer

    def put(self,request,pk):
        id_validateur= request.data['id_validateur']
        rapport = Rapport.objects.filter(id_rapport=pk)
        rapport.update(id_validateur_id=id_validateur,date_derniere_modification=date.today(),validation=date.today())
        rapport1 = Rapport.objects.filter(id_rapport=pk).values()
         
       
        return Response( rapport1 , status=status.HTTP_200_OK)
       


        

class rapport_envoyeDetail(APIView):
    def get(self,request,id_envoye):
        rapport= Rapport.objects.filter(id_envoye1_id=id_envoye).values()
        return Response(rapport)

class rapport_verif(APIView):
    def get(self,request):
        print(request.data)
        rapport= ''
        return Response(rapport)

class Config_rapportList(generics.ListCreateAPIView):
     queryset = Config_rapport.objects.all()
     serializer_class = Config_rapportSerializer


     

class Config_rapportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset =Config_rapport.objects.all()
    serializer_class =  Config_rapportSerializer

class Contrainte(APIView):
    def get(self,request,id_process):
        stepproces= Stepprocess.objects.filter(id_process_id=id_process).order_by('order_steps').values()
        lsstepproces={}
        ls=[]
        i=0
        val=''
        print(stepproces)
        for step in stepproces:
            lsstepproces=dict(lsstepproces)
            typest= Typesteps.objects.filter(id_typesteps=step['type_steps_id']).values()
            group = Group.objects.filter(pk=step['cible_id']).values()
            #lsstepproces[typest['id_typesteps']]=typest['nom_typesteps']
            if typest[0]['nom_typesteps']== 'validation':
                val=" "+str(group[0]['name'])
            else:
                val=''
            lsstepproces['id_stepprocess']=step['id_stepprocess']
            lsstepproces['nom_typesteps']= str(typest[0]['nom_typesteps'])+val
            ls.append(lsstepproces)
            i=i+1
            print(lsstepproces)
            
        return Response(ls)


class fiche_mission(APIView):
    def post(self,request):
        return Response("ok")










    



