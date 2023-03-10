"""Routes to manage URL's."""
from typing import List, Union

from fastapi import APIRouter, Depends, Request, status

from config.settings import get_settings
from managers.auth import oauth2_schema
from managers.url import URLManager
from schemas.url import AdminURLInfo, URLBase, URLInfo

router = APIRouter(tags=["URL Management"])


def add_url_to_response(item):
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
            AdminURLInfo(**add_url_to_response(item))  # type: ignore
            for item in url_list
        ]
    else:
        return [
            URLInfo(**add_url_to_response(item))  # type: ignore
            for item in url_list
        ]


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
    response_model=URLInfo,
)
async def edit_redirect(url: URLBase, url_key: str, request: Request):
    """Edit an existing URL entry destination."""
    return await URLManager.edit_redirect(url_key, url, request.state.user)


@router.get("/{url_key}/peek", name="peek_a_redirect", response_model=URLBase)
async def peek_redirect(url_key: str):
    """Return the target of the URL redirect only.

    Anon users can access this.
    """
    return await URLManager.peek_redirect(url_key)


@router.delete(
    "/{url_key}",
    name="remove_redirect",
    dependencies=[Depends(oauth2_schema)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_redirect(url_key: str, request: Request):
    """Delete the specified URL redirect."""
    return await URLManager.delete_redirect(url_key, request.state.user)


@router.post(
    "/{url_key}/deactivate",
    dependencies=[Depends(oauth2_schema)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deactivate_redirect(url_key: str, request: Request):
    """Deactivate the specified URL redirect."""
    return await URLManager.toggle_redirect(url_key, request.state.user, False)


@router.post(
    "/{url_key}/activate",
    dependencies=[Depends(oauth2_schema)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def activate_redirect(url_key: str, request: Request):
    """Activate the specified URL redirect."""
    return await URLManager.toggle_redirect(url_key, request.state.user, True)
