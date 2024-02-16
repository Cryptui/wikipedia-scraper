import requests
import re
from bs4 import BeautifulSoup
import json
import logging



# The object should contain at least these six attributes
class WikipediaScraper:
    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com" # containing the base url of the API
        self.country_endpoint = "/countries" # endpoint to get the list of supported countries
        self.leaders_endpoint = "/leaders" # endpoint to get the list of leaders for a specific country
        self.cookies_endpoint = "/cookie" # endpoint to get a valid cookie to query the API
        self.leaders_data = {} # is a dictionary where you store the data you retrieve before saving it into the JSON file
        self.cookie = None # is the cookie object used for the API calls

    # The object should contain at least these five methods
    def refresh_cookie(self): 
        """
        Returns a new cookie if the cookie has expired
        Refresh the cookie used for API calls.
        """
        try:
            response = requests.get(self.base_url + self.cookies_endpoint)
            response.raise_for_status()  # Raise an exception for bad status codes
            self.cookie = response.cookies
        except requests.RequestException as e:
            logging.error("Failed to refresh cookie: %s", e)

    def get_countries(self):
        """
        Returns a list of the supported countries from the API
        Retrieve a list of supported countries from the API.
        Returns:
            list: A list of supported countries.
        """
        try:
            response = requests.get(self.base_url + self.country_endpoint, cookies=self.cookie)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error("Failed to get supported countries: %s", e)
            return []

    def get_leaders(self, country):
        """
        Populate the leaders_data object with the leaders of a country retrieved from the API.
        Args:
            country (str): The name of the country.
        """
        try:
            params = {"country": country}
            response = requests.get(self.base_url + self.leaders_endpoint, params=params, cookies=self.cookie)
            response.raise_for_status()
            leaders = response.json()
            # Update the leaders with first paragraph from Wikipedia
            for leader in leaders:
                leader['first_paragraph'] = self.get_first_paragraph(leader['wikipedia_url'])
            self.leaders_data[country] = leaders
        except requests.RequestException as e:
            logging.error("Failed to get leaders for country %s: %s", country, e)

    def to_json_file(self, filepath):
        """
        Store the data structure into a JSON file.

        Args:
            filepath (str): The path to the JSON file.
        """
        try:
            with open(filepath, "w") as file:
                json.dump(self.leaders_data, file)
            logging.info("Data saved to %s", filepath)
        except Exception as e:
            logging.error("Failed to save data to JSON file: %s", e)


    def get_first_paragraph(self, wikipedia_url):
        """
        Retrieve the first paragraph with details about the leader from a Wikipedia URL.

        Args:
            wikipedia_url (str): The URL of the Wikipedia page.

        Returns:
            str: The first paragraph with details about the leader, or an empty string if there's an error.
        """
        try:
            response = requests.get(wikipedia_url)
            response.raise_for_status()  # Raise an exception for bad status codes

            if response.status_code == 200:
                content = response.text
                start_index = content.find("<p>")
                end_index = content.find("</p>", start_index)
                return content[start_index + 3:end_index]

        except requests.RequestException as e:
            logging.error("Failed to get first paragraph from Wikipedia URL %s: %s", wikipedia_url, e)

        return ""