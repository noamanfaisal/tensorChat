✅ tensorChat GitHub Task List

🔌 Model Integration & Prompt System
	•	Integrate Langchain as the backend for context and memory management
	•	Add support for local models (Ollama, Code LLaMA, Mistral, Gemma)
	•	Add support for remote API models (OpenAI, Claude, Anthropic)
	•	Implement streaming token support for supported models
	•	Build PromptProcessorFactory to load prompt templates per model from settings.ini

⸻

💬 Chat & Context Management
	•	Implement topic-based chat sessions with numbered messages
	•	Create @add_context file.md command to inject file into context
	•	Create @add_context topic:45 to reuse past chat thread as context
	•	Implement @grab https://example.com to fetch and convert webpage into context
	•	Implement @grab_output "df -h" to run a command and use output as context
	•	Implement @load file.txt to directly inject file into active prompt
	•	Enable dynamic addition/removal of context items at runtime
	•	Merge multiple context types (file + chat + web + shell output) into one prompt window

⸻

📋 Message Utilities & Execution
	•	Implement @copy <message_id> to copy full message content
	•	Implement @copycode <message_id> to copy only code blocks
	•	Implement @run <message_id> to execute a message’s output as a command
	•	Support @grab_output "command" > filename.txt to save output to file

⸻

🧠 AI Features
	•	Implement @summary to summarize the current topic thread
	•	Implement @summarize topic:xyz to summarize a selected topic
	•	Ensure context windows are memory-efficient across merged sources
	•	Allow Langchain context TTL (e.g., auto-expiry after 30 minutes)

⸻

☁️ Cloud Sync & Storage
	•	Support saving/loading user config and session data to/from Dropbox
	•	Support saving/loading user config and session data to/from Amazon S3
	•	Support saving/loading user config and session data to/from Google Drive
	•	Implement periodic auto-backup to selected cloud storage
	•	Add cross-device settings loader using remote config pull

⸻

⚙️ Settings & Extensibility
	•	Use INI file format for configuration at ~/.config/chatui/settings.ini
	•	Support model-specific overrides in [model_name] sections
	•	Make ChatState, PromptProcessor, and CommandParser fully pluggable
	•	Add plugin system for custom commands and transformers