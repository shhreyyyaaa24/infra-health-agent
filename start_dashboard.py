#!/usr/bin/env python3
"""
Simple dashboard server for testing screenshots
"""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # Set content type
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Generate dashboard HTML based on path
        if path == '/':
            self.wfile.write(self.generate_main_page().encode())
        elif '/gcp-dashboard' in path:
            self.wfile.write(self.generate_dashboard('GCP', '#4285F4').encode())
        elif '/aws-dashboard' in path:
            self.wfile.write(self.generate_dashboard('AWS', '#FF9900').encode())
        elif '/azure-dashboard' in path:
            self.wfile.write(self.generate_dashboard('Azure', '#0078D4').encode())
        else:
            self.wfile.write(b'<h1>Dashboard not found</h1>')
    
    def generate_main_page(self):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Infrastructure Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                .dashboard-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .dashboard-card h3 { margin-top: 0; }
                .nav { background: #333; color: white; padding: 10px; margin: -20px -20px 20px -20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Infrastructure Health Dashboard</h1>
                <div class="dashboard-grid">
                    <div class="dashboard-card">
                        <div class="nav">🔵 Google Cloud Platform</div>
                        <h3>GCP Dashboard</h3>
                        <p>Monitor GCP resources and performance</p>
                        <a href="/gcp-dashboard">View GCP Dashboard →</a>
                    </div>
                    <div class="dashboard-card">
                        <div class="nav">🟠 Amazon Web Services</div>
                        <h3>AWS Dashboard</h3>
                        <p>Monitor AWS resources and performance</p>
                        <a href="/aws-dashboard">View AWS Dashboard →</a>
                    </div>
                    <div class="dashboard-card">
                        <div class="nav">🔵 Microsoft Azure</div>
                        <h3>Azure Dashboard</h3>
                        <p>Monitor Azure resources and performance</p>
                        <a href="/azure-dashboard">View Azure Dashboard →</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def generate_dashboard(self, provider, color):
        import datetime
        
        # Mock data
        projects = [
            {"name": f"{provider} Project 1", "status": "Healthy", "cpu": 45, "budget": 100},
            {"name": f"{provider} Project 2", "status": "Warning", "cpu": 78, "budget": 100},
            {"name": f"{provider} Project 3", "status": "Critical", "cpu": 92, "budget": 100},
        ]
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{provider} Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; background: #f8f9fa; }}
                .header {{ background: {color}; color: white; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
                .metric-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .status-healthy {{ color: #28a745; }}
                .status-warning {{ color: #ffc107; }}
                .status-critical {{ color: #dc3545; }}
                .progress-bar {{ width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; }}
                .progress-fill {{ height: 100%; background: linear-gradient(90deg, #28a745, #ffc107, #dc3545); }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 {provider} Infrastructure Dashboard</h1>
                <p>Real-time monitoring and performance metrics</p>
            </div>
            <div class="container">
                <div class="metrics">
                    <div class="metric-card">
                        <h3>Total Projects</h3>
                        <h2>{len(projects)}</h2>
                    </div>
                    <div class="metric-card">
                        <h3>Healthy Projects</h3>
                        <h2 class="status-healthy">1</h2>
                    </div>
                    <div class="metric-card">
                        <h3>Warning Projects</h3>
                        <h2 class="status-warning">1</h2>
                    </div>
                    <div class="metric-card">
                        <h3>Critical Projects</h3>
                        <h2 class="status-critical">1</h2>
                    </div>
                </div>
                
                <h2>Project Status</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Project Name</th>
                            <th>Status</th>
                            <th>CPU Usage</th>
                            <th>Budget</th>
                            <th>Progress</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for project in projects:
            status_class = f"status-{project['status'].lower()}"
            progress_color = "#28a745" if project['cpu'] < 70 else "#ffc107" if project['cpu'] < 90 else "#dc3545"
            
            dashboard_html += f"""
                        <tr>
                            <td>{project['name']}</td>
                            <td class="{status_class}">{project['status']}</td>
                            <td>{project['cpu']}%</td>
                            <td>{project['budget']}%</td>
                            <td>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {project['cpu']}%; background: {progress_color};"></div>
                                </div>
                            </td>
                        </tr>
            """
        
        dashboard_html += f"""
                    </tbody>
                </table>
                
                <div style="margin-top: 40px; padding: 20px; background: white; border-radius: 8px;">
                    <p><strong>Last Updated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><em>This is a mock dashboard for testing Infrastructure Health Agent screenshots.</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return dashboard_html

def start_dashboard_server(port=63645):
    """Start the dashboard server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    
    print(f"🚀 Starting Dashboard Server")
    print(f"📡 Server running at: http://127.0.0.1:{port}/")
    print(f"📸 Screenshots will be captured from:")
    print(f"   - http://127.0.0.1:{port}/gcp-dashboard")
    print(f"   - http://127.0.0.1:{port}/aws-dashboard")
    print(f"   - http://127.0.0.1:{port}/azure-dashboard")
    print(f"\n💡 In another terminal, run: python3 main.py")
    print(f"⏹️  Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n⏹️  Dashboard server stopped")
        httpd.server_close()

if __name__ == "__main__":
    start_dashboard_server()
