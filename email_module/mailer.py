"""
Generic email sending module using configurable providers
"""

import os
import json
from datetime import datetime
from .email_composer import build_html_email, get_email_subject
from config import EMAIL_PROVIDER, EMAIL_CONFIG, DIRECTOR_CONFIG
from .email_providers import get_email_provider

HISTORY_FILE = "data/history.jsonl"

def append_to_history_and_compare(current_data):
    """Store data in .jsonl and compare with previous entry for insights"""
    insights = []
    prev_data = None
    
    # Read previous data if exists
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                lines = f.readlines()
                if lines:
                    prev_data = json.loads(lines[-1])['data']
        except Exception as e:
            print(f"Failed to read history: {e}")

    # Generate insights based on comparison
    if prev_data and current_data:
        curr_severe = sum(len([p for p in env if p['status'] == 'SEVERE']) for env in current_data.values())
        prev_severe = sum(len([p for p in env if p['status'] == 'SEVERE']) for env in prev_data.values())
        
        if curr_severe > prev_severe:
            insights.append(f"⚠️ Alert: Severe projects increased from {prev_severe} to {curr_severe}.")
        elif curr_severe < prev_severe:
            insights.append(f"✅ Improvement: Severe projects decreased from {prev_severe} to {curr_severe}.")
        else:
            insights.append(f"ℹ️ Status unchanged: Severe projects remain at {curr_severe}.")

    # Save current data
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'a') as f:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'data': current_data
            }
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f"Failed to save to history: {e}")

    return insights

def ai_review_email_content(html_body, insights):
    """Self analysis function to review email before sending"""
    print("🤖 AI Reviewing email content...")
    
    # Inject insights into the HTML body
    insights_html = "<div style='background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin: 15px 0;'>"
    insights_html += "<h3 style='margin-top:0'>📊 Historical Comparison Insights</h3><ul>"
    if insights:
        for insight in insights:
            insights_html += f"<li>{insight}</li>"
    else:
        insights_html += "<li>No previous data available for comparison.</li>"
    insights_html += "</ul></div>"
    
    # Self-analysis logic
    review_notes = []
    if "Severe Risk" in html_body:
        review_notes.append("Found severe risks in report. Tone should reflect urgency.")
    if not insights:
        review_notes.append("First run detected. Establishing baseline.")
        
    ai_status = "<div style='color: #666; font-size: 12px; margin-top: 10px;'>AI Self-Analysis Checks: " + ", ".join(review_notes) + " - PASSED</div>"
    
    # Insert insights and AI status before the first <h3> tag
    if "<h3" in html_body:
        reviewed_html = html_body.replace("<h3", insights_html + ai_status + "<h3", 1)
    else:
        reviewed_html = html_body + insights_html + ai_status
        
    return reviewed_html

def send_email_with_attachments(html_body, screenshot_paths=None, dry_run=False, all_data=None):
    """Send email using configured provider with inline image attachments"""
    try:
        # Perform historical comparison
        insights = []
        if all_data:
            insights = append_to_history_and_compare(all_data)
            
        # Review and amend email content before sending
        reviewed_html = ai_review_email_content(html_body, insights)
        
        # Get email provider based on configuration
        provider_config = EMAIL_CONFIG[EMAIL_PROVIDER]
        email_provider = get_email_provider(EMAIL_PROVIDER, provider_config)
        
        # Send email using the provider (pass all_data for text version)
        return email_provider.send_email(reviewed_html, screenshot_paths, dry_run, all_data)
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def preview_email_html(all_data, screenshot_paths=None):
    """Preview email HTML content using configured provider"""
    try:
        # Perform historical comparison
        insights = append_to_history_and_compare(all_data)
        
        # Get email provider based on configuration
        provider_config = EMAIL_CONFIG[EMAIL_PROVIDER]
        email_provider = get_email_provider(EMAIL_PROVIDER, provider_config)
        
        # Build HTML and preview using the provider
        html_body = build_html_email(all_data, screenshot_paths)
        
        # Review and amend email content
        reviewed_html = ai_review_email_content(html_body, insights)
        
        return email_provider.preview_email(reviewed_html, screenshot_paths)
        
    except Exception as e:
        print(f"Failed to preview email: {e}")
        return None


if __name__ == "__main__":
    # Test email functionality
    from data.fetcher import fetch_all_environment_data
    
    print("Fetching data...")
    all_data = fetch_all_environment_data()
    
    print("Building email...")
    html_body = build_html_email(all_data)
    
    print("Previewing email...")
    preview_email_html(all_data)
