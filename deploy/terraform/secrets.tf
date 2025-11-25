resource "aws_secretsmanager_secret" "secrets" {
  name                    = "${local.project_name}-secrets"
  description             = "Secrets for ${local.project_name} project"
  recovery_window_in_days = 0

  tags = {
    Name = "${local.project_name}-secrets"
  }
}

resource "aws_secretsmanager_secret_version" "secrets" {
  secret_id = aws_secretsmanager_secret.secrets.id
  secret_string = jsonencode({
    JWT_PRIVATE_KEY = tls_private_key.jwt_key.private_key_pem
    JWT_PUBLIC_KEY  = tls_private_key.jwt_key.public_key_pem,
    JWT_JWK         = jose_jwk.example_rsa.jwk
  })
}
