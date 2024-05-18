# ISB_AMPBA_Capstone-Project_Deloitte-Anomaly-Detection-in-Business-Processes-using-Generative-AI

## Introduction
This repository contains the code and resources for the ISB Capstone Project with Deloitte, focused on anomaly detection in business processes using generative AI. The goal of this project is to enhance fraud detection, streamline audit processes, and improve operational efficiency using generative AI.

## Project Overview
### Business Problem
Expense reimbursement fraud accounts for a significant portion of asset misappropriation cases, presenting challenges for timely detection and significant financial losses. This project aims to address these challenges by leveraging generative AI to detect anomalies in transactional data, providing actionable insights for non-technical personnel.

### Benefits
- **Management**: Empowers management with actionable intelligence to mitigate risks proactively.
- **T&E Team**: Streamlines the process of reviewing and approving expenses, ensuring policy compliance.
- **Internal Auditors**: Enhances the audit process by effectively identifying potential fraud and policy deviations.

## Project Workflow
The project follows a structured workflow from data cleaning to the deployment of the anomaly detection model. Below is a high-level overview of the steps involved:

1. **Data Cleaning**: Removing empty columns and eliminating inconsistencies.
2. **Exploratory Data Analysis (EDA)**: Generating detailed reports and visualizations.
3. **Data Transformation**: Merging relevant columns and preparing the data for modeling.
4. **Data Modeling**: For Dashboarding, Using KNN for anomaly detection and applying KRIs for rule-based modeling. 
5. **Model Evaluation**: Evaluating models using classification metrics and comparing results with ground truth.
6. **Dashboard Requirements**: Gathering wireframe dashboard requirements and generating results/plots.
7. **Generative AI Implementation**: Utilizing LLM Agent/GenAI for insights and action plans.

### Workflow Diagram
![Project Workflow Diagram](https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte-Anomlay-Detection-in-Business-Processes-using-Generative-AI/blob/main/images/Workflow%20diagram.12.png)

## Architecture Diagram
The architecture diagram provides a detailed view of the system components and data flow involved in the project.

![Architecture Diagram](https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte-Anomlay-Detection-in-Business-Processes-using-Generative-AI/blob/main/images/Architecture%20Diagram.drawio%20(2).png)

## Data Orchestration/ETL using Mage AI
The data orchestration and ETL process leverages Mage AI to manage and streamline the data flow. The raw CSV tables from PostgreSQL are ingested, transformed, and exported back to PostgreSQL, ensuring data consistency and readiness for subsequent analysis. Mage AI is installed using Docker for efficient ETL and data pipeline management. This approach not only automates data handling but also significantly enhances the reliability and scalability of the entire data processing workflow.

(https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte--Anomaly-Detection-in-Business-Processes-using-Generative-AI/blob/main/images/Mage%20AI%20Pipeline%20Flow%20chart.png)
(https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte--Anomaly-Detection-in-Business-Processes-using-Generative-AI/blob/main/images/Data%20Loader_ETL.png)
(https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte--Anomaly-Detection-in-Business-Processes-using-Generative-AI/blob/main/images/Transformation_ETL.png)
(https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte--Anomaly-Detection-in-Business-Processes-using-Generative-AI/blob/main/images/Exporter_ETL.png)

## App Interface
The app interface allows users to interact with the anomaly detection model, view results, and gain insights from the data.

![App Interface](https://github.com/adarshb3/ISB_AMPBA_Capstone-Project_Deloitte-Anomlay-Detection-in-Business-Processes-using-Generative-AI/blob/main/images/App%20Interface%20Screenshot.png)

## Tools and Technologies

### Tools
1. **Python 3.10.9**: Required for running the scripts.
2. **VS Code**: Recommended IDE with Docker and Azure CLI extensions.
3. **Docker Dekstop**: For containerizing the application.
4. **Docker Extension**: For running Docker images.
5. **Azure Tools Extension**: For managing Azure resources.
6. **Azure CLI Tools Extension**: Tools for developing and running commands of the Azure CLI.
7. **Mage AI**: Installed using Docker for ETL ; data pipelines.[https://github.com/mage-ai/mage-ai]
8. **PostgreSQL - pgAdmin4**: Database management system ; GUI for PostgreSQL.
10. **Tableau**: For dashboarding and data visualization.

### Python Libraries
Based on the `app3.py` file, the following libraries need to be installed:
```text
streamlit==1.29.0
pandas==2.2.1
python-dotenv==1.0.0
langchain-openai==0.1.4
openai==1.23.6
langchain==0.1.16
langchain-community==0.0.33
langchain-core==0.1.46
langchain-experimental==0.0.57
langchain-openai==0.1.4
langchain-text-splitters==0.0.1
tabulate==0.9.0
