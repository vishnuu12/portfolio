"""All site content, in one place. The generator imports from here."""

from .experience import EDUCATION, EXPERIENCE
from .profile import PROFILE
from .projects import PERSONAL_PROJECTS, WORK_PROJECTS
from .skills import SKILL_GROUPS
from .writing import NOTES

SECTIONS = [
    ("about", "About"),
    ("experience", "Experience"),
    ("work", "Selected work"),
    ("projects", "Built for myself"),
    ("skills", "Skills"),
    ("now", "Now"),
    ("writing", "Writing"),
    ("contact", "Contact"),
]
