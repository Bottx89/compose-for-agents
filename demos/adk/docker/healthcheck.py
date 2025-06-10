#!/usr/bin/env python3
"""
Health check script for Academic Research Agent Docker container.
This script verifies that the application is running correctly.
"""

import sys
import time
import requests
import os
from typing import Dict, Any


def check_web_interface() -> Dict[str, Any]:
    """Check if the web interface is responding."""
    try:
        response = requests.get('http://localhost:8080', timeout=10)
        return {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    except requests.exceptions.RequestException as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }


def check_environment_variables() -> Dict[str, Any]:
    """Check if required environment variables are set."""
    required_vars = [
        'GOOGLE_CLOUD_PROJECT',
        'GOOGLE_CLOUD_LOCATION',
        'GOOGLE_GENAI_USE_VERTEXAI'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return {
        'status': 'healthy' if not missing_vars else 'unhealthy',
        'missing_variables': missing_vars
    }


def check_google_cloud_auth() -> Dict[str, Any]:
    """Check if Google Cloud authentication is working."""
    try:
        # Try to import and initialize Google Cloud client
        from google.cloud import aiplatform
        
        project = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_LOCATION')
        
        if not project or not location:
            return {
                'status': 'unhealthy',
                'error': 'Missing project or location configuration'
            }
        
        # Initialize AI Platform (this will fail if auth is not working)
        aiplatform.init(project=project, location=location)
        
        return {
            'status': 'healthy',
            'project': project,
            'location': location
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }


def check_adk_availability() -> Dict[str, Any]:
    """Check if ADK is properly installed and available."""
    try:
        from google.adk.agents import LlmAgent
        return {
            'status': 'healthy',
            'adk_version': 'available'
        }
    except ImportError as e:
        return {
            'status': 'unhealthy',
            'error': f'ADK not available: {str(e)}'
        }


def main():
    """Run all health checks and report results."""
    print("🏥 Academic Research Agent Health Check")
    print("=" * 50)
    
    checks = {
        'Environment Variables': check_environment_variables,
        'ADK Availability': check_adk_availability,
        'Google Cloud Auth': check_google_cloud_auth,
        'Web Interface': check_web_interface,
    }
    
    all_healthy = True
    results = {}
    
    for check_name, check_func in checks.items():
        print(f"\n🔍 Checking {check_name}...")
        try:
            result = check_func()
            results[check_name] = result
            
            if result['status'] == 'healthy':
                print(f"✅ {check_name}: Healthy")
                if 'response_time' in result:
                    print(f"   Response time: {result['response_time']:.2f}s")
                if 'project' in result:
                    print(f"   Project: {result['project']}")
                if 'location' in result:
                    print(f"   Location: {result['location']}")
            else:
                print(f"❌ {check_name}: Unhealthy")
                if 'error' in result:
                    print(f"   Error: {result['error']}")
                if 'missing_variables' in result and result['missing_variables']:
                    print(f"   Missing variables: {', '.join(result['missing_variables'])}")
                all_healthy = False
                
        except Exception as e:
            print(f"❌ {check_name}: Failed with exception: {str(e)}")
            results[check_name] = {'status': 'unhealthy', 'error': str(e)}
            all_healthy = False
    
    print("\n" + "=" * 50)
    if all_healthy:
        print("🎉 All health checks passed! The application is healthy.")
        sys.exit(0)
    else:
        print("⚠️  Some health checks failed. Please review the issues above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
