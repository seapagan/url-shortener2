"""This file contains Custom Metadata for your API Project.

Be aware, this will be re-generated any time you run the
'api-admin custom metadata' command!
"""
from config.helpers import MetadataBase

custom_metadata = MetadataBase(
    title="URL Shortener2",
    description="A URL-Shortener written in Python with FastAPI",
    repository="https://github.com/seapagan/url-shortener2",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    contact={
        "name": "Grant Ramsay (seapagan)",
        "url": "https://www.gnramsay.com",
    },
    email="seapagan@gmail.com",
    year="2023",
)
