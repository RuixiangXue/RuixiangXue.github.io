import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.render_site import render_site  # noqa: E402


class RenderSiteTest(unittest.TestCase):
    def test_render_site_uses_profile_and_target_tags(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))

        profile = {
            "person": {
                "name": "Ruixiang Xue",
                "name_zh": "薛瑞翔",
                "title": "Ph.D. Student, Nanjing University",
                "email": "xrxee@smail.nju.edu.cn",
                "phone": "+86-13777803815",
                "location": "Nanjing, China",
                "summary": "Researcher in intelligent point cloud compression.",
                "research_interests": ["Point cloud compression"],
            },
            "links": [{"label": "GitHub", "url": "https://github.com/RuixiangXue"}],
            "education": [
                {
                    "school": "Nanjing University",
                    "degree": "Ph.D.",
                    "period": "2021 - 2027",
                    "details": [],
                }
            ],
            "experience": [],
            "projects": [
                {"name": "Point Cloud Compression", "tags": ["compression"], "summary": "39% geometry gain.", "bullets": []},
                {"name": "Camera Assistant", "tags": ["demo"], "summary": "AI coding demo.", "bullets": []},
            ],
            "publications": [],
            "skills": [],
            "awards": [],
        }
        pipeline = {
            "jobs": [
                {
                    "company": "Example AI Lab",
                    "role": "Research Intern",
                    "status": "to_apply",
                    "priority": "high",
                    "next_action": "Tailor resume",
                    "next_action_date": "2026-07-01",
                }
            ]
        }
        target = {
            "title": "Research Resume",
            "focus": "Compression research roles",
            "include_project_tags": ["compression"],
        }

        profile_path = tmp / "profile.json"
        target_path = tmp / "target.json"
        data_dir = tmp / "data"
        jobs_dir = tmp / "jobs"
        data_dir.mkdir()
        jobs_dir.mkdir()
        profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
        (jobs_dir / "pipeline.json").write_text(json.dumps(pipeline, ensure_ascii=False), encoding="utf-8")
        target_path.write_text(json.dumps(target, ensure_ascii=False), encoding="utf-8")

        outputs = render_site(root=tmp, profile_path=profile_path, target_path=target_path)
        outputs_zh = render_site(root=tmp, profile_path=profile_path, target_path=target_path, lang="zh")

        home = outputs["home"].read_text(encoding="utf-8")
        resume = outputs["resume"].read_text(encoding="utf-8")
        jobs_page = outputs["jobs"].read_text(encoding="utf-8")
        home_zh = outputs_zh["home"].read_text(encoding="utf-8")
        resume_zh = outputs_zh["resume"].read_text(encoding="utf-8")
        self.assertIn("Ruixiang Xue", home)
        self.assertIn("薛瑞翔", home)
        self.assertIn("中文", home)
        self.assertIn("prism-static.css", home)
        self.assertIn('title="CV EN"', home)
        self.assertIn('title="CV 中文"', home)
        self.assertIn('href="https://ruixiangxue.github.io/assets/cv/resume-en.pdf"', home)
        self.assertIn('href="https://ruixiangxue.github.io/assets/cv/resume-zh.pdf"', home)
        self.assertNotIn("Download my CV", home)
        self.assertIn("Work Experience", home)
        self.assertIn("research-map", home)
        self.assertNotIn("logo-cloud", home)
        self.assertNotIn("Field Notes", home)
        self.assertIn("Point Cloud Compression", resume)
        self.assertNotIn("Camera Assistant", resume)
        self.assertIn("Research Resume", resume)
        self.assertIn("Example AI Lab", jobs_page)
        self.assertIn("Tailor resume", jobs_page)
        self.assertEqual(outputs_zh["home"].name, "index-zh.html")
        self.assertEqual(outputs_zh["resume"].name, "resume-zh.html")
        self.assertIn("English", home_zh)
        self.assertIn('title="CV EN"', home_zh)
        self.assertIn('title="CV 中文"', home_zh)
        self.assertIn("空间智能", home_zh)
        self.assertIn("研究简历", resume_zh)


if __name__ == "__main__":
    unittest.main()
