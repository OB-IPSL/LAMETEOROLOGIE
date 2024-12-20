# This script is to log the doi on the CrossRef server 
# The xml filename is to be adjusted each time
# first we test on the test server, this generates an email to confirm all is fine
# then we can log the doi on the real server by commenting the test curl and decommenting the second curl
# Météo & Climat pays an annual fee and has a login / passwd to access the CrossRef servers as described below

#--how to log a draft doi as a test
curl -F 'operation=doMDUpload' -F 'login_id=mcsf' -F 'login_passwd=mcsf_f4r2' -F 'fname=@meteo_2025_128_crossref.xml' https://test.crossref.org/servlet/deposit

#--how to log a doi for real ! 
#curl -F 'operation=doMDUpload' -F 'login_id=mcsf' -F 'login_passwd=mcsf_f4r2' -F 'fname=@meteo_2025_128_crossref.xml' https://doi.crossref.org/servlet/deposit
