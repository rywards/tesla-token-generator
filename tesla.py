# Tesla API Access and Refresh Token Generator
# Written by: rywards

import requests
import secrets, hashlib, base64

# Define the Tesla API endpoints
AUTH_URL = "https://auth.tesla.com/oauth2/v3/authorize"
TOKEN_URL = "https://auth.tesla.com/oauth2/v3/token"

code_verifier = secrets.token_urlsafe(64)

# Calculate the SHA256 hash of the code verifier
code_verifier_bytes = code_verifier.encode("utf-8")
sha256_hash = hashlib.sha256(code_verifier_bytes).digest()

# Base64-URL-encode the hash
code_challenge = base64.urlsafe_b64encode(sha256_hash).rstrip(b"=").decode("utf-8")
random_state = secrets.token_hex(8)

# Create a session
session = requests.Session()

# Get authorization code
params = {
    "client_id": "ownerapi",
    "code_challenge": code_challenge,  # Generate a code challenge (e.g., using hashlib)
    "code_challenge_method": "S256",
    "redirect_uri": "https://auth.tesla.com/void/callback",
    "response_type": "code",
    "scope": "openid email offline_access",
    "state": random_state,
}

response = session.get(AUTH_URL, params=params)

# copy this response url, log into tesla, then copy the auth code and paste in console window
print(response.url)
authorization_code = input("Enter the authorization code from the URL: ")

# Step 2: Exchange authorization code for tokens
data = {
    "grant_type": "authorization_code",
    "client_id": "ownerapi",
    "code_verifier": code_verifier,  # Generate a code verifier (e.g., using secrets)
    "code": authorization_code,
    "redirect_uri": "https://auth.tesla.com/void/callback",
}

response = session.post(TOKEN_URL, data=data)
tokens = response.json()

access_token = tokens["access_token"]
refresh_token = tokens["refresh_token"]

# Copy these tokens and you should be able to successfully connect now
print(f"Access Token: {access_token}")
print(f"Refresh Token: {refresh_token}")
