# Bina.az Sale Property Scraper

A high-performance asynchronous web scraper for extracting property listings from bina.az using Python's asyncio and aiohttp libraries.

## Features

- **Asynchronous scraping** with asyncio and aiohttp for maximum performance
- **Pagination support** with automatic cursor-based navigation through all pages
- **Comprehensive data extraction** of all property fields including:
  - Property details (area, rooms, floor, etc.)
  - Location information (city, district)
  - Pricing data
  - Company/agent information
  - Property features (mortgage, repair status, etc.)
  - Photo URLs
  - Metadata
- **Multiple output formats**: JSON and CSV
- **Robust error handling** with automatic retry logic
- **Rate limiting** to respect server resources
- **Progress tracking** with detailed logging
- **Statistics generation** for scraped data

## Requirements

- Python 3.7+
- aiohttp
- asyncio

## Installation

1. Clone the repository or download the files:
```bash
cd bina_az
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper:
```bash
python sale.py
```

The scraper will:
1. Connect to the bina.az GraphQL API
2. Scrape all sale property listings
3. Save data to both JSON and CSV formats in the `data/` directory
4. Display statistics about the scraped data

### Output Files

The scraper creates the following files in the `data/` directory:

- `bina_sale_YYYYMMDD_HHMMSS.json` - Complete data in JSON format
- `bina_sale_YYYYMMDD_HHMMSS.csv` - Complete data in CSV format
- `scraper.log` - Detailed log file with scraping progress and any errors

## Data Fields Extracted

The scraper extracts the following fields for each property:

### Basic Information
- `id` - Property ID
- `area_value` - Property area size
- `area_units` - Area units (usually m²)
- `leased` - Whether the property is leased
- `floor` - Floor number
- `floors` - Total floors in building
- `rooms` - Number of rooms

### Location
- `city_id` - City ID
- `city_name` - City name
- `location_id` - District/location ID
- `location_name` - District/location name
- `location_full_name` - Full location name

### Price
- `price_value` - Property price
- `price_currency` - Currency (usually AZN)

### Company/Agent
- `company_id` - Company/agent ID
- `company_name` - Company/agent name
- `company_target_type` - Type (AGENCY, RESIDENCE, etc.)

### Features
- `has_mortgage` - Mortgage availability
- `has_bill_of_sale` - Bill of sale status
- `has_repair` - Repair status
- `paid_daily` - Daily payment option
- `is_business` - Business listing flag

### Promotion
- `vipped` - VIP status
- `featured` - Featured listing status

### Metadata
- `updated_at` - Last update timestamp
- `path` - Relative URL path
- `photos_count` - Number of photos
- `photos` - JSON array of photo URLs
- `url` - Full URL to property page
- `scraped_at` - Scraping timestamp

## Configuration

You can modify the scraper behavior by editing the class constants in `sale.py`:

```python
ITEMS_PER_PAGE = 50              # Items per page (increase for faster scraping)
MAX_CONCURRENT_REQUESTS = 5      # Maximum concurrent requests
RETRY_ATTEMPTS = 3               # Number of retry attempts on failure
RETRY_DELAY = 2                  # Delay between retries (seconds)
```

## Performance

- Uses asynchronous requests for optimal speed
- Implements semaphore-based rate limiting to avoid overwhelming the server
- Automatic retry logic for failed requests
- Efficient memory usage with streaming data processing

## Error Handling

The scraper includes comprehensive error handling:
- Automatic retries for failed requests
- Timeout handling
- Connection error recovery
- Detailed error logging

## Logging

All operations are logged to:
- Console output (INFO level)
- `scraper.log` file (detailed logging)

## Statistics

After scraping, the tool displays statistics including:
- Total items scraped
- Items with photos, mortgage, repair, etc.
- Price range and average
- Area range and average
- City distribution
- Room distribution

## Example Output

```
================================================================================
Bina.az Sale Property Scraper
================================================================================
2025-11-17 15:00:00 - INFO - Starting scrape...
2025-11-17 15:00:00 - INFO - Fetching page 1...
2025-11-17 15:00:01 - INFO - Total items to scrape: 73199
2025-11-17 15:00:01 - INFO - Scraped 50 / 73199 items
...
2025-11-17 15:30:00 - INFO - Scraping completed! Total items scraped: 73199

================================================================================
SCRAPING STATISTICS
================================================================================
Total items scraped: 73199
Items with photos: 71543
Items with mortgage: 15234
Items with repair: 58932
VIP items: 8234
Featured items: 3421
Business listings: 45678

Price range: 25,000 - 5,000,000 AZN
Average price: 185,430 AZN

Area range: 25.0 - 500.0 m²
Average area: 95.3 m²

Top cities:
  Bakı: 68234 listings
  Sumqayıt: 2145 listings
  ...
================================================================================
```

## Notes

- The scraper respects server resources by implementing rate limiting
- Scraping large amounts of data may take time depending on total listings
- Ensure you have sufficient disk space for the output files
- The scraper only targets sale properties (leased: false)

## Troubleshooting

### Connection Errors
If you encounter connection errors, check your internet connection and try increasing the `RETRY_DELAY`.

### Rate Limiting
If you get rate-limited, reduce `MAX_CONCURRENT_REQUESTS` and add delays between pages.

### Memory Issues
For very large datasets, consider processing data in batches or reducing `ITEMS_PER_PAGE`.

## License

This project is provided as-is for educational and research purposes.

## Disclaimer

Please ensure you comply with bina.az's terms of service and robots.txt when using this scraper. Use responsibly and respect the website's resources.
