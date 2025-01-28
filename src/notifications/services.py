import logging

import requests

from src.config import app_settings

logger = logging.getLogger(__name__)


def send_telegram(message: str, chat_id: str) -> None:
    """ Sends a message via Telegram API."""
    url = app_settings.telegram.TELEGRAM_URL
    token = app_settings.telegram.TELEGRAM_API_TOKEN
    try:
        response = requests.post(url=f'{url}{token}/sendMessage?chat_id={chat_id}&text={message}')
        response.raise_for_status()
        logger.info(f"Telegram message sent to chat_id {chat_id}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message to chat_id {chat_id}: {str(e)}")
        raise RuntimeError(f"Telegram delivery error: {str(e)}")
