import requests

def check_email_in_database(email: str) -> bool:
    api_url = "https://aialpha.ngrok.io/check-email"
    try:
        response = requests.get(api_url, params={"email": email})
        response.raise_for_status()  # Esto generará una excepción si el código de estado no es 2xx
    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        # Aquí puedes manejar el error, por ejemplo, registrándolo o notificándolo
        return False
    
    try:
        data = response.json()
        return data.get("exists", False)
    except ValueError:
        print("Error parsing the response JSON")
        return False
