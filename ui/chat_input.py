from textual.containers import Horizontal
from textual.widgets import Button, TextArea
from textual.widget import Widget
from textual.app import ComposeResult
# from ui.chat_view import ChatView
class ChatInput(Widget):
    
    """
    This controls covers the textarea and button portion of chat window 
    """
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
                # self.post_message(self.Submitted(self, text))
                textarea.text = ""  # Clear after sending
