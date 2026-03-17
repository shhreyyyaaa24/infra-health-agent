#!/usr/bin/env python3
"""
Send HTML email with colored table format
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def send_html_table_email():
    """Send HTML email with professional colored table"""
    print("📧 Sending HTML Table Email\n")
    
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        from data.fetcher import fetch_all_environment_data
        from config.user_config import user_config
        
        gmail_config = user_config.EMAIL_CONFIG['gmail']
        
        print("📊 Fetching infrastructure data...")
        all_data = fetch_all_environment_data()
        
        if not all_data:
            print("❌ No data fetched")
            return False
        
        print(f"✅ Data fetched: {len(all_data)} environments")
        
        # Calculate statistics
        total_projects = sum(len(projects) for projects in all_data.values())
        healthy_projects = sum(len([p for p in projects if p['status'] == 'HEALTHY']) for projects in all_data.values())
        severe_projects = sum(len([p for p in projects if p['status'] == 'SEVERE']) for projects in all_data.values())
        medium_projects = total_projects - healthy_projects - severe_projects
        
        from config import DIRECTOR_CONFIG
        director_name = DIRECTOR_CONFIG.get('name', 'Team Lead')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build HTML with colored table
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Infrastructure Health Report</title>
</head>
<body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px;">
    
    <div style="font-size: 16px; color: #2c3e50; margin-bottom: 15px; font-weight: 500;">Hi {director_name},</div>
    
    <div style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 15px 0; border-radius: 4px;">
        <h3 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: 600;">📊 Infrastructure Status Summary</h3>
        <p style="margin: 0 0 10px 0;">Here's the current health status of your infrastructure as of {timestamp}:</p>
        <p style="margin: 0;">
            <strong>Total Projects: {total_projects}</strong> | 
            <span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{healthy_projects} Healthy</span> | 
            <span style="background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{severe_projects} Severe Risk</span> | 
            <span style="background-color: #ffc107; color: #212529; padding: 2px 8px; border-radius: 12px; font-size: 12px;">{medium_projects} Medium Risk</span>
        </p>
        <p style="margin: 10px 0 0 0;">✅ <strong>Good News:</strong> All projects are operating within acceptable limits.</p>
    </div>
    
    <h3 style="margin: 20px 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: 600;">📋 Project Details</h3>
    
    <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 13px;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="text-align: left; padding: 10px; border: 1px solid #ddd; font-weight: 600;">Environment</th>
                <th style="text-align: left; padding: 10px; border: 1px solid #ddd; font-weight: 600;">Project Name</th>
                <th style="text-align: left; padding: 10px; border: 1px solid #ddd; font-weight: 600;">CPU Usage</th>
                <th style="text-align: left; padding: 10px; border: 1px solid #ddd; font-weight: 600;">CPU Budget</th>
                <th style="text-align: left; padding: 10px; border: 1px solid #ddd; font-weight: 600;">Shutdown Limit</th>
                <th style="text-align: left; padding: 10px; border: 1px solid #ddd; font-weight: 600;">Overbudget Projection</th>
                <th style="text-align: left; padding: 10px; border: 1px solid #ddd; font-weight: 600;">Status</th>
            </tr>
        </thead>
        <tbody>
"""
        
        # Add table rows
        for env_name, projects in all_data.items():
            for project in projects:
                status = project['status']
                
                # Determine row color based on status
                if status == 'HEALTHY':
                    row_style = 'background-color: #d4edda;'
                    status_color = '#28a745'
                    status_text = 'Healthy'
                elif status == 'SEVERE':
                    row_style = 'background-color: #f8d7da;'
                    status_color = '#dc3545'
                    status_text = 'Severe Risk'
                else:
                    row_style = 'background-color: #fff3cd;'
                    status_color = '#ffc107'
                    status_text = 'Medium Risk'
                
                overbudget = f"${project['overbudgetProjection']}" if project['overbudgetProjection'] > 0 else "$0"
                
                html_content += f"""
            <tr style="{row_style}">
                <td style="padding: 10px; border: 1px solid #ddd;">{env_name}</td>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>{project['name']}</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">{project['cpu']}%</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{project['cpusBudget']}%</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{project['cpusShutdownLimit']}%</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{overbudget}</td>
                <td style="padding: 10px; border: 1px solid #ddd; color: {status_color}; font-weight: 600;">{status_text}</td>
            </tr>
"""
        
        html_content += """
        </tbody>
    </table>
    
    <div style="background-color: #e7f3ff; padding: 15px; border-radius: 4px; margin: 20px 0;">
        <h3 style="margin: 0 0 10px 0;">📸 Dashboard Screenshots</h3>
        <p style="margin: 0;"><strong>Screenshots attached:</strong> Dashboard screenshots have been attached to this email as separate files for better viewing.</p>
    </div>
    
    <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
    <p style="font-size: 12px; color: #666; margin: 0;"><small>This report was generated automatically by the Infrastructure Health Agent.</small></p>
</body>
</html>
"""
        
        print(f"📏 HTML content length: {len(html_content)} characters")
        
        # Get screenshot paths
        screenshot_paths = [
            "screenshots/gcp_shreya_component_1.png",
            "screenshots/aws_shreya_component_1.png", 
            "screenshots/azure_shreya_component_1.png"
        ]
        
        # Create message
        msg = MIMEMultipart('mixed')
        msg['Subject'] = gmail_config['subject_template']
        msg['From'] = gmail_config['sender_email']
        msg['To'] = ", ".join(gmail_config['to_emails'])
        
        # Attach HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Attach screenshots
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
        
        print("✅ HTML table email sent successfully!")
        print("📬 Check your email - it should display with the colored table format")
        
        return True
        
    except Exception as e:
        print(f"❌ HTML table email failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    from datetime import datetime
    send_html_table_email()
