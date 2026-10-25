"""
Build the portfolio site.

    python tools/build_site.py

Reads the content package and writes plain HTML into dist/. No framework, no
build step beyond this script, so GitHub Pages serves it as-is and there is
nothing that can rot.

Two conventions worth knowing:

1. RELATIVE LINKS EVERYWHERE. A project site is served from /<repo>/, so an
   absolute /static/style.css would 404. Relative paths work on Pages, locally,
   and from a file:// path.

2. EVERYTHING IS ESCAPED. The content is hand-written today, but a generator
   that trusts its input is a generator that breaks the first time someone puts
   an ampersand in a job title.
"""

from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

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

SITE_TITLE = f"{PROFILE['name']} - {PROFILE['title']}"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def prefix(depth: int) -> str:
    return "../" * depth


def chips(items: list[str]) -> str:
    if not items:
        return ""
    return '<div class="chips">' + "".join(
        f'<span class="chip">{esc(item)}</span>' for item in items
    ) + "</div>"


def ticks(items: list[str]) -> str:
    if not items:
        return ""
    return '<ul class="ticks">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def page(
    title: str,
    description: str,
    depth: int,
    body: str,
    extra_head: str = "",
) -> str:
    p = prefix(depth)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="{esc(PROFILE['name'])}">
<meta name="theme-color" content="#faf7f2">
<link rel="canonical" href="{esc(PROFILE['github'].replace('github.com/vishnuu12', 'vishnuu12.github.io/portfolio'))}/">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">

<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:image" content="{esc(PROFILE['avatar'])}">
<meta name="twitter:card" content="summary_large_image">
{extra_head}
<link rel="stylesheet" href="{p}static/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{nav(depth)}
<main id="main">
{body}
</main>
{footer(depth)}
<script src="{p}static/app.js" defer></script>
</body>
</html>
"""


def nav(depth: int) -> str:
    p = prefix(depth)
    links = "".join(
        f'<a href="{p}#{esc(anchor)}">{esc(label)}</a>' for anchor, label in SECTIONS
    )
    return f"""<header class="nav">
  <div class="nav__inner">
    <a class="brand" href="{p}#top">
      <span class="brand__mark">VS</span>
      <span>{esc(PROFILE['name'])}</span>
    </a>
    <button class="nav__toggle" type="button" aria-label="Menu" aria-expanded="false"><span></span></button>
    <nav class="nav__links">
      {links}
      <a class="nav__cta" href="{p}#contact">Get in touch</a>
    </nav>
  </div>
</header>"""


def footer(depth: int) -> str:
    p = prefix(depth)
    return f"""<footer class="footer">
  <div class="wrap footer__inner">
    <span>&copy; <span data-year>2026</span> {esc(PROFILE['name'])} &middot; {esc(PROFILE['location'])}</span>
    <span>
      <a href="{esc(PROFILE['github'])}" rel="noopener">GitHub</a> &middot;
      <a href="mailto:{esc(PROFILE['email'])}">{esc(PROFILE['email'])}</a> &middot;
      <a href="{p}resume.pdf">Resume</a>
    </span>
  </div>
</footer>"""


# --------------------------------------------------------------------------
# the sections
# --------------------------------------------------------------------------


def hero(depth: int) -> str:
    stats = "".join(
        f'<div class="stat"><div class="stat__value">{esc(s["value"])}</div>'
        f'<div class="stat__label">{esc(s["label"])}</div></div>'
        for s in PROFILE["stats"]
    )
    return f"""<section class="hero" id="top">
  <div class="hero__glow" aria-hidden="true"></div>
  <div class="wrap hero__grid">
    <div>
      <span class="hero__status"><i></i> Open to interesting work &middot; {esc(PROFILE['location'])}</span>
      <h1 class="hero__name">{esc(PROFILE['name'])}</h1>
      <p class="hero__role">
        <span>{esc(PROFILE['title'])}</span>
        <span> &middot; {esc(PROFILE['subtitle'])}</span>
      </p>
      <p class="hero__pitch">{esc(PROFILE['pitch'])}</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="#work">See the work</a>
        <a class="btn" href="mailto:{esc(PROFILE['email'])}">Email me</a>
        <a class="btn" href="{esc(PROFILE['github'])}" rel="noopener">GitHub</a>
      </div>
      <div class="hero__stats">{stats}</div>
    </div>
    <div class="monogram" role="img" aria-label="{esc(PROFILE['name'])}">
      <span>VS</span>
    </div>
  </div>
