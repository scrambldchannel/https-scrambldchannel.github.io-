Title: Adventures with pre-commit
Date: 2020-09-30 11:01
Category: docs
Tags: python, git, flake8, black, isort, mypy, pre-commit
slug: adventures-with-pre-commit
Authors: Alexander
featured_image: images/pre_commit_love.png
Summary: I started using the [pre-commit](https://pre-commit.com/) framework a while back on my projects but only with a very basic setup on pretty simple codebases. Common uses are apply code formatters like [black](https://github.com/psf/black) or to run static type checking with [mypy](http://mypy-lang.org/). I tried to create a rough framework for my Python projects.

I started using the [pre-commit](https://pre-commit.com/) framework a while back on my projects but only with a very basic setup on pretty simple codebases. Common uses are apply code formatters like [black](https://github.com/psf/black) or to run static type checking with [mypy](http://mypy-lang.org/).

The cool thing about using them is that it reduces the noise in your repository by formatting your code, and flagging issues, _before_ it gets committed. I'd previously tended to run tools like black sporadically but this just creates an extra, often quite large commit, that doesn't change the functionality of the code but just adds noise.

My initial setup was pretty basic and it was only when I started working with the Airflow codebase that I dove into them in more detail. If you look at the project's [.pre-commit-config.yaml](https://github.com/apache/airflow/blob/master/.pre-commit-config.yaml) file, it uses a huge number of hooks, including quite a few that call custom scripts. While I don't need anything that complicated, it made me realise I could do a bit more so I spent a bit of time trying to create a starting template I could role into new projects. I'm still tweaking, but thought I'd scribble down this draft while the thinking behind it was fresh in my mind.

## How to setup pre-commit

Pre-commit is written in Python and can be installed using pip:

```sh
$ pip install pre-commit
```

To use it in a project, run it in the root of the project's git repository:

```sh
$ pre-commit install
```

For it to do something, you need to define a configuration in a ```.pre-commit-config.yaml``` file. Out of the box, there's a command to send a sample config to stdout:

```sh
$ pre-commit sample-config
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
```

The yaml above is fairly easy to understand, it has a link to a repo where the hook code is maintained, a specific version and the list of hooks you want to run and the names are pretty self-explanatory.

## Adding more hooks

The sample config includes a couple of useful tools but pre-commit can leverage a lot more power than that. I want to code re-formatting, linting and type checking to my Python projects by default.

**Note:** I'm using it here for a Python project but it can be used for projects in all sorts of languages, you'd just need to take advantage of different hooks. Take a look at the [list here](https://pre-commit.com/hooks.html) to get an idea of what is possible.

### Using isort to arrange imports

In the words of the [project](https://github.com/PyCQA/isort) "isort your imports, so you don't have to". I like this approach, having imports arranged consistently helps with readability and this makes it easy. It can be used here as a hook by adding the following to the project's ```.pre-commit-config.yaml```:

```yaml
-   repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.1.4
    hooks:
    -   id: isort
```

### Using black to format code

I love black, I don't have any strong opinions on code style, I mainly just care that it's consistent. I certainly don't want to waste time ever arguing about it. Running black prior to every commit means that code is clean and consistent. It can be added as a hook like this:

```yaml
-   repo: https://github.com/ambv/black
    rev: stable
    hooks:
    - id: black
```

Black ships with sensible defaults and I don't really want to change many things, or even really think about it that much. However, I do like to keep lines to a max of 80 characters. You can add configuration options for Black into your project's ```pyproject.toml``` file and tailored for the specific project. Here I override the line length, specify the python versions I'm targeting and exclude a few directories:

```toml
[tool.black]
line-length = 79
target-version = ['py37', 'py38']
include = '\.pyi?$'
exclude = '''

(
  /(
      \.eggs
    | \.git
    | \.mypy_cache
    | _build
    | build
    | dist
  )
)
'''
```

### Static type checking with mypy

For any new Python projects I start, I'm getting into the habit of adding type hints. On a couple of projects, I've made the mistake of not really checking them as I go and find that I have a complicated mess to unpick when I finally run mypy. Using it as a pre-commit hook means I can fix them incrementally which avoids a future headache. For simpler projects, I'd probably not bother but it makes sense to have it as default. The following snippet adds mypy as a hook:

```yaml
-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.782
    hooks:
    -   id: mypy
```

### Style checks and basic linting with Flake8

Although I'm using black to format the code, I've been playing around with using Flake8 in parallel for a couple of reasons. Firstly, it also does some linting of your code, flagging up unused imports for example which I find useful. I've also noticed that black doesn't seem to do anything about comment lines or long strings that breach the line length limit, flake8 will flag these. It can be added as a hook by adding the following yaml:

```yaml
-   repo: https://gitlab.com/pycqa/flake8
    rev: 3.7.9
    hooks:
    - id: flake8
```

One thing that black and flake8 couldn't agree on by default was whether or not to have a trailing space after the last comma in a list specified on a single line. That is, black wanted it to look like this: 

```python
    install_requires=["Click",],
```

But flake8 insisted it should look this and complained:

```python
    install_requires=["Click", ],
```

```sh
setup.py:7:30: E231 missing whitespace after ','
```

I don't care but sided with black on this occasion. I found a bit of [chat](https://gitlab.com/pycqa/flake8/-/issues/428) about adding support for an entry ```pyproject.toml``` to manage the flake8 config but I couldn't see any evidence that it worked. Instead I create a ```.flake8``` file with the following:


```
[flake8]
ignore = E231
max-line-length = 120
```

I suspect as time goes on I might add a few more codes to that ignore list. Setting the max length to 100 means I get _really_ long lines that black doesn't re-format flagged up but others get through.

Another option here is to use the ominously named [flakehell](https://github.com/life4/flakehell) instead which does offer ```pyproject.toml``` support as well as a number of other options on top of flake8. I'll certainly keep an eye on it.

I did look at using pylint instead but it complained about so many things I didn't care about that I didn't persevere. I'll maybe revisit this later. From the reading I did it's recommended to use it as a local hook as [documented here]().

## Running the checks

Once you've installed pre-commit in a git repo the checks will all run every time you try to commit. Hooks like isort and black will change any files as necessary and have you need to re-stage them and re-commit. Flake8 and mypy will just throw up issues and you need to fix them manually to get the commit through. One thing that is a bit fiddly is that it can be a bit fiddly to understand what checks have failed when I try to commit via vscode but I mostly commit things via the command line these days anyway.

You can also run the various checks from the command line outside of a commit. This gives you finer grained control and also allows running tools like black and isort on demand from their repos without needing to install them. For example all checks can be run on all files with the following:

```sh
pre-commit run --all-files
```

This can be particularly useful if you're adding a set of hooks to an existing project and want to flag any issues you might run into at a later date. 

Or you can use the ```--files``` option to run hooks on a list of specific files:

```sh
pre-commit run --files app.py class.py
```

It's also possible to run only a specific hook. The command below will apply black to all files, irrespective of whether they are staged:
```sh
pre-commit run black --all-files
```

## Conclusion

I love the pre-commit framework and will use it on every new project from now on. I've dumped my setup into a [repo on github](https://github.com/scrambldchannel/python-pre-commit-template) which I'll continue to tinker with as it evolves.