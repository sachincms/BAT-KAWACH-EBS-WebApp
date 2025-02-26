# PH-Vector-Database
Web application and API codebase for Precision Health's Event Based Surveillance (EBS) tool. Although this codebase contains more than just the vector database's operations, this repo is named after the EC2 instance to avoid any confusion.

EBS URL: http://13.126.45.20:8502/  
API endpoint: http://13.126.45.20/  

## Accessing the API-
- No parameters (default): Returns latest cached data, including historical data
```
import requests

API_URL = http://13.126.45.20/
response = requests.get(API_URL)
```

- Start and end date parameters: Returns data between the specified dates
```
import requests

API_URL = http://13.126.45.20/

params = {
    'start_date': '01-01-2023',
    'end_date': '01-02-2023'
}

response = requests.get(API_URL, params=params)
```

## Weaviate Scripts:
```handlers/id_converter.py```
Converts a MongoDB ObjectId to a version 1 UUID.

```handlers/Mongo2Weaviate.py```
Migrates data from MongoDB to Weaviate.

```models/meta.py```
Intended to be run only once to set up the database schema.

```models/Search.py```
Performs the search operation.

```models/Articles.py```
Defines the schema for the Weaviate database.

```settings.py```
Defines variables for Weaviate.

### Setup-
1. Ensure docker is installed and docker daemon is running.
2. On console, change directory to root containing docker-compose.yml and use command-
```
docker-compose up -d
```

### Order of execution-
1. Run meta.py to create the schema.
2. Run Mongo2Weaviate.py to migrate data from MongoDB to Weaviate.
