import os

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "comunisafe_super_secret_key_change_me_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./comunisafe.db")
    
    # Fictitious municipality endpoint for integration requirements
    MUNICIPALITY_API_URL: str = os.getenv(
        "MUNICIPALITY_API_URL", 
        "https://api.municipalidad.gob.cl/v1/incidencias"
    )

settings = Settings()
