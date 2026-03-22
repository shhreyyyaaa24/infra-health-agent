# GitHub Actions Setup for Infrastructure Health Agent

This repository uses GitHub Actions to automatically send infrastructure health reports via email. You can trigger reports manually or schedule them to run automatically.

## 🚀 Quick Start

### 1. Fork/Clone this Repository

Make sure the repository is pushed to GitHub.

### 2. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

#### Required Secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `GMAIL_APP_PASSWORD` | Gmail App Password (16-character code) | `abcd efgh ijkl mnop` |

#### Optional Secrets (will use defaults if not set):

| Secret Name | Description | Default Value |
|-------------|-------------|---------------|
| `GMAIL_SENDER_EMAIL` | Sender Gmail address | `shreyaa.developer@gmail.com` |
| `DIRECTOR_EMAIL` | Recipient email address | `shhreyyyaa1@gmail.com` |
| `DIRECTOR_NAME` | Director name for personalized emails | `Shreya Tiwari` |
| `API_ENDPOINT` | API endpoint for fetching project data | `http://localhost:8000/api/projects` |
| `DASHBOARD_BASE_URL` | Dashboard URL for screenshots | `http://localhost:5173/` |
| `EMAIL_PROVIDER` | Email provider to use | `gmail` |

### 3. How to Get Gmail App Password

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to Security → 2-Step Verification → App passwords
3. Select "Mail" and generate a 16-character app password
4. Copy this password and add it as `GMAIL_APP_PASSWORD` secret

## 📋 Workflows Available

### 1. Main Workflow - `infrastructure-health-report.yml`

**Triggers:**
- 🕘 **Scheduled**: Daily at 9:00 AM UTC
- 🖱️ **Manual**: Via "Run workflow" button in Actions tab
- 📝 **Push**: On every push to main branch

**Features:**
- Captures dashboard screenshots
- Sends HTML email with colored status table
- Uploads screenshots as artifacts
- Supports environment filter (all/gcp/aws/azure)

### 2. Reusable Workflow - `send-email-reusable.yml`

Can be called from other workflows in your organization.

### 3. Custom Action - `send-infrastructure-email`

Reusable custom action that can be used in any workflow.

## 🖱️ Manual Triggering

1. Go to **Actions** tab in your GitHub repository
2. Click **"Infrastructure Health Report"** workflow
3. Click **"Run workflow"** button
4. (Optional) Select environment filter
5. Click **"Run workflow"**

## ⏰ Schedule Configuration

The workflow runs automatically every day at 9:00 AM UTC. To change the schedule:

Edit `.github/workflows/infrastructure-health-report.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9:00 AM UTC
  # - cron: '0 9 * * 1'  # Weekly on Monday at 9:00 AM UTC
  # - cron: '0 */6 * * *'  # Every 6 hours
```

**Cron Format:** `minute hour day-of-month month day-of-week`

Common schedules:
- Daily at 9 AM: `0 9 * * *`
- Weekly on Monday: `0 9 * * 1`
- Every 6 hours: `0 */6 * * *`

## 🔧 Customization

### Change Default Settings

Edit `config/user_config.py` or set environment variables:

```python
# In user_config.py or via env vars
DIRECTOR_NAME = "Your Name"
DIRECTOR_EMAIL = "your.email@example.com"
DASHBOARD_BASE_URL = "https://your-dashboard.com"
```

### Use Different Email Provider

Set `EMAIL_PROVIDER` secret to:
- `gmail` (default)
- `outlook` (requires Outlook app password)

### Add Multiple Recipients

Set `DIRECTOR_CC_EMAILS` secret with comma-separated emails:
```
manager1@example.com,manager2@example.com
```

## 📁 Workflow Files

| File | Purpose |
|------|---------|
| `.github/workflows/infrastructure-health-report.yml` | Main workflow with all triggers |
| `.github/workflows/send-email-reusable.yml` | Reusable workflow for calling from other repos |
| `.github/actions/send-infrastructure-email/action.yml` | Custom GitHub Action |

## 🔒 Security Best Practices

1. **Never commit passwords** - Always use GitHub Secrets
2. **Use App Passwords** - Don't use your main Gmail password
3. **Limit permissions** - Only give necessary permissions to workflows
4. **Rotate secrets** - Change app passwords periodically

## 🐛 Troubleshooting

### Workflow Not Triggering

- Check if Actions are enabled in repository settings
- Verify the workflow file syntax
- Check if the schedule is set correctly

### Email Not Sending

- Verify `GMAIL_APP_PASSWORD` is set correctly
- Check if 2-Factor Authentication is enabled on Gmail
- Look at workflow logs in Actions tab
- Check spam folder in recipient email

### Screenshots Not Capturing

- Verify dashboard is accessible from GitHub Actions runners
- Check if `DASHBOARD_BASE_URL` is correct
- Review screenshot artifacts in workflow run

## 📊 Workflow Outputs

After each run, you can find:

1. **Email Status** in workflow logs
2. **Screenshots** as downloadable artifacts
3. **Error logs** if anything fails

## 🎯 Example Use Cases

### Daily Monitoring Report
Schedule runs every morning to check overnight infrastructure status.

### On-Demand Health Check
Manually trigger before deployments or during incidents.

### Multi-Environment Monitoring
Use environment filter to check specific environments separately.

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Cron Expression Generator](https://crontab.guru/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)

---

**Need Help?** Create an issue in this repository!
