"""
Tests for the portfolio build.

A portfolio is judged in about ten seconds, and the things that break it are
boring: a dead link, a page that 404s, an email address that goes nowhere, a
placeholder that shipped. These tests cover exactly those.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_site  # noqa: E402

from content import (  # noqa: E402
    EDUCATION,
    EXPERIENCE,
    NOTES,
    PERSONAL_PROJECTS,
    PROFILE,
    SECTIONS,
    SKILL_GROUPS,
    WORK_PROJECTS,
)


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("portfolio")
    build_site.build(out / "dist")
    return out / "dist"


# --------------------------------------------------------------- the build


def test_expected_pages_exist(built: Path):
    assert (built / "index.html").exists()
    assert (built / "404.html").exists()
    assert (built / "static" / "style.css").exists()
    assert (built / "static" / "app.js").exists()
    assert (built / "favicon.svg").exists()
    for note in NOTES:
        assert (built / "writing" / f"{note['slug']}.html").exists()


def test_all_internal_links_resolve(built: Path):
    """
    The check that catches the classic Pages mistake: an absolute path works at
    the domain root and 404s on a project site served from /<repo>/.
    """
    href = re.compile(r'(?:href|src)="([^"#]+)(#[^"]*)?"')
    broken: list[str] = []

    for page in built.rglob("*.html"):
        for target, _fragment in href.findall(page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            if not (page.parent / target).resolve().exists():
                broken.append(f"{page.relative_to(built)} -> {target}")

    assert not broken, "broken internal links:\n" + "\n".join(broken)


def test_no_absolute_asset_paths(built: Path):
    for page in built.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        assert 'href="/' not in text, f"{page.name} has an absolute href"
        assert 'src="/' not in text, f"{page.name} has an absolute src"


def test_no_placeholders_shipped(built: Path):
    """Nothing half-written may reach a live site."""
    smells = ("TODO", "FIXME", "Lorem ipsum", "XXX", "{{", "}}", "PLACEHOLDER")
    for page in built.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for smell in smells:
            assert smell not in text, f"{page.name} contains {smell!r}"


def test_every_nav_target_exists_on_the_page(built: Path):
    """A nav link to a section that does not exist is a silent dead end."""
    index = (built / "index.html").read_text(encoding="utf-8")
    for anchor, _label in SECTIONS:
        assert f'id="{anchor}"' in index, f"nav links to #{anchor} but no such section"


# ------------------------------------------------------------- the content


def test_contact_details_are_real_and_consistent(built: Path):
    assert "@" in PROFILE["email"], "the contact email must be a real address"
    assert PROFILE["email"].endswith(".com")
    assert "gmai.com" not in PROFILE["email"], "the resume's typo must not have followed us"

    for page in built.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        # Any address in the markup must be the one in the profile.
        for found in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
            assert found == PROFILE["email"], f"{page.name} mentions {found}"


def test_no_phone_number_on_the_site(built: Path):
    """Vishnu asked for email only - a public phone number invites scam calls."""
    for page in built.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        assert "9092697353" not in text, f"{page.name} exposes the phone number"


def test_personal_hr_details_stay_off_the_site(built: Path):
    """
    Date of birth, father's name and marital status are on the resume but have no
    business on a page anyone can read.
    """
    forbidden = ("Saravanan", "12-03-2000", "UnMarried", "Marital", "Father")
    for page in built.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for item in forbidden:
            assert item not in text, f"{page.name} exposes {item!r}"


def test_every_project_has_a_way_to_be_checked(built: Path):
    """A project with no link is an unverifiable claim."""
    index = (built / "index.html").read_text(encoding="utf-8")
    for project in PERSONAL_PROJECTS:
        assert project.get("repo") or project.get("live"), project["name"]
        if project.get("live"):
            assert project["live"].startswith("https://")
        if project.get("repo"):
            assert f'{PROFILE["github"]}/{project["repo"]}' in index


def test_work_projects_and_roles_are_complete():
    for project in WORK_PROJECTS:
        for field in ("name", "client", "role", "duration", "summary", "contributions", "stack"):
            assert project.get(field), f"{project.get('name')} is missing {field}"

    for job in EXPERIENCE:
        for field in ("role", "company", "period", "summary", "highlights", "stack"):
            assert job.get(field), f"{job.get('company')} is missing {field}"

    assert EXPERIENCE[0]["current"] is True, "the newest role should be marked current"
    assert len(EDUCATION) >= 1


def test_skills_and_notes_are_not_empty():
    assert len(SKILL_GROUPS) >= 4
    for group in SKILL_GROUPS:
        assert group["items"], f"{group['group']} has no items"

    for note in NOTES:
        assert len(note["body"]) >= 5, f"{note['slug']} is too short to publish"
        assert note["summary"].endswith((".", "!"))
        # Blocks must be one of the shapes the generator understands.
        for block in note["body"]:
            assert set(block) & {"p", "h", "list", "code", "quote"}, block


def test_no_claim_of_ai_credit_where_none_exists(built: Path):
    """
    A guard for the one thing a portfolio must never do: overstate. The site
    describes what was built, not how impressive it was.
    """
    hype = ("world-class", "10x", "revolutionary", "guru", "ninja", "rockstar")
    for page in built.rglob("*.html"):
        lowered = page.read_text(encoding="utf-8").lower()
        for word in hype:
            assert word not in lowered, f"{page.name} contains hype: {word}"
