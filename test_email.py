#!/usr/bin/env python3
"""
Simple test script for Gmail email functionality
"""

import os
import sys
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gmail_config():
    """Test Gmail configuration loading"""
    print("🔧 Testing Gmail Configuration...")
    
    # Check environment variable
    password = os.getenv("GMAIL_APP_PASSWORD")
    print(f"✅ Environment variable loaded: {'Yes' if password else 'No'}")
    
    # Check config
    from config.user_config import user_config
    gmail_config = user_config.EMAIL_CONFIG['gmail']
    print(f"✅ Sender email: {gmail_config['sender_email']}")
    print(f"✅ Password in config: {'Set' if gmail_config['app_password'] else 'Not set'}")
    print(f"✅ To emails: {gmail_config['to_emails']}")
    
    return bool(password)

def test_gmail_connection():
    """Test Gmail SMTP connection"""
    print("\n🔌 Testing Gmail SMTP Connection...")
    
    try:
        from config.user_config import user_config
        gmail_config = user_config.EMAIL_CONFIG['gmail']
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_config['sender_email'], gmail_config['app_password'])
        server.quit()
        
        print("✅ Gmail SMTP connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Gmail connection failed: {e}")
        return False

def test_email_dry_run():
    """Test email sending with dry run"""
    print("\n📧 Testing Email Dry Run...")
    
    try:
        from config.user_config import user_config
        gmail_config = user_config.EMAIL_CONFIG['gmail']
        
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = gmail_config['subject_template']
        msg['From'] = gmail_config['sender_email']
        msg['To'] = ", ".join(gmail_config['to_emails'])
        
        html_content = '''
        <html>
        <body>
            <h1>Infrastructure Health Test Email</h1>
            <p>This is a test email from Infrastructure Health Agent.</p>
            <p>If you receive this, Gmail configuration is working!</p>
        </body>
        </html>
        '''
        
        msg.attach(MIMEText(html_content, 'html'))
        
        # Save as .eml file for preview
        preview_file = "draft_email.eml"
        with open(preview_file, "w") as f:
            f.write(msg.as_string())
        
        print("✅ Email dry run successful - check for draft_email.eml file")
        return True
            
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Gmail Email Tests\n")
    
    # Test configuration
    config_ok = test_gmail_config()
    
    if not config_ok:
        print("\n❌ Configuration test failed. Please check your .env file.")
        sys.exit(1)
    
    # Test connection
    connection_ok = test_gmail_connection()
    
    # Test email dry run
    email_ok = test_email_dry_run()
    
    print(f"\n📊 Test Results:")
    print(f"   Configuration: {'✅' if config_ok else '❌'}")
    print(f"   Connection: {'✅' if connection_ok else '❌'}")
    print(f"   Email Dry Run: {'✅' if email_ok else '❌'}")
    
    if config_ok and connection_ok and email_ok:
        print("\n🎉 All tests passed! Your Gmail setup is working.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
