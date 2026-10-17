# AI-Based Intrusion Detection System

## Project Overview

The **AI-Based Intrusion Detection System** is a Python-based cybersecurity project designed to analyze network traffic records and identify potentially malicious activity using machine learning.

The application provides a web interface where users can upload network traffic data in CSV format, view prediction results, review previous analyses, and download a PDF report.

This project demonstrates how machine learning can support network security monitoring and intrusion detection.

## Objectives

- Analyze network traffic records.
- Classify network activity using a trained prediction model.
- Identify records associated with potential network attacks.
- Display prediction summaries and risk information.
- Maintain a history of recent analyses.
- Generate downloadable PDF security reports.

## Technologies Used

- **Python** — Application development
- **Flask** — Web application framework
- **Pandas** — Data processing and CSV handling
- **Machine Learning** — Network traffic classification
- **NSL-KDD Dataset** — Network intrusion detection data
- **ReportLab** — PDF report generation
- **HTML and CSS** — Web interface, if included in the project templates

## Key Features

### 1. Network Traffic Analysis
Upload a CSV file containing network traffic features for analysis.

### 2. AI-Based Prediction
Use the integrated prediction module to classify the uploaded records.

### 3. Analysis Summary
Display the prediction, confidence score, risk level, total records, attack records, normal records, and their percentages.

### 4. Analysis History
Store and view recent analysis results using a JSON history file.

### 5. PDF Report Generation
Generate a downloadable report containing analysis details and security recommendations.

### 6. Sample Dataset Download
Download a sample CSV file to understand the expected input format.

## System Workflow

1. Upload network traffic data in CSV format.
2. Validate the input columns.
3. Prepare the data for prediction.
4. Pass the data to the trained prediction module.
5. Display the classification results.
6. Save the analysis summary in the history.
7. Generate a PDF report when requested.

## Project Structure

```text
AI-Based-Intrusion-Detection-System/
│
├── app.py
├── predict.py
├── sample_test.csv
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── history.html
│
├── reports/
│
└── model files/
    └── Add your trained model files here
```

*Adjust this structure to match your actual files. Include the trained model files or the documented steps needed to obtain them.*

## Installation and Setup

### Prerequisites

- Python 3
- pip
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Based-Intrusion-Detection-System.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 2: Open the project folder

```bash
cd AI-Based-Intrusion-Detection-System
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

Ensure `requirements.txt` contains the dependencies required by your application and prediction module.

### Step 5: Run the application

```bash
python app.py
```

Open the local address shown in the terminal in your browser.

## Dataset

The application is designed around network traffic features associated with the NSL-KDD dataset.

The input data should follow the feature format expected by the prediction module. Use the supplied sample CSV or the dataset preparation instructions to prepare compatible input.

## Security and Limitations

- Model predictions are indicators, not definitive proof of an attack.
- Detection performance depends on the training data and model quality.
- This project should not be considered a replacement for a complete production network security system.
- Do not upload confidential network logs or sensitive data to an untrusted deployment.
- Test the application with authorized datasets and systems.

## Future Enhancements

- Add more detailed model evaluation metrics.
- Improve visualization of network traffic and detection results.
- Add support for additional intrusion categories.
- Integrate authorized live network monitoring.
- Improve error handling and report presentation.

## Learning Outcomes

This project provides practical experience with Python, web application development, data preprocessing, machine learning integration, cybersecurity concepts, and automated report generation.

## Author

**Geethika Inakollu**

GitHub: https://github.com/geethikainakollu8-prog

## Disclaimer

This project is intended for educational purposes and authorized cybersecurity research. Use it responsibly and only with systems and data you are permitted to analyze.
