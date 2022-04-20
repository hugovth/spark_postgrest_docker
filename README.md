# postgrest

## Folder Structure

### config
This folder contains the configuration files for postgrest

| Name        	| Description  |
| ------------- |:-------------:|
| postgrest.cong      	| configuration file for postgrest	|

### pyspark
This folder contains the files to build a pyspark docker
| Name        	| Description  |
| ------------- |:-------------:|
| create_docker_image.sh    	| generate an image and push it to dockerhub	|
| Dockerfile    	| generate a docker runing pyspark and connecting to postgresql	|

#### ressources
This folder contains the folders and files needed to be pushed by the Dockerfile 
| Name        	| Description  |
| ------------- |:-------------:|
| entrypoint.sh 	| entrypoint files for docker	|
| requirement.txt 	| python depedentie 	|
| json data 	| contains all the json to be processed by the python script	|
| script.py 	| dat processing pyspark script	|

### sql
This folder contains the executables SQL of postgresql 
| Name        	| Description  |
| ------------- |:-------------:|
| init.sql	| Contains the executable SQL to be run at db initialisation	|

