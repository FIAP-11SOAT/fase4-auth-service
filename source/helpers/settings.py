from dataclasses import dataclass


@dataclass
class Settings:
    private_key: str

    @classmethod
    def from_dict(cls, secrets: dict):
        return cls(
            private_key=secrets["JWT_PRIVATE_KEY"]
        )