from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings

# from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import FormattedTextToolbar

# from pygments.lexers.python import PythonLexer

import subprocess
import tempfile


kb = KeyBindings()


@kb.add("c-q")
@kb.add("c-d")
@kb.add("c-c")
@kb.add("c-g")
def exit_(event):
    event.app.exit()


class App:
    toolbar_style = Style([("bgcolor", "reverse"), ("color", "reverse")])
    error_text = ""
    output_text = ""
    script = ""

    def __init__(self, inpipe):
        self.inpipe = inpipe
        self.tempfile = tempfile.NamedTemporaryFile(mode="w", delete=True)
        self.initialize_nodes()

        root = VSplit(
            [
                # Input buffer and status line
                HSplit(
                    [
                        self.first_line,
                        Window(
                            content=BufferControl(
                                buffer=self.input_buffer,
                                # This lexer is disabled for now because
                                # I don't want to mess with colourschemes
                                # lexer=PygmentsLexer(PythonLexer),
                            )
                        ),
                        self.error_output,
                    ],
                    width=Dimension(),
                ),
                Window(width=1, char="|"),
                # Output display area
                Window(ignore_content_width=True, content=self.output, wrap_lines=True),
            ],
            width=Dimension(),
        )

        layout = Layout(root)

        self.app = Application(layout=layout, key_bindings=kb, full_screen=True)

    def initialize_nodes(self):
        self.first_line = FormattedTextToolbar(
            self.get_first_line_text(), style="#ffffff bg:#444444"
        )
        self.input_buffer = Buffer(on_text_changed=self.on_change)
        self.output = FormattedTextControl(text=self.get_output_text)
        self.error_output = FormattedTextToolbar(
            self.get_error_text, style="#ffffff bg:#444444"
        )

    def on_change(self, b):

        self.tempfile.seek(0)
        self.tempfile.truncate()
        self.tempfile.write("inpipe = {}\n{}".format(self.inpipe, b.text))
        self.tempfile.flush()
        self.execute(self.tempfile.name)

    def execute(self, script):
        try:
            proc = subprocess.run(["python", script], capture_output=True, timeout=5)
            self.write(proc.stderr, True)
            self.write(proc.stdout)
        except subprocess.TimeoutExpired:
            self.tempfile.truncate(0)
            self.write(b"Run time exceeded 5s and was killed", True)

    def write(self, msg, error=False):
        msg = msg.decode("utf-8")
        if error:
            self.error_text = str(msg)
        else:
            self.output_text = str(msg)

    def get_first_line_text(self):
        full_text = str(self.inpipe)

        if len(full_text) > 28:
            full_text = full_text[:25] + "..."

        return f"inpipe = {full_text}"

    def get_error_text(self):
        return self.error_text

    def get_output_text(self):
        return self.output_text

    def start(self):
        with patch_stdout(self.app):
            self.app.run()

        return self.tempfile
