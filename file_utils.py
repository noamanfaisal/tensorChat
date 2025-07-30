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

def check_filepaths(filepaths: list[str]) -> list[str]:

    validities = [os.path.exists(filepath) for filepath in filepaths]
    if sum(validities) == len(validities):
        return []
    else:
        return [item[1] for item in zip(validities, filepaths) if not(item[0])]

def inject_website_into_text(text: str, website_text: str) -> str:
    return f'{text}\n{website_text}'




