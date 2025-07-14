import requests
import pandas as pd
from datetime import datetime

API_KEY = "750d7fbbecb63b26a4c839a781299b65"

# Date range (TODO: adjust as needed)
START_DATE = "2025-03"
END_DATE = "2025-06"

# Function wrapper to allow parameters from main file
def run_key_brand_3(start_date=None, end_date=None, yyyymm=None, output_folder=""):
    # Use parameters if provided, otherwise use defaults
    _start_date = start_date if start_date else START_DATE
    _end_date = end_date if end_date else END_DATE

    # List of companies and their domains
    companies_and_domains = {   "Wego": ["wego.com", "wego.com.bd", "wego.com.ng", "wego.com.ph", "wego.ir", "wego.lk", "wego.ly", "wego.pk", "wego.ps", "wego.qa", "wego.sd", "wegotravel.ma", "wego.ae", "wego.com.au", "wegoviajar.com.br", "wegotravel.ca", "wegotravel.ch", "wego.cl"],
       "Airbnb": ["airbnb.cat", "airbnb.co.cr", "airbnb.co.ve", "airbnb.com.bo", "airbnb.com.bz", "airbnb.com.ec", "airbnb.com.gt", "airbnb.com.hn", "airbnb.com.mt", "airbnb.com.ni", "airbnb.com.pa", "airbnb.com.pe", "airbnb.com.py", "airbnb.com.sv", "airbnb.cz", "airbnb.gy", "airbnb.hu", "airbnb.is", "airbnb.com.ar", "airbnb.at", "airbnb.com.au", "airbnb.be", "airbnb.com.br", "airbnb.ca", "airbnb.ch", "airbnb.cl", "airbnb.com.co", "airbnb.de", "airbnb.dk", "airbnb.es", "airbnb.fi", "airbnb.fr", "airbnb.gr", "airbnb.com.hk", "airbnb.co.id", "airbnb.ie", "airbnb.co.in", "airbnb.it", "airbnb.jp", "airbnb.co.kr", "airbnb.mx", "airbnb.com.my", "airbnb.nl", "airbnb.no", "airbnb.co.nz", "airbnb.pl", "airbnb.pt", "airbnb.ru", "airbnb.se", "airbnb.com.sg", "airbnb.com.tr", "airbnb.com.tw", "airbnb.co.uk", "airbnb.com"],
       "Booking.com": ["booking.hr", "booking.lv", "booking.cn", "booking.com", "bookingkhazana.com", "flybooking.com", "fastbooking.com", "guindaisbooking.com"],
       "Expedia": ["expedia.co.th", "expedia.com.ph", "expedia.com.ar", "expedia.at", "expedia.com.au", "expedia.be", "expedia.com.br", "expedia.ca", "expedia.ch", "expedia.cn", "expedia.de", "expedia.dk", "expedia.es", "expedia.fi", "expedia.fr", "expedia.com.hk", "expedia.co.id", "expedia.ie", "expedia.co.in", "expedia.it", "expedia.co.jp", "expedia.co.kr", "expedia.com.mx", "expedia.mx", "expedia.com.my", "expedia.nl", "expedia.no", "expedia.co.nz", "expedia.se", "expedia.com.sg", "expedia.com.tw", "expedia.co.uk", "expedia.com.vn", "expedia.com"],
       "Trivago": ["trivago.bg", "trivago.co.th", "trivago.com.ph", "trivago.com.uy", "trivago.cz", "trivago.hr", "trivago.hu", "trivago.pe", "trivago.ro", "trivago.rs", "trivago.si", "trivago.sk", "trivago.ae", "trivago.com.ar", "trivago.at", "trivago.com.au", "trivago.be", "trivago.com.br", "trivago.ca", "trivago.ch", "trivago.cl", "trivago.com.co", "trivago.de", "trivago.dk", "trivago.es", "trivago.fi", "trivago.fr", "trivago.gr", "trivago.hk", "trivago.co.id", "trivago.ie", "trivago.co.il", "trivago.in", "trivago.it", "trivago.jp", "trivago.co.kr", "trivago.com.mx", "trivago.com.my", "trivago.nl", "trivago.no", "trivago.co.nz", "trivago.pl", "trivago.pt", "trivago.ru", "trivago.se", "trivago.sg", "trivago.com.tr", "trivago.com.tw", "trivago.co.uk", "trivago.vn", "trivago.co.za", "trivago.com", "youzhan.com"],
       "Ixigo": ["ixigo.com"],
       "Almosafer": ["almosafer.com", "almosafr.com"],
       "Agoda": ["agoda.co.th", "agoda.com.cn", "agoda.com.hk", "agoda.co.id", "agoda.com.my", "agoda.com.sg", "agoda.com.tw", "agoda.com.vn", "agoda.vn", "agoda.com", "agoda.net"],
       "TripAdvisor": ["tripadvisor.co.hu", "tripadvisor.com.eg", "tripadvisor.com.pe", "tripadvisor.com.ph", "tripadvisor.com.ve", "tripadvisor.cz", "tripadvisor.rs", "tripadvisor.sk", "tripadvisor.com.ar", "tripadvisor.at", "tripadvisor.com.au", "tripadvisor.be", "tripadvisor.com.br", "tripadvisor.ca", "tripadvisor.ch", "tripadvisor.cl", "tripadvisor.cn", "tripadvisor.co", "tripadvisor.de", "tripadvisor.dk", "tripadvisor.es", "tripadvisor.fi", "tripadvisor.fr", "tripadvisor.com.gr", "tripadvisor.com.hk", "tripadvisor.co.id", "tripadvisor.ie", "tripadvisor.co.il", "tripadvisor.in", "tripadvisor.it", "tripadvisor.jp", "tripadvisor.co.kr", "tripadvisor.com.mx", "tripadvisor.com.my", "tripadvisor.nl", "tripadvisor.co.nz", "tripadvisor.pt", "tripadvisor.ru", "tripadvisor.se", "tripadvisor.com.sg", "tripadvisor.com.tr", "tripadvisor.com.tw", "tripadvisor.tw", "tripadvisor.co.uk", "tripadvisor.com.vn", "tripadvisor.co.za", "bookingbuddy.com", "tripadvisor.com", "tripadvisorsupport.com"],
       "MakeMyTrip": ["makemytrip.ae", "makemytrip.co.in", "makemytrip.in", "makemytrip.com", "makemytrip.net"],
       "Skyscanner": ["skyscanner.co.th", "skyscanner.com.ph", "skyscanner.com.ua", "skyscanner.cz", "skyscanner.gg", "skyscanner.hu", "skyscanner.ne", "skyscanner.ro", "skyscanner.ae", "skyscanner.at", "skyscanner.com.au", "skyscanner.com.br", "skyscanner.ca", "skyscanner.ch", "skyscanner.de", "skyscanner.dk", "skyscanner.es", "skyscanner.fi", "skyscanner.fr", "skyscanner.com.hk", "skyscanner.co.id", "skyscanner.ie", "skyscanner.co.il", "skyscanner.co.in", "skyscanner.it", "skyscanner.jp", "skyscanner.co.kr", "skyscanner.com.my", "skyscanner.com.nl", "skyscanner.nl", "skyscanner.no", "skyscanner.co.nz", "skyscanner.pl", "skyscanner.pt", "skyscanner.ru", "skyscanner.com.sa", "skyscanner.se", "skyscanner.com.sg", "skyscanner.com.tr", "skyscanner.com.tw", "skyscanner.com.vn", "skyscanner.com", "skyscanner.ru.com", "tianxun.com", "skyscanner.net"],
       "Trip.com": ["trip.com"],
    }

    # Headers for the API request
    headers = {"accept": "application/json"}

    # Base URL for deduplicated audiences and total visits
    BASE_URL_DEDUP = "https://api.similarweb.com/v1/website/{}/dedup/deduplicated-audiences"
    BASE_URL_VISITS = "https://api.similarweb.com/v1/website/{}/total-traffic-and-engagement/visits"

    # Data storage
    data_records = []

    # Fetch data for each company and their domains
    for company, domains in companies_and_domains.items():
       for domain in domains:
           # Fetch deduplicated audience data
           url_dedup = f"{BASE_URL_DEDUP}?api_key={API_KEY}&start_date={_start_date}&end_date={_end_date}&country=world&main_domain_only=false&format=json".format(domain)

           # Fetch total visits data
           url_visits = f"{BASE_URL_VISITS}?api_key={API_KEY}&start_date={_start_date}&end_date={_end_date}&country=world&granularity=monthly&main_domain_only=false&format=json".format(domain)

           try:
               # Fetch deduplicated audience data
               response_dedup = requests.get(url_dedup, headers=headers)
               dedup_data = response_dedup.json()

               # Fetch total visits data
               response_visits = requests.get(url_visits, headers=headers)
               visits_data = response_visits.json()

               # Extract relevant data
               dedup_dates = {entry["date"]: entry["dedup_data"]["total_deduplicated_audience"] for entry in dedup_data.get("data", [])}
               visit_dates = {entry["date"]: entry["visits"] for entry in visits_data.get("visits", [])}

               # Combine data for matching dates
               for date in dedup_dates:
                   formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
                   dedup_audience = dedup_dates.get(date, 0)
                   total_visits = visit_dates.get(date, 0)

                   data_records.append({
                       "Month": formatted_date,
                       "Company": company,
                       "Domain": domain,
                       "Deduplicated Audience": dedup_audience,
                       "Total Visits": total_visits
                   })

           except Exception as e:
               print(f"Error fetching data for {domain}: {e}")

    # Create a DataFrame
    df = pd.DataFrame(data_records)

    # Group data by company and month, summing deduplicated audience and total visits
    grouped_df = df.groupby(["Month", "Company"]).agg({
       "Deduplicated Audience": "sum",
       "Total Visits": "sum"
    }).reset_index()

    # Calculate Unique Visit Growth from Last Month
    grouped_df["Unique Visit Growth from Last Month"] = grouped_df.groupby("Company")["Deduplicated Audience"].pct_change().fillna(0)

    # Set output file path
    if output_folder:
        if yyyymm:
            output_file = f"{output_folder}/{yyyymm}_similarweb_audience_and_visits.csv" 
        else:
            output_file = f"{output_folder}/similarweb_audience_and_visits.csv" 
    else:
        if yyyymm:
            output_file = f"{yyyymm}_similarweb_audience_and_visits.csv" 
        else:
            output_file = "similarweb_audience_and_visits.csv"
    
    # Save the output to a CSV file
    grouped_df.to_csv(output_file, index=False)

    print(f"Data has been saved to {output_file}")
    return output_file

# Run the script if it's executed directly (for backward compatibility)
if __name__ == "__main__":
    run_key_brand_3()
