# -*- coding: utf-8 -*-
#--modified on 31/01/2024 to cope with latest pyPDF2 
import sys, os.path, glob
from xml.dom.minidom import *
from xml.etree.ElementTree import Element,SubElement,Comment,tostring,register_namespace,QName
from PyPDF2 import PdfReader
import encodings
import unicodedata
import datetime
import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
from email.mime.image import MIMEImage
#from email.utils import make_msgid
#import mimetypes
from yagmail import SMTP

print(sys.stdout.encoding)

#--expecting inputs : number year
print("You are running",sys.argv[0])
if len(sys.argv)!=3:
  print("You are missing the arguments issue and year")
else:
  num=str(sys.argv[1])
  annee=str(sys.argv[2])
print("Dealing with issue",num)

#--location of data
dir="/data/oboucher/LAMETEO_PDF/num"+num+"/"

#--output files
file_rvt=dir+'meteo_'+annee+'_'+num+'_rvt.xml'
file_crossref=dir+'meteo_'+annee+'_'+num+'_crossref.xml'

#--detect month of issue
if int(num) % 4 == 0: mois="02" #--February issue
if int(num) % 4 == 1: mois="05" #--May issue
if int(num) % 4 == 2: mois="08" #--August issue
if int(num) % 4 == 3: mois="11" #--November issue

print("This is the issue from",mois,' ',annee)

nbindex=0

if int(num) % 4 == 0: #--February issue
  #--beginning for doi (4 digits) - needs to change with each new issue - starts at 0 in new year
  nbdoi=0
else: 
  #--read nbdoi
  f=open('nb_items_'+str(int(num)-1), "r")
  nbdoi=int(f.readlines()[0])
  f.close()

print("Issue doi items will start at ",nbdoi)

#--declare JATS namespace
jats_ns="http://www.ncbi.nlm.nih.gov/JATS1"
register_namespace("jats",jats_ns)

#--journal details
full_title="La Météorologie"
abbrev_title="Météorologie"
issn="0026-1181"
issn_online="2107-0830"

#--prepare email with table of content
message_html=""

#--------

now = datetime.datetime.now()
date=str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)

#--get a list of pdfs available for the issue
pdfs=glob.glob(dir+"/meteo_"+annee+"_"+num+"*.pdf")
pdfs=[x[x.index('meteo'):] for x in pdfs]

#--input file
files=[dir+'/meteo_'+annee+'_'+num+'.xml']

#--RVT
#--output file for RVT
root_rvt = Element("notices_simples",numero=num)

#--define cover element for rvt xml
nbindex=nbindex+1
element = Element("notice")
SubElement(element,"rubrique").text='Couverture'
SubElement(element,"annee").text=annee
SubElement(element,"mois").text=mois
SubElement(element,"numero").text=num
pdffile='meteo_'+annee+'_'+num+'_couv.pdf'
if not os.path.isfile(dir+'/'+pdffile): 
   print('HOUSTON we have a problem with',pdffile)
else: 
   SubElement(element,"url_pdf").text=pdffile
root_rvt.insert(nbindex,element)

