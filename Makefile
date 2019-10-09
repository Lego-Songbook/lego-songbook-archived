
.PHONY: serve

serve:
	cd docs && bundle exec jekyll serve

.PHONY: clean

clean:
	rm -rf docs/_site/
