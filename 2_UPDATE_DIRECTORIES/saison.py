# -*- coding: utf-8 -*-
#from PyPDF2 import PdfFileWriter, PdfFileReader
import csv, glob, os, sys, encodings, unicodedata
from distutils.util import strtobool
from xml.dom.minidom import parse
#
yrbeg=2007
yrend=2023
#
dict={}
#
#--Met Mar 
#
#--files
pathin='/homedata/oboucher/METMAR/INPUT/'
pathout='/homedata/oboucher/METMAR/SAISONS/'
#
#--HTML output file
fhtml = open('output/saison_cyclonique_combine.html', 'w')
fhtml.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
fhtml.write('<H1>Répértoire des saisons cycloniques de <I>Met Mar</I> et <I>La Météorologie</I></H1><P>'+'\n')
#
#--XML output file
fxml = open('output/repertoire_saisons_cycloniques.xml', 'w')
fxml.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
fxml.write('<saisons_cycloniques>'+'\n')
#
keybasin={}
keybasin['atlantique']='ATL'
keybasin['pacifique nord-est']='PNE'
keybasin['pacifique nord-ouest']='PNO'
keybasin['pacifique sud']='PS'
keybasin['indien nord']='IN'
keybasin['indien sud']='IS'
#
#--initialize lists
Titre_list=[]
Yr_list=[]
Basin_list=[]
Numero_list=[]
PageBeg_list=[]
PageEnd_list=[]
#
#--load MF library infos
url_metmar={}
filein="input/URL_directe_MetMar.csv"
reader0 = csv.reader(open(filein, "r",encoding='ISO-8859-1'), delimiter=";")
for col in reader0:
  if col[0]=='Met Mar':
    url_metmar[col[2].zfill(3)]=col[6]
    print(col[2],col[6])
#
#--load JPJ infos
filein="input/Tab-Saison-Cyclonique-20160715.csv"
reader0 = csv.reader(open(filein, "r", encoding='ISO-8859-1'), delimiter=";")
for col in reader0: 
  if col[0][0:3] == 'Art' and col[1][0:3] == 'Num':  #--article non supprimé
      print(col[0], col[1], col[2], col[3], col[4], col[5], col[6], col[7])
      Titre=col[2].lower()  #--go lower case
      Titre=Titre[0].upper()+Titre[1:]
      Titre=Titre.replace("É","é")
      Titre=Titre.replace("È","è")
      Titre=Titre.replace("Ç","ç")
      Titre=Titre.replace('"reva"','"Reva"')
      Titre=Titre.replace("ocean","océan")
      Titre=Titre.replace(" tres "," très ")
      Titre=Titre.replace("phenomene","phénomène")
      Titre=Titre.replace("tempete","tempête")
      Titre=Titre.replace("tahiti","Tahiti")
      Titre=Titre.replace("arabie","Arabie")
      Titre=Titre.replace("bengale","Bengale")
      Titre=Titre.replace("madagascar","Madagascar")
      Titre=Titre.replace("atlantique","Atlantique")
      Titre=Titre.replace("queensland","Queensland")
      Titre=Titre.replace("pacifique","Pacifique")
      Titre=Titre.replace("polynesie","Polynésie")
      Titre=Titre.replace("polynésie","Polynésie")
      Titre=Titre.replace("indien","Indien")
      Titre=Titre.replace("nouvelle-calédonie","Nouvelle-Calédonie")
      Titre=Titre.replace("hong-kong","Hong-Kong")
      Titre=Titre.replace("gamède","Gamède")
      Titre=Titre.replace("la réunion","La Réunion")
      Titre=Titre.replace("la nina","la Niña")
      Titre=Titre.replace("el nino","el Niño")
      Titre=Titre.replace("a dominante","à dominante")
      Titre=Titre.replace("activite","activité")
      Titre=Titre.replace("une annee","une année")
      loc=Titre.find(" - ")
      if loc != -1: 
         Titre=Titre[:loc+3]+Titre[loc+3].upper()+Titre[loc+4:]
      Titre_list.append(Titre)
      Numero_list.append(col[1][4:7])
      pagerange=col[4]
      ind=pagerange.index('-')
      PageBeg_list.append(int(pagerange[:ind])+int(col[5]))
      PageEnd_list.append(int(pagerange[ind+1:])+int(col[5]))
      Yr_list.append(col[6])
      Basin_list.append(col[7])
