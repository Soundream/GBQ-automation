-- Web Traffic SQL Template
-- Replace the date values when pasting your SQL from Google Sheets:
-- WHERE month BETWEEN "{{start_date}}" AND "{{end_date}}"

SELECT * from SimilarWeb.traffic_data
WHERE month BETWEEN "{{start_date}}" AND "{{end_date}}"
AND company_type IN ('Meta','OTA')
AND company IN ('Agoda', 'Almosafer', 'Aviasales', 'Booking.com', 'Cleartrip', 'Expedia', 'HotelsCombined', 'Ixigo', 'Jetcost', 'Kayak', 'Kojaro', 'MakeMyTrip', 'Momondo', 'Neredekal', 'Rome2Rio', 'Safarmarket', 'Skyscanner', 'Swoodoo', 'Travelstart', 'TripAdvisor', 'Trivago', 'Turismocity', 'Wego')
