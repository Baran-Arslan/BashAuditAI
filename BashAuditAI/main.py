import subprocess
import os
import re
import httpx  # For sending HTTP requests to LM Studio

def shellcheck_scan(filepath):
    """Run ShellCheck on a file and return output."""
    result = subprocess.run(['shellcheck', '-f', 'gcc', filepath], capture_output=True, text=True)
    return result.stdout

def extract_suspicious_lines(filepath):
    """Extract lines with risky patterns (eval, user input, secrets)."""
    suspicious = []
    with open(filepath, 'r') as f:
        for i, line in enumerate(f, 1):
            # Simple check for common risky Bash constructs
            if re.search(r"(eval|read|source|\$[{\(]?[a-zA-Z_][a-zA-Z0-9_]*[}\)]?|secret|password)", line):
                suspicious.append((i, line.strip()))
    return suspicious

def prompt_llm(line_num, code_line, context=""):
    """
    Send a prompt to LM Studio's local LLM via OpenAI-compatible API.
    """
    prompt = f"""You are a security expert. Analyze this shell script line for security risks:
Line {line_num}: {code_line}
{f'Context:\n{context}' if context else ''}
Explain any vulnerabilities in plain English and suggest mitigations."""
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "meta-llama_-_meta-llama-3-8b-instruct",  # Model name from LM Studio
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.3
    }
    try:
        response = httpx.post(url, headers=headers, json=data, timeout=120)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error contacting local LLM: {e}"

def analyze_script(filepath):
    print(f"Running ShellCheck on {filepath}...\n")
    shellcheck_output = shellcheck_scan(filepath)
    print("ShellCheck Issues:\n", shellcheck_output or "No basic issues found.")

    print("\nScanning for suspicious lines...")
    suspects = extract_suspicious_lines(filepath)
    if not suspects:
        print("No suspicious lines found.")
        return

    print("\nLLM Security Analysis:")
    for num, line in suspects:
        context = ""  # Optionally, add code before/after for more context
        analysis = prompt_llm(num, line, context)
        print(f"\n[Line {num}] {line}\n{analysis}\n{'-'*40}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: py main.py <script.sh>")
        exit(1)
    analyze_script(sys.argv[1])