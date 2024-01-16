## Project Title: "SalesFlow Pro: Transformative Analytics Pipeline"

### Overview

Welcome to "SalesFlow Pro," a dynamic analytics pipeline designed to revolutionize sales data analysis. This project seamlessly integrates Python, Apache Airflow, Google Cloud Storage, and BigQuery to orchestrate a comprehensive end-to-end solution. Dive into the details below to understand how this pipeline transforms raw sales data into actionable insights.

### Project Highlights:

- **Data Source to BigQuery:**
  - Task: `upload_csv_to_gcs`
  - Description: Initiates the journey by uploading a local CSV file to Google Cloud Storage, setting the stage for further processing.

- **BigQuery Transformation:**
  - Task: `load_csv`
  - Description: Transforms the uploaded CSV data into the raw_invoices table in BigQuery, unleashing the power of cloud-based data processing.

-  **SODA Data Validation:**
   - Utilizes SODA (Socrata Open Data API) to perform data validation checks, ensuring adherence to predefined quality standards.

- **Query Execution and Result Storage:**
  - Task: `execute_query_save`
  - Description: Executes a strategic SQL query to calculate total purchases and meticulously stores the results in the Sales_Data table.

- **BigQuery Constraints:**
   - Implements constraints within BigQuery tables to enforce data integrity at the storage level.

- **Archiving Excellence:**
  - Task: `archive_files`
  - Description: Achieves perfection by archiving the processed CSV file in Google Cloud Storage, ensuring data integrity and historical record-keeping.

- **Looker Studio Integration:**
  - Dashboard: A Google Looker Studio dashboard has been created, connecting seamlessly to the data fact table for insightful visualizations.

- **Looker Studio Data Integrity:**
   - Leverages Looker Studio's built-in data validation features to monitor and verify the integrity of data visualizations.

3.
### DAG Schedule and Initialization:

- **Start Date:** December 1, 2023
- **Schedule Interval:** 07:05 UTC daily
- **Catchup:** Disabled

### The Grand Kickoff:

- The `intial_kick` function initiates the project with finesse. It creates the 'retail' dataset, archives an initial file, and performs crucial setup tasks to lay the foundation for success.
- 
### Project Structure

- **.astro:** Contains configuration files for Astro, including database connection details and file definitions.

- **dags:** Holds the Apache Airflow DAG (Directed Acyclic Graph) definitions for the sales analytics pipeline.

- **include:** Stores additional files or datasets used in the project.

- **plugins:** Contains any custom Airflow plugins that enhance functionality.

- **tests:** Houses test cases for ensuring code quality and reliability.

- **venv:** Virtual environment for managing project dependencies.

- **.dockerignore:** Specifies files and directories to be excluded when building Docker images.

- **.env:** Configuration file for environment variables.

- **.gitignore:** Defines files and directories to be ignored by Git.

- **airflow_settings.yaml:** Configuration file for Airflow settings.

- **Dockerfile:** Instructions for building a Docker image of the project.

- **packages.txt:** List of Python packages and dependencies.

- **README.md:** Main documentation file providing an overview, usage instructions, and other project details.

- **requirements.txt:** Specifies Python packages and versions required for the project.

- ## Screenshots

### Airflow DAG Graph View

![image](https://github.com/nambatibuf/SalesFlow-Pro-Transformative-Analytics-Pipeline/assets/130098870/5eaf6870-3385-4469-baa4-a221ae768369)

### Looker Studio Dashboard

![Looker Studio Dashboard](screenshots/looker_dashboard.png)

### Google Cloud Storage (GCS) Bucket

![image](https://github.com/nambatibuf/SalesFlow-Pro-Transformative-Analytics-Pipeline/assets/130098870/ba0577c2-23e8-4309-8018-b0c02c308a2c)

### BigQuery Console

![image](https://github.com/nambatibuf/SalesFlow-Pro-Transformative-Analytics-Pipeline/assets/130098870/d5b11c75-984b-40be-a2f6-428cb4362ea8)

### Archiving Files
![image](https://github.com/nambatibuf/SalesFlow-Pro-Transformative-Analytics-Pipeline/assets/130098870/83403326-9f85-489e-9919-e6d08bbcd85f)

### Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/salesflow-pro.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Google Cloud credentials:

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
    ```

4. Run the Airflow DAG:

    ```bash
    airflow dags trigger retail
    ```

### Contributing

Contributions are welcome! Please follow our [contribution guidelines](CONTRIBUTING.md).

### License

This project is licensed under the [MIT License](LICENSE).

### Credits

- Mention any contributors or external libraries/tools used in the project.

Embark on a journey of sales data excellence with "SalesFlow Pro: Transformative Analytics Pipeline"! Customize and adapt as needed for your project's unique achievements and impact.
