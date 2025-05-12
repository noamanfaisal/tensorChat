from textual.app import ComposeResult
from textual.widgets import Markdown
import random
from texitual.containers import VerticalScroll
from ..processor import MessageProcessor

class Prompt(Markdown):
    pass

class Response(Markdown):
    pass

class ChatView(VerticalScroll):
    """
    This includes all chat view, which will be visible to user for 
    response and request
        
    """
    
    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="chat-view")
    
    async def send(self, message):
        chat_view = self.query_one("#chat-view")
        await chat_view.mount(Prompt(message))
        response = await MessageProcessor().process(message)
        await chat_view.mount(Response(response))
