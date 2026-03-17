#!/usr/bin/env python3
"""
Send a test email with both HTML and text content
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def send_test_email_with_text():
    """Send email with both HTML and text fallback"""
    print("🧪 Testing Email with Text Fallback\n")
    
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from config.user_config import user_config
        
        gmail_config = user_config.EMAIL_CONFIG['gmail']
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Test Email - HTML + Text"
        msg['From'] = gmail_config['sender_email']
        msg['To'] = ", ".join(gmail_config['to_emails'])
        
        # Text version
        text_content = """
Hi Shreya Tiwari,

📊 Infrastructure Status Summary

Here's the current health status of your infrastructure:

Total Projects: 7
- 3 Healthy
- 4 Severe Risk  
- 0 Medium Risk

⚠️ Attention Required: You have 4 projects with severe risk that need immediate attention.

📋 Project Details:
[GCP Environment - 3 projects]
[AWS Environment - 2 projects]  
[Azure Environment - 2 projects]

This report was generated automatically by the Infrastructure Health Agent.
        """
        
        # HTML version
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Test Email</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .summary { background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; }
        .healthy { color: #28a745; font-weight: bold; }
        .severe { color: #dc3545; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Hi Shreya Tiwari,</h2>
    
    <div class="summary">
        <h3>📊 Infrastructure Status Summary</h3>
        <p><strong>Total Projects:</strong> 7 | <span class="healthy">3 Healthy</span> | <span class="severe">4 Severe Risk</span> | 0 Medium Risk</p>
        <p>⚠️ <strong>Attention Required:</strong> You have 4 projects with severe risk that need immediate attention.</p>
    </div>
    
    <h3>📋 Project Details</h3>
    <p>GCP Environment: 3 projects<br>
    AWS Environment: 2 projects<br>
    Azure Environment: 2 projects</p>
    
    <hr>
    <p><small>This report was generated automatically by the Infrastructure Health Agent.</small></p>
</body>
</html>
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_config['sender_email'], gmail_config['app_password'])
        
        all_recipients = gmail_config['to_emails'] + gmail_config.get('cc_emails', [])
        server.send_message(msg, to_addrs=all_recipients)
        server.quit()
        
        print("✅ Test email with text fallback sent successfully!")
        print("📬 Check your email - you should see content now.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    send_test_email_with_text()
