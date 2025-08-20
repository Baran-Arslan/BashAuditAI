import json
import os

class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path
        self.config = {}

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.create_default()
        return self.config

    def create_default(self):
        self.config = {
            "llm_url": "http://127.0.0.1:1234/v1/chat/completions",
            "llm_model": "meta-llama-3-8b-instruct",
            "shellcheck_path": "",
            "default_scan_dir": "."
        }
        self.save()

    def get(self, key, default=None):
        return self.config.get(key, default)

    def update(self, **kwargs):
        self.config.update(kwargs)
        self.save()

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