#
dico={}
for num in range(1,218): 
  dico[str(num).zfill(3)]=0
#
for num,Titre,PageBeg,PageEnd,Yr,Basin in zip(Numero_list,Titre_list,PageBeg_list,PageEnd_list,Yr_list,Basin_list): 
  #
  print(num, Titre, PageBeg, PageEnd, Yr, Basin)
  #
  dico[num]=dico[num]+1
  # 
  metmar='MetMar'+num+'reduit.pdf'
  print('\n'+'dealing with file ', metmar)
  #
  #--define a reader
  #reader=PdfFileReader(pathin+metmar)
  #
  namefileout='saison_cyclonique_'+num+'_'+str(dico[num]).zfill(1)+'.pdf'
  #
  if int(num) < 198:
    #
    #--define a writer
    #writer=PdfFileWriter()
    #fileout=open(pathout+namefileout,'wb')
    #
    #--write pages to PDF
    #print('ART=', num, Titre, 'extract for pages ', PageBeg, PageEnd)
    #for page in range(PageBeg, PageEnd+1): 
    #   writer.addPage(reader.getPage(page))
    #print('Writer written')
    #     
    #--write file
    #writer.write(fileout)
    #fileout.close()
 
    #--updating html file
    fhtml.write("<A HREF=SAISONS/"+namefileout+">"+Titre+"</A><BR>"+'\n')
  #
  else:
    fhtml.write("<A HREF=SAISONS/"+namefileout+">"+Titre+"</A><BR>"+'\n')
  #
  #--ranking by basin
  print(Titre.lower())
  #
  if int(num) < 198: 
      Page=PageBeg+1
  else:
      Page=PageBeg
  #
  if int(Yr) not in dict.keys(): 
      dict[int(Yr)]={}
  #
  if Basin not in dict[int(Yr)].keys(): 
      dict[int(Yr)][Basin]={}
  else: 
      print(Yr, Basin, 'existe deja')
  dict[int(Yr)][Basin]['titre']=Titre
  dict[int(Yr)][Basin]['url']=url_metmar[num]+'#page='+str(Page)
  dict[int(Yr)][Basin]['revue']='metmar'
#
#---La Meteorologie

files=sorted(glob.glob("input/meteo*Sort.xml")+glob.glob('input/meteo_????_???_rvt.xml'))

#--HTML output file
#fhtml.write("<A HREF=http://documents.irevues.inist.fr/bitstream/handle/2042/17794/meteo_2008_61_75.pdf>Introduction</A><BR>"+'\n') 

nb=0

for file in files:
  print(file)
  dom = parse(file)
  notices=dom.getElementsByTagName('notice')
  for notice in notices: 
     rubrique=notice.getElementsByTagName('rubrique')
     rubrique_print=rubrique[0].childNodes[0].nodeValue
     if rubrique_print == 'Saison cyclonique': 
       #lire le numero et le stocker dans une liste
       num=notice.getElementsByTagName('numero')
       num_print=num[0].childNodes[0].nodeValue
       #lire l annee et le stocker dans une liste
       annee=notice.getElementsByTagName('annee')
       annee_print=annee[0].childNodes[0].nodeValue
       #lire le titre
       titre=notice.getElementsByTagName('titre')
       titre_print=titre[0].childNodes[0].nodeValue
       #lire le url_pdf
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
       fhtml.write("<A HREF="+url_print+">"+titre_print+"</A><BR>"+'\n') 
       nb=nb+1
       #
       #--ranking by basin
       for yr in range(yrbeg,yrend+1):
         yrm1=yr-1
         if yr not in dict.keys(): dict[yr]={}
         if str(yr) in titre_print and str(yrm1) not in titre_print[:-4]: 
           for basin in ['atlantique','pacifique nord-est','pacifique nord-ouest',\
                         'pacifique sud','indien nord','indien sud']: 
              if basin in titre_print.lower():
                dict[yr][keybasin[basin]]={}
                dict[yr][keybasin[basin]]['titre']=titre_print
                dict[yr][keybasin[basin]]['url']=url_print
                dict[yr][keybasin[basin]]['revue']='lameteorologie'
                dict[yr][keybasin[basin]]['titre']=titre_print

