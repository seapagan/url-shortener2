"""Routes to manage URL's."""
from typing import List, Union

from fastapi import APIRouter, Depends, Request

from config.settings import get_settings
from managers.auth import oauth2_schema
from managers.url import URLManager
from schemas.url import AdminURLInfo, URLBase, URLInfo

router = APIRouter(tags=["URL Management"])


def add_url(item):
    """Adds a generated URL to the response."""
    base_url = get_settings().base_url
    return {**item, "url": f"{base_url}/{item.key}"}


@router.get(
    "/list",
    dependencies=[Depends(oauth2_schema)],
    name="list_redirects",
    response_model=Union[List[AdminURLInfo], List[URLInfo]],
    response_model_exclude_unset=True,
)
async def list_redirects(request: Request):
    """List all URL's for the logged in user.

    Admin users can see all, anon users see nothing.
    """
    url_list = await URLManager.list_redirects(request.state.user)
    if request.state.user.role == "admin":

        return [
            AdminURLInfo(**add_url(item)) for item in url_list  # type: ignore
        ]
    else:
        return [URLInfo(**add_url(item)) for item in url_list]  # type: ignore


@router.post(
    "/create",
    dependencies=[Depends(oauth2_schema)],
    name="create_a_redirect",
    response_model=URLInfo,
)
async def create_redirect(url: URLBase, request: Request):
    """Create a new URL redirection belonging to the current User."""
    return await URLManager.create_redirect(url, request.state.user.id)


@router.patch(
    "/{url_key}/edit",
    dependencies=[Depends(oauth2_schema)],
    name="edit_a_redirect",
)
async def edit_redirect(url_key: str):
    """Edit an existing URL entrys destination..

    For admin user only, can also edit the key.
    """
    pass


@router.get("/{url_key}/peek", name="peek_a_redirect", response_model=URLBase)
async def peek_redirect(url_key: str):
    """Return the target of the URL redirect only.

    Anon users can access this.
    """
    return await URLManager.peek_redirect(url_key)
