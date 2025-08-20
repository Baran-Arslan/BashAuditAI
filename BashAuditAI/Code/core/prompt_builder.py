def build_security_prompt(line_num, code_line, context=""):
        context_block = f"\nContext:\n{context}" if context else ""
        prompt = f"""
Role: You are a senior security auditor specialized in Bash and POSIX shell scripts.
Task: Analyze the given code line for security issues and shell best practices.
{context_block}

[Target]
Line {line_num}: {code_line}

Constraints:
- Be precise and practical.
- Prefer POSIX-safe recommendations.
- If relevant, mention ShellCheck rule IDs (e.g., SC2086).
- Assume this might run on Linux/macOS CI.

Output Format:
[Risks] - bullet list of concrete risks
[Impact] - what happens if exploited
[Mitigation] - exact changes or commands (show safe code snippet)

Style/Tone:
- Professional, concise, direct.
- No fluff.
"""
        return prompt.strip()
