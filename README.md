# WebTestX — Automated Web Application Testing & Security Validation Framework

> A Python-based test automation framework for functional, API, regression, negative, boundary, and security-oriented testing of web applications.

## 📌 Overview

**WebTestX** is an automated web application testing framework designed to make repetitive software testing faster, more consistent, and easier to analyze.

The framework combines **API automation, functional testing, negative testing, boundary-value testing, regression testing, and security validation** into a reusable test architecture.

The project was built with a focus on real-world QA engineering practices such as:

* Reusable test components
* Structured test cases
* Positive and negative testing
* Automated assertions
* API validation
* Web UI automation
* Boundary and edge-case testing
* Regression testing
* Failure evidence collection
* Test reporting
* Logging
* Continuous integration

The project also incorporates a security-testing layer to validate how applications behave when they receive unexpected, malformed, or security-sensitive inputs.

> **Important:** Security tests are intended for applications that are owned by the tester or explicitly authorized for testing, including local applications, intentionally vulnerable applications, and dedicated security labs.

---

# 🎯 Project Objectives

The primary objectives of WebTestX are to:

1. Automate repetitive web application testing.
2. Reduce manual effort when executing large numbers of test cases.
3. Validate application behavior using automated assertions.
4. Detect unexpected application responses and failures.
5. Support both positive and negative test scenarios.
6. Validate REST API behavior.
7. Automate browser-based functional testing.
8. Provide reusable test components instead of duplicated test logic.
9. Generate structured and human-readable test reports.
10. Support regression testing after application changes.
11. Integrate automated tests into a CI/CD workflow.
12. Demonstrate practical QA automation and software testing concepts.

---

# 🏗️ Architecture

```text
                         WebTestX
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        API Testing     UI Testing    Security Testing
             │              │              │
         Requests       Playwright     Python Tests
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                       Pytest Engine
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
         Assertions      Logging      Test Data
              │             │             │
              └─────────────┼─────────────┘
                            │
                            ▼
                     Result Processing
                            │
                            ▼
                    HTML / JSON Reports
                            │
                            ▼
                     GitHub Actions
```

---

# ✨ Key Features

## 1. API Automation

WebTestX uses Python to automate REST API testing.

The framework can validate:

* HTTP status codes
* Response bodies
* JSON structures
* Required fields
* Expected values
* Invalid endpoints
* Invalid parameters
* Error responses
* Response consistency
* Response time

Example:

```python
response = client.get("/users/1")

assert response.status_code == 200

data = response.json()

assert "id" in data
assert "name" in data
```

---

# 2. Functional Testing

Functional tests verify whether an application behaves according to its expected requirements.

Example test scenarios include:

```text
Valid user input
Invalid user input
Required fields
Valid API endpoint
Invalid API endpoint
Valid authentication
Invalid authentication
Correct application workflow
```

The objective is to validate **expected application functionality**, rather than simply checking whether an endpoint responds.

---

# 3. Positive Testing

Positive tests verify that the application behaves correctly when valid input is provided.

Example:

```text
Input:
Valid user ID

Expected:
HTTP 200
Valid JSON response
Required fields present
```

Positive testing helps verify normal application workflows.

---

# 4. Negative Testing

Negative testing verifies how the application behaves when invalid or unexpected input is provided.

Examples:

```text
Empty input
Invalid ID
Negative values
Unexpected characters
Malformed parameters
Missing required parameters
Invalid authentication
Unsupported values
```

Example:

```python
def test_invalid_user():

    response = client.get("/users/999999")

    assert response.status_code == 404
```

Negative testing is particularly important because applications often behave differently under invalid conditions.

---

# 5. Boundary Value Testing

Boundary-value testing is used to identify issues around the limits of accepted input.

Example:

```text
Minimum valid value
Maximum valid value
Below minimum
Above maximum
Empty value
Very large value
```

For example, if a field accepts values from `1–100`:

```text
0       → Invalid
1       → Valid
2       → Valid
99      → Valid
100     → Valid
101     → Invalid
```

These cases can be automated using parameterized Pytest tests.

---

# 6. Parameterized Testing

Pytest parameterization allows multiple test scenarios to be executed using a single reusable test function.

Example:

