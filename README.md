# Infrastructure Health Agent

An intelligent infrastructure monitoring system with AI-powered analysis, anomaly detection, and automated reporting. Fetches data from REST APIs, analyzes trends, and sends HTML email reports.

## Features

- **API Data Fetching**: REST API integration with configurable credentials
- **AI-Powered Analysis**: Anomaly detection, trend analysis, and predictive insights
- **Dashboard Screenshots**: Captures screenshots with Playwright
- **HTML Email Reports**: Color-coded reports with inline screenshots
- **Email Providers**: Gmail & Outlook SMTP support (configurable)
- **Smart Scheduling**: Cron-based scheduling via configuration (no code edits)
- **CI/CD Ready**: GitHub Actions workflow for automated daily reports

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### Configuration

Edit `config/user_config.py` to customize:
- `EMAIL_PROVIDER`: "gmail" or "outlook"
- `API_ENDPOINT`: Your API base URL
- `DASHBOARD_TAB_URLS`: Dashboard URLs to capture
- `EMAIL_CRON_SCHEDULE`: Scheduling options (day_of_week, send_time, timezone)
- `DIRECTOR_CONFIG`: Email recipients and sender details

### Usage

```bash
# Run once and send email
python main.py

# Run with scheduler (uses EMAIL_CRON_SCHEDULE config)
python main.py --schedule

# Dry run (preview email, no send)
python main.py --dry-run
```

## AI Agent System

The system includes intelligent analysis and decision-making:

- **Analysis Module** (`ai_agent/analysis/`): Anomaly detection, trend analysis, severity scoring
- **Decision Module** (`ai_agent/decision/`): Alert evaluation, action recommendations, escalation logic
- **Learning Module** (`ai_agent/learning/`): Pattern matching, issue prediction, historical analysis

All three modules are automatically invoked during report generation to provide intelligent insights and anomaly detection.

## Configuration

Two-tier configuration system in `config/` package:

### System Constants (`config/constants.py`)
System defaults - do not modify.

### User Settings (`config/user_config.py`)
Customize these settings:

```python
# Email
EMAIL_PROVIDER = "gmail"  # or "outlook"
DIRECTOR_CONFIG = {
    "name": "John Doe",
    "email": "john@example.com",
    "cc_emails": ["manager@example.com"]
}

# API
API_ENDPOINT = "https://api.example.com"

# Dashboards
DASHBOARD_TAB_URLS = {
    "GCP": "http://localhost:5173/gcp-dashboard",
    "AWS": "http://localhost:5173/aws-dashboard"
}

# Scheduling (no code changes needed)
EMAIL_CRON_SCHEDULE = {
    "enabled": True,
    "day_of_week": "fri",      # mon, tue, wed, thu, fri, sat, sun
    "send_time": "09:00",      # 24-hour format
    "timezone": None           # None = UTC
}
```

Set email credentials via environment variables:
- Gmail: `GMAIL_APP_PASSWORD`
- Outlook: `OUTLOOK_APP_PASSWORD`

## Project Structure

```
infra-health-agent/
├── main.py                  # CLI entry point
├── requirements.txt         # Dependencies
├── config/                  # Configuration package
│   ├── constants.py        # System constants (read-only)
│   ├── user_config.py      # User settings (edit this)
│   └── config.py           # Configuration loader
├── data/                    # Data handling
│   ├── fetcher.py          # API data fetching
│   └── screenshotter.py    # Playwright screenshots
├── email_module/           # Email handling
│   ├── email_composer.py   # HTML generation
│   ├── email_providers.py  # Gmail/Outlook SMTP
│   └── mailer.py           # Email interface
├── ai_agent/               # AI Intelligence
│   ├── core_agent.py       # Main AI Agent
│   ├── custom_actions.py   # Email scheduling & cron
│   ├── analysis/           # Data analysis
│   │   ├── analyzer.py
│   │   ├── anomaly_detector.py
│   │   └── trend_analyzer.py
│   ├── decision/           # Decision making
│   │   ├── decision_engine.py
│   │   ├── alert_evaluator.py
│   │   └── action_recommender.py
│   └── learning/           # Pattern learning
│       ├── learning.py
│       ├── pattern_matcher.py
│       └── predictor.py
└── utils/                   # Utilities

## Authentication

### Email Providers

**Gmail**: Requires App Password
- Enable 2-factor authentication on Google Account
- Generate App Password from account settings
- Set `GMAIL_APP_PASSWORD` environment variable

**Outlook**: Requires App Password
- Set `OUTLOOK_APP_PASSWORD` environment variable

### API Authentication

Configure in `user_config.py`:
- `API_ENDPOINT`: Base URL for your API
- Credentials via environment variables or config

## GitHub Actions

Automated daily reports via GitHub Actions:

1. Add GitHub secret: `GMAIL_APP_PASSWORD` (Settings → Secrets → Actions)
2. Workflow runs daily at 9 AM UTC (configurable in workflow file)
3. Supports manual trigger via workflow dispatch

See `.github/workflows/infrastructure-health-report.yml` for setup details.

## Scheduling

When using `--schedule` flag:
- Runs every Friday at `SEND_TIME` from config
- Uses APScheduler CronTrigger
- Only imports APScheduler when needed
- Press Ctrl+C to stop scheduler

## Troubleshooting

1. **Authentication Issues**: Use `--login` flag to establish session manually
2. **Screenshot Failures**: Check `DASHBOARD_TAB_URLS` and network connectivity
3. **Email Issues**: Ensure Outlook is installed and configured
4. **Permission Errors**: Verify write access to screenshot directory

## Adapting to Your Use Case

1. **Open `config/user_config.py`** - This is the only file you need to modify
2. **Email Provider**: Set `EMAIL_PROVIDER` to "outlook" or "gmail"
3. **Director Configuration**: Update `DIRECTOR_CONFIG` with name, email, and CC emails
4. **API Settings**: Modify `API_ENDPOINT` and authentication credentials
5. **Dashboard URLs**: Customize `DASHBOARD_TAB_URLS` for your dashboards
6. **Email Configuration**: 
   - For Gmail: Configure sender email and app password in `EMAIL_CONFIG['gmail']`
   - For Outlook: Update recipient lists in `EMAIL_CONFIG['outlook']`
7. **Custom Environments**: Add custom environments in `CUSTOM_ENVIRONMENTS` if needed
8. **Scheduling**: Adjust `SEND_TIME` for your preferred schedule

**Note**: Do not modify `config/constants.py` - it contains system defaults.

## Package Structure Benefits

- **Modular Design**: Each package has a specific responsibility
- **Easy Maintenance**: Related functionality grouped together
- **Scalable**: Easy to add new modules to appropriate packages
- **Clean Imports**: Explicit imports make dependencies clear
- **Testable**: Individual packages can be tested in isolation

## Dependencies

- `requests` - HTTP client library
- `requests-negotiate-sspi` - Windows authentication
- `requests-ntlm` - NTLM authentication fallback
- `playwright` - Browser automation for screenshots
- `pywin32` - Windows COM interface for Outlook
- `apscheduler` - Task scheduling (optional)
- `numpy` - Numerical computing for AI analysis
- `scipy` - Scientific computing for pattern recognition

### AI Agent Requirements
The AI Agent requires additional dependencies for intelligent analysis:
```bash
pip install numpy scipy
```
