# Deep Learning - Distant Galaxies
https://eksamen.ku.dk/api/file/opg/275756 - LSDA2017GalaxiesTest.csv
https://eksamen.ku.dk/api/file/opg/275757 - LSDA2017GalaxiesTrain.csv
https://eksamen.ku.dk/api/file/opg/275758 - LSDA2017GalaxiesValidate.csv

# Neighbors - Distant Galaxies HW5
https://absalon.instructure.com/files/1328110/download?download_frd=1 - neighbors folder

# LSH - Enron emails
https://archive.ics.uci.edu/ml/datasets/Bag+of+Words - main page
https://archive.ics.uci.edu/ml/machine-learning-databases/bag-of-words/docword.enron.txt.gz - Direct Data download

# Trees - Landsat data
https://sid.erda.dk/share_redirect/hm33L7oPna - landsat_train.csv
https://sid.erda.dk/share_redirect/ex9cLH1QU1 - landsat_test.csv

# Hadoop - Airlines data
https://absalon.instructure.com/files/1328110/download?download_frd=1 - hadoop/airline_data folder

### MOUNT DATA FROM SMB SHARE :
## ON HOST
# powershell create smb shared folder - run as administrator
New-SmbShare -Name "lsda_data" -Path "C:\Code\DIKU\LSDA\exam\data" -Temporary -ReadAccess "Lu"
net config server /autodisconnect:-1

## ON VM : 
# ensure cifs-utils is installed
sudo apt-get install cifs-utils
# link folder - replace IP address and username accordingly
sudo mount -t cifs -o username=Lu //192.168.111.192/lsda_data ./data
