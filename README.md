# LAMETEOROLOGIE
------------------

PROCEDURE POUR METTRE EN LIGNE UN NOUVEAU NUMERO

1/ PROCESS NEW ISSUE
- créer un répertoire numXXX pour processer le numéro où XXX est le numéro de la revue
- réceptionner le fichier zip en provenance de Météo-France dans ce répertoire 
- le dezipper puis effacer le fichier zip devenu inutile
- garder une copie du xml original de MF (par ex. "cp meteo_2024_127.xml meteo_2024_127.xml.ori")
- enlever si nécessaire les majuscules dans le xml de MF, en particulier sur les noms de rubrique 
- enlever si nécessaires les "leading zeros" sur les numéros de page
- enlever si nécessaires les retour chariot dans titre / rubrique / citation
- traiter les PDF manuellement s'il le faut 
- modifier le répertoire dans le script "process_newissue.sh"
- lancer le script "process_newissue.sh numero année pageRM" où pageRM est le numéro de page des Résumés Climatiques
- modifier les xml si besoin en particulier si deux Echos démarrent sur meme page (ajouter b au deuxième écho)
- positionner manuellement les articles en libre accès avec open_access = 0 dans le fichier xml destiné à RVT (River Valley Technology)
- vérifier la numérotation des doi et leur continuité par rapport aux précédents numéros de l'année 
- positionner manuellement les éventuels supplements dans le fichier xml destiné à RVT (1 entrée xml pour chaque supplément)
<supplement>
   <fichier>meteo_2018_101_30_supp1.pdf</fichier>
</supplement>
- ajouter une entrée dans le xml pour le fichier PDF complet
- recréer le zip manuellement dans le répertoire du numXXX
- uploader le numéro sur le site de la revue 
weblink: https://lameteorologie.fr/admin/
User name: meteo_admin
Password: meteoclim@
Onglet "Upload Issues": Browse, Upload, Process

- vérifier que le numéro apparaît correctement sur le site de la revue


2/ UPDATE DIRECTORIES ON WEB SITE 
- updater l'année de fin (yrend) dans le script saison.py quand on commence une nouvelle année des saisons cycloniques
- générer les répertoires avec ./process.sh => les répertoires se retrouvent dans output
- uploader un par un les répertoires (fichiers *xml uniquement) sur le site
weblink: https://lameteorologie.fr/admin/
User name: meteo_admin
Password: meteoclim@
Onglet "Indices manager": "choisir un fichier" puis Upload cnsécutivement pour les 5 fichiers xml des répertoires

- vérifier que les répertoire sont bien à jour sur le site


3/ LOG DOIs ON CROSSREF SERVERS
- modifier le script de soumission avec le bon nom de fichier
- soumettre le xml destiné à crossref en mode test puis pour de vrai
