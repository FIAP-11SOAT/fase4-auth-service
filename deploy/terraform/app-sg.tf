# resource "aws_security_group" "ecs_sg" {
#   name        = "${local.project_name}-ecs-sg"
#   description = "Security group for ECS tasks"
#   vpc_id      = data.aws_vpc.existing.id
#
#   ingress {
#     from_port       = 80
#     to_port         = 80
#     protocol        = "tcp"
#     security_groups = [data.aws_security_group.alb_sg.id]
#   }
#
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }
