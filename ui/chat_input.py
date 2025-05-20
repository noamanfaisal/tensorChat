from chat_state.factory import ChatStateFactory
from textual.containers import Horizontal
from textual.widgets import Button, TextArea
from textual.widget import Widget
from textual.app import ComposeResult
from copy import deepcopy
from textual.message import Message
from textual import events
from config import settings


class SubmitText(Message):
    def __init__(self, sender: Widget, text: str) -> None:
        self.text = text
        super().__init__()

class ChatTextArea(TextArea):
    async def on_key(self, event: events.Key) -> None:
        if event.key == settings.submit_key:
            text = self.text.strip()
            if text:
                self.post_message(SubmitText(self, text))
                self.text = ""
                event.prevent_default()
        # else:
        #     await super().on_key(event)
           
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
    
    def on_mount(self):
        self.query_one("#chatinput_textarea").focus()
        
    def compose(self) -> ComposeResult:
        """
        this is compose method of control 
        """
        # yield Horizontal()
        with Horizontal():
            yield ChatTextArea(id="chatinput_textarea")
            yield Button("Send", id="chatinput_button")
 
              
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "chatinput_button":
            textarea = self.query_one("#chatinput_textarea", ChatTextArea)
            text = textarea.text.strip()
            if text:
                text_to_pass = deepcopy(textarea.text)
                self.post_message(self.Submitted(self, text_to_pass))
                # self.post_message(self.Submitted(self, text))
                textarea.text = ""  # Clear after sending
                
    def on_submit_text(self, message: SubmitText) -> None:
        self.post_message(self.Submitted(self, message.text))