```python
@pytest.mark.parametrize(
    "user_id, expected_status",
    [
        (1, 200),
        (2, 200),
        (5, 200),
        (999999, 404),
    ]
)
def test_get_user(user_id, expected_status):

    response = client.get(
        f"/users/{user_id}"
    )

    assert response.status_code == expected_status
```

This makes the test suite easier to maintain and expand.

---

# 7. UI Automation

Browser-based functional testing is implemented using **Playwright**.

The UI automation layer is designed to test workflows such as:

```text
Open application
        ↓
Login
        ↓
Navigate
        ↓
Search
        ↓
Interact with application
        ↓
Validate expected result
```

Typical UI test scenarios include:

* Login
* Logout
* Form validation
* Search
* Navigation
* Product interactions
* Cart operations
* Session handling
* Invalid input handling

---

# 8. Page Object Model

The UI automation layer follows the **Page Object Model (POM)** design pattern.

Instead of putting browser interaction directly inside every test, page-specific operations are encapsulated into reusable classes.

Example:

```text
tests/
    test_login.py

pages/
    login_page.py
```

A test can then use:

```python
login_page.login(
    username,
    password
)
```

instead of repeatedly implementing selectors and browser interactions.

### Benefits

* Reduced code duplication
* Better maintainability
* Easier selector updates
* Cleaner test cases
* Better separation of test logic and UI interaction

---

# 9. API Client Abstraction

API communication is separated from individual tests through a reusable API client.

Example:

```python
class APIClient:

    def get(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def post(self, url, **kwargs):
        return requests.post(url, **kwargs)

    def put(self, url, **kwargs):
        return requests.put(url, **kwargs)

    def delete(self, url, **kwargs):
        return requests.delete(url, **kwargs)
```

This provides a central layer for HTTP communication and allows future features such as:

* Authentication handling
* Headers
* Timeouts
* Logging
* Retry handling
* Request tracking

to be implemented without modifying every test.

---

# 10. Security Validation

WebTestX includes security-oriented validation for authorized applications.

The objective is not to replace dedicated security scanners, but to automate repeatable checks that can be incorporated into a broader QA workflow.

Security-oriented tests may validate:

* Input handling
* Parameter validation
* Unexpected input behavior
* Security-related response patterns
* HTTP security headers
* Authentication behavior
* Error handling
* Input sanitization

Example categories:

```text
Input Validation
Parameter Handling
Authentication Validation
Security Headers
Error Handling
Security Regression Tests
```

Security tests are executed only against systems where testing is authorized.

---

# 11. Regression Testing

Regression tests verify that existing functionality continues to work after changes are introduced.

Example workflow:

```text
Application Change
        ↓
Run Regression Suite
        ↓
Execute Existing Test Cases
        ↓
Compare Actual vs Expected
        ↓
PASS / FAIL
```

This helps detect situations where a new change unintentionally breaks existing functionality.

Security-related fixes can also be converted into regression tests.

For example:

```text
Issue discovered
       ↓
Developer fixes issue
       ↓
Create automated regression test
       ↓
Run test repeatedly
       ↓
Ensure issue remains fixed
```

---

# 12. Automated Assertions

Tests use assertions to compare actual application behavior with expected behavior.

Examples:

```python
assert response.status_code == 200
```

```python
assert "id" in response.json()
```

```python
assert page.title == expected_title
```

Assertions allow the framework to automatically determine whether a test has passed or failed.

---

# 13. Failure Evidence

When a test fails, the framework can capture information useful for debugging.

Depending on the test type, failure evidence can include:

```text
Test case name
Request URL
HTTP method
Request parameters
Response status
Response body
Failure reason
Timestamp
Screenshot
```

This helps developers and QA engineers reproduce failures more efficiently.

---

# 📊 Test Reporting

Test results can be generated using Pytest reporting capabilities.

Example:

```bash
pytest --html=reports/test-report.html --self-contained-html
```

The generated report provides information such as:

```text
Total Tests
Passed Tests
Failed Tests
Skipped Tests
Execution Duration
Failure Details
```

Example:

```text
========================================
        WebTestX Test Report
========================================

Total Tests:       42
Passed:            37
Failed:             3
Skipped:            2

Pass Rate:        88.1%

Execution Time:   12.4 seconds
========================================
```

