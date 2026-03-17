#!/usr/bin/env python3
"""
Send a test email with minimal content to debug the issue
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def send_simple_test_email():
    """Send a simple test email to isolate the issue"""
    print("🧪 Sending Simple Test Email\n")
    
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from config.user_config import user_config
        
        gmail_config = user_config.EMAIL_CONFIG['gmail']
        
        # Create simple message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Simple Test Email - Debug"
        msg['From'] = gmail_config['sender_email']
        msg['To'] = ", ".join(gmail_config['to_emails'])
        
        # Simple text content
        text_content = """Hi Shreya Tiwari,

This is a simple test email to debug the issue.

Status: Testing
Summary: This email should be complete.

This is the end of the test email.

Thanks,
Infrastructure Health Agent
        """
        
        # Simple HTML content
        html_content = """<!DOCTYPE html>
<html>
<body>
    <p>Hi Shreya Tiwari,</p>
    <p>This is a simple test email to debug the issue.</p>
    <p><strong>Status:</strong> Testing</p>
    <p><strong>Summary:</strong> This email should be complete.</p>
    <p>This is the end of the test email.</p>
    <p>Thanks,<br>Infrastructure Health Agent</p>
</body>
</html>
        """
        
        # Attach both versions
        msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        print(f"📧 Text content length: {len(text_content)} characters")
        print(f"📧 HTML content length: {len(html_content)} characters")
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_config['sender_email'], gmail_config['app_password'])
        
        all_recipients = gmail_config['to_emails'] + gmail_config.get('cc_emails', [])
        server.send_message(msg, to_addrs=all_recipients)
        server.quit()
        
        print("✅ Simple test email sent successfully!")
        print("📬 Check if you receive the complete simple email")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        return False

if __name__ == "__main__":
    send_simple_test_email()
