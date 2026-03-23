"""
Email composition module for building HTML emails with inline images
"""

import os
from datetime import datetime
from config import EMAIL_CONFIG
from config.constants import STATUS_COLORS, STATUS_LABELS


def build_project_details_list(all_data):
    """Build project details as a colored table"""
    html = """
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 13px;">
        <thead>
            <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                <th style="font-weight: 600; color: #495057; padding: 8px; border: 1px solid #ddd;">Environment</th>
                <th style="font-weight: 600; color: #495057; padding: 8px; border: 1px solid #ddd;">Project Name</th>
                <th style="font-weight: 600; color: #495057; padding: 8px; border: 1px solid #ddd;">CPU Usage</th>
                <th style="font-weight: 600; color: #495057; padding: 8px; border: 1px solid #ddd;">CPU Budget</th>
                <th style="font-weight: 600; color: #495057; padding: 8px; border: 1px solid #ddd;">Shutdown Limit</th>
                <th style="font-weight: 600; color: #495057; padding: 8px; border: 1px solid #ddd;">Overbudget Projection</th>
                <th style="font-weight: 600; color: #495057; padding: 8px; border: 1px solid #ddd;">Status</th>
            </tr>
        </thead>
        <tbody>
    """
    
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
            
            overbudget_display = f"${project['overbudgetProjection']}" if project['overbudgetProjection'] > 0 else "$0"
            
            html += f"""
            <tr style="{row_style}">
                <td style="padding: 8px; border: 1px solid #ddd;">{env_name.upper()}</td>
                <td style="padding: 8px; border: 1px solid #ddd;"><strong>{project['name']}</strong></td>
                <td style="padding: 8px; border: 1px solid #ddd;">{project['cpu']}%</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{project['cpusBudget']}%</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{project['cpusShutdownLimit']}%</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{overbudget_display}</td>
                <td style="padding: 8px; border: 1px solid #ddd; color: {status_color}; font-weight: 600;">{status_text}</td>
            </tr>
            """
    
    html += """
        </tbody>
    </table>
    """
    
    return html


