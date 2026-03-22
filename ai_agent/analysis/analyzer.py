"""
Core Data Analyzer for AI Agent
Orchestrates anomaly detection and trend analysis
"""

import logging
from datetime import datetime
from statistics import mean
from typing import Dict, List, Any

from .anomaly_detector import AnomalyDetector
from .trend_analyzer import TrendAnalyzer


class DataAnalyzer:
    """
    Intelligent data analyzer for infrastructure monitoring.
    Orchestrates anomaly detection, trend analysis, and risk assessment.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.anomaly_detector = AnomalyDetector()
        self.trend_analyzer = TrendAnalyzer()

        # Analysis thresholds
        self.severity_thresholds = {
            'critical': 0.8,
            'high': 0.6,
            'medium': 0.4,
            'low': 0.2
        }

        self.logger.info("DataAnalyzer initialized with modular analysis components")

    def analyze_infrastructure(self, infrastructure_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of infrastructure data
        """
        self.logger.info("🔍 Performing intelligent infrastructure analysis...")

        analysis = {
            'timestamp': datetime.now().isoformat(),
            'summary': self._create_summary(infrastructure_data),
            'anomalies': [],
            'trends': [],
            'critical_issues': [],
            'high_risk_projects': [],
            'performance_metrics': self._calculate_performance_metrics(infrastructure_data),
            'recommendations': [],
            'overall_severity_score': 0.0,
            'risk_assessment': {}
        }

        # Analyze each environment
        for env_name, projects in infrastructure_data.items():
            env_analysis = self._analyze_environment(env_name, projects)

            # Aggregate findings
            analysis['anomalies'].extend(env_analysis['anomalies'])
            analysis['trends'].extend(env_analysis['trends'])
            analysis['critical_issues'].extend(env_analysis['critical_issues'])
            analysis['high_risk_projects'].extend(env_analysis['high_risk_projects'])

        # Generate overall insights
        analysis['overall_severity_score'] = self._calculate_overall_severity(analysis)
        analysis['risk_assessment'] = self._assess_overall_risk(analysis)
        analysis['recommendations'] = self._generate_recommendations(analysis)

        self.logger.info(f"Analysis complete: {len(analysis['anomalies'])} anomalies, {len(analysis['critical_issues'])} critical issues")

        return analysis

    def _analyze_environment(self, env_name: str, projects: List[Dict]) -> Dict[str, Any]:
        """Analyze a specific environment"""
        env_analysis = {
            'environment': env_name,
            'anomalies': [],
            'trends': [],
            'critical_issues': [],
            'high_risk_projects': []
        }

        for project in projects:
            # Detect anomalies
            anomalies = self.anomaly_detector.detect_all_anomalies(project)
            env_analysis['anomalies'].extend(anomalies)

            # Analyze trends
            trends = self.trend_analyzer.analyze_all_trends(project)
            env_analysis['trends'].extend(trends)

            # Assess project criticality
            if project['status'] == 'SEVERE':
                env_analysis['critical_issues'].append({
                    'project': project['name'],
                    'environment': env_name,
                    'type': self._determine_critical_type(project),
                    'severity': 'critical',
                    'description': self._generate_critical_description(project),
                    'recommended_action': self._generate_recommended_action(project),
                    'cost_impact': self._estimate_cost_impact(project),
                    'customer_impact': self._assess_customer_impact(project)
                })

            elif project['status'] == 'MEDIUM':
                env_analysis['high_risk_projects'].append({
                    'project': project['name'],
                    'environment': env_name,
                    'risk_factors': self._identify_risk_factors(project),
                    'severity': 'high'
                })

        return env_analysis

    def _determine_critical_type(self, project: Dict) -> str:
        """Determine the type of critical issue"""
        cpu_usage = project.get('cpu', 0)
        overbudget = project.get('overbudgetProjection', 0)

        if cpu_usage > project.get('cpusShutdownLimit', 90):
            return 'cpu_overload'
        elif overbudget > 1000:
            return 'budget_overrun'
        else:
            return 'performance_degradation'

    def _generate_critical_description(self, project: Dict) -> str:
        """Generate description for critical issue"""
        critical_type = self._determine_critical_type(project)

        if critical_type == 'cpu_overload':
            return f"Critical CPU overload in {project['name']}: {project.get('cpu', 0)}% usage exceeds shutdown limit"
        elif critical_type == 'budget_overrun':
            return f"Critical budget overrun in {project['name']}: ${project.get('overbudgetProjection', 0)} over budget"
        else:
            return f"Critical performance issue in {project['name']}: Multiple metrics in severe range"

    def _generate_recommended_action(self, project: Dict) -> str:
        """Generate recommended action for critical issue"""
        critical_type = self._determine_critical_type(project)

        if critical_type == 'cpu_overload':
            return "Immediately scale up resources or optimize workload to prevent service disruption"
        elif critical_type == 'budget_overrun':
            return "Urgent budget review and cost optimization measures required"
        else:
            return "Comprehensive performance audit and optimization needed"

    def _estimate_cost_impact(self, project: Dict) -> float:
        """Estimate cost impact of critical issue"""
        overbudget = project.get('overbudgetProjection', 0)
        cpu_usage = project.get('cpu', 0)

        # Simple cost estimation
        base_cost = overbudget
        cpu_cost = max(0, (cpu_usage - 80) * 50)  # $50 per % over 80%

        return base_cost + cpu_cost

    def _assess_customer_impact(self, project: Dict) -> bool:
        """Assess if critical issue impacts customers"""
        cpu_usage = project.get('cpu', 0)
        overbudget = project.get('overbudgetProjection', 0)

        return cpu_usage > 90 or overbudget > 500

    def _identify_risk_factors(self, project: Dict) -> List[str]:
        """Identify risk factors for high-risk projects"""
        risk_factors = []

        cpu_usage = project.get('cpu', 0)
        overbudget = project.get('overbudgetProjection', 0)

        if cpu_usage > 70:
            risk_factors.append("High CPU usage")

        if overbudget > 0:
            risk_factors.append("Budget overrun")

        if cpu_usage > project.get('cpusShutdownLimit', 90) * 0.9:
            risk_factors.append("Approaching CPU limit")

        return risk_factors

    def _calculate_performance_metrics(self, infrastructure_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall performance metrics"""
        all_projects = []
        for projects in infrastructure_data.values():
            all_projects.extend(projects)

        if not all_projects:
            return {}

        cpu_usages = [p.get('cpu', 0) for p in all_projects]
        overbudgets = [p.get('overbudgetProjection', 0) for p in all_projects]

        metrics = {
            'total_projects': len(all_projects),
            'average_cpu_usage': mean(cpu_usages),
            'max_cpu_usage': max(cpu_usages),
            'total_overbudget': sum(overbudgets),
            'projects_overbudget': len([o for o in overbudgets if o > 0]),
            'health_distribution': {
                'healthy': len([p for p in all_projects if p['status'] == 'HEALTHY']),
                'medium': len([p for p in all_projects if p['status'] == 'MEDIUM']),
                'severe': len([p for p in all_projects if p['status'] == 'SEVERE'])
            }
        }

        return metrics

    def _calculate_overall_severity(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall severity score (0-1)"""
        critical_issues = len(analysis['critical_issues'])
        anomalies = len(analysis['anomalies'])
        high_risk_projects = len(analysis['high_risk_projects'])

        # Weight factors
        critical_weight = 0.5
        anomaly_weight = 0.3
        high_risk_weight = 0.2

        # Calculate weighted score
        total_projects = analysis['summary']['total_projects']
        if total_projects == 0:
            return 0.0

        critical_score = (critical_issues / total_projects) * critical_weight
        anomaly_score = (anomalies / total_projects) * anomaly_weight
        high_risk_score = (high_risk_projects / total_projects) * high_risk_weight

        overall_score = min(critical_score + anomaly_score + high_risk_score, 1.0)

        return round(overall_score, 3)

    def _assess_overall_risk(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall risk level"""
        severity_score = analysis['overall_severity_score']

        if severity_score >= 0.8:
            risk_level = 'critical'
            risk_description = "Critical risk level - Immediate action required"
        elif severity_score >= 0.6:
            risk_level = 'high'
            risk_description = "High risk level - Urgent attention needed"
        elif severity_score >= 0.4:
            risk_level = 'medium'
            risk_description = "Medium risk level - Monitor closely"
        else:
            risk_level = 'low'
            risk_description = "Low risk level - Normal operations"

        return {
            'risk_level': risk_level,
            'severity_score': severity_score,
            'description': risk_description,
            'factors': {
                'critical_issues': len(analysis['critical_issues']),
                'anomalies': len(analysis['anomalies']),
                'high_risk_projects': len(analysis['high_risk_projects'])
            }
        }

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate intelligent recommendations based on analysis"""
        recommendations = []

        critical_issues = analysis['critical_issues']
        anomalies = analysis['anomalies']
        high_risk_projects = analysis['high_risk_projects']

        if critical_issues:
            recommendations.append(f"Address {len(critical_issues)} critical issues immediately to prevent service disruption")

        if anomalies:
            recommendations.append(f"Investigate {len(anomalies)} detected anomalies for potential optimization opportunities")

        if high_risk_projects:
            recommendations.append(f"Monitor {len(high_risk_projects)} high-risk projects closely to prevent escalation")

        # Performance recommendations
        metrics = analysis['performance_metrics']
        if metrics.get('average_cpu_usage', 0) > 70:
            recommendations.append("Consider scaling resources to optimize CPU utilization")

        if metrics.get('total_overbudget', 0) > 1000:
            recommendations.append("Implement cost optimization measures to reduce budget overruns")

        if analysis['overall_severity_score'] < 0.3:
            recommendations.append("System performing well - consider implementing preventive monitoring")

        return recommendations

    def _create_summary(self, infrastructure_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create summary of infrastructure data"""
        total_projects = sum(len(projects) for projects in infrastructure_data.values())

        status_counts = {"HEALTHY": 0, "MEDIUM": 0, "SEVERE": 0}
        for projects in infrastructure_data.values():
            for project in projects:
                status_counts[project['status']] += 1

        return {
            'total_projects': total_projects,
            'environments': list(infrastructure_data.keys()),
            'status_distribution': status_counts,
            'analysis_timestamp': datetime.now().isoformat()
        }
