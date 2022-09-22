# Django GraphQL (Setup)!

Django GraphQL, in this repo I am going to write all the steps needed to start your first GraphQL api with **django<4**.

## Installation

- First you will need to install [poetry](https://python-poetry.org/docs/)
- Then install [pyenv](https://github.com/pyenv/pyenv#getting-pyenv)
- Then go to your file directory where you want your project to be in and run `poetry init`
- Then use python 3.9.13 by running `pyenv local 3.9.13`
- Then install django using `poetry add "dajngo<4"`
- Then start a django project by running `poetry run django-admin startproject YOUR_APP_NAME .` - Don't forget the dot at the end!

## Manage shortcut

- Add this script in **pyproject.toml**

```
	 [tool.poetry.scripts]
	 manage = "manage:main"
```

- Then add this line of code in manage file

```
	sys.argv[0] = "manage.py"
	execute_from_command_line(sys.argv)
```

Instead of this `execute_from_command_line(sys.argv)`

## Switch to psql database

- First install these libraries by running this code
  `poetry add python-decouple dj-database-url psycopg2 django-stubs`
- Then import these in the **settings** file

```
	import django_stubs_ext
	from decouple import UndefinedValueError, config
	from dj_database_url import parse as db_url
```

- Edit the **SECRET_KEY** to be
  `SECRET_KEY = config("SECRET_KEY", default="django-insecure--(=_(29t6nzet-h3m@#_%r)m#vj164r5pywclb)s!=-%39z-_(")`

- Edit **DEBUG** to be
  `DEBUG = config("DEBUG", default=False, cast=bool)`
- Edit **DATABASE** to be

```
	DATABASES = {
		"default": config(
			"DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3", cast=db_url
		)
	}
```

- Example of a **.env** file

```
	DEBUG=True
	SECRET_KEY=a19bf95779aa01467fa26a091d84a54ad8bb8cfe31b6f7f8bbade0eb20669cbe
	DATABASE_URL=postgres://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME
```

if there is no password
`DATABASE_URL=postgres://USERNAME@localhost:5432/DATABASE_NAME`

## Set cors

- First install cors by running `poetry add django-cors-headers`
- Then add `corsheaders` to the installed apps
- Then add `"corsheaders.middleware.CorsMiddleware"` to the list of middleware
- Lastly add `CORS_ALLOW_ALL_ORIGINS = True` in the settings

## Setting up GraphQL

- First install the libraries by running
  `poetry add graphene-django graphene-file-upload Pillow`
- Add `graphene` and `graphene_django` in the install apps
- Create **schemas .py** file and add this code

```
	import  graphene
	class  Query(graphene.ObjectType):
		test = graphene.String()
		def  resolve_test(self, info:graphene.ResolveInfo)->str:
			return  "Hello World!"
	class  Mutation( graphene.ObjectType):
		pass
	SCHEMA = graphene.Schema(
		query=Query,
	)
```

- Edit the **url .py** file to be

```
	from  django.contrib  import  admin
	from  django.urls  import  path
	from  django.views.decorators.csrf  import  csrf_exempt
	from  graphene_file_upload.django  import  FileUploadGraphQLView
	from  django.conf  import  settings
	from  root.schemas  import  SCHEMA

	urlpatterns = [
		path('admin/', admin.site.urls),
		path(
			"graphql/",
			csrf_exempt(
				FileUploadGraphQLView.as_view(
					schema=SCHEMA, graphiql=settings.DEBUG
				)
			),
		),
	]
```

- Let's create a test app to add some examples of queries and mutations, run
  `manage startapp testapp`
- Rename the **views .py** to `mutations` and add a new files `queries`, `types`
- In the model file lets add a `name`, `image` fields

```
	from  django.db  import  models

	# Create your models here.
	class  TestApp(models.Model):
		name = models.CharField(max_length=255)
		image = models.ImageField()

	def  __str__(self)->str:
		return  self.name
```

- In the **queries** file add this code:

```
import  graphene
from  testapp.types  import  TestAppType
from  testapp  import  models

class  TestAppQuery(graphene.ObjectType):
	get_all_test_app = graphene.List(TestAppType)
	get_test_app_by_id = graphene.Field(TestAppType, id=graphene.Int())

	def  resolve_get_test_app_by_id(self, info:graphene.ResolveInfo, id:int)->models.TestApp:
		return  models.TestApp.objects.get(id=id)
	def  resolve_get_all_test_app(self, info:graphene.ResolveInfo)->models.TestApp:
		return  models.TestApp.objects.all()
```

- In the **types** file ass this code:

```
	import  graphene
	import  graphene_django
	from  testapp  import  models
	class  TestAppType(graphene_django.DjangoObjectType):
		class  Meta:
			model = models.TestApp
		image_url = graphene.String()

		def  resolve_image_url(self, info:graphene.ResolveInfo)->str:
			return  info.context.build_absolute_uri(self.image.url)
```

- In the **mutation** file add this code:

```
	from  typing  import  Any
	import  graphene
	from  graphene_file_upload.scalars  import  Upload
	from  testapp.types  import  TestAppType
	from  testapp  import  models
	from  graphql  import  GraphQLError

	class  CreateTestApp(graphene.Mutation):
		class  Arguments:
			name = graphene.String(required=True)
			image = Upload(required=True)

		test_app = graphene.Field(TestAppType)

		def  mutate(self, info:graphene.ResolveInfo, **kwargs:Any)->'CreateTestApp':
			test_app = models.TestApp.objects.create(**kwargs)
			return  CreateTestApp(test_app=test_app)

	class  UpdateTestApp(graphene.Mutation):
		class  Arguments:
			id = graphene.Int(required=True)
			name = graphene.String(required=True)
			image = Upload(required=True)

		test_app = graphene.Field(TestAppType)

		def  mutate(self, info:graphene.ResolveInfo, **kwargs:Any)->'UpdateTestApp':
			try:
				test_app = models.TestApp.objects.get(id=kwargs.get('id'))
			except  models.TestApp.DoesNotExist  as  exc:
				raise  GraphQLError(str(exc))
			for  key, value  in  kwargs.items():
				setattr(test_app, key, value)
			test_app.save()
			return  UpdateTestApp(test_app=test_app)

	class  DeleteTestApp(graphene.Mutation):
		class  Arguments:
			id = graphene.Int(required=True)

		status = graphene.Boolean()

		def  mutate(self, info:graphene.ResolveInfo, id:int)->'DeleteTestApp':
			try:
				test_app = models.TestApp.objects.get(id=id)
			except  models.TestApp.DoesNotExist  as  exc:
				raise  GraphQLError(str(exc))
			test_app.delete()
			return  DeleteTestApp(status=True)

	class TestAppMutation(graphene.ObjectType):
		create_test_app = CreateTestApp.Field()
		update_test_app = UpdateTestApp.Field()
		delete_test_app = DeleteTestApp.Field()
```

- Don't forget to add `testapp` to the installed apps

## Setup GraphQL AUTH

- First install these libraries by running this
  `poetry add django-graphql-auth "django-graphql-jwt^0.3.0"`
- Then create a users app by running
  `manage startapp users`
- Edit **models** file to include the following:

```
	from  django.contrib.auth.models  import  AbstractUser

	class  CustomUser(AbstractUser):
		pass
```

- Add a **mutations** file and add this code:

```
	import  graphene
	from  graphql_auth  import  mutations

	class  AuthMutation(graphene.ObjectType):
		register = mutations.Register.Field()
		token_auth = mutations.ObtainJSONWebToken.Field()
		login = mutations.ObtainJSONWebToken.Field()
```

- Go to the **settings** and add these to the installed apps bellow `graphene_django`

```
	"graphql_auth",
	"graphql_jwt.refresh_token.apps.RefreshTokenConfig",
	"users",
```

- Then add these bellow `CORS_ALLOW_ALL_ORIGINS`

```
	AUTH_USER_MODEL = "users.CustomUser"

	GRAPHENE = {
		"MIDDLEWARE": [
			"graphql_jwt.middleware.JSONWebTokenMiddleware",
		],
	}

	AUTHENTICATION_BACKENDS = [
		"graphql_jwt.backends.JSONWebTokenBackend",
		"django.contrib.auth.backends.ModelBackend",
		"graphql_auth.backends.GraphQLAuthBackend",
	]

	GRAPHQL_JWT = {
		"JWT_VERIFY_EXPIRATION": True,
		# optional
		"JWT_LONG_RUNNING_REFRESH_TOKEN": True,
		"JWT_ALLOW_ANY_CLASSES": [
			"graphql_auth.mutations.Register",
			"graphql_auth.mutations.ObtainJSONWebToken",
		],
		"JWT_EXPIRATION_DELTA": timedelta(minutes=60),
	}
```

- Then go to the **schemas** file in the root folder and import
  `from users.mutations import AuthMutation`
  **then add it to the mutations**

## Setup Heroku deploy

- First run `poetry add django-heroku`
- Then create a file called `Procfile` with the following content:

```
web: python manage.py runserver 0.0.0.0:$PORT
```

- Then go to the root settings and add at the end of the file the following:

```
import django_heroku
django_heroku.settings(locals())
```

## Setup formatting and type checking

- First run
  `poetry add -D annotated-types black isort mypy pylint pylint-django pytest pytest-cov pytest-django`
- Then add this code in **pyproject.toml** bellow the `[build-system]`

```
[tool.black]
line-length = 79
include = '\.pyi?$'
exclude = '''
	(
		/(
		\.eggs
		| \.git
		| \.hg
		| \.mypy_cache
		| \.tox
		| \.venv
		| _build
		| buck-out
		| build
		| dist
		)/
	)
'''

[tool.isort]
multi_line_output = 3
lines_after_imports = 2
force_grid_wrap = 0
combine_as_imports = true
include_trailing_comma = true

[tool.mypy]
plugins = "mypy_django_plugin.main"
ignore_missing_imports = true
strict_optional = true
follow_imports = "silent"
warn_redundant_casts = true
warn_unused_ignores = true
check_untyped_defs = true
disallow_untyped_defs = true
disallow_any_generics = true
show_error_codes = true

[tool.django-stubs]
django_settings_module = "root.settings"

[tool.pylint.main]
load-plugins = ["pylint_django"]
django-settings-module = "root.settings"

[tool.pylint.message_control]
disable =
'''
	attribute-defined-outside-init,
	duplicate-code,
	invalid-name,
	missing-docstring,
	protected-access,
	too-few-public-methods,
	no-member,
	raise-missing-from,
	no-self-argument,
	fixme,
	unsubscriptable-object,
	unused-argument,
	too-many-arguments,
	invalid-str-returned,
	redefined-outer-name,
	inherit-non-class,
	import-outside-toplevel,
	too-many-ancestors,
	cyclic-import,
	format,
	wrong-import-order,
	ungrouped-imports,
	wrong-import-position
'''

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "root.settings"
python_files = "tests.py test_*.py *_tests.py"
addopts = "--cov=. --no-cov-on-fail --cov-report term-missing:skip-covered"
filterwarnings = [
	"ignore::django.utils.deprecation.RemovedInDjango40Warning",
	"ignore::django.utils.deprecation.RemovedInDjango41Warning",
]

[tool.coverage.run]
omit = []
```

- Then add a **.vscode** folder and add **settings.json** file, inside it add this code:

```
{
	// Python Linting
	"python.linting.enabled": true,
	"python.linting.pylintEnabled": true,
	"python.linting.mypyEnabled": true,
	"python.linting.pylintArgs": [],
	// Python Formating
	"python.formatting.provider": "black",
	"[python]": {
		"editor.defaultFormatter": null,
		"editor.semanticHighlighting.enabled": false,
		"editor.codeActionsOnSave": {
			"source.organizeImports": true
		}
	}
}
```

- Then add a `Makefile` file and add this code:

```
pre-commit: format lint test
format:
poetry run isort .
poetry run black .
lint:
poetry run mypy .
poetry run pylint **/*.py
test:
poetry run pytest
lock:
git checkout --theirs poetry.lock
poetry lock --no-update
```
