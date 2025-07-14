# by Soundream (Peter), July 14th, 2025
# tested on python3.10
# only use your own authentication


"""
BigQuery Runner
Tool for executing multiple BigQuery queries and saving results to organized CSV files.
"""

import csv
import os
import json
import importlib.util
from datetime import datetime, timedelta
from google.cloud import bigquery
from tqdm import tqdm
from auth import BigQueryAuth
from sql_processor import load_query_template, get_date_params_by_template

# Dynamically import key_brand scripts
def import_key_brand_module(file_path, module_name):
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(f"Warning: Could not import {module_name}: {e}")
    return None

# Import key brand modules
key_brand_1 = import_key_brand_module("run_with_key_brand_1.py", "key_brand_1")
key_brand_2 = import_key_brand_module("run_with_key_brand_2.py", "key_brand_2")
key_brand_3 = import_key_brand_module("run_with_key_brand_3.py", "key_brand_3")

class QueryRunner:
    def __init__(self):
        self.auth = BigQueryAuth()
        self.client = None
    
    def setup(self):
        """
        Setup authentication and BigQuery client.
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        if self.auth.authenticate():
            self.client = self.auth.get_client()
            return True
        return False
    
    def execute_query_and_save(self, sql_query, folder, filename_pattern, legacy=False):
        """
        Execute a query and directly save results to CSV in specified folder.
        
        Args:
            sql_query (str): SQL query to execute
            folder (str): Folder to save results in
            filename_pattern (str): Filename pattern (e.g., 'appannie_mm_yyyy')
            legacy (bool): Whether to use legacy SQL syntax
            
        Returns:
            str: Generated filename with path
        """
        if not self.client:
            raise Exception("Client not initialized. Please run setup() first")
        
        # Ensure folder exists
        os.makedirs(folder, exist_ok=True)
        
        # Configure job to use legacy SQL if requested
        job_config = bigquery.QueryJobConfig(use_legacy_sql=legacy)
        
        # Execute the query silently
        query_job = self.client.query(sql_query, job_config=job_config)
        
        # Wait for the query to complete
        results = query_job.result()
        
        # Generate filename with timestamp
        current_date = datetime.now()
        month = current_date.strftime("%m")  # Two-digit month
        year = current_date.strftime("%Y")   # Four-digit year
        
        # Standardize all filenames to yyyymm_name format
        if "yyyymm" in filename_pattern:
            # Already in correct format: 'yyyymm_name'
            filename = f"{filename_pattern.replace('yyyymm', f'{year}{month}')}.csv"
        else:
            # Convert from 'name_mm_yyyy' to 'yyyymm_name'
            # First remove any date patterns
            clean_name = filename_pattern.replace('mm_yyyy', '').replace('yyyy_mm', '')
            clean_name = clean_name.replace('mm', '').replace('yyyy', '')
            
            # Remove any leading or trailing underscores
            clean_name = clean_name.strip('_')
            
            # Create new standardized filename
            filename = f"{year}{month}_{clean_name}.csv"
            
        filepath = os.path.join(folder, filename)
        
        # Extract field names (column headers)
        field_names = [field.name for field in results.schema]
        
        # Progress bar will update automatically
            
        # Directly write to CSV without pandas
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(field_names)
            
            # Write data rows with progress bar
            row_count = 0
            for row in tqdm(results, desc=f"Writing to {filename}", 
                           unit="rows", leave=False):
                # Convert row to a list of values
                row_values = [row[field] for field in field_names]
                writer.writerow(row_values)
                row_count += 1
        
        return filepath
    
# Removed save_to_csv method as it's integrated into execute_legacy_query_and_save

def main():
    """
    Main function to run multiple BigQuery queries based on JSON configuration.
    """
    # Load query configurations from JSON
    try:
        with open('queries.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return
    
    # Initialize runner
    runner = QueryRunner()
    
    # Setup authentication (silently)
    if not runner.setup():
        print("Setup failed. Please run 'auth.py'")
        return
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Track successful and failed queries
    results = {
        "successful": [],
        "failed": []
    }
    
    # Process each folder with nested progress bars
    for folder_config in tqdm(config.get('folders', []), desc="Processing folders"):
        folder_name = folder_config.get('name', 'Unknown')
        folder_path = os.path.join(output_dir, folder_config.get('folder', 'default'))
        
        # Create folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Process each query in the folder
        for query_config in tqdm(folder_config.get('queries', []), 
                                desc=f"Processing {folder_name}", leave=False):
            try:
                # Get query parameters
                name = query_config.get('name', 'Query')
                filename_pattern = query_config.get('filename_pattern', 'data_mm_yyyy')
                legacy = query_config.get('legacy', False)
                
                # Check if using a template
                query = query_config.get('query')
                if not query and 'template' in query_config:
                    # Get template path
                    template_path = query_config.get('template')
                    
                    # Get appropriate date parameters based on template
                    params = get_date_params_by_template(template_path)
                    
                    # Load and substitute template
                    query = load_query_template(template_path, params)
                    if query is None:
                        raise Exception(f"Failed to load template: {template_path}")
                
                # Execute query and save results
                filepath = runner.execute_query_and_save(
                    sql_query=query,
                    folder=folder_path,
                    filename_pattern=filename_pattern,
                    legacy=legacy
                )
                
                # Record success
                results["successful"].append({
                    "folder": folder_name,
                    "name": name,
                    "file": filepath
                })
                
            except Exception as e:
                # Record failure
                results["failed"].append({
                    "folder": folder_name,
                    "name": name,
                    "error": str(e)
                })
    
    # Print summary
    print("\nExecution Summary:")
    
    if results["successful"]:
        print(f"\n✓ {len(results['successful'])} queries completed successfully:")
        # Group by folder
        by_folder = {}
        for item in results["successful"]:
            folder = item["folder"]
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(item)
        
        # Print by folder
        for folder, items in by_folder.items():
            print(f"\n  {folder}:")
            for item in items:
                print(f"    - {item['name']}: {item['file']}")
    
    if results["failed"]:
        print(f"\n⚠ {len(results['failed'])} queries failed:")
        # Group by folder
        by_folder = {}
        for item in results["failed"]:
            folder = item["folder"]
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(item)
        
        # Print by folder
        for folder, items in by_folder.items():
            print(f"\n  {folder}:")
            for item in items:
                print(f"    - {item['name']}: {item['error']}")
    
    # After all queries are completed, run key brand scripts if available
    print("\nRunning additional key brand data collection...")
    
    # Hard-coded month sets to ensure consistency
    months = {
        1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 
        7: "07", 8: "08", 9: "09", 10: "10", 11: "11", 12: "12"
    }
    
    # Get current year and month
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    
    # Calculate previous months consistently
    # If we're in month M, we want data for months M-3, M-2, and M-1
    # For example, if it's July (7), we want data for April (4), May (5), and June (6)
    end_month = current_month - 1 if current_month > 1 else 12
    end_year = current_year if current_month > 1 else current_year - 1
    
    start_month = current_month - 3 if current_month > 3 else current_month + 9
    start_year = current_year if current_month > 3 else current_year - 1
    
    # Format dates as YYYY-MM
    start_str = f"{start_year}-{months[start_month]}"
    end_str = f"{end_year}-{months[end_month]}"
    
    # Find the key_brands folder path
    key_brands_folder = None
    for folder_config in config.get('folders', []):
        if folder_config.get('folder') == "key_brands":
            key_brands_folder = os.path.join(output_dir, "key_brands")
            break
    
    if key_brands_folder:
        print(f"Running key brand scripts with date range: {start_str} to {end_str}")
        
        current_date = datetime.now()
        month = current_date.strftime("%m")  # Two-digit month
        year = current_date.strftime("%Y")   # Four-digit year
        yyyymm = f"{year}{month}"

        # Run each key brand script
        try:
            if key_brand_1:
                print("Running key brand script 1...")
                key_brand_1.run_key_brand_1(start_str, end_str, key_brands_folder)
        except Exception as e:
            print(f"Error running key brand script 1: {e}")
            
        try:
            if key_brand_2:
                print("Running key brand script 2...")
                key_brand_2.run_key_brand_2(start_str, end_str, key_brands_folder)
        except Exception as e:
            print(f"Error running key brand script 2: {e}")
            
        try:
            if key_brand_3:
                print("Running key brand script 3...")
                key_brand_3.run_key_brand_3(start_str, end_str, key_brands_folder)
        except Exception as e:
            print(f"Error running key brand script 3: {e}")
    else:
        print("Key brands folder not found in configuration, skipping additional scripts")

if __name__ == "__main__":
    main()
