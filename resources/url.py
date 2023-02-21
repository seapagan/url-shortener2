"""Routes to manage URL's."""
from fastapi import APIRouter, Depends, Request

from managers.auth import oauth2_schema
from managers.url import URLManager
from schemas.url import URLBase, URLInfo

router = APIRouter(tags=["URL Management"], prefix="/url")


@router.get(
    "/list", dependencies=[Depends(oauth2_schema)], name="list_redirects"
)
async def list_redirects():
    """List all URL's for the logged in user.

    Admin users can see all, anon users see nothing.
    """
    pass


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
    "/edit/{url_key}",
    dependencies=[Depends(oauth2_schema)],
    name="edit_a_redirect",
)
async def edit_redirect(url_key: str):
    """Edit an existing URL entrys destination..

    For admin user only, can also edit the key.
    """
    pass


@router.get("/peek/{url_key}", name="peek_a_redirect")
async def peek_redirect(url_key: str):
    """Return the target of the URL redirect only.

    Anon users can access this.
    """
    pass
