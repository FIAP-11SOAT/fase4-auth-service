# resource "aws_ecs_service" "service1" {
#   name            = "${local.project_name}-service"
#   cluster         = data.aws_ecs_cluster.ecs_cluster.id
#   task_definition = aws_ecs_task_definition.service1_task.arn
#   desired_count   = 2
#   launch_type     = "FARGATE"
#   network_configuration {
#     subnets         = data.aws_subnets.private_subnets.ids
#     security_groups = [aws_security_group.ecs_sg.id]
#     assign_public_ip = false
#   }
#   load_balancer {
#     target_group_arn = aws_lb_target_group.service1_tg.arn
#     container_name   = "${local.project_name}-container"
#     container_port   = 80
#   }
#   depends_on = [aws_lb_listener_rule.service1_rule]
# }
#
# resource "aws_ecs_task_definition" "service1_task" {
#   family                   = "${local.project_name}-task"
#   network_mode             = "awsvpc"
#   requires_compatibilities = ["FARGATE"]
#   cpu                      = 10
#   memory                   = 512
#   execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
#   task_role_arn            = aws_iam_role.ecs_task_role.arn
#
#   container_definitions = jsonencode([
#     {
#       name      = "${local.project_name}-container"
#       image     = "${aws_ecr_repository.ecs_repository.repository_url}:latest"
#       essential = true
#       portMappings = [
#         {
#           containerPort = 8080
#           hostPort      = 80
#           protocol      = "tcp"
#         }
#       ]
#       environment = []
#       logConfiguration = {
#         logDriver = "awslogs"
#         options = {
#           "awslogs-group"         = aws_cloudwatch_log_group.app_log_group.name
#           "awslogs-region"        = data.aws_region.current.region
#           "awslogs-stream-prefix" = "ecs"
#         }
#       }
#     }
#   ])
# }