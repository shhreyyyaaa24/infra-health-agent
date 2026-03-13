"""
Email provider implementations for Outlook and Gmail
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from abc import ABC, abstractmethod
import win32com.client


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
    """Outlook email provider using win32com"""
    
    def __init__(self, config):
        self.config = config
    
    def generate_cid_for_image(self, image_path):
        """Generate a content ID for an image file"""
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        return f"{name_without_ext}@infrahealth.local"
    
    def attach_image_with_cid(self, mail, image_path):
        """Attach an image with CID for HTML embedding"""
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return None
        
        cid = self.generate_cid_for_image(image_path)
        
        # Add attachment
        attachment = mail.Attachments.Add(Source=image_path)
        
        # Set PR_ATTACH_CONTENT_ID property for CID
        attachment.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F",  # PR_ATTACH_CONTENT_ID
            cid
        )
        
        return cid
    
    def send_email(self, html_body, screenshot_paths=None, dry_run=False):
        """Send email via Outlook with inline image attachments"""
        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)  # 0 = olMailItem
            
            # Set email properties
            mail.Subject = self.config['subject_template']
            mail.To = "; ".join(self.config['to_emails'])
            
            if self.config['cc_emails']:
                mail.CC = "; ".join(self.config['cc_emails'])
            
            # Attach images if provided
            if screenshot_paths:
                for screenshot_path in screenshot_paths:
                    self.attach_image_with_cid(mail, screenshot_path)
            
            # Set HTML body
            mail.HTMLBody = html_body
            
            if dry_run:
                # Save as draft for preview instead of sending
                draft_path = os.path.join(os.getcwd(), "draft_email.msg")
                mail.SaveAs(draft_path)
                print(f"Dry run: Email saved as draft: {draft_path}")
                return True
            else:
                # Send the email
                mail.Send()
                print("Email sent successfully via Outlook!")
                return True
                
        except Exception as e:
            print(f"Failed to send email via Outlook: {e}")
            return False
    
    def preview_email(self, html_body, screenshot_paths=None):
        """Preview email HTML content"""
        preview_file = "email_preview.html"
        with open(preview_file, "w", encoding="utf-8") as f:
            f.write(html_body)
        
        print(f"Email preview saved to: {preview_file}")
        print(f"Subject: {self.config['subject_template']}")
        print(f"To: {', '.join(self.config['to_emails'])}")
        if self.config['cc_emails']:
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
    
    def send_email(self, html_body, screenshot_paths=None, dry_run=False):
        """Send email via Gmail SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.config['subject_template']
            msg['From'] = self.config['sender_email']
            msg['To'] = ", ".join(self.config['to_emails'])
            
            if self.config['cc_emails']:
                msg['Cc'] = ", ".join(self.config['cc_emails'])
            
            # For Gmail, embed images as base64 in HTML
            html_content = self.embed_images_in_html(html_body, screenshot_paths)
            msg.attach(MIMEText(html_content, 'html'))
            
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
