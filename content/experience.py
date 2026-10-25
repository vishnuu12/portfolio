"""
Work history and education, from the resume.

Dates are written as the resume has them. The notes under each role are the
responsibilities and the outcomes that are actually checkable - no adjectives
doing the work of evidence.
"""

EXPERIENCE = [
    {
        "role": "Senior Software Engineer",
        "company": "Zuci Systems Pvt. Ltd.",
        "period": "Oct 2025 - Present",
        "location": "Chennai",
        "current": True,
        "summary": (
            "Senior engineer on a healthcare prior-authorization platform, working "
            "across the Angular interface, the .NET 8 APIs, the database and the "
            "background processing."
        ),
        "highlights": [
            "Deliver client-requested enhancements and defect fixes across UI, APIs, "
            "business logic, database and background jobs.",
            "Analyse requirement impact across every layer before changing anything, "
            "so existing workflows and integrations keep working.",
            "Design and maintain SQL Server schema changes and stored procedures, "
            "applying normalisation principles to the data model.",
            "Investigate and remove performance bottlenecks in Angular screens, APIs "
            "and stored procedures.",
            "Write xUnit tests for changed functionality and support regression "
            "testing across related workflows.",
            "Carry changes through release: deployment coordination and production "
            "support, including investigating what comes back from production.",
        ],
        "stack": [
            ".NET 8", "C#", "ASP.NET Core Web API", "ASP.NET Webforms",
            "Entity Framework Core", "Angular", "TypeScript", "MSSQL", "xUnit",
        ],
    },
    {
        "role": "Dotnet Developer",
        "company": "Vega Intellisoft Pvt. Ltd.",
        "period": "Oct 2023 - Oct 2025",
        "location": "Chennai",
        "current": False,
        "summary": (
            "Full-stack developer on a logistics automation platform for a building-"
            "materials manufacturer, from the Angular dashboard down to the Azure "
            "Functions."
        ),
        "highlights": [
            "Led full-stack development with Angular, ASP.NET Core Web API and "
            "SQL Server on a logistics automation platform.",
            "Integrated real-time GPS and FASTag tracking through external APIs for "
            "truck movement monitoring.",
            "Automated the in-plant workflow end to end - Truck Reported, Weighing, "
            "Loading, Dispatch - cutting delays and manual effort.",
            "Built Angular dashboards and reports for turnaround time, challans and "
            "bay occupancy on live data.",
            "Developed reusable APIs with clean architecture, holding quality with "
            "GitLab CI/CD and SonarQube.",
            "Shipped features that reduced truck idle time and improved dispatch "
            "efficiency.",
        ],
        "stack": [
            ".NET Core", "C#", "Web API", "Entity Framework", "Azure Cosmos DB",
            "Angular", "PrimeNG", "Azure Functions", "Logic Apps",
            "API Management", "Key Vault", "SonarQube", "xUnit",
        ],
    },
    {
        "role": "Dotnet Developer",
        "company": "Cinthu Solutions",
        "period": "Oct 2022 - Oct 2023",
        "location": "Chennai",
        "current": False,
        "summary": (
            "Built ERP features for a small team, replacing standalone tools with one "
            "platform."
        ),
        "highlights": [
            "Designed responsive UI in Angular and built dynamic forms with real-time "
            "validation.",
            "Built RESTful APIs in ASP.NET Core and optimised SQL queries for "
            "high-performance database access.",
            "Wrote xUnit tests to keep backend services reliable.",
            "Unified several standalone tools into a single ERP platform, improving "
            "operational transparency across departments.",
            "Automated data flows and cut paper-based processes.",
        ],
        "stack": [
            "ASP.NET Web Forms", ".NET Core Web API", "C#", "Entity Framework",
            "SQL Server", "Repository Pattern", "Angular", "SignalR", "xUnit",
        ],
    },
]

EDUCATION = [
    {
        "qualification": "B.E. Computer Science and Engineering",
        "institution": "Chettinad College of Engineering and Technology",
        "affiliation": "Anna University",
        "period": "2017 - 2021",
    },
]
