from textual.app import ComposeResult
from textual.widgets import Markdown
import random
from textual.containers import VerticalScroll
from processor import MessageProcessor
from textual import on, work


class Prompt(Markdown):
    pass

class Response(Markdown):
    pass

class ChatView(VerticalScroll):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # this lets `id=` and others pass through
        self.processor = MessageProcessor()  # persistent for lifetime of ChatView

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat-view")

    @work(thread=True)
    def _run_in_thread(self, message: str, response_widget: Response) -> None:
        response = self.processor.process(message)
        chunks = self.processor.process(message)  # should yield strings
        full_response = ""

        for chunk in chunks:
            full_response += chunk
            self.app.call_from_thread(response_widget.update, full_response)
    
    async def send(self, message: str):
        chat_view = self.query_one("#chat-view")
        await chat_view.mount(Prompt(message))
        response_widget = Response("")  # Empty for now
        await chat_view.mount(response_widget)
        self._run_in_thread(message, response_widget)

    # async def send(self, message):
    #     chat_view = self.query_one("#chat-view")
    #     await chat_view.mount(Prompt(message))
    #     # response = self.get_response()
    #     response = MessageProcessor().process(message)
    #     await chat_view.mount(Response(response))
