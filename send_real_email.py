#!/usr/bin/env python3
"""
Send a real test email via Gmail
"""

import os
import sys
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def send_real_test_email():
    """Send an actual test email"""
    print("🚀 Sending Real Test Email via Gmail\n")
    
    try:
        from config.user_config import user_config
        gmail_config = user_config.EMAIL_CONFIG['gmail']
        
        # Check configuration
        if not gmail_config['app_password']:
            print("❌ Gmail app password not configured. Please set GMAIL_APP_PASSWORD in .env file.")
            return False
        
        print(f"✅ Configuration loaded:")
        print(f"   From: {gmail_config['sender_email']}")
        print(f"   To: {gmail_config['to_emails']}")
        
        # Create email message
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Infrastructure Health Agent Test - {os.path.basename(__file__)}"
        msg['From'] = gmail_config['sender_email']
        msg['To'] = ", ".join(gmail_config['to_emails'])
        
        if gmail_config.get('cc_emails') and gmail_config['cc_emails'][0]:
            msg['Cc'] = ", ".join(gmail_config['cc_emails'])
        
        # HTML content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h2 style="color: #2c3e50;">🚀 Infrastructure Health Agent Test Email</h2>
            
            <div style="background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>✅ Test Results</h3>
                <p><strong>Status:</strong> Gmail SMTP Configuration Working!</p>
                <p><strong>Sent from:</strong> {gmail_config['sender_email']}</p>
                <p><strong>Timestamp:</strong> {os.popen('date').read().strip()}</p>
            </div>
            
            <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>🎉 Success!</h3>
                <p>Your Gmail configuration is working correctly. The Infrastructure Health Agent can now send emails.</p>
            </div>
            
            <hr style="margin: 20px 0;">
            <p style="color: #6c757d; font-size: 12px;">
                This email was sent automatically by Infrastructure Health Agent test script.
            </p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect and send
        print("\n🔌 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("🔐 Authenticating...")
        server.login(gmail_config['sender_email'], gmail_config['app_password'])
        
        print("📧 Sending email...")
        all_recipients = gmail_config['to_emails'] + gmail_config.get('cc_emails', [])
        server.send_message(msg, to_addrs=all_recipients)
        server.quit()
        
        print("✅ Email sent successfully!")
        print(f"📬 Check your inbox at: {gmail_config['to_emails'][0]}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    success = send_real_test_email()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("Your Gmail setup is working and ready for Infrastructure Health Agent.")
    else:
        print("\n⚠️ Test failed. Please check the error above and fix your configuration.")
