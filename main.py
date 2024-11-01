import os
import time
import logging
from typing import List, Dict, Set
from datetime import datetime, timedelta

from modules.gsheet import GSheet
from modules.selenium_wrapper import SeleniumWrapper
from modules.telegram import send_notification
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration constants with default values
DEFAULT_LOOP_FREQUENCY_MINUTES = 30
DEFAULT_NOTIFICATION_COOLDOWN_MINUTES = 60


class TicketAvailabilityChecker:
    def __init__(
        self,
        loop_frequency: int = DEFAULT_LOOP_FREQUENCY_MINUTES,
        notification_cooldown: int = DEFAULT_NOTIFICATION_COOLDOWN_MINUTES,
        telegram_bot_api_key: str = None,
        telegram_chat_id: str = None,
    ):
        """
        Initialize the ticket availability checker.

        Args:
            loop_frequency (int): Frequency of checking tickets in minutes.
            notification_cooldown (int): Cooldown period for repeated notifications in minutes.
            telegram_bot_api_key (str): Telegram bot API key.
            telegram_chat_id (str): Telegram chat ID for notifications.
        """
        self.loop_frequency = loop_frequency
        self.notification_cooldown = notification_cooldown
        self.telegram_bot_api_key = telegram_bot_api_key or os.getenv(
            "TELEGRAM_BOT_API_KEY"
        )
        self.telegram_chat_id = telegram_chat_id or os.getenv("TELEGRAM_CHAT_ID")

        # Track notification times for each link
        self.notification_timestamps: Dict[str, datetime] = {}

    def _extract_link_from_sheet(self, sheet_data: List[Dict]) -> List[str]:
        """
        Extract links from sheet data.

        Args:
            sheet_data (List[Dict]): Data from Google Sheet.

        Returns:
            List[str]: List of extracted links.
        """
        return [entry["link"] for entry in sheet_data if "link" in entry]

    def _check_ticket_quantities(self, spider: SeleniumWrapper, row) -> str:
        """
        Check ticket quantities for a given row.

        Args:
            spider (SeleniumWrapper): Selenium wrapper instance.
            row: Ticket row element.

        Returns:
            str: Ticket availability status.
        """
        quantity_elem = spider.find_element("td[class*='quantity']", parent=row)
        if quantity_elem:
            quantity_text = quantity_elem.text.strip().lower()
            if any(
                status in quantity_text
                for status in ["unavailable", "not available", "sold out"]
            ):
                return "Not available"
            return "Available"
        return "Not available"

    def _is_notification_allowed(self, link: str) -> bool:
        """
        Check if notification is allowed based on cooldown period.

        Args:
            link (str): Link to check notification status.

        Returns:
            bool: Whether notification is allowed.
        """
        if link not in self.notification_timestamps:
            return True

        last_notification_time = self.notification_timestamps[link]
        cooldown_period = timedelta(minutes=self.notification_cooldown)

        return datetime.now() - last_notification_time > cooldown_period

    def run(self):
        """
        Main method to run ticket availability checks in a loop.
        """
        spider = SeleniumWrapper()
        spider.setup_driver(headless=False)
        gsheet = GSheet(json_filename="sheet_reader_service_account.json")

        while True:
            try:
                sheet_data = gsheet.read_sheet(
                    filename="SEE tickets SOLD OUT", sheetname="Sheet1"
                )
                extracted_links = self._extract_link_from_sheet(sheet_data)

                for link in extracted_links:
                    if not self._is_notification_allowed(link):
                        logger.info(f"Skipping {link} - within notification cooldown")
                        continue

                    spider.get_page(link, sleep=5)
                    ticket_rows = spider.find_elements(selector="tr[class*='ticket']")

                    if not ticket_rows:
                        logger.info(f"No ticket rows found for {link}")
                        continue

                    quantities = [
                        self._check_ticket_quantities(spider, row)
                        for row in ticket_rows
                        if self._check_ticket_quantities(spider, row)
                    ]

                    is_eligible_to_notify = "Available" in quantities

                    if is_eligible_to_notify:
                        message = f"🎫 Tickets are now available!\n\nLink: {link}"
                        if send_notification(
                            message, self.telegram_bot_api_key, self.telegram_chat_id
                        ):
                            logger.info(f"Notification sent for {link}")
                            self.notification_timestamps[link] = datetime.now()
                        else:
                            logger.error(f"Failed to send notification for {link}")
                    else:
                        logger.info(f"No tickets available for {link}")

                # Sleep for the configured loop frequency
                logger.info(f"Sleeping for {self.loop_frequency} minutes...")
                time.sleep(self.loop_frequency * 60)

            except Exception as e:
                logger.error(f"An error occurred: {e}")
                time.sleep(self.loop_frequency * 60)  # Retry after loop frequency


def main():
    """
    Entry point for the ticket availability checker.
    """
    checker = TicketAvailabilityChecker(
        loop_frequency=5,  # Check every 30 minutes
        notification_cooldown=10,  # 60 minutes cooldown between notifications for the same link
    )
    checker.run()


if __name__ == "__main__":
    main()
