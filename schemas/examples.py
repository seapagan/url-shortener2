"""Example data for Schemas."""


class ExampleUser:
    """Define a dummy user for Schema examples."""

    id = 25
    first_name = "John"
    last_name = "Doe"
    email = "user@example.com"
    password = "My S3cur3 P@ssw0rd"
    role = "user"
    banned = False


class ExampleURL:
    """Define an example URL response for the docs."""

    target_url = "https://github.com/seapagan"
    is_active = True
    clicks = 0
    url = "https://myredirector.com/a1b2c3"
