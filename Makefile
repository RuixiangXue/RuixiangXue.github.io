.PHONY: render render-all test serve clean

render:
	python3 scripts/render_site.py

render-all:
	python3 scripts/render_site.py
	python3 scripts/render_site.py --target targets/ai-product.json
	python3 scripts/render_site.py --target targets/driving-world-model.json
	python3 scripts/render_site.py --lang zh
	python3 scripts/render_site.py --lang zh --target targets/ai-product.zh.json
	python3 scripts/render_site.py --lang zh --target targets/driving-world-model.zh.json

test:
	python3 -m unittest discover -s tests

serve: render-all
	python3 -m http.server 8080

clean:
	rm -f index.html index-zh.html jobs.html jobs-zh.html assets/cv/resume*.html

jobs:
	python3 scripts/jobs.py list
