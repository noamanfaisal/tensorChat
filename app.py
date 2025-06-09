from processor import MessageProcessor
from streamer import StreamdownStreamer
from chat_completion import SmartCompleter
from prompt_toolkit import prompt
import os
import time

processor = MessageProcessor()
completer = SmartCompleter()

while True:
    try:
        user_input = prompt("> ", completer=completer, complete_while_typing=True).strip()
        if user_input.lower() in ("exit", "quit", "exit()", "Exit", "Exit()", "quit()"):
            break
        if user_input == "" or user_input == None:
            continue

        chunks = processor.process(user_input)  # Must be a generator or string
        streamer = StreamdownStreamer()
        breakpoint()
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
