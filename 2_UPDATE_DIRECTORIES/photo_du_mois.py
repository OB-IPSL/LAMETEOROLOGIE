# -*- coding: utf-8 -*-
import sys
import glob
from xml.dom.minidom import parse
import encodings
import unicodedata

print(sys.stdout.encoding)

files=sorted(glob.glob("input/meteo*Sort.xml")+glob.glob('input/meteo_????_???_rvt.xml'))

liste_mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]

f = open('output/photos_du_mois.html', 'w')
f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
f.write('<H1>Les photos du mois</H1><P>'+'\n')

nb=0

for file in files:
  print(file)
  dom = parse(file)
  notices=dom.getElementsByTagName('notice')
  for notice in notices: 
     rubrique=notice.getElementsByTagName('rubrique')
     rubrique_print=rubrique[0].childNodes[0].nodeValue
     #print rubrique_print
     if rubrique_print  in ['Les photos du mois','La photo du mois',"Vu de l'espace"] : 
       titre=notice.getElementsByTagName('titre')
       titre_print=titre[0].childNodes[0].nodeValue
       annee=notice.getElementsByTagName('annee')
       annee_print=annee[0].childNodes[0].nodeValue
       num=notice.getElementsByTagName('numero')
       num_print=num[0].childNodes[0].nodeValue
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
       mois_text='  '
       for mois in liste_mois:
         #moislower=mois.lower().encode('ASCII', 'ignore')
         #titrelower=titre_print.lower().encode('ASCII', 'ignore') 
         moislower=mois.lower()
         titrelower=titre_print.lower()
         if moislower in titrelower:
           mois_text=mois_text+mois+' '
       for year in range(1992,2020):
         if str(year) in titre_print: 
           if (int(num_print)-1)/4 + 1990 < year:
             mois_text=mois_text+str(year)+' '
       #f.write("<A HREF="+url_print+">"+titre_print+"</A><BR>"+'\n') 
       f.write("<A HREF="+url_print+">Photos du mois - numéro ")
       f.write(num_print+"</A>"+mois_text+"<BR>"+'\n') 
       nb=nb+1

print(nb,' photos du mois trouves')
