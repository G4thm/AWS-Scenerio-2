FROM grafana/grafana:latest

# Copy datasource and dashboard configurations
COPY grafana-datasources.yml /etc/grafana/provisioning/datasources/
COPY grafana-dashboard.json /etc/grafana/provisioning/dashboards/

# Set environment variables
ENV GF_SECURITY_ADMIN_PASSWORD=admin
ENV GF_USERS_ALLOW_SIGN_UP=false
ENV GF_AUTH_ANONYMOUS_ENABLED=false

# Expose Grafana port
EXPOSE 3000
