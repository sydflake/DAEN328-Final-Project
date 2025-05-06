# DAEN328-Final-Project
The objective of this project is to create a complete ETL (Extract, Transform, Load) pipeline using a real-world API. 

This project simulates a data engineering pipeline, handling, and processing live data. We chose to use the Chicago Food Inspections dataset provided by the City of Chicago and the Chicago Data Portal, which updates daily.We chose this data because the data is accessible, meaningful, and high-volume meaning we had lots of data to work with. The API we used was the O data or the Open Data Protocol.

The instructions to run the dockerized files are as follows:
  - Download all files in the github repository.
  - Change the file ".env.sample" to ".env"
     - Update information to match your own credentials
  - Open Docker App
  - Open terminal:
      - Find the directory where the folder with the repository files are
      - Open this directory
      - Type the following command into terminal:
          - docker-compose up --build
      - go to the following link in a web browser to see the Streamlit application:
          - http://localhost:8501

What Streamlit should look like:
<img width="1510" alt="Screenshot 2025-05-05 at 3 28 28 PM" src="https://github.com/user-attachments/assets/f03ad93b-7b74-47fc-a0cc-7182f92edd0c" />


Sydney Flake - Dockerized, helped clean the data, worked on the presentation, set up the Streamlit, and worked on the read me file.  
Jade Winebright - Cleaned the data, made the presentation, and made the categorial feature dictionaries.  
Vedh Jaishankar - Made all visualizations for Streamlit.  
Manaswi Luitel - Cleaned the data, worked on the read me file, and made the presentation.
