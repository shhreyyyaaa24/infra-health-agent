"""
Data fetcher module for API calls and data processing
"""

import requests
import json
import platform
from datetime import datetime
from config import API_ENDPOINT, USE_WINDOWS_AUTH, BASIC_AUTH_USER, BASIC_AUTH_PASS, DIRECTOR_CONFIG, ENVIRONMENTS
from config.constants import DEFAULT_API_TIMEOUT

# Only import Windows auth modules on Windows
if platform.system().lower() == 'windows':
    try:
        from requests_negotiate_sspi import HttpNegotiateAuth
        from requests_ntlm import HttpNtlmAuth
        WINDOWS_AUTH_AVAILABLE = True
    except ImportError:
        WINDOWS_AUTH_AVAILABLE = False
else:
    WINDOWS_AUTH_AVAILABLE = False


def get_auth_session():
    """Create an authenticated requests session"""
    session = requests.Session()
    
    if USE_WINDOWS_AUTH and WINDOWS_AUTH_AVAILABLE:
        try:
            # Try Windows authentication first
            session.auth = HttpNegotiateAuth()
        except Exception as e:
            print(f"Windows auth failed: {e}")
            if BASIC_AUTH_USER and BASIC_AUTH_PASS:
                # Fallback to NTLM
                session.auth = HttpNtlmAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS)
            else:
                raise Exception("No valid authentication method available")
    elif BASIC_AUTH_USER and BASIC_AUTH_PASS:
        if WINDOWS_AUTH_AVAILABLE:
            session.auth = HttpNtlmAuth(BASIC_AUTH_USER, BASIC_AUTH_PASS)
        else:
            # Use basic auth on non-Windows platforms
            session.auth = (BASIC_AUTH_USER, BASIC_AUTH_PASS)
    elif USE_WINDOWS_AUTH and not WINDOWS_AUTH_AVAILABLE:
        print("Warning: Windows auth requested but not available on this platform")
        print("Falling back to basic auth if credentials provided")
        if BASIC_AUTH_USER and BASIC_AUTH_PASS:
            session.auth = (BASIC_AUTH_USER, BASIC_AUTH_PASS)
    
    return session


def fetch_api_data():
    """Fetch data from the REST API"""
    session = get_auth_session()
    
    try:
        response = session.get(API_ENDPOINT, timeout=DEFAULT_API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None


def filter_projects_by_owner(projects, owner_name):
    """Filter projects by owner/director name"""
    filtered = []
    for project in projects:
        # Check if project has budget array and owner matches
        if 'budget' in project and isinstance(project['budget'], list):
            for budget_item in project['budget']:
                if 'owner' in budget_item and budget_item['owner'] == owner_name:
                    filtered.append(project)
                    break
    return filtered


def compute_project_status(project):
    """Compute health status based on CPU and budget projections"""
    overbudget_projection = project.get('overbudgetProjection', 0)
    cpu = project.get('cpu', 0)
    cpus_shutdown_limit = project.get('cpusShutdownLimit', 0)
    
    if overbudget_projection <= 0:
        return "HEALTHY"
    elif overbudget_projection > 0 and cpu <= cpus_shutdown_limit:
        return "MEDIUM"
    else:  # overbudget_projection > 0 and cpu > cpus_shutdown_limit
        return "SEVERE"


def process_environment_data(env_key, projects):
    """Process data for a specific environment"""
    env_config = ENVIRONMENTS[env_key]
    director_name = DIRECTOR_CONFIG["name"]
    filtered_projects = filter_projects_by_owner(projects, director_name)
    
    processed_projects = []
    for project in filtered_projects:
        status = compute_project_status(project)
        processed_projects.append({
            'name': project.get('name', 'Unknown'),
            'cpu': project.get('cpu', 0),
            'cpusBudget': project.get('cpusBudget', 0),
            'cpusShutdownLimit': project.get('cpusShutdownLimit', 0),
            'overbudgetProjection': project.get('overbudgetProjection', 0),
            'status': status,
            'environment': env_config['display_name']
        })
    
    return processed_projects


def fetch_all_environment_data():
    """Fetch and process data for all environments"""
    # For now, return mock data since we don't have a real API
    # In production, this would call fetch_api_data() for each environment
    
    director_name = DIRECTOR_CONFIG["name"]
    
    mock_data = {
        "gcp": [
            {
                "name": "AI - Common Components",
                "cpu": 45,
                "cpusBudget": 100,
                "cpusShutdownLimit": 90,
                "overbudgetProjection": 0,
                "budget": [{"owner": director_name}]
            },
            {
                "name": "Data Analytics Pipeline", 
                "cpu": 85,
                "cpusBudget": 100,
                "cpusShutdownLimit": 80,
                "overbudgetProjection": 250,
                "budget": [{"owner": director_name}]
            },
            {
                "name": "ML Training Infrastructure",
                "cpu": 95,
                "cpusBudget": 100,
                "cpusShutdownLimit": 80,
                "overbudgetProjection": 750,
                "budget": [{"owner": director_name}]
            }
        ],
        "aws": [
            {
                "name": "EKS Production Cluster",
                "cpu": 30,
                "cpusBudget": 100,
                "cpusShutdownLimit": 90,
                "overbudgetProjection": 0,
                "budget": [{"owner": director_name}]
            },
            {
                "name": "Batch Processing Jobs",
                "cpu": 88,
                "cpusBudget": 100,
                "cpusShutdownLimit": 85,
                "overbudgetProjection": 450,
                "budget": [{"owner": director_name}]
            }
        ],
        "azure": [
            {
                "name": "Web Apps Cluster",
                "cpu": 25,
                "cpusBudget": 100,
                "cpusShutdownLimit": 90,
                "overbudgetProjection": 0,
                "budget": [{"owner": director_name}]
            },
            {
                "name": "Database Services",
                "cpu": 92,
                "cpusBudget": 100,
                "cpusShutdownLimit": 85,
                "overbudgetProjection": 1200,
                "budget": [{"owner": director_name}]
            }
        ]
    }
    
    all_data = {}
    for env_key, projects in mock_data.items():
        all_data[env_key] = process_environment_data(env_key, projects)
    
    return all_data


def get_summary_stats(all_data):
    """Generate summary statistics across all environments"""
    total_projects = 0
    status_counts = {"HEALTHY": 0, "MEDIUM": 0, "SEVERE": 0}
    
    for env_data in all_data.values():
        total_projects += len(env_data)
        for project in env_data:
            status_counts[project['status']] += 1
    
    return {
        'total_projects': total_projects,
        'status_counts': status_counts,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
