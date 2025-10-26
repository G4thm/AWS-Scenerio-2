# Security Group for EC2 instance
resource "aws_security_group" "smv_secure_access_group" {
  name        = "${var.project_name}_secure-access-group"
  description = "Security group for SMV data processing and AI services"

  # SSH access
  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_cidr
  }

  # PostgreSQL access
  ingress {
    description = "PostgreSQL access"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  # AI Model API access
  ingress {
    description = "AI Model API"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = var.allowed_http_cidr
  }

  # Grafana dashboard
  ingress {
    description = "Grafana dashboard"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = var.allowed_http_cidr
  }

  # CloudWatch agent
  ingress {
    description = "CloudWatch agent"
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  # Outbound traffic
  egress {
    description = "All outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.project_name}_secure-access-group"
    Project = var.project_name
  }
}

# IAM role for EC2 instance
resource "aws_iam_role" "smv_ec2_role" {
  name = "${var.project_name}_ec2_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name    = "${var.project_name}_ec2_role"
    Project = var.project_name
  }
}

# IAM policy for S3 access
resource "aws_iam_role_policy" "smv_s3_policy" {
  name = "${var.project_name}_s3_policy"
  role = aws_iam_role.smv_ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject"
        ]
        Resource = [
          "arn:aws:s3:::${var.project_name}-data-bucket",
          "arn:aws:s3:::${var.project_name}-data-bucket/*"
        ]
      }
    ]
  })
}

# IAM policy for CloudWatch
resource "aws_iam_role_policy_attachment" "cloudwatch_policy" {
  role       = aws_iam_role.smv_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

# IAM instance profile
resource "aws_iam_instance_profile" "smv_instance_profile" {
  name = "${var.project_name}_instance_profile"
  role = aws_iam_role.smv_ec2_role.name
}

# EC2 Instance - smv_data-ai-node
resource "aws_instance" "smv_data_ai_node" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.smv_secure_access_group.id]
  iam_instance_profile   = aws_iam_instance_profile.smv_instance_profile.name

  user_data = templatefile("${path.module}/user_data.sh", {
    db_password = var.db_password
  })

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }

  tags = {
    Name    = "${var.project_name}_data-ai-node"
    Project = var.project_name
    Role    = "data-processing-and-ai"
  }
}

# Get latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# S3 bucket for data storage
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.project_name}-data-bucket"

  tags = {
    Name    = "${var.project_name}-data-bucket"
    Project = var.project_name
  }
}

# S3 bucket versioning
resource "aws_s3_bucket_versioning" "data_bucket_versioning" {
  bucket = aws_s3_bucket.data_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "smv_logs" {
  name              = "/aws/ec2/${var.project_name}"
  retention_in_days = 7

  tags = {
    Name    = "${var.project_name}-logs"
    Project = var.project_name
  }
}

# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "smv_cloud_insight" {
  dashboard_name = "${var.project_name}_cloud-insight"

  dashboard_body = jsonencode({
    widgets = [
      {
        type = "metric"
        properties = {
          metrics = [
            ["AWS/EC2", "CPUUtilization", { stat = "Average", label = "CPU Utilization" }],
            [".", "NetworkIn", { stat = "Sum", label = "Network In" }],
            [".", "NetworkOut", { stat = "Sum", label = "Network Out" }]
          ]
          period = 300
          stat   = "Average"
          region = var.aws_region
          title  = "EC2 Instance Metrics"
        }
      },
      {
        type = "log"
        properties = {
          query   = "SOURCE '${aws_cloudwatch_log_group.smv_logs.name}' | fields @timestamp, @message | sort @timestamp desc | limit 20"
          region  = var.aws_region
          title   = "Recent Logs"
        }
      }
    ]
  })
}
