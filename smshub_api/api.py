import os
from dotenv import load_dotenv

import asyncio
import logging
import httpx

from settings.config import MAIN_URL

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class SmsHubAPI:
    """
    SmsHubAPI class for interacting with the SmsHub API.
    """

    def __init__(self):
        """
        Initialize the SmsHubAPI class.
        """
        self.main_url = MAIN_URL
        self.country = os.getenv("COUNTRY", 6)  # Default country code to 6 if not provided in .env

    async def get_balance(self):
        """
        Get balance from smshub.org

        :return: string: balance available on the smshub account
        """
        url = f'{self.main_url}getBalance'
        try:
            response = await httpx.AsyncClient().get(url)
            logger.info(f'Balance requested: {response.text}')
            return response.text[15:]
        except Exception as e:
            logger.error(e)
            return e

    async def get_number(self, service):
        """
        Get phone number from smshub.org for the specified service and country.

        :param service: string: service for which the number is needed
        :return: tuple: phone number and its id, or error message
        in case of issues
        """
        url = f'{self.main_url}getNumber&service={service}&country={self.country}'
        try:
            response = await httpx.AsyncClient().get(url)
            logger.info(f'Number requested: {response.text}')
            if response.text == 'NO_NUMBERS':
                return 'Numbers are over'
            elif response.text == 'NO_BALANCE':
                return 'Not enough money'
            number_id = response.text[14:23]
            number = response.text[24:38]
            return number, number_id
        except Exception as e:
            logger.error(e)
            return e