---

# 📁 Project Structure

```text
WebTestX/
│
├── tests/
│   │
│   ├── api/
│   │   ├── test_users.py
│   │   ├── test_negative.py
│   │   └── test_validation.py
│   │
│   ├── ui/
│   │   ├── test_login.py
│   │   ├── test_search.py
│   │   └── test_cart.py
│   │
│   ├── security/
│   │   ├── test_input_validation.py
│   │   ├── test_security_headers.py
│   │   └── test_parameter_handling.py
│   │
│   └── regression/
│       └── test_regression_suite.py
│
├── pages/
│   ├── login_page.py
│   ├── home_page.py
│   └── cart_page.py
│
├── utils/
│   ├── api_client.py
│   ├── config.py
│   └── logger.py
│
├── test_data/
│   └── test_data.json
│
├── reports/
│
├── screenshots/
│
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| Python         | Test automation and framework development |
| Pytest         | Test execution and test organization      |
| Requests       | REST API automation                       |
| Playwright     | Browser/UI automation                     |
| Pytest-HTML    | Test reporting                            |
| JSON           | Test data and API validation              |
| Git            | Version control                           |
| GitHub         | Source-code management                    |
| GitHub Actions | CI/CD automation                          |
| Linux          | Development/testing environment           |

---

# ⚙️ Installation

## Prerequisites

Make sure the following are installed:

* Python 3.10+
* Git
* pip

Verify Python:

```bash
python --version
```

Verify pip:

```bash
pip --version
```

---

# 📥 Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project directory:

```bash
cd Web-application_testing
```

---

# 🐍 Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright browsers (required for UI tests only)

```bash
playwright install chromium
```

> **Note:** The Playwright browser download is only needed if you plan to run UI tests (`tests/ui/`).
> All API, functional, security, and regression tests work without it.

---

# ▶️ Complete Running Guide

## Step 1 — Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Step 2 — Run the full test suite (API + Security + Regression + Functional)

```bash
pytest tests/api/ tests/functional/ tests/security/ tests/regression/
```

Expected output:

```text
============================ 107 passed in ~35s ============================
```

---

## Step 3 — Run individual test suites

### API Tests (positive, negative, schema validation)

```bash
pytest tests/api/ -v
```

### Functional Tests (CRUD workflows)

```bash
pytest tests/functional/ -v
```

### Security Validation Tests

```bash
pytest tests/security/ -v
```

### Regression Tests

```bash
pytest tests/regression/ -v
```

### UI Tests — Playwright (requires browser install first)

```bash
playwright install chromium
pytest tests/ui/ -v
```

---

## Step 4 — Run tests by pytest marker

Markers let you filter tests across all directories without specifying paths.

```bash
# API endpoint tests
pytest -m api

# Browser-based UI tests
pytest -m ui

# Security validation tests
pytest -m security

# Regression tests
pytest -m regression

# Functional tests
pytest -m functional

# Negative (invalid-input) tests only
pytest -m negative

# Boundary-value tests only
pytest -m boundary

# Smoke tests (quick sanity checks)
pytest -m smoke

# Combine markers — e.g. API and regression only
pytest -m "api or regression"
```

---

## Step 5 — Generate an HTML test report

```bash
pytest tests/api/ tests/functional/ tests/security/ tests/regression/ \
    --html=reports/test-report.html \
    --self-contained-html
```

The report is saved to:

```text
reports/test-report.html
```

Open it in any browser to see a full breakdown of passed, failed, and skipped tests with timing information.

---

## Step 6 — Generate separate reports per suite

```bash
# API report
pytest tests/api/ --html=reports/api-report.html --self-contained-html

# Security report
pytest tests/security/ --html=reports/security-report.html --self-contained-html

# Regression report
pytest tests/regression/ --html=reports/regression-report.html --self-contained-html

