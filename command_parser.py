import re
from typing import Optional, List, Dict, Union


class CommandParser:
    COMMAND_PATTERN = re.compile(r'^@(\w+)(?:\s+(.*))?')
    FILE_PATTERN = re.compile(r'\^\^\^(.+?)\^\^\^')
    MSG_REF_PATTERN = re.compile(r'#(\d+)\b')
    TAG_PATTERN = re.compile(r'#(\w+)\b')

    def parse(self, text: str) -> Dict[str, Union[str, int, List[str], Dict]]:
        result = {
            "type": "text",      # default: plain prompt
            "raw": text,
            "command": None,
            "args": None,
            "msg_id": None,
            "tags": [],
            "file_refs": [],
            "url_refs": [],
        }

        stripped = text.strip()
        command_match = self.COMMAND_PATTERN.match(stripped)
        file_refs = self.FILE_PATTERN.findall(stripped)

        # Parse command-based input
        if command_match:
            cmd, args = command_match.groups()
            result["type"] = "command"
            result["command"] = cmd.lower()
            result["args"] = args.strip() if args else ""

            # Optional values
            if cmd in {"write_to", "run_as_command", "save_as_file"}:
                result["msg_id"] = self._extract_msg_id(args)

            if cmd in {"save", "save_file", "encrypt_save_my_password"}:
                result["tags"] = self._extract_tags(args)
            
            if cmd == "save_file":
                result["tags"] = self._extract_tags(args)
                result["filename"] = args.split()[0] if args else None

        # Parse file or URL references
        result["file_refs"] = [f for f in file_refs if not f.startswith("http")]
        result["url_refs"] = [f for f in file_refs if f.startswith("http")]

        # If not command and has no file/url reference, treat as a model prompt
        if not result["command"] and not result["file_refs"] and not result["url_refs"]:
            result["type"] = "prompt"  # changed from "text"

        return result

    def _extract_msg_id(self, arg_str: str) -> Optional[int]:
        match = self.MSG_REF_PATTERN.search(arg_str or "")
        return int(match.group(1)) if match else None

    def _extract_tags(self, arg_str: str) -> List[str]:
        return self.TAG_PATTERN.findall(arg_str or "")

