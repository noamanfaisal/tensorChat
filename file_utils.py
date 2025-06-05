import os

def inject_files_into_text(text: str, filepaths: list[str], base_path: str = ".") -> str:
    """
    Append file contents into user input, used before passing into PromptTemplate.
    """
    if not filepaths:
        return text

    parts = [text]
    for path in filepaths:
        full_path = os.path.join(base_path, path)
        try:
            with open(full_path, "r") as f:
                content = f.read()
                parts.append(f"\n[File: {path}]\n{content}")
        except Exception as e:
            parts.append(f"\n[Error loading {path}]: {e}")

    return "\n".join(parts)

