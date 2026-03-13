"""
Email composition module for building HTML emails with inline images
"""

import os
import base64
from datetime import datetime
from config import STATUS_COLORS, STATUS_LABELS, EMAIL_CONFIG


def generate_cid_for_image(image_path):
    """Generate a content ID for an image file"""
    filename = os.path.basename(image_path)
    name_without_ext = os.path.splitext(filename)[0]
    return f"{name_without_ext}@infrahealth.local"


def embed_image_as_base64(image_path):
    """Convert image file to base64 for embedding"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def build_html_summary_table(all_data):
    """Build HTML table summarizing project status by environment"""
    html = """
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th>Environment</th>
                <th>Project Name</th>
                <th>CPU Usage</th>
                <th>CPU Budget</th>
                <th>Shutdown Limit</th>
                <th>Overbudget Projection</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for env_name, projects in all_data.items():
        for project in projects:
            status = project['status']
            color = STATUS_COLORS[status]
            status_label = STATUS_LABELS[status]
            
            # Format overbudget projection
            overbudget = project['overbudgetProjection']
            overbudget_display = f"${overbudget:,}" if overbudget > 0 else "$0"
            
            html += f"""
            <tr style="background-color: {color}20; border-left: 4px solid {color};">
                <td>{project['environment']}</td>
                <td><strong>{project['name']}</strong></td>
                <td>{project['cpu']}%</td>
                <td>{project['cpusBudget']}%</td>
                <td>{project['cpusShutdownLimit']}%</td>
                <td>{overbudget_display}</td>
                <td style="color: {color}; font-weight: bold;">{status_label}</td>
            </tr>
            """
    
    html += """
        </tbody>
    </table>
    """
    
    return html


def build_status_summary(all_data):
    """Build a status summary section"""
    total_projects = sum(len(projects) for projects in all_data.values())
    status_counts = {"HEALTHY": 0, "MEDIUM": 0, "SEVERE": 0}
    
    for projects in all_data.values():
        for project in projects:
            status_counts[project['status']] += 1
    
    html = f"""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h3>Summary</h3>
        <p><strong>Total Projects:</strong> {total_projects}</p>
        <ul>
            <li><span style="color: {STATUS_COLORS['HEALTHY']};">●</span> <strong>Healthy:</strong> {status_counts['HEALTHY']} projects</li>
            <li><span style="color: {STATUS_COLORS['MEDIUM']};">●</span> <strong>Medium Risk:</strong> {status_counts['MEDIUM']} projects</li>
            <li><span style="color: {STATUS_COLORS['SEVERE']};">●</span> <strong>Severe Risk:</strong> {status_counts['SEVERE']} projects</li>
        </ul>
    </div>
    """
    
    return html


def build_screenshots_section(screenshot_paths):
    """Build HTML section with embedded screenshots"""
    html = '<h3>Dashboard Screenshots</h3>\n'
    
    for screenshot_path in screenshot_paths:
        if os.path.exists(screenshot_path):
            cid = generate_cid_for_image(screenshot_path)
            env_name = os.path.basename(screenshot_path).replace('_dashboard.png', '').upper()
            
            html += f"""
            <div style="margin-bottom: 20px;">
                <h4>{env_name} Dashboard</h4>
                <img src="cid:{cid}" alt="{env_name} Dashboard" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px;">
            </div>
            """
    
    return html


def build_html_email(all_data, screenshot_paths=None):
    """Build complete HTML email body"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Infrastructure Health Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
            }}
            table {{
                margin-bottom: 20px;
            }}
            th, td {{
                text-align: left;
                padding: 8px;
            }}
        </style>
    </head>
    <body>
        <h1>Infrastructure Health Report</h1>
        <p><strong>Generated on:</strong> {timestamp}</p>
        
        {build_status_summary(all_data)}
        
        <h3>Project Details</h3>
        {build_html_summary_table(all_data)}
    """
    
    if screenshot_paths:
        html += build_screenshots_section(screenshot_paths)
    
    html += """
        <hr>
        <p><small>This report was generated automatically by the Infrastructure Health Agent.</small></p>
    </body>
    </html>
    """
    
    return html


def get_email_subject():
    """Get formatted email subject with current date"""
    from config import EMAIL_PROVIDER
    date_str = datetime.now().strftime("%Y-%m-%d")
    return EMAIL_CONFIG[EMAIL_PROVIDER]['subject_template'].format(date=date_str)
