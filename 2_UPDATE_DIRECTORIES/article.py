# -*- coding: utf-8 -*-
import encodings
import sys
import glob
import unicodedata
from xml.dom.minidom import parse

print(sys.stdout.encoding)

files=sorted(glob.glob("input/meteo*Sort.xml")+glob.glob('input/meteo_????_???_rvt.xml'))

selections=['Agrométéorologie','AMMA','Applications','Biométéorologie','Campagne expérimentale','Changement climatique',"Chimie de l'atmosphère",'Climatologie','Débat','Dossier','Ecosystèmes','Economie','Education','Enseignement','Environnement','Etudes de cas','Histoire','Hydrologie','Interview','Le temps des écrivains','Médias','Météo pour tous','Météorologie aéronautique','Météorologie dynamique','Météorologie spatiale','Météorologie théorique','Météorologie tropicale','Neige et glace','Nuages et aérosols','Observation','Océan et atmosphère','Océanographie','Optique atmosphérique','Paléoclimatologie','Phénomènes météorologiques','Physique atmosphérique','Planétologie','Prévision','Récit','Retour sur...','Société','Terminologie']
#selections=['Enseignement']

tt_list=["L'","La ","Le ","Les ","Un ","Une ", "De la ", "De l'","Du ", "Des ", "Sur la ", "Au "]

fhtml = open('output/repertoire_articles.html', 'w')
fhtml.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
fhtml.write('<H1>Répértoire des articles</H1><P>'+'\n')

fxml = open('output/repertoire_articles.xml', 'w')
fxml.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
fxml.write('<articles_par_rubrique>'+'\n')

nb=0