# UI report
pytest tests/ui/ --html=reports/ui-report.html --self-contained-html
```

---

## Step 7 — Run with verbose output and short tracebacks

```bash
pytest tests/api/ -v --tb=short
```

## Step 8 — Run a single specific test file

```bash
pytest tests/api/test_users.py -v
```

## Step 9 — Run a single specific test function

```bash
pytest tests/api/test_users.py::test_get_single_user -v
```

## Step 10 — Run tests in parallel (faster execution)

Install `pytest-xdist` for parallel execution:

```bash
pip install pytest-xdist
pytest tests/ -n auto
```

---

# 🔍 Example Test Execution Output

```text
============================= test session starts =============================
platform win32 -- Python 3.11.x, pytest-8.x.x
collected 107 items

tests/api/test_negative.py ............                              [ 11%]
tests/api/test_users.py ..........                                   [ 20%]
tests/api/test_validation.py ..............                          [ 33%]
tests/functional/test_functional.py ..........                       [ 42%]
tests/security/test_input_validation.py ..............               [ 55%]
tests/security/test_parameter_handling.py ..............             [ 68%]
tests/security/test_security_headers.py ...........                  [ 79%]
tests/regression/test_regression_suite.py ....................       [100%]

- Generated html report: reports/test-report.html -
============================ 107 passed in 34.18s =============================
```

---

# 🗂️ Test ID Reference

| Test ID Range | Suite | Description |
|---|---|---|
| API-001 to API-008 | `tests/api/test_users.py` | Positive user endpoint tests |
| NEG-001 to NEG-010 | `tests/api/test_negative.py` | Negative/invalid input tests |
| VAL-001 to VAL-010 | `tests/api/test_validation.py` | Schema and field validation |
| FUNC-001 to FUNC-010 | `tests/functional/test_functional.py` | CRUD workflow tests |
| SEC-IV-001 to SEC-IV-010 | `tests/security/test_input_validation.py` | XSS, SQLi, oversized input |
| SEC-HD-001 to SEC-HD-007 | `tests/security/test_security_headers.py` | HTTP security headers |
| SEC-PH-001 to SEC-PH-008 | `tests/security/test_parameter_handling.py` | Parameter handling |
| REG-001 to REG-015 | `tests/regression/test_regression_suite.py` | Regression tests |
| UI-LGN-001 to UI-LGN-008 | `tests/ui/test_login.py` | Login / authentication UI |
| UI-SRC-001 to UI-SRC-010 | `tests/ui/test_search.py` | Browse / search UI |
| UI-CRT-001 to UI-CRT-008 | `tests/ui/test_cart.py` | Product / basket UI |

---

# 🌐 Test Targets

| Target | Used By |
|---|---|
| `https://jsonplaceholder.typicode.com` | All API, functional, security, regression tests |
| `https://books.toscrape.com` | UI search and cart tests |
| `https://the-internet.herokuapp.com/login` | UI login tests |

All targets are publicly available, intentionally testable demo services.

---

# 🔄 CI/CD Integration

WebTestX can be integrated into a GitHub Actions pipeline so that automated tests execute whenever changes are pushed to the repository.

Example workflow:

```text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Setup Python
    │
    ├── Install dependencies
    │
    ├── Install Playwright
    │
    ├── Execute Pytest
    │
    ├── Generate reports
    │
    └── Return build status
```

This allows automated testing to become part of the development workflow instead of being performed only manually.

---

# 🧪 Testing Strategy

The project follows a layered testing strategy.

## Level 1 — Functional Testing

Validate that application features behave according to expected requirements.

## Level 2 — Negative Testing

Validate application behavior with invalid and unexpected inputs.

## Level 3 — Boundary Testing

Validate application behavior around input limits.

## Level 4 — API Testing

Validate REST API endpoints, responses, status codes, and data.

## Level 5 — UI Testing

Validate critical browser-based user workflows.

## Level 6 — Security Validation

Validate security-sensitive application behavior in authorized environments.

## Level 7 — Regression Testing

Re-run existing tests after application changes to detect regressions.

---

# 📋 Example Test Case

### Test Case: Valid User Retrieval

```text
Test ID: API-001

Title:
Retrieve an existing user

Category:
Functional / API

Precondition:
API endpoint is available

Steps:
1. Send GET request to the user endpoint.
2. Provide a valid user ID.
3. Receive the server response.
4. Validate the response.

Expected Result:
HTTP status should be 200.
Response should contain valid JSON.
Required user fields should be present.

Actual Result:
Validated automatically by the test framework.

Status:
PASS / FAIL
```

---

