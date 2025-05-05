from textual.containers import Horizontal
from textual.widgets import Button, TextArea
from textual.widget import Widget
from textual.app import ComposeResult
from copy import deepcopy
from textual.message import Message
# from ui.chat_view import ChatView
class ChatInput(Widget):
    
    """
    This controls covers the textarea and button portion of chat window 
    """
    class Submitted(Message):
        """
        this is class to notify main class
        """
        
        def __init__(self, sender: Widget, message: str) -> None:
            self.message = message
            super().__init__()
    
    def compose(self) -> ComposeResult:
        """
        this is compose method of control 
        """
        # yield Horizontal()
        with Horizontal():
            yield TextArea(id="chatinput_textarea")
            yield Button("Send", id="chatinput_button")
            
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "chatinput_button":
            textarea = self.query_one("#chatinput_textarea", TextArea)
            text = textarea.text.strip()
            if text:
                text_to_pass = deepcopy(textarea.text)
                self.post_message(self.Submitted(self, text_to_pass))
                # self.post_message(self.Submitted(self, text))
                textarea.text = ""  # Clear after sending
                
