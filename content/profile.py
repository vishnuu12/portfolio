"""
Who this site is about.

Everything here is taken from Vishnu's own resume and his public GitHub. Nothing
is invented - if a fact is not in one of those two places, it does not appear on
the site.

Deliberately NOT included, though the resume contains them: date of birth,
father's name, marital status. Those belong on a form for an employer, not on a
page anyone can read, and they add nothing a recruiter is hiring for.
"""

PROFILE = {
    "name": "Vishnu S",
    "handle": "vishnuu12",
    "title": "Full-Stack Developer",
    "subtitle": ".NET · Angular · React · Azure",
    "location": "Chennai, India",
    "email": "vishnudcrazie@gmail.com",
    "github": "https://github.com/vishnuu12",
    "avatar": "https://avatars.githubusercontent.com/u/101856151?v=4",
    "resume": "resume.pdf",

    # The hero paragraph. Short on purpose: a hero is a first impression, not a
    # summary. The detail lives in the sections below.
    "pitch": (
        "Four years building enterprise .NET and cloud applications end to end - "
        "ASP.NET Core APIs, Angular interfaces, Azure Functions and SQL Server. "
        "Lately I spend my evenings on AI: LLM integration at work, and teaching "
        "machine learning by writing it from scratch at home."
    ),

    "stats": [
        {"value": "4+", "label": "years building software"},
        {"value": "3", "label": "companies, enterprise delivery"},
        {"value": "35", "label": "public repositories"},
        {"value": "6", "label": "apps live in production"},
    ],

    "about": [
        "I work across the whole stack. On the back end that means ASP.NET Core and "
        ".NET 8, Web API, Entity Framework, and SQL Server - with Azure Functions, "
        "Service Bus, Logic Apps and Key Vault doing the plumbing. On the front end "
        "it means Angular, TypeScript and PrimeNG, building the screens that people "
        "actually use to get their work done.",
        "Most of my professional work has been on systems that are half modern and "
        "half legacy, where the job is rarely 'write a new feature' and more often "
        "'change this without breaking the twelve things that depend on it'. That is "
        "where I learned to read a codebase before touching it, to keep SOLID "
        "boundaries when extending old code, and to write the unit test that proves "
        "the change did what I said it did.",
        "Outside work I build things that do not need a client to approve them: "
        "bilingual Tamil sites like Sattam and Mozhi, an Android voice assistant, and "
        "a set of concept playgrounds that explain .NET, Angular, React and machine "
        "learning by making each idea runnable. They are how I keep learning, and "
        "they are the part of my work I would most like to be judged on.",
    ],

    # "Now" is a date-stamped snapshot, which is the point: it goes stale honestly.
    "now": {
        "as_of": "October 2026",
        "intro": "What I am actually spending time on right now.",
        "items": [
            {
                "title": "Healthcare prior-authorization platform",
                "detail": (
                    "Day job: senior engineer on a .NET 8 + Angular platform for "
                    "intake, review routing and outcomes. Mostly enhancements, "
                    "performance work and the unit tests that keep them honest."
                ),
            },
            {
                "title": "Learning AI by building it",
                "detail": (
                    "Fifteen concepts from scratch - gradient descent, k-means, PCA, "
                    "backpropagation - then the LLM side: retrieval, prompting, tool "
                    "calling and evaluation, each with a demo you can drag a slider on."
                ),
            },
            {
                "title": "Tamil-first tools",
                "detail": (
                    "Sattam (everyday Indian law in plain Tamil and English) and "
                    "Mozhi (a Tamil/English conversation app). Both started because "
                    "the information exists but not in the language people read."
                ),
            },
        ],
    },
}
