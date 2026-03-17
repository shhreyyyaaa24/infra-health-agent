#!/usr/bin/env python3
"""
Send plain text only email
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def send_plain_text_email():
    """Send plain text only email"""
    print("📧 Sending Plain Text Email\n")
    
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        from data.fetcher import fetch_all_environment_data
        from email_module.email_composer import build_text_email
        from config.user_config import user_config
        
        gmail_config = user_config.EMAIL_CONFIG['gmail']
        
        print("📊 Fetching infrastructure data...")
        all_data = fetch_all_environment_data()
        
        if not all_data:
            print("❌ No data fetched")
            return False
        
        print(f"✅ Data fetched: {len(all_data)} environments")
        
        # Get screenshot paths
        screenshot_paths = [
            "screenshots/gcp_shreya_component_1.png",
            "screenshots/aws_shreya_component_1.png", 
            "screenshots/azure_shreya_component_1.png"
        ]
        
        print("📧 Building plain text email...")
        text_content = build_text_email(all_data)
        
        print(f"📏 Text content length: {len(text_content)} characters")
        
        # Create message with plain text only
        msg = MIMEMultipart('mixed')  # Use 'mixed' for attachments
        msg['Subject'] = gmail_config['subject_template']
        msg['From'] = gmail_config['sender_email']
        msg['To'] = ", ".join(gmail_config['to_emails'])
        
        # Attach plain text content only (no HTML)
        msg.attach(MIMEText(text_content, 'plain'))
        
        # Attach screenshots
        if screenshot_paths:
            for screenshot_path in screenshot_paths:
                if os.path.exists(screenshot_path):
                    with open(screenshot_path, "rb") as image_file:
                        img_data = image_file.read()
                    
                    img = MIMEImage(img_data)
                    filename = os.path.basename(screenshot_path)
                    img.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    msg.attach(img)
                    
                    print(f"Attached screenshot: {filename}")
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_config['sender_email'], gmail_config['app_password'])
        
        all_recipients = gmail_config['to_emails'] + gmail_config.get('cc_emails', [])
        server.send_message(msg, to_addrs=all_recipients)
        server.quit()
        
        print("✅ Plain text email sent successfully!")
        print("📬 Check your email - it should display as plain text")
        
        return True
        
    except Exception as e:
        print(f"❌ Plain text email failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    send_plain_text_email()
