from textual.app import ComposeResult
from textual.widgets import Markdown
import random
from textual.containers import VerticalScroll
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
        response = self.get_response()
        await chat_view.mount(Response(response))
        
    def get_response(self):
        subjects = ["The cat", "A dog", "My friend", "An alien", "The teacher"]
        verbs = ["eats", "plays with", "jumps over", "writes", "dreams of"]
        objects = ["a ball", "homework", "the moon", "a sandwich", "a secret"]
        return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)}."