</section>"""


def about_section() -> str:
    paras = "".join(f"<p>{esc(p)}</p>" for p in PROFILE["about"])
    return f"""<section class="block" id="about">
  <div class="wrap reveal">
    <p class="eyebrow">01 &mdash; About</p>
    <h2 class="section__title">Half modern, half legacy, and the interesting part is the seam</h2>
    <div class="prose">{paras}</div>
  </div>
</section>"""


def experience_section() -> str:
    jobs = []
    for job in EXPERIENCE:
        current = " is-current" if job.get("current") else ""
        jobs.append(f"""<div class="job{current}">
  <div class="job__head">
    <span class="job__role">{esc(job['role'])}</span>
    <span class="job__company">{esc(job['company'])}</span>
    <span class="job__period">{esc(job['period'])}</span>
  </div>
  <p class="job__summary">{esc(job['summary'])}</p>
  {ticks(job['highlights'])}
  {chips(job['stack'])}
</div>""")

    education = "".join(
        f"""<div class="edu">
  <span class="job__role">{esc(e['qualification'])}</span>
  <span class="job__company">{esc(e['institution'])}</span>
  <span class="job__period edu__period">{esc(e['period'])}</span>
</div>""" for e in EDUCATION
    )

    return f"""<section class="block" id="experience">
  <div class="wrap reveal">
    <p class="eyebrow">02 &mdash; Experience</p>
    <h2 class="section__title">Where I have worked</h2>
    <p class="section__lead">
      Four years across three companies, all enterprise delivery. Each role below
      lists what I actually did rather than what the team did.
    </p>
    <div class="timeline">{''.join(jobs)}</div>
    {education}
  </div>
</section>"""


def work_section() -> str:
    cards = []
    for project in WORK_PROJECTS:
        cards.append(f"""<article class="card project">
  <h3 class="card__title">{esc(project['name'])}</h3>
  <p class="card__meta">{esc(project['client'])} &middot; {esc(project['role'])} &middot; {esc(project['duration'])} &middot; team of {esc(project['team'])}</p>
  <p class="card__body">{esc(project['summary'])}</p>
  {ticks(project['contributions'])}
  <div class="card__foot">{chips(project['stack'])}</div>
</article>""")

    return f"""<section class="block" id="work">
  <div class="wrap reveal">
    <p class="eyebrow">03 &mdash; Selected work</p>
    <h2 class="section__title">Client projects</h2>
    <p class="section__lead">
      Enterprise systems where the hard part is rarely the new feature - it is
      changing one thing without breaking the twelve that depend on it.
    </p>
    <div class="grid">{''.join(cards)}</div>
  </div>
</section>"""


def projects_section() -> str:
    cards = []
    for project in PERSONAL_PROJECTS:
        links = []
        if project.get("live"):
            links.append(f'<a href="{esc(project["live"])}" rel="noopener">Live</a>')
        if project.get("repo"):
            links.append(
                f'<a href="{esc(PROFILE["github"])}/{esc(project["repo"])}" rel="noopener">Code</a>'
            )
        cards.append(f"""<article class="card project">
  <h3 class="card__title">{esc(project['name'])}</h3>
  <p class="project__tagline">{esc(project['tagline'])}</p>
  <p class="card__body">{esc(project['summary'])}</p>
  <p class="project__why">{esc(project['why'])}</p>
  <div class="project__foot">
    {chips(project['stack'])}
    <div class="project__links">{''.join(links)}</div>
  </div>
</article>""")

    return f"""<section class="block" id="projects">
  <div class="wrap reveal">
    <p class="eyebrow">04 &mdash; Built for myself</p>
    <h2 class="section__title">Things nobody asked me to build</h2>
    <p class="section__lead">
      No client, no ticket, no deadline. This is where I keep learning, and it is
      the work I would most like to be judged on. The code is public - go and read it.
    </p>
    <div class="grid">{''.join(cards)}</div>
  </div>
