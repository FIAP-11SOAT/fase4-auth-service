# resource "aws_lb_target_group" "service1_tg" {
#   name     = "service1-tg"
#   port     = 80
#   protocol = "HTTP"
#   vpc_id   = data.aws_vpc.existing.id
#   health_check {
#     path                = "/health"
#     protocol            = "HTTP"
#     matcher             = "200"
#     interval            = 30
#     healthy_threshold   = 2
#     unhealthy_threshold = 2
#   }
# }
#
# resource "aws_lb_listener_rule" "service1_rule" {
#   listener_arn = local.aws_infra_secrets["ALB_LISTENER_ARN"]
#   priority     = 10
#   action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.service1_tg.arn
#   }
#   condition {
#     path_pattern {
#       values = ["/auth/*"]
#     }
#   }
# }