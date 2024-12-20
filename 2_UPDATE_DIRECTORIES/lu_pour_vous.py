# -*- coding: utf-8 -*-
import encodings
import sys
import glob
from xml.dom.minidom import parse

print(sys.stdout.encoding)

files=sorted(glob.glob("input/meteo*Sort.xml")+glob.glob('input/meteo_????_???_rvt.xml'))

selection1='Lu pour vous'
selection2='Vu pour vous'

f = open('output/lpv.html', 'w')
f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
f.write('<H1>Lu pour vous et Vu pour vous</H1><P>'+'\n')

fxml = open('output/repertoire_lpv.xml', 'w')
fxml.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
fxml.write('<lu_pour_vous>'+'\n')

nb=0

for file in files:
  print(file)
  dom = parse(file)
  notices=dom.getElementsByTagName('notice')
  for notice in notices: 
     rubrique=notice.getElementsByTagName('rubrique')
     rubrique_print=rubrique[0].childNodes[0].nodeValue
     if rubrique_print == selection1 or rubrique_print == selection2:
       titre=notice.getElementsByTagName('titre')
       titre_print=titre[0].childNodes[0].nodeValue
       titre_print=titre_print.replace(" & "," &amp; ")
       auteur=notice.getElementsByTagName('auteur')
       auteur_tmp=auteur[0].childNodes[0].nodeValue
       loc1=auteur_tmp.find(',')
       if loc1 != -1:
           nom   =auteur_tmp[0:loc1]
           prenom=auteur_tmp[loc1+1:]
           auteur_print=prenom+' '+nom
       else: 
           auteur_print=auteur_tmp
       num=notice.getElementsByTagName('numero')
       num_print=num[0].childNodes[0].nodeValue
       annee=notice.getElementsByTagName('annee')
       annee_print=annee[0].childNodes[0].nodeValue
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
       f.write("<A HREF="+url_print+">"+titre_print+"</A><BR>"+'\n') 
       if rubrique_print == selection1:
         f.write("Lu par "+auteur_print+"<BR>"+'\n') 
       if rubrique_print == selection2:
         f.write("Vu par "+auteur_print+"<BR>"+'\n') 
       f.write("numéro "+num_print+" - année "+annee_print+"<P>"+'\n') 
       fxml.write("<article>"+'\n')
       fxml.write("<titre>"+titre_print+"</titre>"+'\n')
       fxml.write("<url>"+url_print+"</url>"+'\n')
       fxml.write("<annee>"+annee_print+"</annee>"+'\n')
       fxml.write("<numero>"+num_print+"</numero>"+'\n')
       fxml.write("<auteur>"+auteur_print+"</auteur>"+'\n')
       fxml.write("</article>"+'\n')
       nb=nb+1

print(nb,' lpv trouves')
fxml.write('</lu_pour_vous>'+'\n')