</section>"""


def skills_section() -> str:
    groups = "".join(
        f"""<div class="skillgroup">
  <p class="skillgroup__name">{esc(g['group'])}</p>
  {chips(g['items'])}
</div>""" for g in SKILL_GROUPS
    )
    return f"""<section class="block" id="skills">
  <div class="wrap reveal">
    <p class="eyebrow">05 &mdash; Skills</p>
    <h2 class="section__title">What I work with</h2>
    <p class="section__lead">
      Grouped rather than listed, because "Azure Functions" and "Git" are not the
      same kind of claim and a wall of keywords hides that.
    </p>
    <div class="grid grid--tight">{groups}</div>
  </div>
</section>"""


def now_section() -> str:
    items = "".join(
        f"""<div class="card now__item">
  <span class="now__title">{esc(item['title'])}</span>
  <span class="now__detail">{esc(item['detail'])}</span>
</div>""" for item in PROFILE["now"]["items"]
    )
    return f"""<section class="block" id="now">
  <div class="wrap reveal">
    <p class="eyebrow">06 &mdash; Now</p>
    <div class="now__head">
      <h2 class="section__title" style="margin:0">Currently</h2>
      <span class="now__stamp">{esc(PROFILE['now']['as_of'])}</span>
    </div>
    <p class="section__lead">{esc(PROFILE['now']['intro'])}</p>
    <div class="grid">{items}</div>
  </div>
</section>"""


def writing_section(depth: int) -> str:
    p = prefix(depth)
    cards = "".join(
        f"""<a class="note" href="{p}writing/{esc(note['slug'])}.html">
  <div class="note__meta"><span>{esc(note['date'])}</span><span>{esc(note['reading'])} read</span></div>
  <h3 class="note__title">{esc(note['title'])}</h3>
  <p class="note__summary">{esc(note['summary'])}</p>
  <p class="note__more">Read the note &rarr;</p>
</a>""" for note in NOTES
    )
    return f"""<section class="block" id="writing">
  <div class="wrap reveal">
    <p class="eyebrow">07 &mdash; Writing</p>
    <h2 class="section__title">Notes</h2>
    <p class="section__lead">
      Short pieces written from work that exists. The code is public and the
      numbers are the numbers the tests print.
    </p>
    <div class="grid">{cards}</div>
  </div>
</section>"""


def contact_section() -> str:
    return f"""<section class="block" id="contact">
  <div class="wrap reveal">
    <div class="contact">
      <div class="contact__inner">
        <div>
          <p class="eyebrow">08 &mdash; Contact</p>
          <h2>Let's talk about what you're building.</h2>
          <p>
            I am happy to talk about .NET and Angular work, cloud architecture,
            anything involving an LLM, or a project of yours that needs a second
            pair of hands. Email is the fastest way to reach me.
          </p>
          <div class="emailrow">
            <span class="emailrow__addr">{esc(PROFILE['email'])}</span>
            <button class="copybtn" type="button" data-copy="{esc(PROFILE['email'])}">copy</button>
            <a class="btn btn--primary" href="mailto:{esc(PROFILE['email'])}">Send an email</a>
            <a class="btn" href="{esc(PROFILE['resume'])}" download>Download resume</a>
          </div>
        </div>
        <div class="contact__monogram" aria-hidden="true"><span>VS</span></div>
      </div>
    </div>
  </div>
