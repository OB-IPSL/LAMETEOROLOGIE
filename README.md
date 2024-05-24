# LAMETEOROLOGIE
------------------

PROCEDURE POUR METTRE EN LIGNE UN NOUVEAU NUMERO

créer le répertoire /data/oboucher/LAMETEO_PDF/numXXX
réceptionner fichier de MF dans /data/oboucher/LAMETEO_PDF/numXXX
le dezipper
garder une copie du xml original de MF
enlever les majuscules dans le xml de MF, en particulier sur les noms de rubrique 
enlever les "leading zeros" sur les numéros de page
enlever les retour chariot dans titre / rubrique / citation s'il y en a
traiter les PDF manuellement s'il le faut 
mettre à jour le client_server.json à partir de OVH
lancer le script process_newissue.sh numero année pageRM
modifier les xml si besoin en particulier si deux Echos sur meme page (ajouter b)
positionner manuellement les articles en libre accès avec open_access = 0 dans le xml de rvt
vérifier la numérotation des doi
positionner manuellement les éventuels supplements 
<supplement>
   <fichier>meteo_2018_101_30_supp1.pdf</fichier>
</supplement>
aller dans ../crossref et soumettre le xml à crossref en test puis en vrai
refaire le zip manuellement
uploader une archive zip sur le site 

copier les .xml dans notices/input (fait par le script process_newissue.sh)
update l'année dans saison.py si besoin
générer les répertoires avec ./process.sh
uploader les répertoires sur le site

#--command pour repérer les lignes avec une seule occurrence de titre
for file in */*xml; do  awk '$0 ~ FS { print NF-1, $0 }' IGNORECASE=1 FS="titre" $file | grep "^1" | grep -v resume ; done
