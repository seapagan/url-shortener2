"""Routes to manage URL's."""
from typing import List

from fastapi import APIRouter, Depends, Request

from config.settings import get_settings
from managers.auth import oauth2_schema
from managers.url import URLManager
from schemas.url import AdminURLInfo, URLBase, URLInfo

router = APIRouter(tags=["URL Management"])


@router.get(
    "/list",
    dependencies=[Depends(oauth2_schema)],
    name="list_redirects",
    response_model=List[URLInfo],
)
async def list_redirects(request: Request):
    """List all URL's for the logged in user.

    Admin users can see all, anon users see nothing.
    """
    base_url = get_settings().base_url
    list_with_url = [
        {**item, "url": f"{base_url}/{item.key}"}  # type: ignore
        for item in await URLManager.list_redirects(request.state.user.id)
    ]
    return list_with_url


@router.post(
    "/create",
    dependencies=[Depends(oauth2_schema)],
    name="create_a_redirect",
    response_model=URLInfo,
)
async def create_redirect(url: URLBase, request: Request):
    """Create a new URL redirection belonging to the current User."""
    return await URLManager.create_redirect(url, request.state.user.id)


@router.post(
    "/{url_key}/edit",
    dependencies=[Depends(oauth2_schema)],
    name="edit_a_redirect",
)
async def edit_redirect(url_key: str):
    """Edit an existing URL entrys destination..

    For admin user only, can also edit the key.
    """
    pass


@router.get("/{url_key}/peek", name="peek_a_redirect")
async def peek_redirect(url_key: str):
    """Return the target of the URL redirect only.

    Anon users can access this.
    """
    pass
