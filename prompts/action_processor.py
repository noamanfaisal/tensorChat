from pathlib import Path

class PromptActionHandler:
    def __init__(self):
        pass

    def process(self, parsed_command: dict) -> dict:
        """
        Processes actions from parsed command.
        Supports multiple @load commands.

        Returns:
        {
          "loaded_files": [{"path":..., "content":...}, ...],
          "errors": ["error1", "error2"]
        }
        """
        result = {
            "loaded_files": [],
            "errors": []
        }

        # Handle @load actions
        filepaths = parsed_command.get("filepaths", [])
        for filepath in filepaths:
            try:
                content = Path(filepath).read_text(encoding='utf-8')
                result["loaded_files"].append({
                    "path": filepath,
                    "content": content
                })
            except FileNotFoundError:
                result["errors"].append(f"File not found: {filepath}")
            except Exception as e:
                result["errors"].append(f"Error reading {filepath}: {str(e)}")

        return result
