"""
Skills, grouped the way the resume groups them.

Kept as groups rather than one long list because "Azure Functions" and "Git"
are not the same kind of claim, and a wall of keywords hides that.
"""

SKILL_GROUPS = [
    {
        "group": "Backend",
        "icon": "server",
        "items": [
            "ASP.NET Core", ".NET 8", ".NET Core", "C#", "Web API", "MVC",
            "ASP.NET Web Forms", "REST APIs", "SOLID",
        ],
    },
    {
        "group": "Frontend",
        "icon": "layout",
        "items": [
            "Angular", "TypeScript", "JavaScript", "RxJS", "HTML5", "CSS3",
            "Bootstrap", "PrimeNG",
        ],
    },
    {
        "group": "Data",
        "icon": "database",
        "items": [
            "SQL Server", "Azure Cosmos DB", "Entity Framework Core",
            "Code First & Database First", "Stored Procedures", "Normalisation",
        ],
    },
    {
        "group": "Azure",
        "icon": "cloud",
        "items": [
            "App Services", "Functions (Blob, Queue, Service Bus, Cosmos, Timer)",
            "Logic Apps", "API Management", "Storage Accounts", "Key Vault",
            "App Configuration", "Service Bus",
        ],
    },
    {
        "group": "AI & GenAI",
        "icon": "spark",
        "items": [
            "LLM integration", "Anthropic Claude via Cloudflare AI Gateway",
            "Prompt engineering", "Prompt layering",
            "Automated prompt training & validation", "RAG concepts",
            "Claude Code", "GitHub Copilot",
        ],
    },
    {
        "group": "Testing & Observability",
        "icon": "pulse",
        "items": [
            "xUnit", "SonarQube", "Serilog", "Elastic Cloud (ELK)",
            "GitLab CI/CD", "Code coverage",
        ],
    },
    {
        "group": "Tools",
        "icon": "tool",
        "items": ["Git", "TFS", "Visual Studio", "VS Code"],
    },
    {
        "group": "Also writing",
        "icon": "pen",
        "items": ["Python", "NumPy", "Kotlin", "Jetpack Compose", "pytest", "pandas"],
    },
]
