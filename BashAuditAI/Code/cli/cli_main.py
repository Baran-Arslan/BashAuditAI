import sys
import os
import subprocess
import json

# Proje root klasörünü Python path'e ekle
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from config.config_manager import ConfigManager
from core.llm_client import LLMClient
from core.analyzer import ShellAnalyzer

def get_terminal_input(prompt_text, default=None):
    while True:
        val = input(prompt_text)
        if val.strip():
            return val.strip()
        elif default is not None:
            return default

def main():
    if len(sys.argv) < 2:
        print("Usage: py cli_main.py <script.sh>")
        sys.exit(1)

    script_path = sys.argv[1]
    if not os.path.exists(script_path):
        print(f"File does not exist: {script_path}")
        sys.exit(1)

    cfg = ConfigManager()
    cfg.load()  # Config yükle, yoksa create_default çalışıyor

    # Eğer config dosyası yoksa kullanıcıya sor
    if not os.path.exists(cfg.path):
        choice = get_terminal_input("Should use default config? (y/n): ").lower()
        if choice == "y":
            cfg.create_default()
        else:
            llm_url = get_terminal_input("Enter LLM URL: ")
            llm_model = get_terminal_input("Enter LLM model: ")
            shellcheck_path = get_terminal_input("Enter ShellCheck path (leave blank if not used): ", default="")
            cfg.update(
                llm_url=llm_url,
                llm_model=llm_model,
                shellcheck_path=shellcheck_path
            )

    llm = LLMClient(cfg.get("llm_url"), cfg.get("llm_model"))
    analyzer = ShellAnalyzer(llm, cfg.get("shellcheck_path") or None)

    print(f"[+] Analyzing: {script_path}\n")
    result = analyzer.analyze_file(script_path)

    print("===== ShellCheck =====")
    print(result["shellcheck"] or "No issues found.")

    print("\n===== Suspicious Lines =====")
    if not result["suspicious"]:
        print("(None found)")
    else:
        for ln, code in result["suspicious"]:
            print(f"[Line {ln}] {code}")

    print("\n===== LLM Analysis =====")
    if not result["llm"]:
        print("(No suspicious lines or LLM not run)")
    else:
        for item in result["llm"]:
            print(f"\n[Line {item['line']}] {item['code']}\n{item['analysis']}")
            print("-"*40)

    print("\n[+] Tips: use set -euo pipefail, 'shellcheck <file>' and proper quoting")

if __name__ == "__main__":
    main()
