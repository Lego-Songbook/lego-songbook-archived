from invoke import task


@task
def format(c):
    """Sort the imports and do the black magic."""
    c.run("poetry run isort -rc .")
    c.run("poetry run black .")


@task
def serve(c):
    """Start the local site server."""
    c.run("cd docs", hide=True)
    c.run("bundle exec jekyll serve")


@task(help={"name": "The feature's name."})
def feature(c, name):
    """Start a new feature."""
    if c.run(f"git branch | grep feature/{name}", warn=True).ok:
        c.run(f"git flow feature finish {name}")
    else:
        c.run(f"git flow feature start {name}")


@task(help={"version": "Version of the next release."})
def release(c, version, site_config_path="docs/_config.yml"):
    """Make a new release automatically."""
    if c.run(f"git branch | grep release/{version}", warn=True).failed:

        from yaml import safe_load, dump

        c.run(f"git flow release start {version}")
        c.run(f"poetry version {version}")

        site_config = safe_load(open(site_config_path, "r"))
        site_config["version"] = version
        dump(site_config, open(site_config_path, "w"))
        print(f"The site is bumped to {version}.")

        c.run("poetry lock")

        print("Testing the package...")
        c.run("poetry run tox -q")

    if c.run("git status", hide=True).failed:
        c.run(f"git commit -a -m 'Bump version to {version}'")

    c.run(f"git flow release finish {version} -m 'v{version}'")
