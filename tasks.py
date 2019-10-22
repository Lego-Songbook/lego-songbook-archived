import yaml
from invoke import task


@task
def format(c):
    c.run("poetry run isort -rc .")
    c.run("poetry run black .")


@task
def serve(c):
    c.run("cd docs", hide=True)
    c.run("bundle exec jekyll serve")


@task(help={"version": "Version of the next release."})
def release(c, version, site_config_path="docs/_config.yml"):
    c.run(f"git flow release start {version}")
    c.run(f"poetry version {version}")

    site_config = yaml.safe_load(open(site_config_path, "r"))
    site_config["version"] = version
    yaml.dump(site_config, open(site_config_path, "w"))
    print(f"The site is bumped to {version}.")

    c.run("poetry lock")

    print("Testing the package...")
    c.run("poetry run tox -q")

    c.run(f"git commit -a -m 'Bump version to {version}'")
    c.run(f"git flow release finish {version}")
