from textual.app import App, ComposeResult
from textual.containers import  Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header
from ui.chat_input import ChatInput
from ui.chat_view import ChatView


class TweetScreen(Screen):
    
    def compose(self) -> ComposeResult:
        yield Header(id="header")
        yield Footer(id="footer")
        with Vertical(id="main_vertical"):
            yield ChatView(id="chat_view_widget")
            yield ChatInput()

class LayoutApp(App):
    CSS_PATH = "ui/ui.tcss"
    def on_ready(self) -> None:
        self.push_screen(TweetScreen())

if __name__ == "__main__":
    app = LayoutApp()
    app.run()

