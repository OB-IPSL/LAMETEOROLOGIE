# -*- coding: utf-8 -*-
import sys
import glob
from xml.dom.minidom import parse
import encodings
import unicodedata

print(sys.stdout.encoding)

files=sorted(glob.glob("input/meteo*Sort.xml")+glob.glob('input/meteo_????_???_rvt.xml'))

#--HTML  output file
f = open('output/resume_climatique.html', 'w')
f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
f.write('<H1>Résumés climatiques mensuels</H1><P>'+'\n')

#--XML  output file
fxml = open('output/repertoire_resumes_climatiques.xml', 'w')
fxml.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
fxml.write('<resumes_climatiques>'+'\n')

nb=0

for file in files:
  print(file)
  dom = parse(file)
  notices=dom.getElementsByTagName('notice')
  for notice in notices: 
     rubrique=notice.getElementsByTagName('rubrique')
     rubrique_print=rubrique[0].childNodes[0].nodeValue
     #print rubrique_print
     num=notice.getElementsByTagName('numero')
     num_print=num[0].childNodes[0].nodeValue
     annee=notice.getElementsByTagName('annee')
     annee_print=annee[0].childNodes[0].nodeValue
     #
     if rubrique_print  == 'Résumé climatique' or rubrique_print  == 'Résumés climatiques': 
       titre=notice.getElementsByTagName('titre')
       titre_print=titre[0].childNodes[0].nodeValue
       #
       if titre_print[-4:].isdigit():
         annee_print=titre_print[-4:]   #--overwrite year of print with year of RC
       #
       url=notice.getElementsByTagName('url_pdf')
       url_print=url[0].childNodes[0].nodeValue
       #
       if 'meteo' in url_print:
         url_print=url_print[url_print.index('meteo'):]
       elif 'Meteo' in url_print:
         url_print=url_print[url_print.index('Meteo'):]
       elif 'METEO' in url_print:
         url_print=url_print[url_print.index('METEO'):]
       else:
         print('There is a pb with url_pdf:',url_print)
       #
       url_print=url_print.lower()
       url_print="https://lameteorologie.fr/issues/"+annee_print+"/"+num_print+"/"+url_print[:-4]
       #
       f.write("<A HREF="+url_print+">"+titre_print+"</A><BR>"+'\n') 
       #
       fxml.write('<resume>'+'\n')
       fxml.write('<titre>'+titre_print+'</titre>\n')
       fxml.write('<url>'+url_print+'</url>\n')
       fxml.write('<year>'+annee_print+'</year>\n')
       fxml.write('</resume>'+'\n')
       nb=nb+1

print(nb,' resumes climatiques trouves')
fxml.write('</resumes_climatiques>'+'\n')