# 📋 Example Negative Test Case

```text
Test ID: API-002

Title:
Request a non-existent user

Category:
Negative Testing

Steps:
1. Send GET request.
2. Provide an invalid/non-existent user ID.
3. Analyze response.

Expected Result:
Application should return the appropriate
error response.

Status:
PASS / FAIL
```

---

# 🐞 Bug Reporting Approach

When an automated test identifies unexpected behavior, the issue can be documented using a structured bug report.

Example:

```text
Bug ID: BUG-001

Title:
Invalid input is accepted by the application

Severity:
Medium

Priority:
High

Environment:
Test Environment

Steps to Reproduce:
1. Open the application.
2. Navigate to the target feature.
3. Enter invalid input.
4. Submit the request.

Expected Result:
Application should reject the invalid input
and display an appropriate validation message.

Actual Result:
Application accepts the input and continues
processing the request.

Evidence:
Test report / response / screenshot

Status:
Open
```

---

# 🎯 QA Concepts Demonstrated

This project demonstrates practical implementation of:

* Test Case Design
* Test Scenarios
* Functional Testing
* Non-functional considerations
* Positive Testing
* Negative Testing
* Boundary Value Analysis
* Equivalence Partitioning
* Regression Testing
* API Testing
* UI Testing
* Automated Testing
* Assertions
* Parameterized Testing
* Defect Identification
* Defect Documentation
* Test Reporting
* Test Data Management
* Logging
* CI/CD
* SDLC concepts
* STLC concepts

---

# 🔐 Security Considerations

WebTestX contains security-oriented test capabilities because robust software testing should also consider how applications behave with unexpected or malicious input.

However, the framework should only be used against:

* Applications you own
* Applications where you have explicit authorization
* Local development environments
* Intentionally vulnerable applications
* Dedicated security training labs

Do not use the framework to test third-party systems without authorization.

---

# 📈 Future Improvements

Planned improvements include:

* [ ] Expand UI automation coverage
* [ ] Add more API test suites
* [ ] Add authentication/token management
* [ ] Add schema validation
* [ ] Add configurable test environments
* [ ] Add centralized logging
* [ ] Improve failure screenshots
* [ ] Add retry mechanisms for transient failures
* [ ] Add parallel test execution
* [ ] Add richer HTML reports
* [ ] Add test-data generation
* [ ] Add Docker support
* [ ] Expand GitHub Actions pipeline
* [ ] Add automated regression suites
* [ ] Add performance-oriented checks
* [ ] Improve configuration management

---

# 📚 Learning Outcomes

This project provided practical experience in designing and implementing an automated testing framework rather than writing isolated automation scripts.

Key areas of learning include:

### Software Testing

Understanding how different testing methodologies can be converted into repeatable automated test cases.

### Automation

Learning how to reduce repetitive manual testing through reusable Python-based automation.

### API Testing

Understanding HTTP requests, responses, status codes, JSON data, and API validation.

### UI Automation

Understanding browser automation, selectors, assertions, and page-level abstractions.

### Test Architecture

Learning how to structure a maintainable automation framework using reusable components.

### Debugging

Learning how to analyze failed tests and collect evidence required to reproduce issues.

### Security Testing

Applying a security-oriented mindset to application input validation and unexpected behavior.

### CI/CD

Understanding how automated tests can become part of the software development lifecycle.

---

# 🚀 Project Goals

The long-term goal of WebTestX is to evolve into a reusable automation framework capable of supporting:

```text
Functional Testing
       +
API Testing
       +
UI Automation
       +
Negative Testing
       +
Regression Testing
       +
Security Validation
       +
Automated Reporting
       +
CI/CD
```

The project demonstrates how software testing can move from repetitive manual execution toward **reliable, repeatable, and maintainable automated validation**.

---

# 👨‍💻 Author

**Cahal Agarwalla**

Interested in:

* Software Quality Engineering
* Test Automation
* Web Application Testing
* Cybersecurity
* Python Automation
* Application Security

---

# ⭐ Project Status

**Status:** Actively developing

The framework is being continuously expanded with additional test cases, automation capabilities, reporting functionality, and CI/CD integration.

---

# 📜 License

This project is intended for educational, development, and authorized testing purposes.
