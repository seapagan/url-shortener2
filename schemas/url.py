"""Setup the model schemas."""
from typing import List

from pydantic import BaseModel, Field

from schemas.examples import ExampleURL


class URLBase(BaseModel):
    """Define URLBase class."""

    target_url: str = Field(example=ExampleURL.target_url)

    class Config:
        """Set config for this class."""

        orm_mode = True


class URL(URLBase):
    """Define URL class."""

    is_active: bool = Field(example=ExampleURL.is_active)
    clicks: int = Field(example=ExampleURL.clicks)


class URLListItem(URLBase):
    """A single URL item, with extra 'url' field."""

    url: str = Field(example=ExampleURL.url)


class URLList(BaseModel):
    """List of URLs."""

    urls: List[URLListItem]


class URLInfo(URL):
    """Define URLInfo class."""

    url: str = Field(example=ExampleURL.url)
