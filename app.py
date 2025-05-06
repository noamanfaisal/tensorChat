from textual.app import App, ComposeResult
from textual.containers import  Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header
from ui.chat_input import ChatInput
from ui.chat_view import ChatView
from config import settings

class TweetScreen(Screen):
    
    
    def compose(self) -> ComposeResult:
        yield Header(id="header")
        yield Footer(id="footer")
        with Vertical(id="main_vertical"):
            yield ChatView(id="chat_view_widget")
            yield ChatInput()
    
    async def on_chat_input_submitted(self, message: ChatInput.Submitted) -> None:
        chat_view = self.query_one("#chat_view_widget", ChatView)
        await chat_view.send(message.message)
        
class LayoutApp(App):
    CSS_PATH = "ui/ui.tcss"
    # theme = "dracula"  # <- Set the theme here
    def on_ready(self) -> None:
        # self.set_theme(self.theme)
        self.push_screen(TweetScreen())
        
    def on_mount(self) -> None:
        self.theme = settings.theme
    
        
if __name__ == "__main__":
    app = LayoutApp()
    app.run()

