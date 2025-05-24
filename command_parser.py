import re
from typing import Optional, List, Dict, Union

class CommandParser:
    COMMAND_PATTERN = re.compile(r'^@(\w+)(?:\s+(.*))?')
    MSG_REF_PATTERN = re.compile(r'#(\d+)\b')
    TAG_PATTERN = re.compile(r'#(\w+)\b')

    def parse(self, text: str) -> Dict[str, Union[str, int, List[str], Dict]]:
        result = {
            "type": "text",      # default
            "raw": text,
            "command": None,
            "args": None,
            "msg_id": None,
            "tags": [],
            "filepath": None,    # For @load or @save_file
            "filename": None,    # For @save_file
        }

        stripped = text.strip()
        command_match = self.COMMAND_PATTERN.match(stripped)

        if command_match:
            cmd, args = command_match.groups()
            cmd_lower = cmd.lower()
            result["type"] = "command"
            result["command"] = cmd_lower
            result["args"] = args.strip() if args else ""

            if cmd_lower in {"new_topic", "connect", "load", "save_file", "save_data", "encrypt"}:
                result["msg_id"] = self._extract_msg_id(args)

                # @load path/to/file
                if cmd_lower == "load" and args:
                    result["filepath"] = args.strip()

                # @save_file path/to/file or filename and tags
                if cmd_lower == "save_file" and args:
                    split_args = args.split()
                    result["filepath"] = split_args[0] if split_args else None
                    result["tags"] = self._extract_tags(args)

                # @save_data or @encrypt with optional tags
                if cmd_lower in {"save_data", "encrypt"}:
                    result["tags"] = self._extract_tags(args)

        # If not a command, treat as prompt
        if not result["command"]:
            result["type"] = "prompt"

        return result

    def _extract_msg_id(self, arg_str: str) -> Optional[int]:
        match = self.MSG_REF_PATTERN.search(arg_str or "")
        return int(match.group(1)) if match else None

    def _extract_tags(self, arg_str: str) -> List[str]:
        return self.TAG_PATTERN.findall(arg_str or "")
