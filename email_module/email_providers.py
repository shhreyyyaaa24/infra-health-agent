"""
Email provider implementations (Outlook & Gmail via SMTP)
"""

import os
import base64
import smtplib
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class EmailProvider(ABC):
    """Abstract base class for SMTP email providers"""
    
    def __init__(self, config):
        self.config = config
        self.smtp_server = None
        self.smtp_port = 587
    
    def _embed_images_base64(self, html_body, screenshot_paths):
        """Embed images as base64 in HTML"""
        if not screenshot_paths:
            return html_body
        
        for path in screenshot_paths:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    b64_data = base64.b64encode(f.read()).decode()
                html_body = html_body.replace(f'cid:{os.path.basename(path)}', f'data:image/png;base64,{b64_data}')
        
        return html_body
    
    def _build_message(self, html_body, subject, msg_type='alternative'):
        """Build MIME message"""
        msg = MIMEMultipart(msg_type)
        msg['Subject'] = subject
        msg['From'] = self.config['sender_email']
        msg['To'] = ", ".join(self.config['to_emails'])
        if self.config.get('cc_emails'):
            msg['Cc'] = ", ".join(self.config['cc_emails'])
        return msg
    
    def _send_via_smtp(self, msg):
        """Send message via SMTP"""
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.config['sender_email'], self.config['app_password'])
        all_recipients = self.config['to_emails'] + self.config.get('cc_emails', [])
        server.send_message(msg, to_addrs=all_recipients)
        server.quit()
    
    def _check_credentials(self):
        """Validate email credentials"""
        if not self.config.get('app_password'):
            raise ValueError(f"{self.__class__.__name__} app password not configured. Set environment variable.")
    
    @abstractmethod
    def send_email(self, html_body, screenshot_paths=None, dry_run=False, all_data=None):
        pass
    
    @abstractmethod
    def preview_email(self, html_body, screenshot_paths=None):
        pass


class OutlookProvider(EmailProvider):
    """Outlook SMTP provider"""
    
    def __init__(self, config):
        super().__init__(config)
        self.smtp_server = "smtp-mail.outlook.com"
    
    def send_email(self, html_body, screenshot_paths=None, dry_run=False, all_data=None):
        """Send via Outlook SMTP"""
        try:
            self._check_credentials()
            msg = self._build_message(self._embed_images_base64(html_body, screenshot_paths), self.config['subject_template'])
            msg.attach(MIMEText(msg.get_payload()[0] if msg.get_payload() else html_body, 'html'))
            
            if dry_run:
                with open("draft_outlook_email.eml", "w") as f:
                    f.write(msg.as_string())
                print(f"✓ Outlook email preview saved: draft_outlook_email.eml")
                return True
            
            self._send_via_smtp(msg)
            print("✓ Email sent successfully via Outlook!")
            return True
        except Exception as e:
            print(f"✗ Outlook send failed: {e}")
            return False
    
    def preview_email(self, html_body, screenshot_paths=None):
        """Preview Outlook email"""
        msg = self._build_message(self._embed_images_base64(html_body, screenshot_paths), self.config['subject_template'])
        with open("outlook_email_preview.html", "w", encoding="utf-8") as f:
            f.write(msg.as_string())
        print(f"✓ Preview saved to: outlook_email_preview.html")
        return "outlook_email_preview.html"


class GmailProvider(EmailProvider):
    """Gmail SMTP provider"""
    
    def __init__(self, config):
        super().__init__(config)
        self.smtp_server = "smtp.gmail.com"
    
    def send_email(self, html_body, screenshot_paths=None, dry_run=False, all_data=None):
        """Send via Gmail SMTP with attachments"""
        try:
            self._check_credentials()
            date_str = datetime.now().strftime("%Y-%m-%d")
            subject = self.config['subject_template'].replace("{date}", date_str)
            
            msg = self._build_message(html_body, subject, 'mixed')
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach screenshots
            if screenshot_paths:
                for path in screenshot_paths:
                    if os.path.exists(path):
                        with open(path, "rb") as f:
                            img = MIMEImage(f.read())
                        img.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(path)}"')
                        msg.attach(img)
            
            if dry_run:
                with open("draft_email.eml", "w") as f:
                    f.write(msg.as_string())
                print(f"✓ Gmail email preview saved: draft_email.eml")
                return True
            
            self._send_via_smtp(msg)
            print("✓ Email sent successfully via Gmail!")
            return True
        except Exception as e:
            print(f"✗ Gmail send failed: {e}")
            return False
    
    def preview_email(self, html_body, screenshot_paths=None):
        """Preview Gmail email"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        subject = self.config['subject_template'].replace("{date}", date_str)
        msg = self._build_message(html_body, subject, 'mixed')
        
        with open("email_preview.html", "w", encoding="utf-8") as f:
            f.write(html_body)
        print(f"✓ Preview saved to: email_preview.html")
        return "email_preview.html"


def get_email_provider(provider_name, config):
    """Get email provider instance"""
    providers = {"outlook": OutlookProvider, "gmail": GmailProvider}
    
    if provider_name not in providers:
        raise ValueError(f"Unsupported provider: {provider_name}")
    
    return providers[provider_name](config)
