# Project to mine shoes data from popular e-commerce website

Task :

1 - Scrape all shoes data from https://www.zalora.com.my/

2 - Scrape all shoes data from https://www.zalora.com.my/women/shoes/?from=header&occasion=Casual&brand=aldo

To run the Docker File

1) Download all files in these repo into your machine

2) Run below Docker Command in CMD from where the files in these repo are stored (Reference: https://towardsdatascience.com/how-to-run-a-python-script-using-a-docker-container-ea248e618e32)

>>docker-compose up

>>docker ps

>>docker exec -it shoes-data-mining-main_app_1 bash

(Wait until the script fully run for the data to be available)

3) Open the folders and you will have four json files stored (as per the \data_out folder for reference)
