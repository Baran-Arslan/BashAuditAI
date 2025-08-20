import subprocess
import shutil
import re
from typing import List, Dict, Tuple

from .llm_client import LLMClient
from .prompt_builder import build_security_prompt

class ShellAnalyzer:
    def __init__(self, llm: LLMClient, shellcheck_path: str | None = None):
        self.llm = llm
        self.shellcheck_path = shellcheck_path or ""

    def _find_shellcheck(self) -> str | None:
        if self.shellcheck_path:
            return self.shellcheck_path
        return shutil.which("shellcheck")

    def run_shellcheck(self, filepath: str) -> str:
        exe = self._find_shellcheck()
        if not exe:
            return "(ShellCheck bulunamadı — yalnizca regex taramasi yapilacak.)"
        try:
            completed = subprocess.run([exe, "-f", "gcc", filepath], capture_output=True, text=True, check=False)
            return completed.stdout or "(ShellCheck: ciddi bir sorun bulunamadı.)"
        except Exception as e:
            return f"(ShellCheck calistirilamadi: {e})"

    def extract_suspicious_lines(self, filepath: str) -> List[Tuple[int, str]]:
        suspicious = []
        pattern = re.compile(r"(?:\beval\b|\bread\b|\bsource\b|\$\{?[A-Za-z_][A-Za-z0-9_]*\}?|\bsecret\b|\bpassword\b)")
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    if pattern.search(line):
                        suspicious.append((i, line.rstrip()))
        except Exception as e:
            suspicious.append((0, f"[Dosya okunamadı: {e}]"))
        return suspicious

    def _read_context(self, filepath: str, line_num: int, k: int = 3) -> str:
        lines: List[str] = []
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                all_lines = f.readlines()
            start = max(0, line_num - k - 1)
            end = min(len(all_lines), line_num + k)
            for idx in range(start, end):
                prefix = ">> " if (idx + 1) == line_num else "   "
                lines.append(f"{prefix}{idx+1:>4}: {all_lines[idx].rstrip()}")
        except Exception as e:
            return f"[Context okunamadı: {e}]"
        return "\n".join(lines)

    def analyze_with_llm(self, filepath: str, suspects: List[Tuple[int, str]]) -> List[Dict]:
        results = []
        for (num, line) in suspects:
            ctx = self._read_context(filepath, num, k=3) if num > 0 else ""
            prompt = build_security_prompt(num, line, ctx)
            analysis = self.llm.analyze(prompt)
            results.append({"line": num, "code": line, "analysis": analysis})
        return results

    def analyze_file(self, filepath: str) -> Dict:
        shellcheck_output = self.run_shellcheck(filepath)
        suspects = self.extract_suspicious_lines(filepath)
        llm_results = self.analyze_with_llm(filepath, suspects) if suspects else []
        return {
            "shellcheck": shellcheck_output,
            "suspicious": suspects,
            "llm": llm_results,
        }
