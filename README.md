# Capstone-Project

# Real-Time Buoy Data: Wave and Weather Threat Detection

## Author: Garrett Kopp
## Date: 11.26.23
## GitHub Repo: https://github.com/ggkopp/Capstone-Project

## Overview

This repository contains the project materials for "Real-Time Buoy Data: Wave and Weather Threat Detection." The project focuses on leveraging oceanographic buoy data to detect potential extreme weather events, contributing to the protection of coastal communities and marine environments.

## Project Phases

### 1. Data Collection and Preparation

- **Data Source:** Utilized a Kaggle dataset containing real-time meteorological and oceanographic data from Irish moored Weather Buoys.
- **Data Cleaning:** Process involved restructuring headers, handling missing values, and refining data types.
  
### 2. Data Analysis Using Python

- **Key Parameters:** Focuses on essential metrics, including wave height, wind speed, and gust.
- **Python Script Development:** Used pandas, numpy, and scikit-learn for statistical analysis and linear regression modeling.

### 3. Alert Parameter Development

- **Incorporating Linear Regression Insights:** Utilized coefficients from the linear regression model to understand the influence of wind speed and gust on wave height.
- **Enhanced Alert Metrics:** Implemented an equation (wave_height * wind_gust > 95 or wave_height * wind_speed > 95) for triggering alerts.

### 4. Model and Alert Testing and Validation

- **Testing Procedures:** Included historical data testing, real-time data testing, scenario-based testing, cross-validation, and alert validation.
  
### 5. Deployment and Integration

- **System Configuration:** Optimized alert system configuration for deployment.
- **Live Data Streaming:** Integrated the system with live buoy data streams and RabbitMQ queues.
- **Continuous Monitoring:** Ensured continuous monitoring of buoy data for real-time threat detection.
- **Performance Monitoring:** Regularly evaluated the system's accuracy, reliability, and responsiveness.

## Repository Structure

- `data/`: Contains the Kaggle dataset and cleaned data.
- `code/`: Includes Python scripts, Jupyter Notebooks, and Excel workbooks.
- `reports/`: Contains the Overleaf report providing detailed project documentation.
- `README.md`: The main repository documentation file.

## Key Resources

- [Kaggle Dataset - "Buoy's Oceanographic Foras na Mara"](https://www.kaggle.com/ajaypalsinghlo/oceanography-buoys-data)
- Python Libraries: pandas, numpy, scikit-learn, matplotlib, seaborn
- Overleaf Report: [Project Overleaf Report](https://www.overleaf.com/read/rhtthxfcjddc#92cb46)

## VSCode File Directory Summary

- Buoydata_emitter.py : File sending the code ti RabbitMQ using the 3 key parameters and algorythym to determine and send a severe weather warning to a Gmail email address. 
- BuoyData_listener.py : File recieving the data from RabbitMQ
- Buoydata_modified.csv : File that resulted from the data clening process in file DataCleaning.ipynb 
- Buoydata.csv : Original dataset
- DataCleaning.ipynb : Data Cleaning steps that produced the Buoydata_modified.csv file
- ExploratoryDataAnalytics.ipynb : Visualizations 
- MachineLearning.ipynb : Linear Regression model creation, testing, and results

## Communication and Progression

- Clear and concise commit messages showcase the progression from data collection to model testing.
- Documentation in the README.md provides a comprehensive overview of the project and its phases.

## Note

- Please refer to the Overleaf report for detailed explanations, visualizations, and in-depth analysis.

---
Feel free to explore the project and use the provided resources for a deeper understanding of the methodologies and findings.
