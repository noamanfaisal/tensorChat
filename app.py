from processor import MessageProcessor
from streamer import StreamdownStreamer
import time
processor = MessageProcessor()

while True:
    try:
        user_input = input("> ").strip()
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