print(nb,' saisons cycloniques trouvés dans La Météorologie')
fhtml.close()
#
#--HTML output file as a Table
fhtml = open('output/saison_cyclonique_table_v1.html', 'w')
fhtml.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'+'\n')
fhtml.write('<H1>Répértoire des saisons cycloniques de <I>Met Mar</I> et <I>La Météorologie</I></H1><P>'+'\n')
fhtml.write('<TABLE border="1">'+'\n')
fhtml.write('<TR><TH width="10%">Année</TH><TH width="15%">Atlantique nord</TH><TH width="15%">Pacifique nord</TH>\
                                           <TH width="15%">Pacifique sud</TH>  <TH width="15%">Indien nord</TH>\
                                           <TH width="15%">Indien sud</TH></TR>'+'\n')
#
for yr in range(min(dict.keys()),max(dict.keys())+1):
    #--adding missing entries
    if yr not in dict.keys(): 
       dict[yr]={}
    fhtml.write('<TR><TH>'+str(yr)+'</TH>'+'\n')
    #---atlantique
    fhtml.write('<TD align="center">')
    for kbasin in ['ATL','ATL1','ATL2']:
      if kbasin in dict[yr].keys(): 
         fhtml.write('<A HREF='+dict[yr][kbasin]['url']+'>'+kbasin+'</A> ')
    fhtml.write('</TD>'+'\n')
    #---pacifique nord
    fhtml.write('<TD align="center">')
    for kbasin in ['PN','PNO','PNC','PNE','PNOC','PNEC']:
      if kbasin in dict[yr].keys(): 
         fhtml.write('<A HREF='+dict[yr][kbasin]['url']+'>'+kbasin+'</A> ')
    fhtml.write('</TD>'+'\n')
    #---pacifique sud
    fhtml.write('<TD align="center">')
    for kbasin in ['PS','PS1','PS2','PS3','PSE','PSO']:
      if kbasin in dict[yr].keys(): 
         fhtml.write('<A HREF='+dict[yr][kbasin]['url']+'>'+kbasin+'</A> ')
    fhtml.write('</TD>'+'\n')
    #--indien nord
    fhtml.write('<TD align="center">')
    for kbasin in ['IN','INE','INO']:
      if kbasin in dict[yr].keys(): 
         fhtml.write('<A HREF='+dict[yr][kbasin]['url']+'>'+kbasin+'</A> ')
    fhtml.write('</TD>'+'\n')
    #--indien sud
    fhtml.write('<TD align="center">')
    for kbasin in ['IS','IS1','IS2','ISE','ISO','ISO1','ISO2']:
      if kbasin in dict[yr].keys(): 
         fhtml.write('<A HREF='+dict[yr][kbasin]['url']+'>'+kbasin+'</A> ')
    fhtml.write('</TD>'+'\n')
    #--
    fhtml.write('</TR>'+'\n')
    #
for yr in dict.keys():
   fxml.write('<Year id="'+str(yr)+'">\n')
   for kbasin in ['ATL','ATL1','ATL2','PN','PNO','PNC','PNE','PNOC','PNEC','PS','PS1','PS2','PS3','PSE','PSO',\
                    'IN','INE','INO','IS','IS1','IS2','ISE','ISO','ISO1','ISO2']:
      if kbasin in dict[yr].keys():
        fxml.write('<saison>\n')
        fxml.write('<annee>'+str(yr)+'</annee>\n')
        fxml.write('<bassin>'+kbasin+'</bassin>\n')
        fxml.write('<revue>'+dict[yr][kbasin]['revue']+'</revue>\n')
        fxml.write('<titre>'+dict[yr][kbasin]['titre']+'</titre>\n')
        fxml.write('<url>'+dict[yr][kbasin]['url']+'</url>\n')
        fxml.write('</saison>'+'\n')
   fxml.write('</Year>\n')
#
#--fermer HTML table
fhtml.write('</TABLE>')
fhtml.close()
#
#--fermer XML file 
fxml.write('</saisons_cycloniques>\n')
fxml.close()
fhtml.close()
#
