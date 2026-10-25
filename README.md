# vishnuu12.github.io/portfolio

My portfolio - a single page, plus a few notes, built by a small Python script
and served by GitHub Pages.

**Live:** https://vishnuu12.github.io/portfolio/

## Why it is built this way

It is a portfolio for a developer, so the thing it has to prove is that I can
build something that works. So: no framework, no build tooling to age badly, no
web fonts to flash, and no dependencies at all in what gets served.

```
content/            the words - profile, experience, projects, skills, notes
site/static/        one stylesheet and one small script
tools/build_site.py content -> plain HTML in dist/
tools/build_resume.py   content -> resume.pdf (reportlab)
tests/test_site.py  the build, every link, and the things that must NOT ship
```

```bash
python tools/build_resume.py   # writes resume.pdf
python tools/build_site.py     # writes dist/
python -m pytest tests -q
```

Every push to `main` runs the tests, rebuilds, and republishes. If a link breaks
or a placeholder sneaks in, the build fails and nothing is deployed.

## The choices worth explaining

**One source of truth.** The site and `resume.pdf` are generated from the same
`content/` package. A resume that disagrees with the site it is linked from is
worse than either one alone.

**Relative links everywhere.** A GitHub Pages project site is served from
`/<repo>/`, so an absolute `/static/style.css` would 404. There is a test for
this because it is the mistake everyone makes exactly once.

**Dark by choice, not by default.** No light theme, because a half-considered
second theme is worse than one considered one.

**It degrades.** JavaScript is off: you get a readable, navigable page. Motion is
reduced: the reveals and the drift stop. Nothing is behind a script.

**No invented facts.** Everything on the site comes from my resume or my public
repositories. There are tests that fail if a phone number, a date of birth or a
piece of hype copy reaches the output.

## Editing it

Add a project to `content/projects.py`, add a note to `content/writing.py`, run
the two build commands. The generator escapes everything, so an ampersand in a
job title cannot break the page.
