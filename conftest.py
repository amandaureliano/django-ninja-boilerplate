import os

# SECRET_KEY padrão para testes. As demais vars vêm do .env ou do CI.
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
