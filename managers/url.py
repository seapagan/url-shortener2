import secrets
import string

import validators

from config.settings import get_settings
from database.db import database
from helpers.errors import raise_bad_request
from models.url import URL
from schemas.url import URLBase


def create_random_key(length: int = 5) -> str:
    """Return a random key of the specified length."""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


class URLManager:
    @staticmethod
    async def get_db_url_by_key(url_key: str):
        """Return a URL entry by it's key."""
        result = await database.fetch_one(
            URL.select().where(URL.c.key == url_key)
        )
        if result and result["is_active"] is not False:
            return result
        return None

    @staticmethod
    async def create_redirect(url: URLBase, user_id: int):
        """Create a new redirect with the provided URL"""
        if not validators.url(url.target_url):  # type: ignore
            raise_bad_request(message="Your provided URL is not Valid")

        key = create_random_key()
        while await URLManager.get_db_url_by_key(key):
            key = create_random_key()

        url_base = get_settings().base_url

        data = {
            "user_id": user_id,
            "key": key,
            "target_url": url.target_url,
            "is_active": True,
            "clicks": 0,
        }

        try:
            await database.execute(URL.insert().values({**data}))
        except Exception as e:
            raise_bad_request(message=str(e))

        return {
            **data,
            "url": f"{url_base}/{key}",
        }

    @staticmethod
    async def list_redirects(user_id: int):
        return await database.fetch_all(
            URL.select().where(URL.c.user_id == user_id)
        )
