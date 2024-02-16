from src.scraper import WikipediaScraper
import logging

def main():
    # Set up logging configuration
    logging.basicConfig(level=logging.INFO)

    try:
        # Create a WikipediaScraper object
        scraper = WikipediaScraper()

        # Refresh the cookie
        scraper.refresh_cookie()

        # Get the supported countries
        countries = scraper.get_countries()
        logging.info("Supported countries: %s", countries)

        # Populate leaders data for each country
        for country in countries:
            scraper.get_leaders(country)

        # Save the data into a JSON file
        scraper.to_json_file("leaders_data.json")
        logging.info("Data saved to leaders_data.json")

    except Exception as e:
        logging.error("An error occurred: %s", e)

if __name__ == "__main__":
    main()