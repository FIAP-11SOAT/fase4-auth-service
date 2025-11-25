resource "tls_private_key" "jwt_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "jose_jwk" "example_rsa" {
  kid        = "${local.project_name}-jwk"
  alg        = "RS256"
  public_key = tls_private_key.jwt_key.public_key_pem
  use        = "sig"
}
