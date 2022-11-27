"""Modules"""
import logging
import os
import monobank
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from monobank import Client

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class SetMonoWebhook(Client):
    """Will install the webhook if the client does not have it"""

    @property
    def check_installed_webhook(self) -> bool:
        """
        Check if the webhook is installed

        :return: True if the webhook is installed, False otherwise
        :rtype: bool
        """
        try:
            if self.get_client_info().get('webHookUrl'):
                return True
        except monobank.Error as error:
            raise monobank.errors.Error("Unable to retrieve data", error)
        return False

    def install_webhook(self, url: str) -> dict:
        """
        Installs the webhook

        param url: The url of the webhook
        :type url: str
        """
        if not self.check_installed_webhook:
            try:
                self.create_webhook(url)
                logging.info("Webhook was created")
                return {"status": "created"}
            except monobank.errors.Error as error:
                raise monobank.Error("Unable to create webhook", error)
        logging.info("Webhook alive")
        return {"status": "success"}


def main():
    """Main function"""
    client = SetMonoWebhook(os.environ.get('MONOBANK_TOKEN'))
    client.install_webhook(os.environ.get('MONOBANK_WEBHOOK_URL'))


if __name__ == '__main__':
    # main()
    # Launch Scheduler
    scheduler = BlockingScheduler(timezone=pytz.timezone("Europe/Kiev"))

    # Каждые понедельник в 12:00
    scheduler.add_job(main, 'cron', day_of_week='mon', hour='12', minute="00")

    # Starting the daemon
    scheduler.start()
