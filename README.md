# FastAPI Application Template <!-- omit in toc -->

This a rewrite of my [URL Shortener](https://github.com/seapagan/url-shortener)
which was in turn based on and extended from an original tutorial from [Real
Python](https://realpython.com/courses/url-shortener-fastapi/).

The API uses the [FastAPI framework](https://fastapi.tiangolo.com/)

- [Functionality](#functionality)
- [Configuration](#configuration)
- [Development](#development)
  - [Set up a Virtual Environment](#set-up-a-virtual-environment)
  - [Install required Dependencies](#install-required-dependencies)
  - [Migrate the Database](#migrate-the-database)
  - [Add a user](#add-a-user)
  - [Run a development Server](#run-a-development-server)
- [Deploying to Production](#deploying-to-production)
- [Planned Functionality](#planned-functionality)
- [Contributing](#contributing)
- [Project Organization](#project-organization)
- [Provided Routes](#provided-routes)
  - [**`GET`** _/list_](#get-list)
  - [**`POST`** _/create_](#post-create)
  - [**`PATCH`** _/{url\_key}/edit_](#patch-url_keyedit)
  - [**`GET`** _/{url\_key}/peek_](#get-url_keypeek)
  - [**`DELETE`** _/{url\_key}_](#delete-url_key)
  - [**`GET`** _/users/_](#get-users)
  - [**`GET`** _/users/me_](#get-usersme)
  - [**`POST`** _/users/{user\_id}/make-admin_](#post-usersuser_idmake-admin)
  - [**`POST`** _/users/{user\_id}/password_](#post-usersuser_idpassword)
  - [**`POST`** _/users/{user\_id}/ban_](#post-usersuser_idban)
  - [**`POST`** _/users/{user\_id}/unban_](#post-usersuser_idunban)
  - [**`PUT`** _/users/{user\_id}_](#put-usersuser_id)
  - [**`DELETE`** _/users/{user\_id}_](#delete-usersuser_id)
  - [**`POST`** _/register/_](#post-register)
  - [**`POST`** _/login/_](#post-login)
  - [**`POST`** _/refresh/_](#post-refresh)
  - [**`GET`** _/verify/_](#get-verify)

## Functionality

This application currently has the same functionality as Version 1, with the
addition of User Authentication and Authorization. Anonymous users can use the
redirect functionality, but cannot add new redirects nor edit existing.

Full API documentation is available from the `/docs` route, which also allows to
test out the API.

Future plans are to add a user-friendly front end to this.

## Configuration

Database (and other) settings can be read from environment variables or from a
`.env` file in the project root. By default, these are only used for the
Database setup, Email settings and JWT Secret Key. See the
[.env.example](.env.example) file for how to use.

```ini
# The Base API Url. This is where your API wil be served from, and can be read
# in the application code. It has no effect on the running of the applciation
# but is an easy way to build a path for API responses. Defaults to
# http://localhost:8000
BASE_URL=http://localhost:8000

# Database Settings These must be changed to match your setup.
DB_USER=dbuser
DB_PASSWORD=my_secret_passw0rd
DB_ADDRESS=localhost
DB_PORT=5432
DB_NAME=my_database_name

# generate your own super secret key here, used by the JWT functions.
# 32 characters or longer, definately change the below!!
SECRET_KEY=123456

# List of origins that can access this API, separated by a comma, eg:
# CORS_ORIGINS=http://localhost,https://www.gnramsay.com
# If you want all origins to access (the default), use * or leave commented:
CORS_ORIGINS=*

# Email Settings
MAIL_USERNAME=test_username
MAIL_PASSWORD=s3cr3tma1lp@ssw0rd
MAIL_FROM=test@email.com
MAIL_PORT=587
MAIL_SERVER=mail.server.com
MAIL_FROM_NAME="Seapagan @ URL Redirector"
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
MAIL_USE_CREDENTIALS=True
MAIL_VALIDATE_CERTS=True
```

For a **PUBLIC API** (unless its going through an API gateway!), set
`CORS_ORIGINS=*`, otherwise list the domains (**and ports**) required. If you
use an API gateway of some nature, that will probably need to be listed.

To generate a good secret key you can use the below command on Linux or Mac:

```console
$ openssl rand -base64 32
xtFhsNhbGOJG//TAtDNtoTxV/hVDvssC79ApNm0gs7w=

```

If the database is not configured or cannot be reached, the Application will
disable all routes, print an error to the console, and return a a 500 status
code with a clear JSON message for all routes. This saves the ugly default
"Internal Server Error" from being displayed.

## Development

### Set up a Virtual Environment

It is always a good idea to set up dedicated Virtual Environment when you are
developing a Python application. If you use Poetry, this will be done
automatically for you when you run `poetry install`.

Otherwise, [Pyenv](https://github.com/pyenv/pyenv) has a
[virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin which is very
easy to use.

Also, check out this
[freeCodeCamp](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
tutorial or a similar
[RealPython](https://realpython.com/python-virtual-environments-a-primer/) one
for some great info. If you are going this (oldschool!) way, I'd recommend using
[Virtualenv](https://virtualenv.pypa.io/en/latest/) instead of the built in
`venv` tool (which is a subset of this).

### Install required Dependencies

The project has been set up using [Poetry](https://python-poetry.org/) to
organize and install dependencies. If you have Poetry installed, simply run the
following to install all that is needed.

```console
poetry install
```

If you do not (or cannot) have Poetry installed, I have provided an
auto-generated `requirements.txt` in the project root which you can use as
normal:

```console
pip install -r requirements.txt
```

I definately recommend using Poetry if you can though, it makes dealing with
updates and conflicts very easy.

If using poetry you now need to activate the VirtualEnv:

```console
poetry shell
```

### Migrate the Database

Make sure you have [configured](#configuration) the database. Then run the
following command to setup the database:

```console
alembic upgrade head
```

Everytime you add or edit a model, create a new migration then run the upgrade
as shown below:

```console
alembic revision -m "<My commit message>"
alembic upgrade head
```

Check out the [Alembic](https://github.com/sqlalchemy/alembic) repository for
more information on how to use (for example how to revert migrations).

### Add a user

It is possible to add Users to the database using the API itself, but you cannot
create an Admin user this way, unless you aready have an existing Admin user in
the database.

This template includes a command-line utility to create a new user and
optionally make them Admin at the same time:

```console
./api-admin user create
```

You will be asked for the new user's email etc, and if this should be an
Admin user (default is to be a standard non-admin User). These values can be
added from the command line too, for automated use. See the built in help for
details :

```console
$ ./api-admin user create --help
Usage: api-admin user create [OPTIONS]

  Create a new user.

  Values are either taken from the command line options, or interactively for
  any that are missing.

Options:
  -e, --email TEXT       [required]
  -f, --first_name TEXT  [required]
  -l, --last_name TEXT   [required]
  -p, --password TEXT    [required]
  -a, --admin TEXT       [required]
  --help                 Show this message and exit.
```

Note that any user added manually this way will automatically be verified (no
need for the confirmation email which will not be sent anyway.)

### Run a development Server

The [uvicorn](https://www.uvicorn.org/) ASGI server is automatically installed
when you install the project dependencies. This can be used for testing the API
during development. There is a built-in command to run this easily :

```console
./api-admin dev
```

This will by default run the server on <http://localhost:8000>, and reload after
any change to the source code. You can add options to change this

```console
$ ./api-admin dev --help

Usage: api-admin dev [OPTIONS]

  Run a development server from the command line.

  This will auto-refresh on any changes to the source in real-time.

Options:
  -h, --host TEXT       Define the interface to run the server on.  [default:
                        localhost]
  -p, --port INTEGER    Define the port to run the server on  [default: 8000]
  -r, --reload BOOLEAN  [default: True]
  --help                Show this message and exit.
```

If you need more control, you can run `uvicorn` directly :

```console
uvicorn main:app --reload
```

The above command starts the server running on <http://localhost:8000>, and it
will automatically reload when it detects any changes as you develop.

**Note: Neither of these are suitable to host a project in production, see the
next section for information.**

## Deploying to Production

There are quite a few ways to deploy a FastAPI app to production. There is a
very good discussion about this on the FastAPI [Deployment
Guide](https://fastapi.tiangolo.com/deployment/) which covers using Uvicorn,
Gunicorn and Containers.

My Personal preference is to serve with Gunicorn, using uvicorn workers behind
an Nginx proxy, though this does require you having your own server. There is a
pretty decent tutorial on this at
[Vultr](https://www.vultr.com/docs/how-to-deploy-fastapi-applications-with-gunicorn-and-nginx-on-ubuntu-20-04/).
For deploying to AWS Lambda with API Gateway, there is a really excellent Medium
post (and it's followup)
[Here](https://medium.com/towards-data-science/fastapi-aws-robust-api-part-1-f67ae47390f9),
or for AWS Elastic Beanstalk there is a very comprehensive tutorial at
[testdriven.io](https://testdriven.io/blog/fastapi-elastic-beanstalk/)

> Remember:  you still need to set up a virtual environment, install all the
> dependencies, setup your `.env` file (or use Environment variables if your
> hosting provider uses these - for example Vercel or Heroku) and set up and
> migrate your Database, exactly the same as for Develpment as desctribed above.

## Planned Functionality

See the [TODO.md](TODO.md) file for plans.

## Contributing

Please **do** feel free to open an Issue for any bugs or issues you find, or
even a Pull Request with solutions 😎

Likewise, I am very open to new feature Pull Requests!

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## Project Organization

This project has been deliberately laid out in a specific way. To avoid long
complicated files which are difficult to debug, functionality is separated out
in files and modules depending on the specific functionality.

[main.py](main.py) - The main controlling file, this should be as clean and
short as possible with all functionality moved out to modules.

[database/](/database) - This module controls database setup and configuration,
and should generally not need to be touched.

[config/](/config) - Handles the API settings and defaults, also the Metadata
customization. If you add more settings (for example in the `.env` file) you
should also add them to the [settings.py](config/settings.py) or
[metadata.py](config/metadata.py) with suitable defaults. Non-secret (or
depoloyment independent) settings should go in the `metadata` file, while
secrets (or deployment specific) should go in the `settings` and `.env` files

[commands/](/commands) - This directory can hold any commands you need to write,
for example populating a database, create a superuser or other housekeeping
tasks.

[managers/](/managers) - This directory contains individual files for each
'group' of functionality. They contain a Class that should take care of the
actual work needed for the routes. Check out the [auth.py](managers/auth.py) and
[user.py](managers/user.py)

[migrations/](/migrations) - We use
[Alembic](https://github.com/sqlalchemy/alembic) to handle the database
migrations. Check out their pages for more info. See instructions under
[Development](#development) for more info.

[models/](/models) - Any database models used should be defined here along with
supporting files (eq the [enums.py](models/enums.py)) used here. Models are
specified using the SQLAlchemy format, see [user.py](models/user.py) for an
example.

[resources/](/resources) - Contains the actual Route resources used by your API.
Basically, each grouped set of routes should have its own file, which then
should be imported into the [routes.py](resources/routes.py) file. That file is
automatically imported into the main application, so there are no more changes
needed. Check out the routes in [user.py](resources/user.py) for a good example.
Note that the routes contain minimal actual logic, instead they call the
required functionality from the Manager ([UserManager](managers/user.py) in this
case).

[schemas/](/schemas) - Contains all `request` and `response` schemas used in the
application, as usual with a separate file for each group. The Schemas are
defined as [Pydantic](https://pydantic-docs.helpmanual.io/) Classes.

[helpers/](/helpers) - Contains some helper functions that can be used across the
code base.

[static/](/static) - Any static files used by HTML templates for example CSS or
JS files.

[templates/](/templates) - Any HTML templates. We have one by default - used
only when the root of the API is accessed using a Web Browser (otherwise a
simple informational JSON response is returned). You can edit the template in
[index.html](templates/index.html) for your own API.

## Provided Routes

See below for a full list on implemented routes in this API.

For full info and to test the routes, you can go to the `/docs` path on a
running API for interactive Swagger (OpenAPI) Documentation.

<!-- openapi-schema -->

### **`GET`** _/list_

> List Redirects : _List all URL's for the logged in user._
>
> Admin users can see all, anon users see nothing.

### **`POST`** _/create_

> Create A Redirect : _Create a new URL redirection belonging to the current User._

### **`PATCH`** _/{url_key}/edit_

> Edit A Redirect : _Edit an existing URL entry destination._

### **`GET`** _/{url_key}/peek_

> Peek A Redirect : _Return the target of the URL redirect only._
>
> Anon users can access this.

### **`DELETE`** _/{url_key}_

> Remove Redirect : _Delete the specified URL redirect._

### **`GET`** _/users/_

> Get Users : _Get all users or a specific user by their ID._
>
> To get a specific User data, the requesting user must match the user_id, or
> be an Admin.
>
> user_id is optional, and if omitted then all Users are returned. This is
> only allowed for Admins.

### **`GET`** _/users/me_

> Get My User Data : _Get the current user's data only._

### **`POST`** _/users/{user_id}/make-admin_

> Make Admin : _Make the User with this ID an Admin._

### **`POST`** _/users/{user_id}/password_

> Change Password : _Change the password for the specified user._
>
> Can only be done by an Admin, or the specific user that matches the user_id.

### **`POST`** _/users/{user_id}/ban_

> Ban User : _Ban the specific user Id._
>
> Admins only. The Admin cannot ban their own ID!

### **`POST`** _/users/{user_id}/unban_

> Unban User : _Ban the specific user Id._
>
> Admins only.

### **`PUT`** _/users/{user_id}_

> Edit User : _Update the specified User's data._
>
> Available for the specific requesting User, or an Admin.
>
### **`DELETE`** _/users/{user_id}_

> Delete User : _Delete the specified User by user_id._
>
> Admin only.

### **`POST`** _/register/_

> Register A New User : _Register a new User and return a JWT token plus a Refresh Token._
>
> The JWT token should be sent as a Bearer token for each access to a
> protected route. It will expire after 120 minutes.
>
> When the JWT expires, the Refresh Token can be sent using the '/refresh'
> endpoint to return a new JWT Token. The Refresh token will last 30 days, and
> cannot be refreshed.

### **`POST`** _/login/_

> Login An Existing User : _Login an existing User and return a JWT token plus a Refresh Token._
>
> The JWT token should be sent as a Bearer token for each access to a
> protected route. It will expire after 120 minutes.
>
> When the JWT expires, the Refresh Token can be sent using the '/refresh'
> endpoint to return a new JWT Token. The Refresh token will last 30 days, and
> cannot be refreshed.

### **`POST`** _/refresh/_

> Refresh An Expired Token : _Return a new JWT, given a valid Refresh token._
>
> The Refresh token will not be updated at this time, it will still expire 30
> days after original issue. At that time the User will need to login again.

### **`GET`** _/verify/_

> Verify : _Verify a new user._
>
> The code is sent to  new user by email, which must then be validated here.
<!-- openapi-schema-end -->

The route table above was automatically generated from an `openapi.json` file by
my [openapi-readme](https://pypi.org/project/openapi-readme/) project. Check it
out for your own API documentation! 😊
