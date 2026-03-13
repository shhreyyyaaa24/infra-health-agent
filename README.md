# Infrastructure Health Agent

An automated infrastructure monitoring and reporting system that fetches data from REST APIs, captures dashboard screenshots, and sends HTML email reports with inline images via Outlook.

## Features

- **API Data Fetching**: Retrieves project data from REST APIs with Windows/NTLM authentication
- **Status Computation**: Calculates health status (HEALTHY/MEDIUM/SEVERE) based on CPU usage and budget projections
- **Dashboard Screenshots**: Captures screenshots of multiple dashboard URLs using Playwright
- **HTML Email Reports**: Generates color-coded HTML emails with inline image attachments
- **Outlook Integration**: Sends emails via win32com Outlook with CID image references
- **Scheduling**: Optional weekly scheduling using APScheduler
- **Authentication Support**: Windows Kerberos/NTLM and basic auth fallback

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright Chromium:
```bash
playwright install chromium
```

3. Configure settings in `config.py`:
   - Set your API endpoints and authentication details
   - Configure dashboard URLs and email recipients
   - Set the director name for filtering projects

## Usage

### Initial Setup (One-time)

Open browser for manual authentication and save session state:
```bash
python main.py --login
```

### Run Once

Execute immediately and send email:
```bash
python main.py
```

### Dry Run (Preview Only)

Build email and preview without sending:
```bash
python main.py --dry-run
```

### Scheduled Mode

Run every Friday at the configured time:
```bash
python main.py --schedule
```

## Configuration

Edit `config.py` to customize:

- **Email Provider**: `EMAIL_PROVIDER` - Choose "outlook" or "gmail"
- **Director Config**: `DIRECTOR_CONFIG` - Set director name, email, and CC emails
- **API Settings**: `API_ENDPOINT`, `USE_WINDOWS_AUTH`, authentication credentials
- **Environments**: `ENVIRONMENTS` dict with display names and API keys
- **Screenshots**: `DASHBOARD_TAB_URLS`, `SCREENSHOT_DIR`, selectors
- **Email Settings**: `EMAIL_CONFIG` dict with provider-specific settings
- **Scheduling**: `SEND_TIME` (24-hour format, e.g., "09:00")
- **Status Colors**: Customizable colors for HEALTHY/MEDIUM/SEVERE statuses

## Status Logic

- **HEALTHY**: `overbudgetProjection <= 0`
- **MEDIUM**: `overbudgetProjection > 0` AND `cpu <= cpusShutdownLimit`
- **SEVERE**: `overbudgetProjection > 0` AND `cpu > cpusShutdownLimit`

## File Structure

```
infra-health-agent/
├── main.py              # CLI entry point
├── config.py            # All configuration settings
├── fetcher.py           # API data fetching and processing
├── screenshotter.py     # Playwright screenshot capture
├── email_composer.py    # HTML email generation
├── mailer.py            # Generic email sending interface
├── email_providers.py   # Email provider implementations (Outlook/Gmail)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Authentication

### API Authentication

#### Primary (Windows)
Uses `requests-negotiate-sspi` with current Windows Kerberos ticket - no password needed.

#### Fallback (NTLM)
Uses `requests-ntlm` with configured credentials when Windows auth fails.

#### Basic Auth
Set `USE_WINDOWS_AUTH = False` and provide `BASIC_AUTH_USER` and `BASIC_AUTH_PASS`.

### Email Authentication

#### Outlook
Uses Windows COM interface - requires Outlook to be installed and configured.

#### Gmail
Requires App Password for Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an App Password from Google Account settings
3. Configure `EMAIL_CONFIG['gmail']['sender_email']` and `EMAIL_CONFIG['gmail']['app_password']`

## Email Features

- **Generic Provider System**: Choose between Outlook and Gmail via configuration
- **HTML Email**: Color-coded project status table
- **Inline Screenshots**: Dashboard images embedded in emails
- **Provider-specific Handling**: 
  - Outlook: Uses CID references with MAPI properties
  - Gmail: Uses base64 embedded images
- **Summary Statistics**: Environment grouping and status counts

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

1. **Email Provider**: Set `EMAIL_PROVIDER` to "outlook" or "gmail" in `config.py`
2. **Director Configuration**: Update `DIRECTOR_CONFIG` with name, email, and CC emails
3. **API Settings**: Modify `API_ENDPOINT` and JSON field names to match your data source
4. **Authentication**: 
   - For API: Set `USE_WINDOWS_AUTH = False` and add basic auth credentials if needed
   - For Gmail: Configure sender email and app password in `EMAIL_CONFIG['gmail']`
5. **Environments**: Adjust `ENVIRONMENTS` dict for your cloud providers
6. **Dashboard URLs**: Customize `DASHBOARD_TAB_URLS` for your dashboards

## Dependencies

- `requests` - HTTP client library
- `requests-negotiate-sspi` - Windows authentication
- `requests-ntlm` - NTLM authentication fallback
- `playwright` - Browser automation for screenshots
- `pywin32` - Windows COM interface for Outlook
- `apscheduler` - Task scheduling (optional)
