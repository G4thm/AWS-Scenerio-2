variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "smv"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.large"
}

variable "key_name" {
  description = "SSH key pair name"
  type        = string
}

variable "allowed_ssh_cidr" {
  description = "CIDR blocks allowed to SSH. WARNING: 0.0.0.0/0 is not recommended for production. Restrict to your IP or trusted networks."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allowed_http_cidr" {
  description = "CIDR blocks allowed HTTP access to API and Dashboard. WARNING: 0.0.0.0/0 is not recommended for production. Restrict to trusted networks."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "db_password" {
  description = "PostgreSQL database password"
  type        = string
  sensitive   = true
}
