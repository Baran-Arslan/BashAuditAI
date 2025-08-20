import httpx

class LLMClient:
    def __init__(self, url: str, model: str, timeout_sec: int = 120):
        self.url = url
        self.model = model
        self.timeout_sec = timeout_sec

    def analyze(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.2,
        }
        try:
            resp = httpx.post(self.url, headers=headers, json=data, timeout=self.timeout_sec)
            resp.raise_for_status()
            js = resp.json()
            return js["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"LLM error: {e}"
