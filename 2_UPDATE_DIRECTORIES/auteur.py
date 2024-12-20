# -*- coding: utf-8 -*-
import encodings
import codecs
import sys
import glob
import unicodedata
import numpy
from xml.dom.minidom import parse

print(sys.stdout.encoding)

files=sorted(glob.glob("input/meteo*Sort.xml")+glob.glob('input/meteo_????_???_rvt.xml'))

#selections=['Echos','Lu pour vous','Vu pour vous','Agrométéorologie','AMMA','Applications','Biométéorologie','Campagne expérimentale','Changement climatique',"Chimie de l'atmosphère",'Climatologie','Débat','Dossier','Economie','Education','Environnement','Etudes de cas','Histoire','Hydrologie','Le temps des écrivains','Médias','Météo pour tous','Météorologie aéronautique','Météorologie dynamique','Météorologie spatiale','Météorologie théorique','Météorologie tropicale','Neige et glace','Nuages et aérosols','Observation','Océan et atmosphère','Océanographie','Optique atmosphérique','Paléoclimatologie','Phénomènes météorologiques','Physique atmosphérique','Planétologie','Prévision','Récit','Société','Terminologie']
selections=['Aérosols et nuages','Agrométéorologie','AMMA','Applications','Biométéorologie','Campagne expérimentale','Changement climatique',"Chimie de l'atmosphère",'Climatologie','Débat','Dossier','Economie','Education','Enseignement','Environnement','Etudes de cas','Histoire','Hydrologie','Interview','Médias','Météo pour tous','Météorologie aéronautique','Météorologie dynamique','Météorologie spatiale','Météorologie théorique','Météorologie tropicale','Neige et glace','Nuages et aérosols','Observation','Océan et atmosphère','Océanographie','Optique atmosphérique','Paléoclimatologie','Phénomènes météorologiques','Physique atmosphérique','Planétologie','Prévision','Récit','Société','Terminologie']

f = open('output/repertoire_auteurs_articles.html', 'w')
f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
f.write('<H1>Répértoire des auteurs</H1><P>'+'\n')
f.write('<table style="width:100%">')

g = open('output/repertoire_auteurs_articles_avec_url.html', 'w')
g.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
g.write('<H1>Répértoire des auteurs</H1><P>'+'\n')
g.write('<table style="width:100%">')

gxml = open('output/repertoire_auteurs.xml', 'w')
gxml.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
gxml.write('<repertoire_auteurs>'+'\n')

nb=0

auteur_list=[]
auteur_list_sans_accents=[]
num_list=[]
url_list=[]
#Boucle sur les fichiers
for file in files:
  print(file)
  dom = parse(file)
  notices=dom.getElementsByTagName('notice')
  for notice in notices: 
     #lire la rubrique
     rubrique=notice.getElementsByTagName('rubrique')
     rubrique_print=rubrique[0].childNodes[0].nodeValue
     #si on a detecte une des bonnes rubriques
     if rubrique_print in selections:
       #lire le numero et le stocker dans une liste
       num=notice.getElementsByTagName('numero')
       num_print=num[0].childNodes[0].nodeValue
       #lire l annee et le stocker dans une liste
       annee=notice.getElementsByTagName('annee')
       annee_print=annee[0].childNodes[0].nodeValue
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
       #lire les auteurs les stocker dans une liste
       auteur=notice.getElementsByTagName('auteur')
       for iauteur in range(len(auteur)):
         auteur_print=auteur[iauteur].childNodes[0].nodeValue
         auteur_print=auteur_print.strip(' ') #--strip leading and trailing spaces
         loc1=auteur_print.find(',')
         #MODIF
         if loc1 != -1 and auteur_print[0:6] != 'Benech' and auteur_print[0:5] != 'Stoll' and auteur_print[0:5] != 'David' and 0==1 : 
           nom   =auteur_print[0:loc1] 
           auteur_print_mod=nom+','
           prenom=auteur_print[loc1+1:] 
           prenom_list=prenom.split()
           for pre in prenom_list:
             loc2=pre.find('-')
             if loc2 != -1: 
               pre_court=pre[0]+'.-'+pre[loc2+1]+'.'
             else: 
               pre_court=pre[0]+'.'
             auteur_print_mod=auteur_print_mod+' '+pre_court
         else: 
           auteur_print_mod=auteur_print 
         auteur_list.append(auteur_print_mod)
         auteur_list_sans_accents.append(unicodedata.normalize('NFKD',auteur_print_mod.lower()).encode('ASCII', 'ignore'))
         num_list.append(num_print)
         url_list.append(url_print)
         #index nombre d auteurs trouves
         nb=nb+1

print(nb,' auteurs trouves')

#on trie par auteur 
#supprimer les doublons et reclasser par ordre alphabétique
auteur_unique=sorted(set(auteur_list_sans_accents))
#on boucle sur les auteurs
for iauteur in auteur_unique: 
  #on cherche les indices de cet auteur 
  ii= numpy.where(numpy.array(auteur_list_sans_accents) == iauteur)[0]
  aa= auteur_list[ii[0]]
  f.write('<tr><td>'+aa+'</td>') 
  g.write('<tr><td>'+aa+'</td>') 
  gxml.write('<auteur>\n')
  gxml.write('<nom>'+aa+'</nom>\n')
  num_list_auteur=[]
  url_list_auteur=[]
  for i in ii:
    num_list_auteur.append(num_list[i])
    url_list_auteur.append(url_list[i])

  #on garde les doublons avec les liens pour le fichier g
  g.write('<td>') 
  gxml.write('<numdetails>\n')
  for num,url in zip(num_list_auteur,url_list_auteur):
    gxml.write('<url>'+url+'</url>\n')
    if num == 'NS Histoire': 
      g.write('<A HREF='+url+'>'+'S'+'</A>')
      gxml.write('<num>S</num>\n')
    elif num == 'NS AMMA': 
      g.write('<A HREF='+url+'>'+'A'+'</A>')
      gxml.write('<num>A</num>\n')
    else: 
      g.write('<A HREF='+url+'>'+num+'</A>')
      gxml.write('<num>'+num+'</num>\n')
    if url != url_list_auteur[len(url_list_auteur)-1]:
      g.write(',')
  g.write('<P>\n')
  g.write('</td></tr>') 
  gxml.write('</numdetails>\n')
    
  #on enleve les doublons tout en conservant l'ordre pour le fichier f
  f.write('<td>') 
  num_sorted=[]
  for num in num_list_auteur:
    if num not in num_sorted: 
      num_sorted.append(num)
  #on boucle sur les numeros
  for num in num_sorted:
    #on ecrit dans un fichier html
    if num == 'NS Histoire': 
      f.write('S')
    elif num == 'NS AMMA': 
      f.write('A')
    else: 
      f.write(num)
    #une virgule si ce n'est pas le dernier numéro
    if num != num_sorted[len(num_sorted)-1]: 
      f.write(',')
  f.write('<P>\n')
  f.write('</td></tr>') 
  gxml.write('</auteur>\n')
gxml.write('</repertoire_auteurs>\n')