#--CROSSREF
#--output file for crossref
dico={} ; dico['xmlns']="http://www.crossref.org/schema/4.4.2" 
dico['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance" 
dico['version']="4.4.2" ; dico['xsi:schemaLocation']="http://www.crossref.org/schema/4.4.2 http://www.crossref.org/schema/deposit/crossref4.4.2.xsd"
root_crossref = Element("doi_batch",dico)
#--header crossref file
head=Element("head")
SubElement(head,"doi_batch_id").text='lameteorologie_'+annee+'_'+num
SubElement(head,"timestamp").text=date
depositor=SubElement(head,"depositor")
SubElement(depositor,"depositor_name").text="Olivier Boucher"
##SubElement(depositor,"email_address").text="lameteorologie@meteoetclimat.fr"
SubElement(depositor,"email_address").text="olivier.boucher@ipsl.fr"
SubElement(head,"registrant").text="Météo et Climat"
root_crossref.insert(0,head)
#
body=Element("body")
journal=SubElement(body,"journal")
dico={} ; dico['language']="en"
#
journal_md=SubElement(journal,"journal_metadata",dico)
SubElement(journal_md,"full_title").text=full_title
SubElement(journal_md,"abbrev_title").text=abbrev_title
dico={} ; dico['media_type']="print"
SubElement(journal_md,"issn",dico).text=issn
#dico={} ; dico['media_type']="online"
#SubElement(journal_md,"issn",dico).text=issn_online
#dico={} ; dico['media_type']="electronic"
#
journal_issue=SubElement(journal,"journal_issue")
dico={} ; dico["media_type"]="online"
pub_date=SubElement(journal_issue,"publication_date",dico)
SubElement(pub_date,"month").text=mois
SubElement(pub_date,"year").text=annee
dico={} ; dico["media_type"]="print"
pub_date=SubElement(journal_issue,"publication_date",dico)
SubElement(pub_date,"year").text=annee
SubElement(journal_issue,"issue").text=num
#
#--page ranges beg and end
pages_range=[]
pages_beg=[]
pages_end=[]
#
for file in files:
  print(file)
  dom = parse(file)
  notices=dom.getElementsByTagName('notice') #--change to small caps after issue 125
  for notice in notices: 
    nbindex=nbindex+1
    nbdoi=nbdoi+1
    doc_titre_fr=notice.getElementsByTagName('DOC:DOC_TITRE')        #titre en français
    doc_titre_en=notice.getElementsByTagName('DOC:DOC_TITRE3')       #titre en anglais
    doc_auteur=notice.getElementsByTagName('DOC:DOC_AUTEUR')         #auteur
    doc_autmoral=notice.getElementsByTagName('DOC:DOC_AUTMORAL')     #auteur moral
    doc_type=notice.getElementsByTagName('DOC:DOC_TYPE')             #type
    doc_rubrique=notice.getElementsByTagName('DOC:MF_RUBRIQUE')      #rubrique
    doc_resume_fr=notice.getElementsByTagName('DOC:DOC_AB')          #résumé
    doc_resume_en=notice.getElementsByTagName('DOC:MF_AB_ANGLAIS')   #abstract
    doc_dee=notice.getElementsByTagName('DOC:DOC_DEE')               #mots clés
    doc_dc=notice.getElementsByTagName('DOC:DOC_DC')                 #mots clés
    doc_dl=notice.getElementsByTagName('DOC:DOC_DL')                 #mots clés
    doc_class2=notice.getElementsByTagName('DOC:DOC_CLASS2')         #mots clés
    doc_langue=notice.getElementsByTagName('DOC:DOC_LANGUE')         #langue du document
    doc_source=notice.getElementsByTagName('DOC:DOC_SOURCE')         #collation du document
    doc_page=notice.getElementsByTagName('DOC:MF_PAGE')              #pagination
    doc_comment=notice.getElementsByTagName('DOC:DOC_COMMENT')       #commentaire pour VdP
    doc_annee=notice.getElementsByTagName('DOC:DOC_AN_EDIT')         #année d'édition
    doc_revue=notice.getElementsByTagName('DOC:DOC_PER_TITRE')       #titre de la revue
    doc_issn=notice.getElementsByTagName('DOC:DOC_ISSN')             #ISSN
    doc_numero=notice.getElementsByTagName('DOC:DOC_PER_NUMERO')     #numéro de la revue
    doc_volume=notice.getElementsByTagName('DOC:DOC_PER_NUMVOL')     #numéro de volume ou série
    doc_per_dpar=notice.getElementsByTagName('DOC:DOC_PER_DPAR')     #date de parution
    doc_per_tpar=notice.getElementsByTagName('DOC:DOC_PER_PARUTION') #date de parution textuelle
    #--start notice
    element = Element("notice")
    #--rubrique
    rubrique_print=doc_rubrique[0].childNodes[0].nodeValue
    #--rubriques habituelles
    if rubrique_print=='LA VIE DE METEO ET CLIMAT':  rubrique_print='La vie de Météo et Climat'
    if rubrique_print=='RESUMES CLIMATIQUES':        rubrique_print='Résumés climatiques'
    if rubrique_print=='RESUME CLIMATIQUE':          rubrique_print='Résumés climatiques'
    if rubrique_print=='LES PHOTOS DU MOIS':         rubrique_print='Les photos du mois'
    if rubrique_print=='ECHOS':                      rubrique_print='Echos'
    if rubrique_print=='EDITORIAL':                  rubrique_print='Editorial'
    if rubrique_print=='LU POUR VOUS':               rubrique_print='Lu pour vous'
    if rubrique_print=='LA PHOTO DU TRIMESTRE':      rubrique_print='La photo du trimestre'
    if rubrique_print=='SAISON CYCLONIQUE':          rubrique_print='Saison cyclonique'
    if rubrique_print=='VIENT DE PARAITRE':          rubrique_print='Vient de paraître'
    if rubrique_print=='DEBAT':                      rubrique_print='Débat'
    if rubrique_print=='DOSSIER':                    rubrique_print='Dossier'
    if rubrique_print=='INTERVIEW':                  rubrique_print='Interview'
    if rubrique_print=='LA VIE DES LABOS':           rubrique_print='La vie des labos'
    if rubrique_print=='LE TEMPS DES ECRIVAINS':     rubrique_print='Le temps des écrivains'
    #--articles
    if rubrique_print=='AGROMETEOROLOGIE':           rubrique_print='Agrométéorologie'
    if rubrique_print=='APPLICATIONS':               rubrique_print='Applications'
    if rubrique_print=='BIOMETEOROLOGIE':            rubrique_print='Biométérologie'
    if rubrique_print=='CAMPAGNE EXPERIMENTALE':     rubrique_print='Campagne expérimentale'
    if rubrique_print=='CHANGEMENT CLIMATIQUE':      rubrique_print='Changement climatique'
    if rubrique_print=='CHIMIE DE L ATMOSPHERE':     rubrique_print="Chimie de l'atmosphère"
    if rubrique_print=="CHIMIE DE L'ATMOSPHERE":     rubrique_print="Chimie de l'atmosphère"
    if rubrique_print=='CLIMATOLOGIE':               rubrique_print='Climatologie'
    if rubrique_print=='ECOSYSTEMES':                rubrique_print='Ecosystèmes'
    if rubrique_print=='EDUCATION':                  rubrique_print='Education'
    if rubrique_print=='ENSEIGNEMENT':               rubrique_print='Enseignement'
    if rubrique_print=='ENVIRONNEMENT':              rubrique_print='Environnement'
    if rubrique_print=='ETUDE DE CAS':               rubrique_print='Etude de cas'
    if rubrique_print=='HISTOIRE':                   rubrique_print='Histoire'
    if rubrique_print=='HYDROLOGIE':                 rubrique_print='Hydrologie'
    if rubrique_print=='INTRODUCTION':               rubrique_print='Introduction'
    if rubrique_print=='MEDIAS':                     rubrique_print='Médias'
    if rubrique_print=='METEO POUR TOUS':            rubrique_print='Météo pour tous'
    if rubrique_print=='METEOROLOGIE AERONAUTIQUE':  rubrique_print='Météorologie aéronautique'
    if rubrique_print=='METEOROLOGIE DYNAMIQUE':     rubrique_print='Météorologie dynamique'
    if rubrique_print=='METEOROLOGIE SPATIALE':      rubrique_print='Météorologie spatiale'
    if rubrique_print=='METEOROLOGIE THEORIQUE':     rubrique_print='Météorologie théorique'
    if rubrique_print=='METEOROLOGIE TROPICALE':     rubrique_print='Météorologie tropicale'
    if rubrique_print=='NEIGE ET GLACE':             rubrique_print='Neige et glace'
    if rubrique_print=='NUAGES ET AEROSOLS':         rubrique_print='Nuages et aérosols'
    if rubrique_print=='OBSERVATION':                rubrique_print='Observation'
    if rubrique_print=='OCEAN ET ATMOSPHERE':        rubrique_print='Océan et atmosphère'
    if rubrique_print=='OCEANOGRAPHIE':              rubrique_print='Océanographie'
    if rubrique_print=='OPTIQUE ATMOSPHERIQUE':      rubrique_print='Optique atmosphérique'
    if rubrique_print=='PALEOCLIMATOLOGIE':          rubrique_print='Paléoclimatologie'
    if rubrique_print=='PHENOMENES METEOROLOGIQUES': rubrique_print='Phénomènes météorologiques'
    if rubrique_print=='PHYSIQUE ATMOSPHERIQUE':     rubrique_print='Physique atmosphérique'
    if rubrique_print=='PLANETOLOGIE':               rubrique_print='Planétologie'
    if rubrique_print=='PREVISION':                  rubrique_print='Prévision'
    if rubrique_print=='RECIT':                      rubrique_print='Récit'
    if rubrique_print=='RETOUR SUR...':              rubrique_print='Retour sur...'
    if rubrique_print=='RETOUR SUR':                 rubrique_print='Retour sur...'
    if rubrique_print=='SOCIETE':                    rubrique_print='Société'
    if rubrique_print=='TERMINOLOGIE':               rubrique_print='Terminologie'
    #--RVT
    #--define element for RVT xml
    SubElement(element,"rubrique").text=rubrique_print
    #--titre
    titre_print=doc_titre_fr[0].childNodes[0].nodeValue
    SubElement(element,"titre").text=titre_print
    #--titre english
    if len(doc_titre_en)>0: 
       titre_en_print=doc_titre_en[0].childNodes[0].nodeValue
       SubElement(element,"titre_en").text=titre_en_print
    #--auteur
    for auteur in doc_auteur:
       auteur_print=auteur.childNodes[0].nodeValue
       SubElement(element,"auteur").text=auteur_print
    if len(doc_auteur)==0: 
       for auteur in doc_autmoral:
          auteur_print=auteur.childNodes[0].nodeValue
          SubElement(element,"auteur").text=auteur_print
    #--annee
    annee_print=doc_annee[0].childNodes[0].nodeValue
    SubElement(element,"annee").text=annee_print
    #--numero
    numero_print=doc_numero[0].childNodes[0].nodeValue
    SubElement(element,"numero").text=numero_print
    if num!=numero_print: print('PB num !=numero_print',num, numero_print)
    #--pages
    page_range=doc_page[0].childNodes[0].nodeValue
    if page_range[0:3]==u'p. ': page_range=page_range[3:]
    if page_range[0:3]==u'P. ': page_range=page_range[3:]
    if page_range[0:2]==u'p.':  page_range=page_range[2:]
    if page_range[0:2]==u'P.':  page_range=page_range[2:]
    SubElement(element,"pages").text=page_range
    #--add page ranges
    pages_range.append(page_range)
    #--compute page beg and page end
    if 'S' not in page_range: #--normal pages
      if '-' not in page_range:
         nbpagefromxml=1
         page_beg=page_range.zfill(3)
         page_end=page_range.zfill(3)
      else:
         x=page_range
         page_beg=x[:x.index('-')].zfill(3)
         page_end=x[x.index('-')+1:].zfill(3)
    else:                     #--supplementary pages 
      if '-' not in page_range:
         nbpagefromxml=1
         page_beg=page_range
         page_end=page_range
      else:
         x=page_range
         page_beg=x[:x.index('-')]
         page_end=x[x.index('-')+1:]
    print(page_range,page_beg,page_end)
    #--doi
    doi_article="10.37053/lameteorologie-"+annee+"-"+str(nbdoi).zfill(4)
    SubElement(element,"doi").text=doi_article
    #--construct pdf file
    if page_beg.isdigit():
      pdffile='meteo_'+annee+'_'+num+'_'+str(int(page_beg))+'.pdf'
    else: #--Sx type of pages
      pdffile='meteo_'+annee+'_'+num+'_'+page_beg.lstrip('0')+'.pdf'
    #--find pdf file
    if not os.path.isfile(dir+'/'+pdffile): 
        print('HOUSTON we have a problem with',pdffile)
    else: 
        SubElement(element,"url_pdf").text=pdffile
    #--check number of pages in pdf
    #nbpagefrompdf=PdfReader(open(dir+'/'+pdffile, "rb")).getNumPages()
    nbpagefrompdf=len(PdfReader(open(dir+'/'+pdffile, "rb")).pages)
    #--compute number of pages
    if page_beg.isdigit(): 
      nbpagefromxml=int(page_end)-int(page_beg)+1
    else: 
      nbpagefromxml=int(page_end.lstrip('0').lstrip('S'))-int(page_beg.lstrip('0').lstrip('S'))+1
    #--test consistency in page ranges
    if nbpagefromxml != nbpagefrompdf:
       print ('inconsistency in number of pages in xml & pdf', page_range, nbpagefromxml, nbpagefrompdf)
    #--store page beg and end
    pages_beg.append(page_beg)
    pages_end.append(page_end)
    #--citation
    citation_print=""
    #--citation on ajoute les auteurs
    if len(doc_auteur) > 0:                  #--normal authors
       for auteur in doc_auteur:
          auteur_print=auteur.childNodes[0].nodeValue
          citation_print=citation_print+auteur_print+' ; '
       citation_print=citation_print[:-3]+'. ' #--remove last ;
    else:                                    #--moral authors
       for auteur in doc_autmoral:
         auteur_print=auteur.childNodes[0].nodeValue
         citation_print=citation_print+auteur_print+' ; '
       if len(doc_autmoral) > 0: citation_print=citation_print[:-3]+'. ' #--remove last ;
    #--citation on ajoute la rubrique si résumé
    if rubrique_print=='Résumés climatiques': citation_print=citation_print+'Résumé climatique, '
    #--citation on ajoute le titre
    citation_print=citation_print+titre_print+'. La Météorologie, '
    citation_print=citation_print+numero_print+', '+page_range+', '+annee_print+'.'
    SubElement(element,"citation").text=citation_print
    #--publication date for open access
    pub_date=SubElement(element,"pub_date")
    SubElement(pub_date,"jour").text="01"
    SubElement(pub_date,"mois").text=mois
    SubElement(pub_date,"annee").text=annee
    #--open access
    if rubrique_print in ['Résumé climatique','Résumés climatiques','Résumés climatiques (ancienne formule)',\
                          'Echos','Échos','La vie de Météo et Climat','Introduction',\
                          'La photo du trimestre','Les photos du mois','Saison cyclonique','Vient de paraître', \
                          'La vie des labos', 'Lu pour vous', 'Débat', 'Interview', 'Le temps des écrivains',\
                          "Vu de l'espace",'Retour sur...']:
        open_access_print='2'
    else: 
        open_access_print='0'
    ##open_access_print='0'
    SubElement(element,"open_access").text=open_access_print
    #--type 
    if rubrique_print in ['Résumé climatique','Résumés climatiques','Résumés climatiques (ancienne formule)',\
                          'Echos','Échos','Éditorial','Editorial','La vie de Météo et Climat','Introduction',\
                          'La photo du trimestre','Les photos du mois','Saison cyclonique','Vient de paraître', \
                          'La vie des labos', 'Lu pour vous', 'Débat', 'Dossier', 'Interview', 'Le temps des écrivains',\
                          "Vu de l'espace",'Retour sur...']:
      SubElement(element,"type").text='Rubrique régulière dans publication en série'
      article=False
    else:
      SubElement(element,"type").text='Article'
      article=True
    #--motscles
    doc_motscles_print=''
    ##for item in doc_class2 + doc_dee + doc_dc + doc_dl:
    for item in doc_dee + doc_dc + doc_dl:
       doc_motscles_print=doc_motscles_print+item.childNodes[0].nodeValue+', '
    if len(doc_motscles_print) > 0:
       doc_motscles_print=doc_motscles_print[:-2]   #--remove last comma
       SubElement(element,"mots_cles").text=doc_motscles_print
    #--description pour le VdP
    if len(doc_comment) > 0:
       doc_comment_print=doc_comment[0].childNodes[0].nodeValue
       SubElement(element,"description").text=doc_comment_print
    #--resume
    if len(doc_resume_fr) > 0:
       doc_resume_fr_print=doc_resume_fr[0].childNodes[0].nodeValue
       SubElement(element,"resume_fr").text=doc_resume_fr_print
    #--resume
    if len(doc_resume_en) > 0:
       doc_resume_en_print=doc_resume_en[0].childNodes[0].nodeValue
       SubElement(element,"resume_en").text=doc_resume_en_print
    #--insert element in rvt xml
    root_rvt.insert(nbindex,element)
    #--end xml for RVT
    #
    #--CROSSREF
    #--prepare element article in crossref xml
    dico={} ; dico["publication_type"]="full_text" ; dico["language"]="fr"
    journal_article=SubElement(journal,"journal_article",dico)
    titles=SubElement(journal_article,"titles")
    SubElement(titles,"title").text=titre_print
    if len(doc_auteur) + len(doc_autmoral) >0: 
      contributors=SubElement(journal_article,"contributors")
      if len(doc_auteur) > 0:                                      #--normal authors
         dico={} ; dico["contributor_role"]="author" ; dico["sequence"]="first"
         person_name=SubElement(contributors,"person_name",dico)
         auteur=doc_auteur[0]
         auteur_print=auteur.childNodes[0].nodeValue
         SubElement(person_name,"given_name").text=auteur_print[auteur_print.index(',')+2:]
         SubElement(person_name,"surname").text=auteur_print[0:auteur_print.index(',')]
         for auteur in doc_auteur[1:]:
            auteur_print=auteur.childNodes[0].nodeValue
            dico={} ; dico["contributor_role"]="author" ; dico["sequence"]="additional"
            person_name=SubElement(contributors,"person_name",dico)
            SubElement(person_name,"given_name").text=auteur_print[auteur_print.index(',')+2:]
            SubElement(person_name,"surname").text=auteur_print[0:auteur_print.index(',')]
      else:          #--moral authors
         dico={} ; dico["contributor_role"]="author" ; dico["sequence"]="first"
         auteur=doc_autmoral[0]
         auteur_print=auteur.childNodes[0].nodeValue
         SubElement(contributors,"organization",dico).text=auteur_print
    #--abstract
    if len(doc_resume_fr) > 0 or len(doc_resume_en) > 0 :
      jats_abstract=SubElement(journal_article,QName(jats_ns,"abstract"))
    if len(doc_resume_fr) > 0 :
      SubElement(jats_abstract,QName(jats_ns,"p")).text=doc_resume_fr_print
    if len(doc_resume_en) > 0 :
      SubElement(jats_abstract,QName(jats_ns,"p")).text=doc_resume_en_print
    #
    dico={} ; dico["media_type"]="online"
    publication_date=SubElement(journal_article,"publication_date", dico)
    SubElement(publication_date,"month").text=mois
    SubElement(publication_date,"year").text=annee
    dico={} ; dico["media_type"]="print"
    publication_date=SubElement(journal_article,"publication_date", dico) #--only last one applies - need to close ?
    SubElement(publication_date,"year").text=annee
    pages=SubElement(journal_article,"pages")
    SubElement(pages,"first_page").text=page_beg
    doi_data=SubElement(journal_article,"doi_data")
    SubElement(doi_data,"doi").text=doi_article
    link_article="https://lameteorologie.fr/issues/"+annee+"/"+str(num)+"/"+pdffile[:-4]
    SubElement(doi_data,"resource").text=link_article
    #--end xml for CROSSREF
    #--message html for email 
    if article: 
      message_html=message_html + '<b>' + rubrique_print + ' : </b> ' + '<a href="'+link_article+'">'+titre_print+'</a><br>\n'
    else:
      message_html=message_html + '<b>' + rubrique_print + ' : </b> ' + '<a href="'+link_article+'">'+titre_print+'</a><br>\n'
##page_beg + '-' + page_end + 
  #--insert PDF element in rvt xml
  #nbindex=nbindex+1
  #element = Element("notice")
  #SubElement(element,"type").text='Numéro complet'
  #SubElement(element,"rubrique").text='Numéro complet'
  #SubElement(element,"annee").text=annee
  #SubElement(element,"mois").text=mois
  #SubElement(element,"numero").text=num
  #SubElement(element,"pages").text='999'
  #SubElement(element,"open_access").text='2'
  #pdffile='MTO_'+num+'_optimise.pdf'
  #if not os.path.isfile(dir+'/'+pdffile): 
  #   print('HOUSTON we have a problem with',pdffile)
  #else: 
  #   SubElement(element,"url_pdf").text=pdffile
  #root_rvt.insert(nbindex,element)

#--finalize crossref xml with body
root_crossref.insert(1,body)
#--finalise message email 
image_file='/data/oboucher/LAMETEO_PDF/num'+num+'/meteo_'+annee+'_'+num+'_couv_medium.png'
#image_cid=make_msgid(domain='https://lameteorologie.fr/issues/'+annee+'/'+num)
message_html='<a href="https://lameteorologie.fr/issues/'+annee+'/'+num+'"> <img src="cid:image_cid"> </a> <br> \n' + \
             "Chères lectrices, Chers lecteurs,<br>\n" \
             "Le numéro "+num+" de <I>La Météorologie</I> est disponible en ligne.\n" + \
             "Vous trouverez le sommaire ci-dessous avec toutes les rubriques habituelles et les articles du trimestre.\n" + \
             "L'accès est possible par login / mot de passe pour les abonnés de Météo et Climat ou par filtrage\n" + \
             "d'adresse IP pour les abonnés institutionnels.<br>\n" + \
             "Cette revue est aussi celle de nos lecteurs, n'hésitez pas à nous proposer des brèves et des articles.<br>\n" +\
             "Bonne lecture,<br>\n" + \
             "Serge Soula, rédacteur en chef, et le comité de rédaction<br><br>\n" + \
             "Au sommaire de ce numéro<br>" + message_html
#--embed into html
message_html="""<html> <head></head> <body> <p>"""+message_html+"""</p> </body> </html>"""
#--prepare and write RVThost xml
file_object = open(file_rvt, "w")
nbchar=file_object.write(parseString(tostring(root_rvt,encoding='utf-8')).toprettyxml(indent=" "))
file_object.close()
#--prepare and write CrossRef xml
file_object = open(file_crossref, "w")
nbchar=file_object.write(parseString(tostring(root_crossref,encoding='utf-8')).toprettyxml(indent=" "))
file_object.close()

#--send email 
check_email='olivier.boucher.1@gmail.com'
gmail_user='ob.consulting.jo@gmail.com'
#--old way to send email
#s = smtplib.SMTP(host='smtp.gmail.com', port=587)
#s.starttls()
#s.login(gmail_user,gmail_passwd)
#msg = MIMEMultipart()
#msg['From']=gmail_user
#msg['To']=check_email
#msg['Subject']='Publication du n° '+num+" de La Météorologie"
#msg.attach(MIMEText(message_html, 'html'))
#--Open image 
#fp = open(image_file, 'rb')
#msgImage = MIMEImage(fp.read())
#fp.close()
#--Define the image's ID as referenced above
#msgImage.add_header('Content-ID', '<image_cid>')
#--Attach the image
#msg.attach(msgImage)
#print(message_html)
#s.send_message(msg)
#--new way to send email
#conn = SMTP(gmail_user, oauth2_file="/home/oboucher/LAMETEO/client_secret.json")
#conn.send(to=check_email,subject="Publication du n° "+num+" de La Météorologie",contents=[image_file,message_html])
f=open('email_a_envoyer.html','w')
f.write(message_html)
f.close()

#--print nb
f=open('nb_items_'+num, "w")
f.write(str(nbdoi))
f.close()
