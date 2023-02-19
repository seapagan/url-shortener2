"""Define the URL model."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from database.db import metadata

URL = Table(
    "urls",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("key", String, unique=True, index=True, nullable=False),
    Column("target_url", String, index=True, nullable=False),
    Column("is_active", Boolean, default=True),
    Column("clicks", Integer, default=0),
)
