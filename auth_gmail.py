from google_auth_oauthlib.flow import InstalledAppFlow
from app.email_service import SCOPES, TOKEN_FILE, CREDENTIALS_FILE

import os

if not os.path.exists(CREDENTIALS_FILE):
    print(f"No se encuentra {CREDENTIALS_FILE}")
    exit(1)

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
creds = flow.run_local_server(port=0)

with open(TOKEN_FILE, "w") as f:
    f.write(creds.to_json())

print(f"Token guardado en {TOKEN_FILE}. Ya podés enviar correos.")
