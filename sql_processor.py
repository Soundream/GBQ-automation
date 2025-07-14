#!/usr/bin/env python3
"""
SQL Processor
Module for handling SQL templates and parameter substitution.
"""

import os
from datetime import datetime, timedelta

def load_query_template(template_path, params):
    """
    Load SQL template and substitute parameters
    
    Args:
        template_path (str): Template file path
        params (dict): Parameter dictionary
        
    Returns:
        str: SQL query with parameters substituted
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
            
        # Replace parameters
        for param_name, param_value in params.items():
            placeholder = "{{" + param_name + "}}"
            template = template.replace(placeholder, param_value)
            
        return template
    except Exception as e:
        print(f"Error loading template {template_path}: {e}")
        return None

def calculate_date_range(format_with_dash=True):
    """
    Calculate the date range:
    - End date: First day of previous month
    - Start date: First day of month from 2 years ago
    
    Args:
        format_with_dash (bool): If True, return dates in 'YYYY-MM-DD' format, 
                                 if False, return in 'YYYYMMDD' format
    
    Returns:
        tuple: (start_date, end_date) in specified format
    """
    today = datetime.now()
    
    # End date: First day of previous month
    if today.month == 1:
        end_month = 12
        end_year = today.year - 1
    else:
        end_month = today.month - 1
        end_year = today.year
    
    # Start date: 2 years before the end date (same month)
    start_year = end_year - 2
    start_month = end_month
    
    # Format dates according to the requested format
    if format_with_dash:
        start_date = f"{start_year}-{start_month:02d}-01"
        end_date = f"{end_year}-{end_month:02d}-01"
    else:
        start_date = f"{start_year}{start_month:02d}01"
        end_date = f"{end_year}{end_month:02d}01"
    
    return start_date, end_date

def get_date_params_by_template(template_name):
    """
    Get appropriate date parameters based on the template name
    
    Args:
        template_name (str): Name of the template file
        
    Returns:
        dict: Dictionary with date parameters in appropriate format
    """
    # Determine which format to use based on template name
    if "appannie_app_ratings" in template_name.lower():
        # App Annie uses dates without dashes
        start_date, end_date = calculate_date_range(format_with_dash=False)
    else:
        # Default format with dashes
        start_date, end_date = calculate_date_range(format_with_dash=True)
    
    return {
        'start_date': start_date,
        'end_date': end_date
    } 