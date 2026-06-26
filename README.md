# Ruixiang Xue Homepage

This repository keeps the personal homepage and resume generated from one structured profile.

## Edit

- Long-term facts: `data/profile.json`
- Job-search pipeline: `jobs/pipeline.json`
- Job-specific resume targets: `targets/*.json`
- Renderer: `scripts/render_site.py`

## Generate

```bash
make test
make render-all
```

The generated files are:

- English site: `index.html`, `jobs.html`
- Chinese site: `index-zh.html`, `jobs-zh.html`
- English resumes: `assets/cv/resume.html`, `assets/cv/resume-ai-product.html`, `assets/cv/resume-driving-world-model.html`
- Chinese resumes: `assets/cv/resume-zh.html`, `assets/cv/resume-ai-product-zh.html`, `assets/cv/resume-driving-world-model-zh.html`

For a job-specific version:

```bash
python3 scripts/render_site.py --target targets/ai-product.json
python3 scripts/render_site.py --target targets/driving-world-model.json
python3 scripts/render_site.py --lang zh
python3 scripts/render_site.py --lang zh --target targets/driving-world-model.zh.json
```

To create a new targeted resume, copy `targets/default.json`, adjust the focus and tags, and render with `--target`.

## Job Pipeline

```bash
make jobs
python3 scripts/jobs.py add --company "Company" --role "Role" --priority high
python3 scripts/jobs.py status company-role applied --next-action "Wait for recruiter reply"
```

Open `jobs.html` after `make render-all` to view the local pipeline page.

## Workflow

Add new facts to `data/profile.json`, create or update a target file for a job description, then regenerate. The homepage design is adapted from PRISM.
