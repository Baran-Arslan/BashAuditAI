import threading
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config.config_manager import ConfigManager
from core.llm_client import LLMClient
from core.analyzer import ShellAnalyzer

class App(tk.Tk):
    def __init__(self, cfg: ConfigManager):
        super().__init__()
        self.title("Shell Analyzer")
        self.geometry("900x650")
        self.cfg = cfg

        self._container = ttk.Frame(self)
        self._container.pack(fill="both", expand=True, padx=10, pady=10)

        self._show_config_frame()

    def _clear_container(self):
        for w in self._container.winfo_children():
            w.destroy()

    def _show_config_frame(self):
        self._clear_container()
        ConfigFrame(self._container, self.cfg, on_done=self._show_analyze_frame).pack(fill="both", expand=True)

    def _show_analyze_frame(self):
        self._clear_container()
        AnalyzeFrame(self._container, self.cfg).pack(fill="both", expand=True)

class ConfigFrame(ttk.Frame):
    def __init__(self, parent, cfg: ConfigManager, on_done):
        super().__init__(parent)
        self.cfg = cfg
        self.on_done = on_done

        ttk.Label(self, text="CONFIG", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))

        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=5)

        self.llm_url = tk.StringVar(value=self.cfg.get("llm_url"))
        self.llm_model = tk.StringVar(value=self.cfg.get("llm_model"))
        self.shellcheck_path = tk.StringVar(value=self.cfg.get("shellcheck_path"))

        self._row(frm, "LLM URL", self.llm_url)
        self._row(frm, "LLM Model", self.llm_model)
        self._row(frm, "ShellCheck Path (optional)", self.shellcheck_path)

        ttk.Button(self, text="Save & Continue", command=self._save_and_continue).pack(pady=15, anchor="e")

    def _row(self, parent, label, var):
        r = ttk.Frame(parent)
        r.pack(fill="x", pady=4)
        ttk.Label(r, text=label, width=24).pack(side="left")
        ttk.Entry(r, textvariable=var).pack(side="left", fill="x", expand=True)

    def _save_and_continue(self):
        self.cfg.update(
            llm_url=self.llm_url.get().strip(),
            llm_model=self.llm_model.get().strip(),
            shellcheck_path=self.shellcheck_path.get().strip()
        )
        messagebox.showinfo("Config", "Saved.")
        self.on_done()

class AnalyzeFrame(ttk.Frame):
    def __init__(self, parent, cfg: ConfigManager):
        super().__init__(parent)
        self.cfg = cfg

        ttk.Label(self, text="UI Mode - Analysis", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0,10))

        top = ttk.Frame(self)
        top.pack(fill="x")

        self.file_path = tk.StringVar(value="")
        ttk.Entry(top, textvariable=self.file_path).pack(side="left", fill="x", expand=True, padx=(0,6))
        ttk.Button(top, text="Select Script (.sh)", command=self._pick_file).pack(side="left", padx=6)
        ttk.Button(top, text="Analyze", command=self._start_analysis).pack(side="left")

        self.output = tk.Text(self, height=25)
        self.output.pack(fill="both", expand=True, pady=10)

        self.progress = ttk.Label(self, text="Ready.")
        self.progress.pack(anchor="w")

    def _pick_file(self):
        p = filedialog.askopenfilename(filetypes=[("Shell Script", "*.sh"), ("All files","*.*")])
        if p:
            self.file_path.set(p)

    def _append(self, text: str):
        self.output.insert("end", text + "\n")
        self.output.see("end")

    def _start_analysis(self):
        path = self.file_path.get().strip('"').strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Select a valid .sh file.")
            return

        self.output.delete("1.0", "end")
        self._append(f"[+] Analyzing: {path}\n")
        self.progress.config(text="Analysis running...")

        t = threading.Thread(target=self._do_analysis, args=(path,), daemon=True)
        t.start()

    def _do_analysis(self, path: str):
        try:
            llm = LLMClient(self.cfg.get("llm_url"), self.cfg.get("llm_model"))
            analyzer = ShellAnalyzer(llm, self.cfg.get("shellcheck_path") or None)

            result = analyzer.analyze_file(path)

            self._append("===== ShellCheck =====")
            self._append(result["shellcheck"] or "No issues found.")

            self._append("\n===== Suspicious Lines =====")
            if not result["suspicious"]:
                self._append("(None found)")
            else:
                for ln, code in result["suspicious"]:
                    self._append(f"[Line {ln}] {code}")

            self._append("\n===== LLM Analysis =====")
            if not result["llm"]:
                self._append("(No suspicious lines or LLM not run)")
            else:
                for item in result["llm"]:
                    block = f"\n[Line {item['line']}] {item['code']}\n{item['analysis']}\n" + "-"*40
                    self._append(block)

            self._append("\n[+] Tips: use set -euo pipefail, 'shellcheck <file>' and proper quoting")

        except Exception as e:
            self._append(f"Error: {e}")
        finally:
            self.progress.config(text="Done.")
