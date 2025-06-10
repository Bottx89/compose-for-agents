#!/bin/bash

# Entrypoint script for Academic Research Agent Docker container

set -e

# Function to print usage
usage() {
    echo "Usage: $0 [web|cli|test|eval|deploy] [additional_args...]"
    echo ""
    echo "Commands:"
    echo "  web                 Start the web interface (default)"
    echo "  cli                 Start the CLI interface"
    echo "  test                Run tests"
    echo "  eval                Run evaluation"
    echo "  deploy              Run deployment commands"
    echo "  health              Run health check"
    echo "  bash                Start bash shell"
    echo ""
    echo "Examples:"
    echo "  $0 web              # Start web interface on port 8080"
    echo "  $0 cli              # Start CLI interface"
    echo "  $0 test             # Run all tests"
    echo "  $0 eval             # Run evaluation"
    echo "  $0 bash             # Start interactive bash shell"
}

# Check if .env file exists and source it
if [ -f "/app/.env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' /app/.env | xargs)
fi

# Note: Using Poetry to run commands instead of direct PATH manipulation

# Main command handling
case "${1:-web}" in
    web)
        echo "Starting Academic Research Agent web interface..."
        cd /app
        exec adk web --host 0.0.0.0 --port 8080
        ;;
    cli)
        echo "Starting Academic Research Agent CLI..."
        cd /app
        exec adk run academic_research
        ;;
    test)
        echo "Running tests..."
        cd /app
        exec python -m pytest tests/ "${@:2}"
        ;;
    eval)
        echo "Running evaluation..."
        cd /app
        exec python -m pytest eval/ "${@:2}"
        ;;
    deploy)
        echo "Running deployment..."
        cd /app
        exec python deployment/deploy.py "${@:2}"
        ;;
    health)
        echo "Running health check..."
        cd /app
        exec python docker/healthcheck.py
        ;;
    debug)
        echo "Debug mode - checking ADK installation..."
        cd /app
        echo "PATH: $PATH"
        echo "Checking if ADK is importable:"
        python -c "import google.adk; print('ADK imported successfully')" || echo "ADK import failed"
        echo "Checking adk command:"
        which adk || echo "adk command not found"
        echo "Python packages:"
        pip list | grep -E "(google|adk)" || echo "No Google/ADK packages found"
        ;;
    bash)
        echo "Starting bash shell..."
        exec /bin/bash
        ;;
    help|--help|-h)
        usage
        exit 0
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        usage
        exit 1
        ;;
esac
