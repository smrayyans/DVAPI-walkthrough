# DVAPI Walkthrough

Hands-on walkthrough of the **OWASP API Security Top 10 (2023)** using [DVAPI](https://github.com/payatu/DVAPI) (Damn Vulnerable API). All 10 vulnerabilities manually exploited — no automated scanners.

## Vulnerabilities Covered

| # | Category | Endpoint |
|---|---|---|
| API1 | Broken Object Level Authorization | `GET /api/getNote` |
| API2 | Broken Authentication | `GET /api/user/user` |
| API3 | Broken Object Property Level Authorization | `POST /api/register` |
| API4 | Unrestricted Resource Consumption | `POST /api/profile/upload` |
| API5 | Broken Function Level Authorization | `DELETE /api/user/:username` |
| API6 | Unrestricted Access to Sensitive Business Flows | `POST /api/addTicket` |
| API7 | Server Side Request Forgery (SSRF) | `POST /api/addNoteWithLink` |
| API8 | Security Misconfiguration | `POST /api/addNote` |
| API9 | Improper Inventory Management | `POST /api/allChallenges` |
| API10 | Unsafe Consumption of APIs (NoSQL Injection) | `POST /api/login` |

## Tools Used

- **Burp Suite** — Proxy, Repeater, Intruder, Collaborator, JWT Editor extension
- **Postman** — API4 and API2 reproduction
- **hashcat / john** — JWT secret cracking (API2)

## Repo Structure

```
├── DVAPI_Walkthrough.md         # Step-by-step walkthrough with screenshots
├── DVAPI.postman_collection.json # Postman collection for reproduction
└── images/                      # All screenshots named by API and sequence
    ├── api1-01-...png
    ├── api2-01-...png
    └── ...
```

## Usage

1. Set up DVAPI locally — follow the [official setup guide](https://github.com/payatu/DVAPI)
2. Open `DVAPI_Walkthrough.md` and follow along
3. Import `DVAPI.postman_collection.json` into Postman for API4/API2 steps

---

> **Disclaimer:** This repo is for educational purposes only. All testing was performed against an intentionally vulnerable application in a local environment.