def add_screenshots_to_html(screenshot_paths=None):
    """Add screenshots to HTML email as embedded base64 images"""
    import base64
    
    if not screenshot_paths:
        return '<p style="color: #666; font-style: italic;">No screenshots available.</p>'
    
    html = '<div style="margin: 20px 0;">'
    
    for screenshot_path in screenshot_paths:
        if os.path.exists(screenshot_path):
            try:
                # Read image and encode as base64
                with open(screenshot_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode()
                
                # Get filename for display
                filename = os.path.basename(screenshot_path)
                
                # Add image to HTML
                html += f'''<div style="margin-bottom: 20px; border: 1px solid #ddd; padding: 10px; border-radius: 4px;">
                    <p style="margin: 0 0 10px 0; font-weight: 600; color: #2c3e50;">{filename}</p>
                    <img src="data:image/png;base64,{img_data}" style="max-width: 100%; height: auto; border-radius: 4px;"/>
                </div>'''
            except Exception as e:
                print(f"Error embedding screenshot {screenshot_path}: {e}")
                html += f'<p style="color: #dc3545;">Failed to embed screenshot: {filename}</p>'
        else:
            html += f'<p style="color: #ffc107;">Screenshot not found: {screenshot_path}</p>'
    
    html += '</div>'
    return html


def build_html_email(all_data, screenshot_paths=None):
    """Build complete HTML email body"""
    from config import DIRECTOR_CONFIG
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    director_name = DIRECTOR_CONFIG.get('name', 'Team Lead')
    
    # Calculate summary statistics
    total_projects = sum(len(projects) for projects in all_data.values())
    healthy_projects = sum(len([p for p in projects if p['status'] == 'HEALTHY']) for projects in all_data.values())
    severe_projects = sum(len([p for p in projects if p['status'] == 'SEVERE']) for projects in all_data.values())
    medium_projects = total_projects - healthy_projects - severe_projects
    
    # Build important updates
    important_updates = []
    for env_name, projects in all_data.items():
        for project in projects:
            if project['status'] == 'SEVERE':
                important_updates.append(f"⚠️ {project['name']} ({env_name.upper()}): CPU at {project['cpu']}% - Overbudget projection ${project['overbudgetProjection']}")
    
    # Generate human-readable status description
    status_description = generate_status_description(all_data, healthy_projects, severe_projects, medium_projects)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Infrastructure Health Report</title>
</head>
<body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px;">
    
    <div style="font-size: 16px; color: #2c3e50; margin-bottom: 15px; font-weight: 500;">Hi {director_name},</div>
    
    <div style="background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 12px 15px; margin: 15px 0; border-radius: 4px;">
        <h3 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: 600;">Status</h3>
        <p style="margin: 0 0 10px 0;">Here's the current infrastructure status as of {timestamp}:</p>
        <p style="margin: 0; line-height: 1.6;">{status_description}</p>
    </div>
    
    <h3 style="margin: 20px 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: 600;">Summary</h3>
    <p style="margin: 10px 0;"><strong>Total Projects: {total_projects}</strong></p>
    <ul style="margin: 10px 0; padding-left: 0; list-style: none;">
        <li style="margin-bottom: 5px; padding-left: 15px; position: relative; color: #28a745; font-weight: 600;">● <strong>Healthy:</strong> {healthy_projects} projects</li>
        <li style="margin-bottom: 5px; padding-left: 15px; position: relative; color: #ffc107; font-weight: 600;">● <strong>Medium Risk:</strong> {medium_projects} projects</li>
        <li style="margin-bottom: 5px; padding-left: 15px; position: relative; color: #dc3545; font-weight: 600;">● <strong>Severe Risk:</strong> {severe_projects} projects</li>
    </ul>
    
    <h3 style="margin: 20px 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: 600;">Project Details</h3>
    {build_project_details_list(all_data)}
    
    <h3 style="margin: 20px 0 10px 0; color: #2c3e50; font-size: 16px; font-weight: 600;">Dashboard Screenshots</h3>
    {add_screenshots_to_html(screenshot_paths)}
    
    <hr>
    <p><small>This report was generated automatically by the Infrastructure Health Agent.</small></p>
    </body>
</html>"""
    
    return html


def generate_status_description(all_data, healthy_projects, severe_projects, medium_projects):
    """Generate AI-like human-readable status description"""
    
    # Count projects by environment
    env_counts = {}
    for env_name, projects in all_data.items():
        env_counts[env_name] = len(projects)
    
    # Get critical projects details
    critical_projects = []
    for env_name, projects in all_data.items():
        for project in projects:
            if project['status'] == 'SEVERE':
                critical_projects.append(f"{project['name']} in {env_name.upper()}")
    
    # Build descriptive text
    descriptions = []
    
    # Overall status
    if severe_projects > 0:
        descriptions.append(f"Your infrastructure currently has <strong>{severe_projects} project(s) at severe risk</strong> requiring immediate attention.")
    elif medium_projects > 0:
        descriptions.append(f"Your infrastructure is stable with <strong>{medium_projects} project(s) showing medium risk</strong> levels.")
    else:
        descriptions.append(f"<strong>Great news!</strong> All {healthy_projects} project(s) in your infrastructure are operating at healthy levels.")
    
    # Environment breakdown
    env_text = []
    for env_name, count in env_counts.items():
        env_text.append(f"<strong>{count}</strong> in {env_name.upper()}")
    
    if env_text:
        descriptions.append(f"You have a total of <strong>{sum(env_counts.values())} projects</strong> across {len(env_counts)} environments: {', '.join(env_text)}.")
    
    # Health status breakdown
    if healthy_projects > 0:
        descriptions.append(f"<strong>{healthy_projects} project(s)</strong> are running efficiently within normal parameters.")
    
    if medium_projects > 0:
        descriptions.append(f"<strong>{medium_projects} project(s)</strong> are approaching resource limits and may need monitoring.")
    
    if severe_projects > 0:
        descriptions.append(f"<strong>{severe_projects} project(s)</strong> are experiencing high resource utilization and require immediate action.")
        if critical_projects:
            descriptions.append(f"Critical attention needed for: {', '.join(critical_projects[:3])}{' and others' if len(critical_projects) > 3 else ''}.")
    
    # Recommendation
    if severe_projects > 0:
        descriptions.append("<strong>Recommendation:</strong> Please review the severe risk projects immediately and consider scaling resources or optimizing workloads.")
    elif medium_projects > 0:
        descriptions.append("<strong>Recommendation:</strong> Monitor the medium risk projects closely to prevent them from escalating to severe status.")
    else:
        descriptions.append("<strong>Status:</strong> Your infrastructure is well-optimized. Continue monitoring to maintain this performance.")
    
    return " ".join(descriptions)


def get_email_subject():
    """Get formatted email subject with current date"""
    from config import EMAIL_PROVIDER, EMAIL_CONFIG
    date_str = datetime.now().strftime("%Y-%m-%d")
    subject_template = EMAIL_CONFIG[EMAIL_PROVIDER]['subject_template']
    # Replace {date} with actual date
    return subject_template.replace("{date}", date_str)
