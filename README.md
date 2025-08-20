Tabii! İşte **GitHub’a direkt koyabileceğin, formatlı ve hazır `README.md`**:

````markdown
# Shell Analyzer TK

Shell Analyzer TK is a Python-based tool for auditing Bash and POSIX shell scripts.  
It provides both a **Graphical User Interface (GUI)** and a **Terminal mode** to detect suspicious lines and perform automated security analysis using ShellCheck and a local LLM.

---

## Features

- Analyze shell scripts for **security risks**.
- Detect **suspicious patterns** such as `eval`, `read`, and sensitive variables.
- Integrates with **ShellCheck** for static analysis.
- Integrates with a **local LLM** for advanced security insights.
- Supports both **UI (Tkinter)** and **Terminal** workflows.
- Fully **configurable** via config file or UI.

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/shell-analyzer-tk.git
cd shell-analyzer-tk
````

2. Install required Python packages:

```bash
py -m pip install -r requirements.txt
```

3. (Optional) Install **ShellCheck** and add it to your system PATH:
   [https://www.shellcheck.net](https://www.shellcheck.net)

4. Run your **local LLM server** (e.g., LM Studio) on `http://127.0.0.1:1234` or your preferred endpoint.

---

## Usage

### UI Mode

Start the GUI:

```bash
py main.py
```

1. On first run, configure LLM URL, model, and optional ShellCheck path.
2. Click **Go with UI**.
3. Select the shell script to analyze and click **Analyze**.
4. Results from ShellCheck, suspicious lines, and LLM analysis are displayed directly in the UI.

---

### Terminal Mode

Start terminal analysis:

```bash
py cli/cli_main.py <path-to-script.sh>
```

Example:

```bash
py cli/cli_main.py C:\Users\Baran\Desktop\BashAuditAI\Code\test.sh
```

* If config is missing, you will be prompted:

  * `Should use default config? (y/n)`
  * If `n`, you can manually enter LLM URL, model, and ShellCheck path.
* Results are printed directly in the terminal.

---

## Configuration

Configuration is stored in `config.json` by default. Example:

```json
{
  "llm_url": "http://127.0.0.1:1234/v1/chat/completions",
  "llm_model": "meta-llama-3-8b-instruct",
  "shellcheck_path": "C:\\tools\\shellcheck\\shellcheck.exe"
}
```

* You can edit the file manually or through the UI.
* `shellcheck_path` is optional if ShellCheck is in your PATH.

---

## Requirements

* Python 3.10+
* Tkinter (included in standard Python)
* `httpx` (`pip install httpx`)
* Local LLM server (LM Studio or similar)
* ShellCheck (optional but recommended)

---

## License

MIT License — feel free to use, modify, and redistribute.

