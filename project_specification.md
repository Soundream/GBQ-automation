# BigQuery Automation Tool - Project Specification

## Project Overview
A Python-based automation tool for executing Google BigQuery legacy SQL queries using personal Google account authentication. The tool is designed for migrating existing queries from legacy systems to a local Windows environment.

## Authentication Requirements
- **Authentication Method**: gcloud CLI Application Default Credentials
- **Reason**: User does not have permissions to create OAuth clients or IAM service accounts
- **Usage**: Single-user, no sharing required
- **Environment**: Local Windows development environment only
- **Setup**: Requires gcloud CLI installation and `gcloud auth application-default login`

## Query Requirements
- **SQL Type**: Legacy SQL syntax (mandatory for migration compatibility)
- **Target Query**: `SELECT * FROM [wego-cloud:appannie.appannie_tableau_report_updated_2019_03_05]`
- **Query Format**: Must support legacy BigQuery syntax `[project:dataset.table]`

## Output Requirements
- **Format**: CSV file export
- **Naming Convention**: `appannie_mm_yyyy.csv` (month_year format)
  - Example: `appannie_01_2024.csv` for January 2024
- **File Location**: Local project directory
- **Note**: Each SQL query may have different naming patterns

## Technical Environment
- **Platform**: Windows 10+ local environment
- **Language**: Python
- **Dependencies**: Google Cloud BigQuery Python client library, pandas
- **Authentication Flow**: gcloud CLI Application Default Credentials
- **Prerequisites**: Google Cloud SDK (gcloud CLI) installation

## Functional Requirements
1. Authenticate user via Google OAuth2 flow
2. Execute legacy SQL queries against BigQuery
3. Export query results to CSV format
4. Generate timestamped filenames based on execution date
5. Handle authentication token refresh automatically
6. Provide clear error handling and logging

## Non-Functional Requirements
- Simple command-line interface
- Minimal external dependencies
- Cross-session credential persistence
- Clear error messages for authentication and query failures

## Project Structure
```
GBQ-automation/
├── bq-runner.py              # Main program file (simplified)
├── auth.py                   # Authentication module
├── project_specification.md  # This specification document
├── README.md                 # Operation manual (not modified)
├── requirements.txt          # Python dependencies
└── output/                   # CSV output directory (optional)
```

## Setup Instructions
1. **Install Google Cloud SDK**: Download from https://cloud.google.com/sdk/docs/install
2. **Install Python dependencies**: `pip install -r requirements.txt`
3. **Authenticate with gcloud**: `gcloud auth application-default login`
4. **Run the tool**: `python bq-runner.py`

## Out of Scope
- IAM service account integration
- Cloud server deployment
- Multi-user sharing capabilities
- Query result processing beyond CSV export
- UI/web interface

## Future Considerations
- Support for multiple SQL queries with different naming patterns
- Automated scheduling capabilities
- Additional output formats 