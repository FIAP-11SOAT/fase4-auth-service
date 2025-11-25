from jwcrypto import jwt, jwk


class JwtSignatureProvider:

    def __init__(self, private_key: str, jwks: str):
        self.private_key = jwk.JWK.from_pem(private_key.encode())
        self.public_jwk = jwk.JWK.from_json(jwks)

    def sign(self, payload: dict) -> str:
        token = jwt.JWT(header={"alg": "RS256"}, claims=payload)
        token.make_signed_token(self.private_key)
        return token.serialize()

    def verify(self, token_str: str) -> dict:
        token = jwt.JWT(jwt=token_str, key=self.private_key)
        return token.claims

    def validate(self, token_str: str) -> bool:
        try:
            token = jwt.JWT(jwt=token_str, key=self.public_jwk)
            return True
        except Exception:
            return False