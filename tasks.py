from invoke import task


@task
def format(c):
    c.run("poetry run black .")
    c.run("poetry run isort -rc .")


@task
def serve(c):
    c.run("cd docs")
    c.run("bundle run jekyll serve")