</section>"""


def render_index() -> str:
    body = "".join(
        [
            hero(0),
            about_section(),
            experience_section(),
            work_section(),
            projects_section(),
            skills_section(),
            now_section(),
            writing_section(0),
            contact_section(),
        ]
    )
    return page(
        SITE_TITLE,
        f"{PROFILE['title']} in {PROFILE['location']}. {PROFILE['subtitle']}. "
        "Enterprise .NET and cloud applications, Angular interfaces, and a habit of "
        "building things nobody asked for.",
        0,
        body,
    )


def render_note(note: dict, index: int) -> str:
    blocks = []
    for block in note["body"]:
        if "h" in block:
            blocks.append(f"<h2>{esc(block['h'])}</h2>")
        elif "list" in block:
            blocks.append("<ul>" + "".join(f"<li>{esc(i)}</li>" for i in block["list"]) + "</ul>")
        elif "code" in block:
            blocks.append(f"<pre><code>{esc(block['code'])}</code></pre>")
        elif "quote" in block:
            blocks.append(f"<blockquote>{esc(block['quote'])}</blockquote>")
        else:
            blocks.append(f"<p>{esc(block['p'])}</p>")

    previous = NOTES[index - 1] if index > 0 else None
    following = NOTES[index + 1] if index < len(NOTES) - 1 else None
    pager = []
    if previous:
        pager.append(f'<a href="{esc(previous["slug"])}.html">&larr; {esc(previous["title"])}</a>')
    if following:
        pager.append(f'<a href="{esc(following["slug"])}.html" style="margin-left:auto">{esc(following["title"])} &rarr;</a>')
    pager_html = f'<div class="pager" style="display:flex;gap:1rem;margin-top:3rem;font-size:.88rem">{"".join(pager)}</div>' if pager else ""

    body = f"""<article class="wrap article">
  <a class="article__back" href="../index.html#writing">&larr; All notes</a>
  <div class="article__meta"><span>{esc(note['date'])}</span><span>{esc(note['reading'])} read</span></div>
  <h1>{esc(note['title'])}</h1>
  <p class="section__lead">{esc(note['summary'])}</p>
  {chips(note['tags'])}
  <div class="article__body">{''.join(blocks)}</div>
  {pager_html}
</article>"""

    return page(f"{note['title']} - {PROFILE['name']}", note["summary"], 1, body)


def render_404() -> str:
    body = """<section class="hero" style="text-align:center">
  <div class="hero__glow" aria-hidden="true"></div>
  <div class="wrap">
    <p class="eyebrow" style="justify-content:center">404</p>
    <h1 class="hero__name" style="font-size:clamp(2rem,6vw,3.2rem)">That page isn't here.</h1>
    <p class="hero__pitch" style="margin:1rem auto 2rem">
      The link may be old, or I may have moved something. Either way, the way back is below.
    </p>
    <div class="hero__actions" style="justify-content:center">
      <a class="btn btn--primary" href="index.html">Back to the portfolio</a>
      <a class="btn" href="index.html#writing">Read the notes</a>
    </div>
  </div>
</section>"""
    return page(f"Not found - {PROFILE['name']}", "Page not found.", 0, body)


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------


def clear_directory(directory: Path) -> None:
    """Empty a directory without removing the directory itself."""
    if not directory.exists():
        return
    for child in directory.iterdir():
        if child.is_dir():
            clear_directory(child)
            child.rmdir()
        else:
            child.unlink()


def build(out_dir: Path) -> dict:
    clear_directory(out_dir)
    (out_dir / "static").mkdir(parents=True, exist_ok=True)
    (out_dir / "writing").mkdir(parents=True, exist_ok=True)

    for name in ("style.css", "app.js"):
        shutil.copy(ROOT / "site" / "static" / name, out_dir / "static" / name)

    favicon = ROOT / "site" / "static" / "favicon.svg"
    if favicon.exists():
        shutil.copy(favicon, out_dir / "favicon.svg")

    # A resume built by tools/build_resume.py, if it has been run.
    resume = ROOT / "resume.pdf"
    if resume.exists():
        shutil.copy(resume, out_dir / "resume.pdf")

    (out_dir / "index.html").write_text(render_index(), encoding="utf-8")
    (out_dir / "404.html").write_text(render_404(), encoding="utf-8")
    for index, note in enumerate(NOTES):
        (out_dir / "writing" / f"{note['slug']}.html").write_text(
            render_note(note, index), encoding="utf-8"
        )

    return {
        "out_dir": str(out_dir),
        "pages": 2 + len(NOTES),
        "notes": len(NOTES),
        "has_resume": resume.exists(),
    }


def main() -> int:
    report = build(ROOT / "dist")
    print(f"built {report['pages']} pages into {report['out_dir']}")
    print(f"  notes      : {report['notes']}")
    print(f"  resume.pdf : {'included' if report['has_resume'] else 'MISSING - run tools/build_resume.py'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
