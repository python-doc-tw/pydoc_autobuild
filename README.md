# PyDoc Auto Build

This repository serves the autobuild of [the Taiwan Translation of Python Official Documentation][python-doc-tw].

You can see the live demo at <http://docs.python.org.tw/_build/>.

[python-doc-tw]: https://github.com/python-doc-tw/python-doc-tw


## Repository Structure

This repo must have the official Python doc repo existed in the same directory.

For example, if we use the [Taiwan maintained doc repo][cpython-tw], the cloning command will be:

    git clone https://github.com/python-doc-tw/cpython-tw.git
    git clone https://github.com/python-doc-tw/pydoc_autobuild.git

The folder structure will be like:

    <root>
    ├── cpython-tw/   # CPython's git repo
    └── pydoc_autobuild/   # this git repo

If the doc repo is at different location, change the path of `PYDOC_ROOT` at `<root>/pydoc_autobuild/pydoc_autobuild/settings/base.py`.

```python
# pydoc_autobuild/settings/base.py
PYDOC_ROOT = abspath(expanduser('../cpython-tw/Doc'))
```

[cpython-tw]: https://github.com/python-doc-tw/cpython-tw


## Getting Started

### Requirements

- Git 1.8+
- Python 3.5


### Virtual Environment `venv`

It is recommended to install all depended Python packages using virtual environment. Using built-in `venv` is sufficient:

    python3 -m venv venv

And enable it:

    . venv/bin/activate


### Install Dependencies for Building PyDoc

The source of CPython documentation is at `<root>/cpython-tw/Doc`. First install the dependencies to build doc:

    pip install -r requirements.txt

You should be able to build the doc now:

    make html


### Set up the Transifex client

We use [Transifex client](http://docs.transifex.com/client/) to communicate with [Transifex](https://www.transifex.com/). The login credentials have to be saved at `~/.transifexrc` (leave the token field blank):

```ini
[https://www.transifex.com]
hostname = https://www.transifex.com
token =
username = <YOUR USERNAME>
password = <YOUR PASSWORD>
```

### Install Dependencies for PyDoc Autobuild

Then we are ready to setup the autobuild server. Install the dependency at `<root>/pydoc_autobuild/`:

    pip install -r requirements.txt

### Set up Local Environment Variables and Database

Settings are stored in environment variables via [django-environ](http://django-environ.readthedocs.org/en/latest/). The quickiest way to start is to copy `local.sample.env` into `local.env`:

    cp <root>/auto_pydoc/settings/local.sample.env src/pycontw2016/settings/local.env

Then edit the `SECRET_KEY` line in `local.env`, replacing `{{ secret_key }}` into any [Django Secret Key](http://www.miniwebtool.com/django-secret-key-generator/) value. An example:

    SECRET_KEY=twvg)o_=u&@6^*cbi9nfswwh=(&hd$bhxh9iq&h-kn-pff0&&3

After that, just run the migration.


### Get Ready for Development

`cd` into the `<root>/auto_pydoc` directory and migrate the database:

    python manage.py migrate

Now you’re all set!


## Run the Development Server

Run the web server for viewing task execution log:

    python manage.py runserver

And run the Django-Q's task queue:

    python manage.py qcluster

You should be able to find the build log at <http://localhost:8000/_build/> and the Python doc at <http://localhost:8000/3/>. To rebuild the doc, just click the "Update Translation" link at the sidebar of the doc page you'd like to update.



## How to Contribute

Follow the [GitHub Flow](https://guides.github.com/introduction/flow/), please **DO NOT push the commits into master directly**. Always create branch by the feature you want to update. You are encouraged to submit a pull request for reviewing before merging things into master.

You are welcomed to join the Taiwan Python official documentation translation [here][python-doc-tw].
