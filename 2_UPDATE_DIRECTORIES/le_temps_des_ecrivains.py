# -*- coding: utf-8 -*-
import encodings
import sys
import glob
from xml.dom.minidom import parse

print(sys.stdout.encoding)

files=sorted(glob.glob("input/meteo*Sort.xml")+glob.glob('input/meteo_????_???_rvt.xml'))

selection='Le temps des écrivains'

f = open('output/ltde.html', 'w')
f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
f.write('<H1>Le temps des écrivains</H1><P>'+'\n')

nb=0

for file in files:
  print(file)
  dom = parse(file)
  notices=dom.getElementsByTagName('notice')
  for notice in notices: 
     rubrique=notice.getElementsByTagName('rubrique')
     rubrique_print=rubrique[0].childNodes[0].nodeValue
     if rubrique_print == selection:
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
       f.write("<A HREF="+url_print+">"+titre_print+"</A><P>"+'\n') 
       nb=nb+1

print(nb,' trouves')
