
  ______   __   __            __    __            __              ________ ________  __       
 /      \ |  \ |  \          |  \  |  \          |  \            |        \        \|  \      
|  $$$$$$\ \$$_| $$_         | $$  | $$ __    __ | $$____        | $$$$$$$$\$$$$$$$$| $$      
| $$ __\$$|  \   $$ \        | $$__| $$|  \  |  \| $$    \       | $$__      | $$   | $$      
| $$|    \| $$\$$$$$$        | $$    $$| $$  | $$| $$$$$$$\      | $$  \     | $$   | $$      
| $$ \$$$$| $$ | $$ __       | $$$$$$$$| $$  | $$| $$  | $$      | $$$$$     | $$   | $$      
| $$__| $$| $$ | $$|  \      | $$  | $$| $$__/ $$| $$__/ $$      | $$_____   | $$   | $$_____ 
 \$$    $$| $$  \$$  $$      | $$  | $$ \$$    $$| $$    $$      | $$     \  | $$   | $$     \
  \$$$$$$  \$$   \$$$$        \$$   \$$  \$$$$$$  \$$$$$$$        \$$$$$$$$   \$$    \$$$$$$$$
                                                                                              

Libraries required:

requests>=2.13.0   (i.e. pip install requests)
json-encoder>=0.4.4
python-status>=1.0.1
aiohttp>=2.2.0
python-simple-rest-client  (https://github.com/allisson/python-simple-rest-client)


Current use:

***Historical (once)
python start.py -s coins_github.csv -hi

***Daily
python start.py -s coins_github.csv

***Upload Bucket S3
python send_to_bucket.py

                                                                                              
Old examples:
python github_etl.py -r -n bitcoin/bitcoin -o -f repository/bitcoin.csv
python github_etl.py -n uab-projects -o -f repository/uab-projects.csv
python github_etl.py -n cryptoapi -f repository/cryptoapi.csv

python github_historical_etl.py -n omise/omise-go -f prueba.csv
python github_historical_etl.py -n zquestz/bitcoincash -f repository/bitcoincash-forks.csv

python start.py -s coins_github.csv