from app.services.auth_service import create_access_token

token = create_access_token(
    {
        "sub": "admin",
        "role": "admin"
    }
)

print(token)