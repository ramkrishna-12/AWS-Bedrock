#!/bin/bash




# Checks whether all Docker images have running containers.
# Verifies container health status (if health checks are configured).
# Collects active container logs.
# Extracts error-related log entries.
# Saves everything into .txt files for later review. /



# Output files
REPORT_FILE="docker_health_report.txt"
ACTIVE_LOGS_FILE="docker_active_logs.txt"
ERROR_LOGS_FILE="docker_error_logs.txt"

# Clear previous reports
> "$REPORT_FILE"
> "$ACTIVE_LOGS_FILE"
> "$ERROR_LOGS_FILE"

echo "Docker Health Check Report - $(date)" >> "$REPORT_FILE"
echo "==================================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check Docker daemon
if ! docker info >/dev/null 2>&1; then
    echo "ERROR: Docker daemon is not running." | tee -a "$REPORT_FILE"
    exit 1
fi

echo "Docker daemon is running." >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Get all containers
containers=$(docker ps -a --format "{{.Names}}")

if [ -z "$containers" ]; then
    echo "No containers found." >> "$REPORT_FILE"
    exit 0
fi

for container in $containers
do
    echo "Checking container: $container" >> "$REPORT_FILE"
    echo "----------------------------------------" >> "$REPORT_FILE"

    status=$(docker inspect --format='{{.State.Status}}' "$container" 2>/dev/null)
    health=$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}No Healthcheck{{end}}' "$container" 2>/dev/null)

    echo "Status : $status" >> "$REPORT_FILE"
    echo "Health : $health" >> "$REPORT_FILE"

    if [ "$status" != "running" ]; then
        echo "WARNING: Container is not running." >> "$REPORT_FILE"
    fi

    # Save active logs
    echo "" >> "$ACTIVE_LOGS_FILE"
    echo "==================================================" >> "$ACTIVE_LOGS_FILE"
    echo "Container: $container" >> "$ACTIVE_LOGS_FILE"
    echo "==================================================" >> "$ACTIVE_LOGS_FILE"

    docker logs --tail 500 "$container" >> "$ACTIVE_LOGS_FILE" 2>&1

    # Extract errors from logs
    echo "" >> "$ERROR_LOGS_FILE"
    echo "==================================================" >> "$ERROR_LOGS_FILE"
    echo "Container: $container" >> "$ERROR_LOGS_FILE"
    echo "==================================================" >> "$ERROR_LOGS_FILE"

    docker logs --tail 500 "$container" 2>&1 | \
        grep -iE "error|exception|fatal|fail|panic|critical" \
        >> "$ERROR_LOGS_FILE"

    echo "" >> "$REPORT_FILE"
done

echo "==================================================" >> "$REPORT_FILE"
echo "Summary" >> "$REPORT_FILE"
echo "==================================================" >> "$REPORT_FILE"

running_count=$(docker ps --format "{{.Names}}" | wc -l)
total_count=$(docker ps -a --format "{{.Names}}" | wc -l)

echo "Running Containers : $running_count" >> "$REPORT_FILE"
echo "Total Containers   : $total_count" >> "$REPORT_FILE"

echo ""
echo "Reports generated:"
echo "  - $REPORT_FILE"
echo "  - $ACTIVE_LOGS_FILE"
echo "  - $ERROR_LOGS_FILE"



# Output Files
# docker_health_report.txt → Container status and health summary.
# docker_active_logs.txt → Last 500 log lines from each container.
# docker_error_logs.txt → Error, exception, fatal, fail, panic, and critical log entries.


# Check Image Integrity

echo ""
echo "Docker Images Check" >> "$REPORT_FILE"
echo "==================================================" >> "$REPORT_FILE"

docker images --format "{{.Repository}}:{{.Tag}}" | while read image
do
    echo "Testing image: $image" >> "$REPORT_FILE"

    docker run --rm --entrypoint="" "$image" true >/dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "OK: $image" >> "$REPORT_FILE"
    else
        echo "FAILED: $image" >> "$REPORT_FILE"
    fi
done