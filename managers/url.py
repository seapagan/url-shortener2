import secrets
import string

import validators
from fastapi import HTTPException, status

from config.settings import get_settings
from database.db import database
from helpers.errors import raise_bad_request
from models.enums import RoleType
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
    async def increment_clicks(url_id: int):
        """Add one to the click total for this URL."""
        db_url = await database.fetch_one(
            URL.select().where(URL.c.id == url_id)
        )
        if db_url:
            await database.execute(
                URL.update()
                .where(URL.c.id == url_id)
                .values(clicks=db_url["clicks"] + 1)
            )

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
    async def list_redirects(user_do):
        """Return a list of the user's redirects."""
        if user_do["role"] == RoleType.admin:
            return await database.fetch_all(URL.select())
        else:
            return await database.fetch_all(
                URL.select().where(URL.c.user_id == user_do["id"])
            )

    @staticmethod
    async def peek_redirect(url_key: str):
        """Return the target url of the provided key, don't redirect."""
        if db_url := await database.fetch_one(
            URL.select().where(URL.c.key == url_key)
        ):
            return db_url
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="A Redirect with that code does not exist.",
            )

    @staticmethod
    async def edit_redirect(url_key: str, url: URLBase, user_do):
        """Edit an existing redirect."""
        if db_url := await database.fetch_one(
            URL.select().where(URL.c.key == url_key)
        ):
            if db_url["user_id"] == user_do.id or user_do.role == "admin":
                await database.execute(
                    URL.update()
                    .where(URL.c.id == db_url["id"])
                    .values(target_url=url.target_url)
                )
                url_base = get_settings().base_url
                return {
                    **db_url,  # type: ignore
                    "target_url": url.target_url,
                    "url": f"{url_base}/{url_key}",
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You do not have permission to do that.",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="A Redirect with that code does not exist.",
            )

    @staticmethod
    async def delete_redirect(url_key: str, user_do):
        """Delete the specified redirect, by key."""
        if db_url := await database.fetch_one(
            URL.select().where(URL.c.key == url_key)
        ):
            if db_url["user_id"] == user_do.id or user_do.role == "admin":
                await database.execute(
                    URL.delete().where(URL.c.id == db_url["id"])
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="You do not have permission to do that.",
                )

        else:
            raise HTTPException(
                status_code=404,
                detail="A Redirect with that code does not exist.",
            )
