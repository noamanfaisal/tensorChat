templates = {
    "connected": lambda model_name: f"\n# Model [{model_name}] has been connected\n\n",
    "not_connected": lambda model_name, lst: f"\n[{model_name}] model name must be in model list {lst}\n\n",
    "load_topic": lambda session_id: f"\n# Topic [{session_id}] has been loaded\n\n",
    "new_topic": lambda new_topic_id: f"\n#New topic [{new_topic_id}] initialized\n\n",
    "list_topics": lambda i, name, model, created, topic_id: f"{i}. **{name}** — `{model}` @ `{created}`    - ID: `{topic_id}`\n",
    "no_topics_found": lambda: "\n\nNo topics found\n",
    "unrecognized": lambda: "\n\nUnrecognized input\n",
    "url_failed": lambda url: f"\n\nFailed to fetch content from {url}, the server might be down or the URL is invalid\n",
    "url_no_text": lambda url: f"\n\nFetched {url}, but could not parse readable text.",
    "files_not_found": lambda files: f"\n\nFile {files} not found\n"
}