#Boucle sur les rubriques
for selection in selections:
  #Ajouter titre de la rubrique
  fhtml.write('<H2>'+selection+'</H2><P>'+'\n')
  fxml.write(' <rubrique id="'+selection+'">'+'\n')
  #Initialiser la liste de titres et d'auteurs
  titre_list=[]
  titre_list_sans_accents=[]
  url_list=[]
  auteur_list=[]
  num_list=[]
  annee_list=[]
  #Boucle sur les fichiers
  for file in files:
    print(file)
    dom = parse(file)
    notices=dom.getElementsByTagName('notice')
    for notice in notices: 
       #lire la rubrique
       rubrique=notice.getElementsByTagName('rubrique')
       rubrique_print=rubrique[0].childNodes[0].nodeValue
       #si on a detecte la bonne rubrique
       if rubrique_print == selection:
         #lire le titre et le stocker dans une liste
         titre=notice.getElementsByTagName('titre')
         titre_print=titre[0].childNodes[0].nodeValue
         print(titre_print)
         if selection != 'Le temps des écrivains':
           #modifier le titre s'il commence par un article
           for tt in tt_list: 
              if titre_print[0:len(tt)] == tt: 
                loc1=titre_print.find(':') 
                loc2=titre_print.find('?')
                loc3=titre_print.find('[')
                loc4=titre_print.find(';')
                loc5=titre_print.find('- ')
                if loc1 != -1 or loc2 != -1 or loc3 != -1 or loc4 != -1 or loc5 != -1:
                  if loc1 == -1: loc1=999
                  if loc2 == -1: loc2=999
                  if loc3 == -1: loc3=999
                  if loc4 == -1: loc4=999
                  if loc5 == -1: loc5=999
                  loc=min(loc1,loc2,loc3,loc4,loc5)
                  ztitre=titre_print[len(tt):loc]+" ("+tt.lower().strip()+") "+titre_print[loc:]
                else:
                  ztitre=titre_print[len(tt):]+" ("+tt.lower().strip()+")"
                #premier lettre en majuscule
                titre_print=ztitre[0].upper()+ztitre[1:]
         titre_list.append(titre_print)
         #preparer une liste sans accents et sans chiffres romains
         #a partir des chaines les plus longues jusqu au plus courtes
         titre_print_bis=titre_print
         titre_print_bis=titre_print_bis.replace('XVIIIe ','0018 ') 
         titre_print_bis=titre_print_bis.replace('XXIXe ', '0029 ') 
         titre_print_bis=titre_print_bis.replace('XVIIe ', '0017 ') 
         titre_print_bis=titre_print_bis.replace('XIIIe ', '0013 ') 
         titre_print_bis=titre_print_bis.replace('VIIIe ', '0008 ') 
         titre_print_bis=titre_print_bis.replace('XVIe ',  '0016 ') 
         titre_print_bis=titre_print_bis.replace('XXXe ',  '0030 ') 
         titre_print_bis=titre_print_bis.replace('XIXe ',  '0019 ') 
         titre_print_bis=titre_print_bis.replace('XIVe ',  '0014 ') 
         titre_print_bis=titre_print_bis.replace('VIIe ',  '0007 ') 
         titre_print_bis=titre_print_bis.replace('XIIe ',  '0012 ') 
         titre_print_bis=titre_print_bis.replace('IIIe ',  '0003 ') 
         titre_print_bis=titre_print_bis.replace('XVe ',   '0015 ') 
         titre_print_bis=titre_print_bis.replace('IIe ',   '0002 ') 
         titre_print_bis=titre_print_bis.replace('IVe ',   '0004 ') 
         titre_print_bis=titre_print_bis.replace('XIe ',   '0011 ') 
         titre_print_bis=titre_print_bis.replace('IXe ',   '0009 ') 
         titre_print_bis=titre_print_bis.replace('VIe ',   '0006 ') 
         titre_print_bis=titre_print_bis.replace('XXe ',   '0020 ') 
         titre_print_bis=titre_print_bis.replace('Ier ',   '0001 ') 
         titre_print_bis=titre_print_bis.replace('Ve ',    '0005 ') 
         titre_print_bis=titre_print_bis.replace('Xe ',    '0010 ') 
         #enlever les accents
         titre_print_bis=titre_print_bis.replace(u'1ère ',  '0001ere ') 
         titre_print_bis=titre_print_bis.replace(u'1er ' ,  '0001er ' ) 
         titre_print_bis=titre_print_bis.replace(u'2ème ',  '0002eme ') 
         titre_print_bis=titre_print_bis.replace(u'3ème ',  '0003eme ') 
         titre_print_bis=titre_print_bis.replace(u'4ème ',  '0004eme ') 
         titre_print_bis=titre_print_bis.replace(u'5ème ',  '0005eme ') 
         titre_print_bis=titre_print_bis.replace(u'6ème ',  '0006eme ') 
         titre_print_bis=titre_print_bis.replace(u'7ème ',  '0007eme ') 
         titre_print_bis=titre_print_bis.replace(u'8ème ',  '0008eme ') 
         titre_print_bis=titre_print_bis.replace(u'9ème ',  '0009eme ') 
         #traitement final pour enlver les caracteres speciaux
         titre_print_bis=''.join(e for e in titre_print_bis if e.isalnum())
         titre_list_sans_accents.append(unicodedata.normalize('NFKD',titre_print_bis.lower()).encode('ASCII', 'ignore'))
         #lire le numero et le stocker dans une liste
         num=notice.getElementsByTagName('numero')
         num_print=num[0].childNodes[0].nodeValue
         num_list.append(num_print)
         #lire l annee et le stocker dans une liste
         annee=notice.getElementsByTagName('annee')
         annee_print=annee[0].childNodes[0].nodeValue
         annee_list.append(annee_print)
         #lire l url et le stocker dans une liste
         url=notice.getElementsByTagName('url_pdf')
         url_print=url[0].childNodes[0].nodeValue
         if 'meteo' in url_print:
           url_print=url_print[url_print.index('meteo'):]
         elif 'Meteo' in url_print:
           url_print=url_print[url_print.index('Meteo'):]
         elif 'METEO' in url_print:
           url_print=url_print[url_print.index('METEO'):]
         else:
           print('There is a pb with url_pdf:',url_print)
         url_print=url_print.lower()
         url_print="https://lameteorologie.fr/issues/"+annee_print+"/"+num_print+"/"+url_print[:-4]
         url_print=url_print.replace(" ","%20")
         url_list.append(url_print)
         #lire les auteurs les stocker dans une liste de listes
         auteur=notice.getElementsByTagName('auteur')
         auteur_article_list=[]
         for iauteur in range(len(auteur)):
           auteur_article_list.append(auteur[iauteur].childNodes[0].nodeValue)
         auteur_list.append(auteur_article_list)
         #index nombre d articles trouves
         nb=nb+1

  #on trie par titre d'article 
  if selection != 'Débat':
    auteur_list=[x for y, x in sorted(zip(titre_list_sans_accents,auteur_list))]
    num_list   =[x for y, x in sorted(zip(titre_list_sans_accents,num_list))]
    annee_list =[x for y, x in sorted(zip(titre_list_sans_accents,annee_list))]
    url_list   =[x for y, x in sorted(zip(titre_list_sans_accents,url_list))]
    titre_list =[x for y, x in sorted(zip(titre_list_sans_accents,titre_list))]
  #on ecrit a l'ecran et dans un fichier html
  for t,a,u,n,an in zip(titre_list,auteur_list,url_list,num_list,annee_list): 
    print(t)
    fhtml.write("<A HREF="+u+">"+t+"</A><BR>"+'\n') 
    fxml.write("  <article>"+'\n') 
    fxml.write("    <titre>"+t+"</titre>"+'\n') 
    fxml.write("    <url>"+u+"</url>"+'\n') 
    fxml.write("    <annee>"+an+"</annee>"+'\n') 
    fxml.write("    <numero>"+n+"</numero>"+'\n') 
    for aa in a:
      print(aa)
      fhtml.write(aa+' ; ') 
      fxml.write("    <auteur>"+aa+"</auteur>"+'\n') 
    print(n)
    fhtml.write('<BR>Numéro  '+n+'  Année '+an+'<P>') 
    fxml.write('  </article>'+'\n') 

  fxml.write(' </rubrique>'+'\n')
fxml.write(' </articles_par_rubrique>'+'\n')

print(nb,' trouves')
