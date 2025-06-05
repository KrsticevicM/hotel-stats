import csv
import re

input_file = "hotel_booking.csv"
output_file = "hotel_bookings.nt"

def sanitize_literal(value):
    if not value:
        return ""
    value = value.replace("\\", "\\\\").replace('"', "'").strip()
    value = re.sub(r'[^\x20-\x7EÀ-ÿ]', '', value)  # Quitar basura
    return value

with open(input_file, newline='', encoding='utf-8-sig', errors='replace') as csvfile:
    reader = csv.DictReader(csvfile)
    with open(output_file, "w", encoding='utf-8') as out:
        for i, row in enumerate(reader):
            booking_uri = f"<http://example.org/booking/{i+1}>"

            def triple(pred, val, datatype=None, is_uri=False):
                if val is None or val == "":
                    return
                val = sanitize_literal(val)
                if is_uri:
                    out.write(f"{booking_uri} {pred} <{val}> .\n")
                elif datatype:
                    out.write(f"{booking_uri} {pred} \"{val}\"^^<{datatype}> .\n")
                else:
                    out.write(f"{booking_uri} {pred} \"{val}\" .\n")

            triple("<http://schema.org/hotel>", row["hotel"])
            triple("<http://example.org/isCanceled>", row["is_canceled"], "http://www.w3.org/2001/XMLSchema#boolean")
            triple("<http://example.org/leadTime>", row["lead_time"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://schema.org/arrivalDateYear>", row["arrival_date_year"], "http://www.w3.org/2001/XMLSchema#gYear")
            triple("<http://schema.org/arrivalDateMonth>", row["arrival_date_month"])
            triple("<http://example.org/arrivalDay>", row["arrival_date_day_of_month"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://example.org/arrivalWeek>", row["arrival_date_week_number"], "http://www.w3.org/2001/XMLSchema#integer")

            triple("<http://example.org/weekNights>", row["stays_in_week_nights"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://example.org/weekendNights>", row["stays_in_weekend_nights"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://schema.org/numberOfAdults>", row["adults"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://example.org/children>", row["children"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://example.org/babies>", row["babies"], "http://www.w3.org/2001/XMLSchema#integer")

            triple("<http://schema.org/meal>", row["meal"])
            triple("<http://schema.org/addressCountry>", row["country"])
            triple("<http://example.org/marketSegment>", row["market_segment"])
            triple("<http://example.org/distributionChannel>", row["distribution_channel"])
            triple("<http://example.org/isRepeatedGuest>", row["is_repeated_guest"], "http://www.w3.org/2001/XMLSchema#boolean")

            triple("<http://example.org/reservedRoomType>", row["reserved_room_type"])
            triple("<http://example.org/assignedRoomType>", row["assigned_room_type"])
            triple("<http://example.org/depositType>", row["deposit_type"])
            triple("<http://example.org/adr>", row["adr"], "http://www.w3.org/2001/XMLSchema#float")
            triple("<http://example.org/carParkingSpaces>", row["required_car_parking_spaces"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://example.org/specialRequests>", row["total_of_special_requests"], "http://www.w3.org/2001/XMLSchema#integer")
            triple("<http://example.org/reservationStatus>", row["reservation_status"])
            triple("<http://example.org/reservationStatusDate>", row["reservation_status_date"], "http://www.w3.org/2001/XMLSchema#date")
            triple("<http://example.org/customerType>", row["customer_type"])

            triple("<http://example.org/name>", row["name"], "http://www.w3.org/2001/XMLSchema#string")
