"""Import modules"""
import logging
import os
import time

# Outside modules
import monobank
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main function"""
    try:
        mono_client = monobank.Client(token=os.environ.get("MONOBANK_TOKEN"))
    except monobank.TooManyRequests as error:
        logging.error(error)
        time.sleep(10)
        mono_client = monobank.Client(token=os.environ.get("MONOBANK_TOKEN"))
        if not mono_client.get_client_info().get("webHookUrl"):
            mono_client.create_webhook(url=os.environ.get("MONOBANK_WEBHOOK_URL"))
            logging.info("Webhook was created")
        else:
            logging.info("Webhook is already installed")
    except monobank.Error as error:
        logging.error(monobank.Error("Wrong api token", error))


if __name__ == '__main__':
    main()
    # Launch Scheduler
    scheduler = BlockingScheduler(timezone=pytz.timezone("Europe/Kiev"))

    # Specified time
    scheduler.add_job(main, 'cron', hour='*/1')

    # Starting the daemon
    scheduler.start()
