from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_json_or(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return fallback
    return load_json(path)


def render_site(
    *,
    root: Path = ROOT,
    profile_path: Path | None = None,
    target_path: Path | None = None,
    lang: str = "en",
) -> dict[str, Path]:
    if lang not in ("en", "zh"):
        raise ValueError(f"unsupported lang: {lang}")
    if profile_path is None:
        profile_path = root / "data" / ("profile.zh.json" if lang == "zh" and (root / "data" / "profile.zh.json").exists() else "profile.json")
    if target_path is None:
        target_path = root / "targets" / ("default.zh.json" if lang == "zh" and (root / "targets" / "default.zh.json").exists() else "default.json")
    profile = load_json(profile_path)
    target = load_json(target_path)
    pipeline = load_json_or(root / "jobs" / "pipeline.json", {"jobs": []})

    suffix = "" if lang == "en" else "-zh"
    home_path = root / f"index{suffix}.html"
    resume_path = root / "assets" / "cv" / target.get("resume_filename", f"resume{suffix}.html")
    jobs_path = root / f"jobs{suffix}.html"
    resume_path.parent.mkdir(parents=True, exist_ok=True)

    home_path.write_text(render_home(profile, lang=lang), encoding="utf-8")
    resume_path.write_text(render_resume(profile, target, lang=lang), encoding="utf-8")
    jobs_path.write_text(render_jobs(profile, pipeline, lang=lang), encoding="utf-8")
    return {
        "home": home_path,
        "resume": resume_path,
        "jobs": jobs_path,
    }


def labels(lang: str) -> dict[str, str]:
    if lang == "zh":
        return {
            "home": "首页",
            "publications": "论文",
            "projects": "项目",
            "jobs": "求职进程",
            "research_focus": "研究内容",
            "about": "空间智能",
            "about_prefix": "我是",
            "affiliation": "单位",
            "advisor": "导师",
            "download_cv": "下载简历",
            "education": "教育经历",
            "experience": "工作经历",
            "awards": "荣誉",
            "job_blurb": "轻量求职看板：JD、定制简历、下一步行动和状态保持联动。",
            "profile": "概览",
            "research_projects": "研究项目",
            "selected_publications": "代表论文",
            "skills": "技能",
            "resume_title": "研究简历",
            "language_label": "English",
        }
    return {
        "home": "Home",
        "publications": "Publications",
        "projects": "Projects",
        "jobs": "Jobs",
        "research_focus": "Research Area",
        "about": "Spatial Intelligence",
        "about_prefix": "I am",
        "affiliation": "Affiliation",
        "advisor": "Advisor",
        "download_cv": "Download my CV",
        "education": "Education",
        "experience": "Work Experience",
        "awards": "Awards",
        "job_blurb": "A lightweight ATS: JD, target resume, next action, and status stay linked.",
        "profile": "Profile",
        "research_projects": "Research Projects",
        "selected_publications": "Selected Publications",
        "skills": "Skills",
        "resume_title": "Research Resume",
        "language_label": "中文",
    }


def lang_attr(lang: str) -> str:
    return "zh-CN" if lang == "zh" else "en"


def local_path(path: str, lang: str) -> str:
    if lang == "en":
        return path
    if path == "./":
        return "index-zh.html"
    stem, dot, ext = path.partition(".html")
    return f"{stem}-zh.html" if dot else path


def switch_path(path: str, lang: str) -> str:
    if lang == "en":
        stem, dot, ext = path.partition(".html")
        return f"{stem}-zh.html" if dot else "index-zh.html"
    return path.replace("-zh.html", ".html").replace("index.html", "index.html")


def render_home(profile: dict[str, Any], *, lang: str = "en") -> str:
    person = profile["person"]
    links = profile.get("links", [])
    t = labels(lang)
    project_previews = build_project_previews(profile, lang=lang)
    resume_links = [
        {
            "label": "CV EN",
            "url": "https://ruixiangxue.github.io/assets/cv/resume-en.pdf",
            "icon": "fa-solid fa-file-arrow-down",
        },
        {
            "label": "CV 中文",
            "url": "https://ruixiangxue.github.io/assets/cv/resume-zh.pdf",
            "icon": "fa-solid fa-file-pdf",
        },
    ]
    lang_switch = "index.html" if lang == "zh" else "index-zh.html"
    return page(
        title=f"{person['name']} - Homepage",
        description=person["summary"],
        body=f"""
  <nav class="top-nav">
    <div class="nav-container">
      <div class="nav-left">
        <a href="#top" data-section-link="top">{t['home']}</a>
        <a href="#about" data-section-link="about">{t['research_focus']}</a>
        <a href="#projects" data-section-link="projects">{t['projects']}</a>
        <a href="#experience" data-section-link="experience">{t['experience']}</a>
        <a href="#publications" data-section-link="publications">{t['publications']}</a>
        <a href="#awards" data-section-link="awards">{t['awards']}</a>
      </div>
      <div class="nav-right">
        <a class="language-link" href="{lang_switch}">{t['language_label']}</a>
        <button id="themeToggle" class="theme-toggle" title="Toggle theme" aria-label="Toggle theme">
          <i class="fa-solid fa-moon"></i>
        </button>
      </div>
    </div>
  </nav>

  <main class="portfolio-shell" id="top">
    <section class="hero-panel section" data-section="top">
      <div class="hero-copy">
        <h1>{esc(person['name'])}<span>{esc(person['name_zh'])}</span></h1>
        <div class="hero-social">
          {render_social_links(links, resume_links=resume_links)}
        </div>
      </div>
      <aside class="hero-visual">
        <div class="portrait-frame">
          <img src="{esc(person.get('avatar', 'assets/img/avatar.svg'))}" alt="{esc(person['name'])} portrait">
          <button class="say-hi" type="button" title="Say Hi" aria-label="Say Hi">
            <i class="fa-solid fa-hand-sparkles"></i>
            <span>Say Hi</span>
          </button>
        </div>
      </aside>
    </section>

    <section class="section focus-section" id="about" data-section="about">
      <div>
        <p class="section-kicker">{t['research_focus']}</p>
        <h2 class="section-title">{t['about']}</h2>
      </div>
      {render_research_bubbles(person.get("research_interests", []), project_previews, lang=lang)}
    </section>

    <section class="section" id="projects" data-section="projects">
      <h2 class="section-title">{t['projects']}</h2>
      <div class="section-body">
        <div class="project-grid">
          {''.join(render_project_card(item) for item in project_previews)}
        </div>
      </div>
    </section>

    <div class="content-grid">
      <div class="section" id="education" data-section="education">
        <h2 class="section-title">{t['education']}</h2>
        <div class="section-body">
          {''.join(render_education(item) for item in profile.get('education', []))}
        </div>
      </div>

      <div class="section" id="experience" data-section="experience">
        <h2 class="section-title">{t['experience']}</h2>
        <div class="section-body">
          {''.join(render_experience(item) for item in profile.get('experience', []))}
        </div>
      </div>
    </div>

      <div class="section" id="publications" data-section="publications">
        <h2 class="section-title">{t['publications']}</h2>
        <div class="section-body">
          <div class="publications">
            <ol class="bibliography">
              {''.join(render_publication(item) for item in profile.get('publications', []))}
            </ol>
          </div>
        </div>
      </div>

      <div class="section" id="awards" data-section="awards">
        <h2 class="section-title">{t['awards']}</h2>
        <div class="section-body">
          <div class="awards-grid">
            {''.join(render_award(item) for item in profile.get('awards', []))}
          </div>
        </div>
      </div>

    <footer class="site-footer">
      <p>
        &copy; 2026 {esc(person['name'])}. All rights reserved.
        <br>
        <span class="template-credit">Design adapted from <a href="https://github.com/xyjoey/PRISM">PRISM</a></span>
      </p>
    </footer>
  </main>
""",
        lang=lang,
    )


def render_jobs(profile: dict[str, Any], data: dict[str, Any], *, lang: str = "en") -> str:
    person = profile["person"]
    jobs = data.get("jobs", [])
    t = labels(lang)
    return page(
        title=f"{person['name']} - Job Pipeline",
        description="Private-facing job search pipeline generated from structured data.",
        body=f"""
  {simple_nav(lang, "jobs.html")}
  <div class="wrapper single-column">
    <section class="content wide-content">
      <div class="section visible">
        <h2 class="section-title">{t['jobs']}</h2>
        <div class="section-body">
          <p class="muted-line">{t['job_blurb']}</p>
          <div class="job-board">
            {''.join(render_job_card(item) for item in jobs)}
          </div>
        </div>
      </div>
    </section>
  </div>
""",
        lang=lang,
    )


def render_resume(profile: dict[str, Any], target: dict[str, Any], *, lang: str = "en") -> str:
    person = profile["person"]
    t = labels(lang)
    resume_title = target.get("title") if lang == "en" else target.get("title_zh", t["resume_title"])
    tags = set(target.get("include_project_tags", []))
    projects = [item for item in profile.get("projects", []) if match_tags(item, tags)]
    publications = [item for item in profile.get("publications", []) if match_tags(item, tags)]
    experiences = [item for item in profile.get("experience", []) if match_tags(item, tags)]

    return resume_page(
        title=resume_title or target.get("title", "Resume"),
        body=f"""
    <main class="resume">
      <header class="resume-head">
        <div>
          <p class="resume-label">{esc(resume_title or t['resume_title'])}</p>
          <h1>{esc(person['name'])} <span>{esc(person['name_zh'])}</span></h1>
          <p class="resume-subtitle">{esc(person['title'])}</p>
        </div>
        <address>{render_resume_contacts(person, profile.get('links', []))}</address>
      </header>

      <section class="resume-summary">
        <p>{esc(target.get('focus') or person.get('summary', ''))}</p>
      </section>

      <section>
        <h2>{t['education']}</h2>
        {''.join(render_resume_education(item) for item in profile.get('education', []))}
      </section>

      <section>
        <h2>{t['experience']}</h2>
        {''.join(render_resume_experience(item) for item in experiences)}
      </section>

      <section>
        <h2>{t['research_projects']}</h2>
        {''.join(render_resume_project(item) for item in projects)}
      </section>

      <section>
        <h2>{t['selected_publications']}</h2>
        {''.join(render_resume_publication(item) for item in publications)}
      </section>

      <section>
        <h2>{t['skills']}</h2>
        <div class="resume-skills">
          {''.join(render_skill(item) for item in profile.get('skills', []))}
        </div>
      </section>

      <section>
        <h2>{t['awards']}</h2>
        {''.join(render_resume_award(item) for item in profile.get('awards', []))}
      </section>
    </main>
""",
    )


def render_resume_contacts(person: dict[str, Any], links: list[dict[str, str]]) -> str:
    github = next((item.get("url", "") for item in links if item.get("label", "").lower() == "github"), "")
    parts = [
        esc(person.get("email", "")),
        esc(person.get("phone", "")),
        esc(person.get("location", "")),
    ]
    if github:
        parts.append(f'<a href="{esc(github)}">{esc(github.replace("https://", ""))}</a>')
    return "<br>".join(part for part in parts if part)


def match_tags(item: dict[str, Any], tags: set[str]) -> bool:
    return not tags or bool(tags.intersection(item.get("tags", [])))


def page(*, title: str, description: str, body: str, lang: str = "en") -> str:
    return f"""<!DOCTYPE html>
<html lang="{lang_attr(lang)}">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="keywords" content="Ruixiang Xue, point cloud compression, 3D Gaussian splatting, Nanjing University">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/academicons/1.8.6/css/academicons.min.css" integrity="sha256-uFVgMKfistnJAfoCUQigIl+JfUaP47GrRKjf6CTPVmw=" crossorigin="anonymous">
  <script src="https://kit.fontawesome.com/a860a211d3.js" crossorigin="anonymous"></script>

  <link rel="stylesheet" href="assets/css/font_sans_serif.css">
  <link rel="stylesheet" href="assets/css/prism-static.css">
</head>
<body class="theme-prism">
{body}
  <script src="assets/js/scale.fix.js"></script>
  <script>
    (function() {{
      const themeToggle = document.getElementById('themeToggle');
      const icon = themeToggle.querySelector('i');

      function setTheme(isDark) {{
        document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
        icon.classList.toggle('fa-sun', isDark);
        icon.classList.toggle('fa-moon', !isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
      }}

      const savedTheme = localStorage.getItem('theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setTheme(savedTheme ? savedTheme === 'dark' : prefersDark);

      themeToggle.addEventListener('click', function() {{
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        setTheme(!isDark);
      }});

      document.querySelectorAll('.say-hi').forEach(function(button) {{
        button.addEventListener('click', function() {{
          const emoji = document.createElement('span');
          const choices = ['👋', '✨', '🙂', '💬'];
          emoji.className = 'hi-emoji';
          emoji.textContent = choices[Math.floor(Math.random() * choices.length)];
          button.appendChild(emoji);
          window.setTimeout(function() {{ emoji.remove(); }}, 1200);
        }});
      }});

      document.querySelectorAll('[data-bibtex-target]').forEach(function(button) {{
        button.addEventListener('click', function() {{
          const target = document.getElementById(button.getAttribute('data-bibtex-target'));
          if (!target) return;
          target.hidden = !target.hidden;
        }});
      }});

      document.querySelectorAll('[data-copy-bibtex]').forEach(function(button) {{
        button.addEventListener('click', async function() {{
          const target = document.getElementById(button.getAttribute('data-copy-bibtex'));
          const code = target && target.querySelector('code');
          if (!code) return;
          await navigator.clipboard.writeText(code.innerText);
          const oldText = button.innerText;
          button.innerText = 'Copied';
          window.setTimeout(function() {{ button.innerText = oldText; }}, 1200);
        }});
      }});

      if ('IntersectionObserver' in window) {{
        const observer = new IntersectionObserver(function(entries) {{
          entries.forEach(function(entry) {{
            if (entry.isIntersecting) {{
              entry.target.classList.add('visible');
              observer.unobserve(entry.target);
            }}
          }});
        }}, {{ threshold: 0.1 }});

        document.querySelectorAll('.section').forEach(function(el) {{
          observer.observe(el);
        }});

      }} else {{
        document.querySelectorAll('.section').forEach(function(el) {{
          el.classList.add('visible');
        }});
      }}

      const navLinks = Array.from(document.querySelectorAll('[data-section-link]'));
      const sections = Array.from(document.querySelectorAll('[data-section]'));

      function setActiveSection(section) {{
        navLinks.forEach(function(link) {{
          link.classList.toggle('active', link.getAttribute('data-section-link') === section);
        }});
      }}

      function updateActiveNav() {{
        if (!sections.length) return;
        const scrollProbe = window.scrollY + window.innerHeight * 0.35;
        let current = sections[0].getAttribute('data-section');
        sections.forEach(function(section) {{
          if (section.offsetTop <= scrollProbe) {{
            current = section.getAttribute('data-section');
          }}
        }});
        if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) {{
          current = sections[sections.length - 1].getAttribute('data-section');
        }}
        setActiveSection(current);
      }}

      updateActiveNav();
      window.addEventListener('scroll', updateActiveNav, {{ passive: true }});
      window.addEventListener('resize', updateActiveNav);
    }})();
  </script>
</body>
</html>
"""


def simple_nav(lang: str = "en", current: str = "index.html") -> str:
    t = labels(lang)
    lang_switch = switch_path(current, lang)
    return f"""
  <nav class="top-nav">
    <div class="nav-container">
      <div class="nav-left">
        <a href="{local_path('./', lang)}">{t['home']}</a>
        <a href="{local_path('jobs.html', lang)}">{t['jobs']}</a>
      </div>
      <div class="nav-right">
        <a class="language-link" href="{lang_switch}">{t['language_label']}</a>
        <button id="themeToggle" class="theme-toggle" title="Toggle theme" aria-label="Toggle theme">
          <i class="fa-solid fa-moon"></i>
        </button>
      </div>
    </div>
  </nav>
"""


def resume_page(*, title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="../css/resume.css">
</head>
<body>
{body}
</body>
</html>
"""


def render_social_links(
    links: list[dict[str, str]],
    resume_links: list[dict[str, str]] | None = None,
) -> str:
    icons = {"GitHub": "fa-brands fa-github", "Email": "fa-solid fa-envelope"}
    rendered = "".join(
        f'<a href="{esc(link["url"])}" title="{esc(link["label"])}"><i class="{icons.get(link["label"], "fa-solid fa-link")}"></i></a>'
        for link in links
    )
    for link in resume_links or []:
        rendered += (
            f'<a href="{esc(link["url"])}" title="{esc(link["label"])}" '
            f'target="_blank" rel="noopener" download>'
            f'<i class="{esc(link.get("icon", "fa-solid fa-file-lines"))}"></i></a>'
        )
    return rendered


def render_interest_list(interests: list[str]) -> str:
    return "".join(f"<span>{esc(item)}</span>" for item in interests)


def render_research_bubbles(interests: list[str], projects: list[dict[str, Any]], *, lang: str) -> str:
    bubbles = "".join(render_research_bubble(item, index, projects) for index, item in enumerate(interests))
    return f"""
      <div class="research-map" aria-label="Spatial intelligence research map">
        <div class="research-core">Spatial<br>Intelligence</div>
        {bubbles}
      </div>
"""


def render_research_bubble(interest: str, index: int, projects: list[dict[str, Any]]) -> str:
    target = find_project_for_interest(interest, projects)
    if target:
        return f'<a class="research-bubble bubble-{index % 6}" href="#{esc(target)}">{esc(interest)}</a>'
    return f'<span class="research-bubble bubble-{index % 6} is-static">{esc(interest)}</span>'


def build_project_previews(profile: dict[str, Any], *, lang: str) -> list[dict[str, Any]]:
    projects = [dict(item) for item in profile.get("projects", [])]
    interests = profile.get("person", {}).get("research_interests", [])
    previews: list[dict[str, Any]] = []
    used: set[int] = set()
    for interest in interests:
        index = best_project_index(interest, projects, used)
        if index is not None and projects[index].get("homepage_project", True) is not False:
            item = dict(projects[index])
            used.add(index)
        else:
            continue
        item["id"] = project_id(item.get("name", interest))
        item["interest"] = interest
        previews.append(item)
    return previews


def best_project_index(interest: str, projects: list[dict[str, Any]], used: set[int]) -> int | None:
    interest_norm = normalize_key(interest)
    alias_groups = [
        (("point", "cloud"), ("point", "cloud")),
        (("3d", "gaussian"), ("gaussian", "splatting")),
        (("splatting",), ("3dgs", "gaussian")),
        (("三维", "高斯"), ("高斯", "3d")),
        (("street", "novel"), ("street", "novel")),
        (("街景",), ("街景",)),
        (("photography",), ("camera", "photography")),
        (("摄影",), ("相机", "摄影")),
    ]
    for index, project in enumerate(projects):
        if index in used:
            continue
        project_text = normalize_key(" ".join([project.get("name", ""), project.get("summary", ""), " ".join(project.get("tags", []))]))
        if interest_norm and interest_norm in project_text:
            return index
        for interest_terms, project_terms in alias_groups:
            if all(term in interest_norm for term in interest_terms) and any(term in project_text for term in project_terms):
                return index
    return None


def find_project_for_interest(interest: str, projects: list[dict[str, Any]]) -> str | None:
    interest_norm = normalize_key(interest)
    for project in projects:
        if normalize_key(project.get("interest", "")) == interest_norm:
            return project.get("id", "projects")
    return None


def project_id(name: str) -> str:
    base = "".join(ch.lower() if ch.isalnum() else "-" for ch in name)
    return "project-" + "-".join(part for part in base.split("-") if part)


def normalize_key(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() or "\u4e00" <= ch <= "\u9fff" else " " for ch in value)


def render_education(item: dict[str, Any]) -> str:
    details = "".join(f"<li>{format_inline(detail)}</li>" for detail in item.get("details", []))
    logo = item.get("logo", "assets/logos/nju.svg")
    return f"""
          <div class="card timeline-item">
            <div class="experience-item">
              <img src="{esc(logo)}" alt="{esc(item['school'])} logo" class="institution-logo">
              <div class="experience-content">
                <p class="exp-title"><strong>{esc(item['school'])}</strong></p>
                <p class="exp-detail">{esc(item['degree'])}</p>
                <p class="exp-period">{esc(item['period'])}</p>
                {f'<ul>{details}</ul>' if details else ''}
              </div>
            </div>
          </div>
"""


def render_experience(item: dict[str, Any]) -> str:
    bullets = "".join(f"<li>{format_inline(bullet)}</li>" for bullet in item.get("bullets", []))
    logo = item.get("logo", "assets/img/institution.svg")
    department = item.get("department", "")
    return f"""
          <div class="card timeline-item">
            <div class="experience-item">
              <img src="{esc(logo)}" alt="{esc(item['organization'])} logo" class="institution-logo">
              <div class="experience-content">
                <p class="exp-title"><strong>{esc(item['organization'])}</strong></p>
                <p class="exp-detail">{esc(department)} · {esc(item['role'])}</p>
                <p class="exp-period">{esc(item['period'])}</p>
                <p>{esc(item.get('summary', ''))}</p>
                <ul>{bullets}</ul>
              </div>
            </div>
          </div>
"""


def render_project_card(item: dict[str, Any]) -> str:
    bullets = "".join(f"<li>{format_inline(bullet)}</li>" for bullet in item.get("bullets", [])[:3])
    bullet_list = f"<ul>{bullets}</ul>" if bullets else ""
    image = item.get("image")
    image_html = f'<img class="project-image" src="{esc(image)}" alt="{esc(item["name"])} preview">' if image else ""
    return f"""
          <article class="card project-card" id="{esc(item.get('id', project_id(item['name'])))}">
            {image_html}
            <div class="project-copy">
              <div class="project-topline">{esc(item.get('interest', item['name']))}</div>
              <strong>{esc(item['name'])}</strong>
              <p>{esc(item.get('summary', ''))}</p>
              {bullet_list}
              {render_project_links(item)}
              {render_project_contributions(item)}
            </div>
          </article>
"""


def render_project_links(item: dict[str, Any]) -> str:
    links = item.get("links", {})
    action_labels = item.get("action_labels", {})
    action_icons = item.get("action_icons", {})
    link_items = [
        ("homepage", "fa-solid fa-globe", "Project"),
        ("paper", "fa-solid fa-file-lines", "Paper"),
        ("code", "fa-brands fa-github", "Code"),
    ]
    rendered = "".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener"><i class="{esc(action_icons.get(key, icon))}"></i><span>{esc(action_labels.get(key, label))}</span></a>'
        for key, icon, label in link_items
        if (url := links.get(key))
    )
    if item.get("contributions"):
        target = f"#{project_id(item['name'])}-contributions"
        rendered += (
            f'<a href="{esc(target)}">'
            f'<i class="{esc(action_icons.get("contributions", "fa-solid fa-list-check"))}"></i>'
            f'<span>{esc(action_labels.get("contributions", "Contributions"))}</span>'
            "</a>"
        )
    return f'<div class="project-actions">{rendered}</div>' if rendered else ""


def render_project_contributions(item: dict[str, Any]) -> str:
    groups = item.get("contributions", [])
    if not groups:
        return ""
    body = []
    for group in groups:
        entries = "".join(f"<li>{esc(entry)}</li>" for entry in group.get("items", []))
        body.append(
            f"""
                <div class="contribution-group">
                  <h3>{esc(group.get('type', 'Contributions'))}</h3>
                  <ol>{entries}</ol>
                </div>
"""
        )
    return f"""
              <div class="project-contributions" id="{esc(project_id(item['name']))}-contributions">
                {''.join(body)}
              </div>
"""


def render_publication(item: dict[str, Any]) -> str:
    links = item.get("links", {})
    action_labels = item.get("action_labels", {})
    action_icons = item.get("action_icons", {})
    badges = "".join(f'<span>{esc(badge)}</span>' for badge in item.get("badges", []))
    link_items = [
        ("homepage", "fa-solid fa-globe", "Project"),
        ("paper", "fa-solid fa-file-lines", "Paper"),
        ("code", "fa-brands fa-github", "Code"),
        ("bibtex", "fa-solid fa-quote-right", "BibTeX"),
    ]
    actions = "".join(
        render_publication_action(
            key,
            links.get(key, ""),
            action_icons.get(key, icon),
            action_labels.get(key, label),
            item,
        )
        for key, icon, label in link_items
    )
    abstract = item.get("abstract") or "Abstract will be added when the public version is available."
    venue_short = item.get("venue_short") or item.get("venue", "")
    venue_full = item.get("venue_full") or item.get("venue", "")
    metadata = item.get("metadata", "")
    doi = item.get("doi", "")
    meta_parts = [part for part in (metadata, f"DOI: {doi}" if doi else "") if part]
    meta_line = " · ".join(meta_parts)
    return f"""
              <li>
                <article class="pub-card">
                  <div class="pub-content">
                    <div class="title">{esc(item['title'])}</div>
                    <div class="periodical"><strong>{esc(venue_short)}</strong> · {esc(venue_full)}</div>
                    {f'<div class="pub-meta">{esc(meta_line)}</div>' if meta_line else ''}
                    <div class="author">{esc(item['authors'])}</div>
                    <div class="pub-badges">{badges}</div>
                    <div class="pub-actions">{actions}</div>
                    <details class="pub-abstract">
                      <summary>Abstract</summary>
                      <p>{esc(abstract)}</p>
                    </details>
                    {render_bibtex_box(item)}
                  </div>
                </article>
              </li>
"""


def render_publication_action(key: str, url: str, icon: str, label: str, item: dict[str, Any]) -> str:
    if label == "BibTeX" and item.get("bibtex"):
        return (
            f'<button class="pub-action" type="button" data-bibtex-target="{esc(bibtex_id(item))}" '
            f'title="{esc(label)}"><i class="{esc(icon)}"></i><span>{esc(label)}</span></button>'
        )
    if url:
        return (
            f'<a class="pub-action" href="{esc(url)}" target="_blank" rel="noopener" '
            f'title="{esc(label)}"><i class="{esc(icon)}"></i><span>{esc(label)}</span></a>'
        )
    if key in item.get("hide_missing_actions", []):
        return ""
    return (
        f'<span class="pub-action disabled" title="{esc(label)} coming soon">'
        f'<i class="{esc(icon)}"></i><span>{esc(label)}</span></span>'
    )


def render_bibtex_box(item: dict[str, Any]) -> str:
    bibtex = item.get("bibtex")
    if not bibtex:
        return ""
    box_id = bibtex_id(item)
    return f"""
                    <div class="bibtex-box" id="{esc(box_id)}" hidden>
                      <div class="bibtex-head">
                        <strong>BibTeX</strong>
                        <button type="button" data-copy-bibtex="{esc(box_id)}">Copy</button>
                      </div>
                      <pre><code>{esc(bibtex)}</code></pre>
                    </div>
"""


def bibtex_id(item: dict[str, Any]) -> str:
    base = "".join(ch.lower() if ch.isalnum() else "-" for ch in item["title"])
    suffix_source = item.get("doi") or item.get("venue_short") or item.get("title")
    suffix = "".join(ch.lower() if ch.isalnum() else "-" for ch in suffix_source)
    slug = "-".join(part for part in base.split("-") if part)[:48]
    suffix_slug = "-".join(part for part in suffix.split("-") if part)[-18:]
    return f"bibtex-{slug}-{suffix_slug}"


def format_inline(text: Any) -> str:
    raw = str(text)
    parts = raw.split("**")
    rendered: list[str] = []
    for index, part in enumerate(parts):
        escaped = format_links(part)
        if index % 2 == 1:
            rendered.append(f"<strong>{escaped}</strong>")
        else:
            rendered.append(escaped)
    return "".join(rendered)


def format_links(text: str) -> str:
    pattern = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
    rendered: list[str] = []
    last = 0
    for match in pattern.finditer(text):
        rendered.append(esc(text[last:match.start()]))
        label, url = match.groups()
        rendered.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>')
        last = match.end()
    rendered.append(esc(text[last:]))
    return "".join(rendered)


def render_award(item: dict[str, Any]) -> str:
    return f"""
            <div class="award-item">
              <span class="award-icon">* </span>
              <div class="award-text"><strong>{esc(item['name'])}</strong><br><span class="exp-period">{esc(item['period'])}</span></div>
            </div>
"""


def render_job_card(item: dict[str, Any]) -> str:
    contacts = ", ".join(item.get("contacts", [])) or "No contacts yet"
    return f"""
          <article class="card job-card">
            <div class="job-topline">
              <span>{esc(item.get('status', ''))}</span>
              <strong>{esc(item.get('priority', ''))}</strong>
            </div>
            <h3>{esc(item['company'])}</h3>
            <p><strong>{esc(item['role'])}</strong> · {esc(item.get('location', ''))}</p>
            <p>Next: {esc(item.get('next_action', ''))}</p>
            <p>Date: {esc(item.get('next_action_date', ''))}</p>
            <p>Resume: {esc(item.get('resume_file', ''))}</p>
            <p>Contacts: {esc(contacts)}</p>
          </article>
"""


def render_resume_education(item: dict[str, Any]) -> str:
    details = "".join(f"<li>{format_inline(detail)}</li>" for detail in item.get("details", []))
    detail_list = f"<ul>{details}</ul>" if details else ""
    return (
        f'<article><h3>{esc(item["school"])} <span>{esc(item["period"])}</span></h3>'
        f'<p class="resume-line">{esc(item["degree"])}</p>{detail_list}</article>'
    )


def render_resume_experience(item: dict[str, Any]) -> str:
    bullets = "".join(f"<li>{format_inline(bullet)}</li>" for bullet in item.get("bullets", []))
    bullet_list = f"<ul>{bullets}</ul>" if bullets else ""
    role_parts = [item.get("department", ""), item.get("role", "")]
    role_line = " · ".join(part for part in role_parts if part)
    return (
        f'<article><h3>{esc(item["organization"])} <span>{esc(item["period"])}</span></h3>'
        f'<p class="resume-line"><strong>{esc(role_line)}</strong> - {esc(item.get("summary", ""))}</p>'
        f'{bullet_list}</article>'
    )


def render_resume_project(item: dict[str, Any]) -> str:
    bullets = "".join(f"<li>{format_inline(bullet)}</li>" for bullet in item.get("bullets", [])[:3])
    bullet_list = f"<ul>{bullets}</ul>" if bullets else ""
    return f'<article><h3>{esc(item["name"])}</h3><p class="resume-line">{esc(item.get("summary", ""))}</p>{bullet_list}</article>'


def render_resume_publication(item: dict[str, Any]) -> str:
    bullets = "".join(f"<li>{esc(bullet)}</li>" for bullet in item.get("bullets", [])[:2])
    bullet_list = f"<ul>{bullets}</ul>" if bullets else ""
    authors = sentence_end(item["authors"])
    venue = item.get("venue_short") or item.get("venue", "")
    notes = item.get("notes", "")
    meta = " · ".join(part for part in [venue, notes] if part)
    return (
        f'<article><h3>{esc(item["title"])}</h3>'
        f'<p class="resume-line">{esc(authors)} <em>{esc(meta)}</em></p>{bullet_list}</article>'
    )


def render_skill(item: dict[str, Any]) -> str:
    return f'<p><strong>{esc(item["group"])}</strong>: {esc(", ".join(item.get("items", [])))}</p>'


def render_resume_award(item: dict[str, Any]) -> str:
    return f'<p class="award-line"><strong>{esc(item["name"])}</strong><span>{esc(item["period"])}</span></p>'


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def sentence_end(value: Any) -> str:
    text = str(value)
    return text if text.endswith((".", "!", "?")) else f"{text}."


def main() -> None:
    parser = argparse.ArgumentParser(description="Render homepage and resume from profile data.")
    parser.add_argument("--profile", type=Path, default=ROOT / "data" / "profile.json")
    parser.add_argument("--target", type=Path, default=ROOT / "targets" / "default.json")
    parser.add_argument("--lang", choices=["en", "zh"], default="en")
    args = parser.parse_args()
    profile_arg = args.profile
    target_arg = args.target
    if args.lang == "zh" and profile_arg == ROOT / "data" / "profile.json":
        profile_arg = None
    if args.lang == "zh" and target_arg == ROOT / "targets" / "default.json":
        target_arg = None
    outputs = render_site(root=ROOT, profile_path=profile_arg, target_path=target_arg, lang=args.lang)
    for label, path in outputs.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
