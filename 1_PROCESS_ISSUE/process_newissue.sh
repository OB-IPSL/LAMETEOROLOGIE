# bashrc script 
# it should be run with three inputs 
# 1/ issue number 
# 2/ year 
# 3/ first page of the Resumés Climatiques to trim the end
# example
# ./process_newissue.sh 125 2024 75
echo "Numéro : $1"
echo "Année  : $2"
echo "Page RM: $3"

#--get arguments
num=$1
year=$2
page=$3

# Directories
dir_issue='/data/oboucher/LAMETEO_PDF/num'${num}
dir_rvt='../2_UPDATE_DIRECTORIES/input'
dir_crossref='../3_LOG_DOI/'

# xml output files
file_rvt='meteo_'${year}'_'${num}'_rvt.xml'
file_crossref='meteo_'${year}'_'${num}'_crossref.xml'

#--treat a couple of files
#--keep 9 pages and remove last 3 pages from last file 
#--last page start
mv -n ${dir_issue}/meteo_${year}_${num}_${page}.pdf ${dir_issue}/meteo_${year}_${num}_${page}.pdf.ori
pdftk ${dir_issue}/meteo_${year}_${num}_${page}.pdf.ori cat 1-9 output ${dir_issue}/meteo_${year}_${num}_${page}.pdf

pdftk ${dir_issue}/"Couverture_${num}.pdf" ${dir_issue}/"Sommaire_${num}.pdf" cat output ${dir_issue}/meteo_${year}_${num}_couv.pdf

#--make small plots from cover
#convert -resize 200x100 ${dir_issue}/meteo_${year}_${num}_couv.pdf[0] ${dir_issue}/meteo_${year}_${num}_couv_low.png
#convert -resize 400x200 ${dir_issue}/meteo_${year}_${num}_couv.pdf[0] ${dir_issue}/meteo_${year}_${num}_couv_medium.png
#convert ${dir_issue}/meteo_${year}_${num}_couv.pdf[0] ${dir_issue}/meteo_${year}_${num}_couv_high.png
#convert -resize 40% ${dir_issue}/Couverture_${num}.png ${dir_issue}/meteo_${year}_${num}_couv_low.png
#convert -resize 60% ${dir_issue}/Couverture_${num}.png ${dir_issue}/meteo_${year}_${num}_couv_medium.png
#convert -resize 100% ${dir_issue}/Couverture_${num}.png ${dir_issue}/meteo_${year}_${num}_couv_high.png
cp ${dir_issue}/Couverture_${num}.png ${dir_issue}/meteo_${year}_${num}_couv_low.png
cp ${dir_issue}/Couverture_${num}.png ${dir_issue}/meteo_${year}_${num}_couv_medium.png
cp ${dir_issue}/Couverture_${num}.png ${dir_issue}/meteo_${year}_${num}_couv_high.png

python newissue.py ${num} ${year}
sed -i -e 's/<?xml version="1.0" ?>/<?xml version="1.0" encoding="UTF-8"?>/g' ${dir_issue}/${file_rvt}
sed -i -e 's/<?xml version="1.0" ?>/<?xml version="1.0" encoding="UTF-8"?>/g' ${dir_issue}/${file_crossref}

cd ${dir_issue}

# to be modified if more files are needed to be included (eg supplements)
zip -r ${num}.zip meteo*pdf meteo*xlsx meteo*gif *rvt.xml meteo*.png 

# copy files in right directories for steps 2 and 3
cp -r ${file_rvt}      ${dir_rvt}/.
cp -r ${file_crossref} ${dir_crossref}/.
