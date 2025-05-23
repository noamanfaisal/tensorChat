from processor import MessageProcessor
from streamer import StreamdownStreamer
from chat_completion import SmartCompleter
from prompt_toolkit import prompt

import time
processor = MessageProcessor()
completer = SmartCompleter()
while True:
    try:
        user_input = prompt("> ",completer=completer, complete_while_typing=True).strip()
        if user_input.lower() in ("exit", "quit"):
            break

        chunks = processor.process(user_input)  # Must be a generator
        streamer = StreamdownStreamer()

        for chunk in chunks:
            streamer.write_chunk(chunk)
            # time.sleep(0.05)  # simulate streaming

        streamer.close()

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        try:
            streamer.cancel()
        except:
            pass
