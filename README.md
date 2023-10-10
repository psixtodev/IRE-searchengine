# IRE-searchengine
University of West Bohemia Plzen
Faculty of Applied Sciences
Information Retrieval - project (IR-E)

# Overview
This project is a small search engine application that utilizes Elasticsearch for search
functionality and Streamlit for developing the graphical user interface (GUI). The
application allows users to search for Airbnb listings based on various criteria and
provides search results with additional information.There is brief PDF documentation describing the 
project, which explains the technical details of the application.

# Dependecies
  - pandas: A data manipulation library used for loading the Airbnb dataset.
  - elasticsearch: A Python client for Elasticsearch, used for interacting with the Elasticsearch search engine.
  - streamlit: A Python framework for building interactive web applications.

# Usage
  1. Install the required dependencies mentioned above.
  2. Ensure that Elasticsearch is running and accessible at:
     ```
     http:localhost:9200
     ```
  3. Execute using a python interpreter:
     ```
     py main.py
     ```
  4. The Streamlit application will launch in a web browser.

The easiest way is using the command ```‘$ streamlit run app.py’``` under directory with
all the source code files
     
  
  
