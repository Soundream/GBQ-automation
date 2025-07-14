# BigQuery Automation Tool

A Python-based tool for executing multiple BigQuery queries and saving results to organized CSV files.

## Quick Start Guide

### Running the Tool

Run the tool with this command (or open and run it in Python):

```
cd /d D:\GitHubProjects\GBQ-automation (change this to your repository path)
python bq-runner.py
```

Then, BigQuery processing is complete and the results are **fully formatted**.

No need to worry about BigQuery, Google Sheets, Python code, or renaming—**it's all taken care of**!


### First-time Setup

Before first use:

1. Make sure you already have Google BigQuery access permissions
2. Run `auth.py` and follow the authentication prompts in your browser
3. Create `apikey.txt` to save the API key locally and safely (outside Github)
   (you can find the `.txt `file, or just search for `API_KEY` in  [BA Guide](https://docs.google.com/document/d/1aGXIwJVwVOf-CDWkDe-NopexRr57tte54TFgjL2FlJE/edit?usp=drive_link), paste the key in a new `.txt` file, and rename it to `apikey.txt`)

### Data Download Process

Once you run the tool:

- All queries configured in `queries.json` will be executed sequentially
- Dates will be automatically converted and
- Data will be automatically downloaded as `.csv` and saved to the `output` folder
- Files will be renamed according to your configured patterns (standardized as `yyyymm_query_name`)
- No further action is needed to access the downloaded data (for Tableau integration, refer to the detailed documentation in [BA Guide](https://docs.google.com/document/d/1aGXIwJVwVOf-CDWkDe-NopexRr57tte54TFgjL2FlJE/edit?usp=drive_link))

## Setup

1. **Install Python Dependencies**:

   ```
   pip install -r requirements.txt
   ```
2. **Authenticate with Google Cloud**
3. **Configure Queries**:

   - Edit `queries.json` to define your folder structure and queries
   - Each folder should specify:
     - `name`: Display name for the folder/report
     - `folder`: Output directory name
     - `queries`: List of queries in this folder/report
   - Each query should specify:
     - `name`: Display name for the query
     - `query`: SQL query string
     - `template`: SQL query string with something to be modified (usually dates). If have `template`, then `query=None`, and a `.sql `file should be matched.
     - `legacy`: Boolean flag for legacy SQL syntax
     - `filename_pattern`: Output filename pattern (standardized as "yyyymm_name")

## Features

- Execute multiple BigQuery queries in sequence
- Organize queries by folders or report types
- Support both legacy SQL and standard SQL syntax
- Modify the date range (originally maintained in Google Sheets)
- Run the associated Python data processing scripts
- Save results to organized folders with customizable naming patterns
- Show progress bars during query execution
- Configure queries using JSON configuration file

## Usage Details

The tool will:

1. Read query configurations from `queries.json`
2. Process each folder and its queries with progress indicators
3. Create output folders if they don't exist
4. Execute queries and save results to the specified folders with timestamped filenames
5. Show a summary of successful and failed queries, organized by folder

## Sample JSON Configuration

```json
{
    "folders": [
        {
            "name": "Travel Market Share Report",
            "folder": "market_share",
            "queries": [
                {
                    "name": "App Annie Report Data",
                    "query": "SELECT * FROM [wego-cloud:appannie.appannie_tableau_report_updated_2019_03_05]",
                    "legacy": true,
                    "filename_pattern": "yyyymm_appannie"
                },
                {
                    "name": "App Annie Ranking Report",
                    "query": "SELECT * FROM [wego-cloud:appannie.appannie_ranking_tableau_report]",
                    "legacy": true,
                    "filename_pattern": "yyyymm_appannie_ranking"
                }
            ]
        },
        {
            "name": "Marketing Performance",
            "folder": "marketing",
            "queries": [
                {
                    "name": "Marketing Data",
                    "query": "SELECT * FROM `wego-cloud.analytics.marketing_performance` LIMIT 1000",
                    "legacy": false,
                    "filename_pattern": "yyyymm_marketing"
                }
            ]
        }
    ]
}
```

## Output Structure

```
output/
├── market_share/
│   ├── 202507_appannie.csv
│   ├── 202507_appannie_ranking.csv
│   └── 202507_similarweb.csv
├── key_brands/
│   └── 202507_appannie_app_ratings.csv
└── shopcash_markets/
    └── 202507_appannie_tableau_report.csv
```
