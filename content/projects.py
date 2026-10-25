"""
Projects, in two groups.

"Selected work" is professional - client projects, described at the same level
the resume describes them. "Built for myself" is the open-source side, where the
code is public and you can go and read it.

Ordering inside each group is by how much there is to say, not by date.
"""

WORK_PROJECTS = [
    {
        "name": "PaHub",
        "client": "Agadia",
        "role": "Senior Software Engineer",
        "duration": "1+ years",
        "team": "6-8",
        "summary": (
            "A healthcare prior-authorization platform. Teams intake authorization "
            "cases, collect supporting and clinical information, route cases through "
            "work queues for review, and record outcomes - across a modern Angular "
            "interface and established legacy workflows that both have to keep "
            "working."
        ),
        "contributions": [
            "Enhancements and defect fixes across UI, APIs, business logic, database "
            "and background processing.",
            "Schema changes and stored procedures, with normalisation applied to the "
            "data model rather than bolted on.",
            "Performance work on Angular screens, APIs and stored procedures.",
            "xUnit tests with AI-validated coverage read from the coverage report, and "
            "AI-generated test data seeded to the dev database for functional checks.",
        ],
        "stack": [
            ".NET 8", "C#", "ASP.NET Core Web API", "ASP.NET Webforms",
            "Entity Framework Core", "Angular", "TypeScript", "MSSQL", "xUnit",
        ],
    },
    {
        "name": "Transport Management System",
        "client": "Saint Gobain",
        "role": "Dotnet Developer",
        "duration": "2+ years",
        "team": "10",
        "summary": (
            "Logistics automation for a building-materials manufacturer. Trucks are "
            "tracked through the plant - reported, weighed, loaded, dispatched - and "
            "the dashboards show turnaround time, challans and bay occupancy on live "
            "data."
        ),
        "contributions": [
            "Real-time GPS and FASTag tracking integrated through external APIs for "
            "truck movement monitoring.",
            "End-to-end automation of the in-plant workflow, cutting delays and manual "
            "effort.",
            "Angular dashboards and reports for turnaround time, challans and bay "
            "occupancy.",
            "Reusable APIs with clean architecture, held to quality with GitLab CI/CD "
            "and SonarQube, and xUnit coverage above 90%.",
        ],
        "stack": [
            ".NET Core", "C#", "Web API", "Entity Framework", "Azure Cosmos DB",
            "Azure Functions", "Blob Storage", "Logic Apps", "API Management",
            "Key Vault", "Angular", "PrimeNG", "SonarQube", "xUnit",
        ],
    },
    {
        "name": "Enterprise Resource Planning",
        "client": "LSERP",
        "role": "Dotnet Developer",
        "duration": "1+ years",
        "team": "3-4",
        "summary": (
            "ERP for a small team, replacing a set of standalone tools with one "
            "platform so departments could see the same data."
        ),
        "contributions": [
            "Responsive Angular UI and dynamic forms with real-time validation.",
            "RESTful ASP.NET Core APIs, with SQL queries optimised for high-"
            "performance access.",
            "xUnit tests for backend service reliability.",
            "Automated data flows and removed paper-based processes, improving "
            "transparency across departments.",
        ],
        "stack": [
            "ASP.NET Web Forms", ".NET Core Web API", "C#", "Entity Framework",
            "SQL Server", "Repository Pattern", "Angular", "SignalR", "xUnit",
        ],
    },
]

PERSONAL_PROJECTS = [
    {
        "name": "Mozhi",
        "tagline": "A conversation in your language",
        "repo": "bhasha",
        "live": "https://bhasha-gray.vercel.app",
        "language": "TypeScript",
        "summary": (
            "A Tamil/English conversation app. You speak, it finds the words - built "
            "for the way people here actually talk, which is a mix of both languages "
            "in the same sentence."
        ),
        "why": "Because typing in Tamil is a different skill from speaking it, and most tools assume the second one.",
        "stack": ["TypeScript", "Speech", "LLM"],
    },
    {
        "name": "Sattam",
        "tagline": "Everyday Indian law, in plain Tamil and English",
        "repo": "sattam-static-site",
        "live": "https://vishnuu12.github.io/sattam-static-site/",
        "language": "HTML",
        "summary": (
            "165 everyday legal points - traffic stops, OTP fraud, rent deposits, "
            "unpaid salary, Aadhaar misuse - grouped by the situation you are in "
            "rather than by the section of the Act."
        ),
        "why": "The information exists. It is just not written in the language, or the order, that helps someone standing in the moment.",
        "stack": ["HTML", "CSS", "Tamil + English"],
    },
    {
        "name": "AI Concepts Playground",
        "tagline": "Fifteen ML and LLM concepts you can drag a slider on",
        "repo": "AIConceptsPlayground",
        "live": "https://vishnuu12.github.io/AIConceptsPlayground/",
        "language": "Python",
        "summary": (
            "Gradient descent, logistic regression, k-means, PCA and backpropagation "
            "written from scratch in NumPy - then embeddings, tokenization, RAG, tool "
            "calling and evaluation. Every concept runs in the browser, every number "
            "on the page came from the code, and 47 tests assert the maths is right."
        ),
        "why": "I could use scikit-learn. I wanted to stop guessing what it was doing.",
        "stack": ["Python", "NumPy", "JavaScript", "pytest"],
    },
    {
        "name": "Angular Concepts Playground",
        "tagline": "Fifteen Angular concepts, with the interview questions",
        "repo": "AngularConceptsPlayground",
        "live": "https://vishnuu12.github.io/AngularConceptsPlayground/",
        "language": "TypeScript",
        "summary": (
            "Components, directives, DI, routing, guards, lazy loading, HttpClient, "
            "forms, lifecycle hooks, RxJS and state management - each with a running "
            "demo, plus 74 interview questions with answers you can say out loud."
        ),
        "why": "Written to explain the framework to the person I was two years ago.",
        "stack": ["Angular 19", "TypeScript", "RxJS"],
    },
    {
        "name": "EnodaAI Voice Assistant",
        "tagline": "A Tamil Nadu style AI voice assistant for Android",
        "repo": "EnodaAI-VoiceAssistant",
        "live": None,
        "language": "Kotlin",
        "summary": (
            "Kotlin and Jetpack Compose, with LLM answers, web search, local app "
            "control, offline and online modes, and both male and female voices - "
            "speaking the way people around here speak."
        ),
        "why": "Every voice assistant I tried sounded like it had never been to Tamil Nadu.",
        "stack": ["Kotlin", "Jetpack Compose", "Android", "LLM"],
    },
    {
        "name": "Teardown & Rebuild",
        "tagline": "Interactive documentaries for machines",
        "repo": "bicycle-teardown-rebuild",
        "live": "https://vishnuu12.github.io/bicycle-teardown-rebuild/",
        "language": "HTML",
        "summary": (
            "A bicycle and a TVS Ronin 225, taken apart part by part: an anatomy map "
            "you can click, the one-to-one support chain (leg to wheel, hand to "
            "brake), and the safe order to dismantle and rebuild. Tamil and English."
        ),
        "why": "Manuals list parts. They do not tell you what depends on what.",
        "stack": ["HTML", "CSS", "JavaScript"],
    },
]
