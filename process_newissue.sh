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

dirout='/data/oboucher/LAMETEO_PDF/num'${num}
file_rvt='meteo_'${year}'_'${num}'_rvt.xml'
file_crossref='meteo_'${year}'_'${num}'_crossref.xml'

#--treat a couple of files
#--keep 9 pages and remove last 3 pages from last file 
#--last page start
mv -n ${dirout}/meteo_${year}_${num}_${page}.pdf ${dirout}/meteo_${year}_${num}_${page}.pdf.ori
pdftk ${dirout}/meteo_${year}_${num}_${page}.pdf.ori cat 1-9 output ${dirout}/meteo_${year}_${num}_${page}.pdf

pdftk ${dirout}/"Couverture_${num}.pdf" ${dirout}/"Sommaire_${num}.pdf" cat output ${dirout}/meteo_${year}_${num}_couv.pdf

#--make small plots from cover
#convert -resize 200x100 ${dirout}/meteo_${year}_${num}_couv.pdf[0] ${dirout}/meteo_${year}_${num}_couv_low.png
#convert -resize 400x200 ${dirout}/meteo_${year}_${num}_couv.pdf[0] ${dirout}/meteo_${year}_${num}_couv_medium.png
#convert ${dirout}/meteo_${year}_${num}_couv.pdf[0] ${dirout}/meteo_${year}_${num}_couv_high.png
#convert -resize 40% ${dirout}/Couverture_${num}.png ${dirout}/meteo_${year}_${num}_couv_low.png
#convert -resize 60% ${dirout}/Couverture_${num}.png ${dirout}/meteo_${year}_${num}_couv_medium.png
#convert -resize 100% ${dirout}/Couverture_${num}.png ${dirout}/meteo_${year}_${num}_couv_high.png
cp ${dirout}/Couverture_${num}.png ${dirout}/meteo_${year}_${num}_couv_low.png
cp ${dirout}/Couverture_${num}.png ${dirout}/meteo_${year}_${num}_couv_medium.png
cp ${dirout}/Couverture_${num}.png ${dirout}/meteo_${year}_${num}_couv_high.png

python newissue.py ${num} ${year}
sed -i -e 's/<?xml version="1.0" ?>/<?xml version="1.0" encoding="UTF-8"?>/g' ${dirout}/${file_rvt}
sed -i -e 's/<?xml version="1.0" ?>/<?xml version="1.0" encoding="UTF-8"?>/g' ${dirout}/${file_crossref}

cd ${dirout}

zip -r ${num}.zip meteo*pdf meteo*xlsx meteo*gif *rvt.xml meteo*.png 

cp -r ${file_rvt}      ~oboucher/LAMETEO/notices/input/.
cp -r ${file_crossref} ~oboucher/LAMETEO/notices/input/.
cp -r ${file_crossref} ~oboucher/LAMETEO/crossref/.
