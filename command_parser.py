import re
from typing import Optional, List, Dict, Union

class CommandParser:
    COMMAND_PATTERN = re.compile(r'^@(\w+)(?:\s+(.*))?')
    MSG_REF_PATTERN = re.compile(r'#(\d+)\b')
    TAG_PATTERN = re.compile(r'#(\w+)\b')
    LOAD_PATTERN = re.compile(r'@load\s+([^\s#]+)')
    CONTEXT_PATTERN = re.compile(r'@context\s+([^\s#]+)')
    GRAB_PATTERN = re.compile((r'@grab\s+([^\s#]+)'))

    def parse(self, text: str) -> Dict[str, Union[str, int, List[str], Dict]]:
        result = {
            "type": "text",
            "raw": text,
            "command": None,
            "args": None,
            "msg_id": None,
            "tags": [],
            "filepaths": [],        # Updated: List of @load paths
            "filename": None,
            "context_value": None,
            "urls": []
        }

        stripped = text.strip()
        command_match = self.COMMAND_PATTERN.match(stripped)

        if command_match:
            cmd, args = command_match.groups()
            cmd_lower = cmd.lower()
            result["type"] = "command"
            result["command"] = cmd_lower
            result["args"] = args.strip() if args else ""

            if cmd_lower in {"new_topic", "connect", "load", "save_file", 
                                                "save_data", "encrypt", "context", "list_topics", "load_topic", "grab"}:
                result["msg_id"] = self._extract_msg_id(args)
                result["tags"] = self._extract_tags(args)

                cleaned_args = re.sub(self.MSG_REF_PATTERN, '', args or "")
                cleaned_args = re.sub(self.TAG_PATTERN, '', cleaned_args).strip()

                if cmd_lower in {"load", "save_file", "context"} and cleaned_args:
                    split_args = cleaned_args.split()
                    result["filepaths"].append(split_args[0])  # Append @load path

                elif cmd_lower == "grab" and cleaned_args:
                    # Capture the URL argument for @grab
                    split_args = cleaned_args.split()
                    print(split_args[0])
                    result["urls"].append(split_args[0])


        # Extract ALL @load paths from the entire text
        load_matches = self.LOAD_PATTERN.findall(text)
        result["filepaths"].extend(load_matches)

        grab_matches = self.GRAB_PATTERN.findall(text)
        result["urls"].extend(grab_matches)

        # Extract @context (first occurrence only for now)
        if not result["context_value"]:
            context_match = self.CONTEXT_PATTERN.search(text)
            if context_match:
                result["context_value"] = context_match.group(1)

        # If no command was detected, mark as prompt
        if not result["command"]:
            result["type"] = "prompt"

        return result

    def _extract_msg_id(self, arg_str: str) -> Optional[int]:
        match = self.MSG_REF_PATTERN.search(arg_str or "")
        return int(match.group(1)) if match else None

    def _extract_tags(self, arg_str: str) -> List[str]:
        return self.TAG_PATTERN.findall(arg_str or "")
