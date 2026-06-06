def sanitize_text(text: str) -> str:
    return (text or "").strip()

def detect_language(text: str) -> str:
    txt = text.lower()
    if "public static void main" in txt or "system.out.println" in txt:
        return "java"
    if "#include" in txt or "std::" in txt or "cout" in txt:
        return "cpp"
    if "function " in txt or "console.log" in txt or "let " in txt or "const " in txt or "=>" in txt:
        return "javascript"
    if "def " in txt or "import " in txt or "print(" in txt:
        return "python"
    return "python"

def format_code_block(language: str, code: str) -> str:
    return f"```{language}\n{code.strip()}\n```"