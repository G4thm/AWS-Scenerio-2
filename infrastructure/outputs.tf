output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.smv_data_ai_node.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.smv_data_ai_node.public_ip
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.smv_data_ai_node.private_ip
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.smv_secure_access_group.id
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.data_bucket.id
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = aws_cloudwatch_log_group.smv_logs.name
}

output "dashboard_url" {
  description = "CloudWatch dashboard URL"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.smv_cloud_insight.dashboard_name}"
}
