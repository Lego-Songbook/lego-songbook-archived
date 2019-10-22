from invoke import task


@task
def format(c):
    c.run("poetry run isort -rc .")
    c.run("poetry run black .")


@task
def serve(c):
    c.run("cd docs")
    c.run("bundle exec jekyll serve")
