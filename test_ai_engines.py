import os
import requests

PROMPT = "Réponds simplement : TEST OK"

def report(name, response):
    print(f"\n===== {name} =====")
    print("HTTP:", response.status_code)

    try:
        data = response.json()
        print("Réponse:", str(data)[:1200])
    except Exception:
        print("Réponse:", response.text[:500])

    if response.ok:
        print("RESULTAT: OK")
    else:
        print("RESULTAT: ECHEC")


def test_gemini():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("GEMINI: CLE ABSENTE")
        return

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-2.5-flash:generateContent"
    )

    try:
        r = requests.post(
            url,
            params={"key": key},
            json={
                "contents": [{
                    "parts": [{"text": PROMPT}]
                }]
            },
            timeout=30
        )
        report("GEMINI", r)
    except Exception as e:
        print("GEMINI ERREUR:", str(e))


def test_groq():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("GROQ: CLE ABSENTE")
        return

    url = "https://api.groq.com/openai/v1/chat/completions"

    try:
        r = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "user", "content": PROMPT}
                ],
                "max_tokens": 50
            },
            timeout=30
        )
        report("GROQ", r)
    except Exception as e:
        print("GROQ ERREUR:", str(e))


def test_cloudflare():
    key = os.getenv("CLOUDFLARE_API_TOKEN")
    account = os.getenv("CLOUDFLARE_ACCOUNT_ID")

    if not key or not account:
        print("CLOUDFLARE: CONFIGURATION ABSENTE")
        return

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account}/ai/run/@cf/meta/llama-3.3-70b-instruct-fp8-fast"
    )

    try:
        r = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "messages": [
                    {"role": "user", "content": PROMPT}
                ],
                "max_tokens": 50
            },
            timeout=30
        )
        report("CLOUDFLARE", r)
    except Exception as e:
        print("CLOUDFLARE ERREUR:", str(e))


if __name__ == "__main__":
    print("DIAGNOSTIC DES MOTEURS IA")
    test_gemini()
    test_groq()
    test_cloudflare()
    print("\nDIAGNOSTIC TERMINE")