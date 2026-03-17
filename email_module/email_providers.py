"""
Email provider implementations for Gmail
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from abc import ABC, abstractmethod

# Load environment variables for email credentials
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, will use existing env vars


class EmailProvider(ABC):
    """Abstract base class for email providers"""
    
    @abstractmethod
    def send_email(self, html_body, screenshot_paths=None, dry_run=False):
        """Send email with HTML body and optional attachments"""
        pass
    
    @abstractmethod
    def preview_email(self, html_body, screenshot_paths=None):
        """Preview email content"""
        pass


class OutlookProvider(EmailProvider):
    """Outlook email provider using Microsoft SMTP"""
    
    def __init__(self, config):
        self.config = config
        self.smtp_server = "smtp-mail.outlook.com"
        self.smtp_port = 587
    
    def generate_cid_for_image(self, image_path):
        """Generate a content ID for an image file"""
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        return f"{name_without_ext}@infrahealth.local"
    
    def embed_images_in_html(self, html_body, screenshot_paths):
        """Embed images as base64 in HTML for Outlook"""
        import base64
        
        if not screenshot_paths:
            return html_body
        
        modified_html = html_body
        
        for screenshot_path in screenshot_paths:
            if os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                cid = self.generate_cid_for_image(screenshot_path)
                # Replace cid: references with base64 data URLs
                modified_html = modified_html.replace(f'cid:{cid}', f'data:image/png;base64,{image_data}')
        
        return modified_html
    
    def send_email(self, html_body, screenshot_paths=None, dry_run=False):
        """Send email via Outlook SMTP"""
        try:
            # Check if credentials are available
            if not self.config.get('app_password'):
                raise ValueError("Outlook app password not configured. Set OUTLOOK_APP_PASSWORD environment variable.")
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.config['subject_template']
            msg['From'] = self.config['sender_email']
            msg['To'] = ", ".join(self.config['to_emails'])
            
            if self.config.get('cc_emails'):
                msg['Cc'] = ", ".join(self.config['cc_emails'])
            
            # For Outlook, embed images as base64 in HTML
            html_content = self.embed_images_in_html(html_body, screenshot_paths)
            msg.attach(MIMEText(html_content, 'html'))
            
            if dry_run:
                # Save as .eml file for preview
                preview_file = "draft_outlook_email.eml"
                with open(preview_file, "w") as f:
                    f.write(msg.as_string())
                print(f"Dry run: Outlook email saved as draft: {preview_file}")
                return True
            else:
                # Send via SMTP
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.config['sender_email'], self.config['app_password'])
                
                all_recipients = self.config['to_emails'] + self.config.get('cc_emails', [])
                server.send_message(msg, to_addrs=all_recipients)
                server.quit()
                
                print("Email sent successfully via Outlook!")
                return True
                
        except Exception as e:
            print(f"Failed to send email via Outlook: {e}")
            return False
    
    def preview_email(self, html_body, screenshot_paths=None):
        """Preview email HTML content"""
        # Embed images for preview
        html_content = self.embed_images_in_html(html_body, screenshot_paths)
        
        preview_file = "outlook_email_preview.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Outlook email preview saved to: {preview_file}")
        print(f"Subject: {self.config['subject_template']}")
        print(f"From: {self.config['sender_email']}")
        print(f"To: {', '.join(self.config['to_emails'])}")
        if self.config.get('cc_emails'):
            print(f"CC: {', '.join(self.config['cc_emails'])}")
        
        return preview_file


class GmailProvider(EmailProvider):
    """Gmail email provider using SMTP"""
    
    def __init__(self, config):
        self.config = config
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def generate_cid_for_image(self, image_path):
        """Generate a content ID for an image file"""
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        return f"{name_without_ext}@infrahealth.local"
    
    def embed_images_in_html(self, html_body, screenshot_paths):
        """Embed images as base64 in HTML for Gmail"""
        import base64
        
        if not screenshot_paths:
            return html_body
        
        modified_html = html_body
        
        for screenshot_path in screenshot_paths:
            if os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                cid = self.generate_cid_for_image(screenshot_path)
                # Replace cid: references with base64 data URLs
                modified_html = modified_html.replace(f'cid:{cid}', f'data:image/png;base64,{image_data}')
        
        return modified_html
    
    def send_email(self, html_body, screenshot_paths=None, dry_run=False, all_data=None):
        """Send email via Gmail SMTP"""
        try:
            # Check if credentials are available
            if not self.config.get('app_password'):
                raise ValueError("Gmail app password not configured. Set GMAIL_APP_PASSWORD environment variable.")
            
            # Create message
            msg = MIMEMultipart('mixed')  # Use 'mixed' for attachments
            msg['Subject'] = self.config['subject_template']
            msg['From'] = self.config['sender_email']
            msg['To'] = ", ".join(self.config['to_emails'])
            
            if self.config['cc_emails']:
                msg['Cc'] = ", ".join(self.config['cc_emails'])
            
            # HTML version with colored table
            html_content = html_body
            msg.attach(MIMEText(html_content, 'html'))
            
            # Attach screenshots as separate attachments
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
            
            if dry_run:
                # Save as .eml file for preview
                preview_file = "draft_email.eml"
                with open(preview_file, "w") as f:
                    f.write(msg.as_string())
                print(f"Dry run: Email saved as draft: {preview_file}")
                return True
            else:
                # Send via SMTP
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.config['sender_email'], self.config['app_password'])
                
                all_recipients = self.config['to_emails'] + self.config.get('cc_emails', [])
                server.send_message(msg, to_addrs=all_recipients)
                server.quit()
                
                print("Email sent successfully via Gmail!")
                return True
                
        except Exception as e:
            print(f"Failed to send email via Gmail: {e}")
            return False
    
    def preview_email(self, html_body, screenshot_paths=None):
        """Preview email HTML content"""
        # Embed images for preview
        html_content = self.embed_images_in_html(html_body, screenshot_paths)
        
        preview_file = "email_preview.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"Email preview saved to: {preview_file}")
        print(f"Subject: {self.config['subject_template']}")
        print(f"From: {self.config['sender_email']}")
        print(f"To: {', '.join(self.config['to_emails'])}")
        if self.config['cc_emails']:
            print(f"CC: {', '.join(self.config['cc_emails'])}")
        
        return preview_file


def get_email_provider(provider_name, config):
    """Factory function to get email provider instance"""
    providers = {
        "outlook": OutlookProvider,
        "gmail": GmailProvider
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unsupported email provider: {provider_name}")
    
    return providers[provider_name](config)
