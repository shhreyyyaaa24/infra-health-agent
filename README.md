# Infrastructure Health Agent

An AI-powered infrastructure monitoring system that automates health checks, anomaly detection, and intelligent reporting. This comprehensive monitoring solution fetches real-time data from REST APIs, captures dashboard screenshots, analyzes trends with machine learning, and sends actionable HTML email reports with intelligent insights.

## What It Does

- **🔍 Continuous Monitoring**: Automatically polls infrastructure APIs to collect health metrics, status data, and performance indicators across multiple environments
- **🤖 Intelligent Analysis**: Uses AI algorithms to detect anomalies, identify patterns, predict potential issues, and provide data-driven recommendations
- **📊 Visual Documentation**: Captures timestamped screenshots of cloud dashboards (AWS, GCP, Azure) to provide visual context alongside numerical data
- **📧 Automated Reporting**: Generates comprehensive HTML email reports with color-coded health status, inline screenshots, trend analysis, and actionable insights
- **⚡ Proactive Alerts**: Identifies critical infrastructure issues before they impact users, with severity-based prioritization and escalation recommendations
- **📈 Historical Tracking**: Maintains data history to analyze trends, compare performance over time, and improve prediction accuracy
- **🔄 Multi-Environment Support**: Monitors across different cloud providers and environments from a unified interface
- **⏰ Scheduled Automation**: Runs automatically on custom schedules without manual intervention, perfect for daily/weekly health reports

## Key Features

- **🤖 AI-Powered Analysis**: Intelligent anomaly detection, trend analysis, and predictive insights
- **📊 Multi-Source Monitoring**: REST API integration with configurable authentication
- **📸 Automated Screenshots**: Captures dashboard screenshots using Playwright
- **📧 Smart Email Reports**: Color-coded HTML reports with inline screenshots and AI recommendations
- **⏰ Flexible Scheduling**: Cron-based scheduling without code changes
- **🔄 CI/CD Ready**: GitHub Actions workflow for automated daily reports
- **🔧 Easy Configuration**: Single config file setup for all settings

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### 2. Configuration

Edit `config/user_config.py` - this is the **only file you need to modify**:

```python
# Email Provider
EMAIL_PROVIDER = "gmail"  # or "outlook"

# Director Info
DIRECTOR_CONFIG = {
    "name": "Your Name",
    "email": "your@email.com",
    "cc_emails": ["manager@email.com"]
}

# API Endpoint
API_ENDPOINT = "https://your-api-server.com/api/projects"

# Dashboard URLs
DASHBOARD_TAB_URLS = {
    "gcp": "http://localhost:5173/gcp-dashboard",
    "aws": "http://localhost:5173/aws-dashboard"
}

# Scheduling (optional)
EMAIL_CRON_SCHEDULE = {
    "enabled": True,
    "day_of_week": "fri",     # Day of week
    "send_time": "09:00",     # 24-hour format
    "timezone": None          # None = system default
}
```

### 3. Set Email Credentials

**Gmail**: Set `GMAIL_APP_PASSWORD` environment variable
**Outlook**: Set `OUTLOOK_APP_PASSWORD` environment variable

### 4. Run

```bash
# Run once and send email
python main.py

# Run with AI Agent for intelligent analysis
python main.py --ai-agent

# Run with scheduler
python main.py --schedule

# Preview email without sending
python main.py --dry-run
```

## AI Agent System

The system includes three intelligent modules that work together:

- **🔍 Analysis Module**: Anomaly detection, trend analysis, and severity scoring
- **🧠 Decision Module**: Alert evaluation, action recommendations, and escalation logic  
- **📈 Learning Module**: Pattern matching, issue prediction, and historical analysis

All modules are automatically invoked during report generation to provide intelligent insights and actionable recommendations.

## Project Architecture

```
infra-health-agent/
├── main.py                    # CLI entry point with multiple modes
├── config/                    # Configuration package
│   ├── user_config.py        # ⭐ Main configuration file (edit this)
│   ├── constants.py          # System defaults (read-only)
│   └── config.py             # Configuration loader
├── data/                     # Data handling
│   ├── fetcher.py           # API data fetching
│   └── screenshotter.py     # Playwright screenshots
├── email_module/            # Email handling
│   ├── email_composer.py    # HTML report generation
│   ├── email_providers.py   # Gmail/Outlook SMTP
│   └── mailer.py           # Email interface
├── ai_agent/               # AI Intelligence
│   ├── core_agent.py       # Main AI coordinator
│   ├── custom_actions.py   # Scheduling & automation
│   ├── analysis/           # Data analysis
│   ├── decision/           # Decision making
│   └── learning/           # Pattern learning
└── screenshots/            # Captured dashboard images
```

## CLI Options

```bash
python main.py [OPTIONS]

Options:
  --login          Open browser for manual authentication
  --dry-run        Preview email without sending
  --schedule       Run with cron scheduler
  --ai-agent       Run AI Agent for intelligent monitoring
```

## Authentication Setup

### Gmail Setup
1. Enable 2-factor authentication on your Google Account
2. Generate an App Password from Google Account settings
3. Set environment variable: `export GMAIL_APP_PASSWORD="your_app_password"`

### Outlook Setup
1. Set environment variable: `export OUTLOOK_APP_PASSWORD="your_app_password"`

### API Authentication
Configure in `user_config.py`:
- Basic Auth: Set `BASIC_AUTH_USER` and `BASIC_AUTH_PASS`
- Windows Auth: Set `USE_WINDOWS_AUTH = True`
- Custom: Modify authentication in `data/fetcher.py`

## GitHub Actions Integration

Automated reports via GitHub Actions:

1. **Add Secret**: `GMAIL_APP_PASSWORD` (Settings → Secrets → Actions)
2. **Workflow**: Runs daily at 9 AM UTC (configurable)
3. **Manual Trigger**: Supports manual workflow dispatch

See `.github/workflows/infrastructure-health-report.yml`

## Important Notes

- **Single Config File**: Only edit `config/user_config.py` - never modify `constants.py`
- **AI Dependencies**: AI Agent requires `numpy` and `scipy` (included in requirements.txt)
- **Screenshot Directory**: Automatically created at `screenshots/`
- **Scheduler**: Press Ctrl+C to stop the cron scheduler
- **Debug Mode**: Enable `DEBUG_MODE = True` in config for verbose logging

## Dependencies

Core dependencies:
- `requests` - HTTP client for API calls
- `playwright` - Browser automation for screenshots
- `apscheduler` - Cron-based task scheduling
- `anthropic` - AI integration
- `python-dotenv` - Environment variable management
- `numpy` & `scipy` - Numerical computing for AI analysis
