from __future__ import annotations
import sys
import pytermgui as ptg
import subprocess
import os
 
from scripts.manage_profiles import create_profile


OUTPUT = {'action': 'REPEAT'}

PALETTE_LIGHT = "#FCBA03"
PALETTE_MID = "#8C6701"
PALETTE_DARK = "#4D4940"
PALETTE_DARKER = "#242321"


def submit_build(manager: ptg.WindowManager, window: ptg.Window) -> None:
    n = 0
    OUTPUT['action'] = 'BUILD'
    for widget in window:
        if isinstance(widget, ptg.InputField):
            OUTPUT[str(n)] = widget.value
            n = n + 1
            continue

        if isinstance(widget, ptg.Container):
            OUTPUT[str(n)] = "Container"
            n = n + 1
            for inner in widget:
                if isinstance(inner, ptg.InputField):
                    OUTPUT[str(n)] = inner.value
                    n = n + 1

                if isinstance(inner, ptg.Splitter):
                    OUTPUT[str(n)] = "Splitter"
                    n = n + 1
                    for in_inner in inner:
                        if isinstance(in_inner, ptg.InputField):
                            OUTPUT[str(n)] = in_inner.value
                            n = n + 1

                        if isinstance(in_inner, ptg.Toggle):
                            OUTPUT[str(n)] = in_inner.checked
                            n = n + 1

    manager.stop()

    # subprocess.Popen('./sandbox/build.sh', shell=True)
    # os.system('./sandbox/build.sh')

    # main()


def _create_aliases() -> None:

    ptg.tim.alias("app.text", "#cfc7b0")

    ptg.tim.alias("app.header", f"bold @{PALETTE_MID} #d9d2bd")
    ptg.tim.alias("app.header.fill", f"@{PALETTE_LIGHT}")

    ptg.tim.alias("app.title", f"bold {PALETTE_LIGHT}")
    ptg.tim.alias("app.button.label", f"bold @{PALETTE_DARK} app.text")
    ptg.tim.alias("app.button.highlight", "inverse app.button.label")

    ptg.tim.alias("app.footer", f"@{PALETTE_DARKER}")


def _configure_widgets() -> None:

    ptg.boxes.SINGLE.set_chars_of(ptg.Window)
    ptg.boxes.SINGLE.set_chars_of(ptg.Container)

    ptg.Button.styles.label = "app.button.label"
    ptg.Button.styles.highlight = "app.button.highlight"

    ptg.Slider.styles.filled__cursor = PALETTE_MID
    ptg.Slider.styles.filled_selected = PALETTE_LIGHT

    ptg.Label.styles.value = "app.text"

    ptg.Window.styles.border__corner = "#C2B280"
    ptg.Container.styles.border__corner = PALETTE_DARK

    ptg.Splitter.set_char("separator", "")


def _define_layout() -> ptg.Layout:

    layout = ptg.Layout()

    layout.add_slot("Header", height=3)
    layout.add_break()

    layout.add_slot("Body")
    layout.add_break()

    layout.add_slot("Footer", height=3)

    return layout


def _confirm_exit(manager: ptg.WindowManager) -> None:
    
    OUTPUT['action'] = 'EXIT'
    manager.stop()


def _confirm_quit(manager: ptg.WindowManager) -> None:

    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                # ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("Yes", lambda *_: _confirm_exit(manager)),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)


def _generate_profile(manager: ptg.WindowManager) -> None:

    modal = ptg.Window(
        "[app.title]Generate Profile",
        "",
        ptg.Container(
            ptg.InputField("", prompt="Profile Name: "),
        static_width=80,
        ),
        ptg.Container(
            "[app.text]Seleccionar tipo de maquina",
        ),
        ptg.Container(
            ptg.InputField("", prompt="Timezone: "),
        ),
        ptg.Container(
            "",
            ptg.Splitter(
                ptg.Label("  CPU         "), 
                ptg.Toggle(("False", "True")),
            ),
            ptg.Splitter(
                ptg.Label("  GPU         "), 
                ptg.Toggle(("False", "True")),
            ),
            ptg.Splitter(
                ptg.Label("  Memoria     "), 
                ptg.Toggle(("False", "True")),
            ),
        static_width=30,
        ),
        "",
        ptg.Container(
            ptg.Splitter(
                ["Build", lambda *_: submit_build(manager, modal)],
                ptg.Button("Cancel", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)


def _run_profile(manager: ptg.WindowManager) -> None:
    """Creates an "Are you sure you want to quit" modal window"""

    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)

def main() -> None:
    """Runs the application."""

    _create_aliases()
    _configure_widgets()

    with ptg.WindowManager() as manager:
        manager.layout = _define_layout()

        header = ptg.Window(
            "[app.header]  ╭ᥥ╮(´• ᴗ •`˵)╭ᥥ╮  ",
            box="EMPTY",
            is_persistant=True,
        )
        header.styles.fill = "app.header.fill"
        manager.add(header)

        footer = ptg.Window(
            ptg.Button("Quit", lambda *_: _confirm_quit(manager)),
            box="EMPTY",
        )
        footer.styles.fill = "app.footer"
        manager.add(footer, assign="footer")

        manager.add(
            ptg.Window(
                "[app.title]Middle Fingerprint",
                "",
                ptg.Container(
                    ptg.Container(
                        ptg.Button("Generate Profile", lambda *_: _generate_profile(manager)),
                    ),
                    ptg.Container(
                        ptg.Button("Run Profile", lambda *_: _run_profile(manager)),
                    ),
                    static_width=60,
                ),
                vertical_align=ptg.VerticalAlignment.CENTER,
                overflow=ptg.Overflow.SCROLL,
            ),
            assign="body",
        )

    ptg.tim.print(f"[{PALETTE_LIGHT}]{OUTPUT}")
    # ptg.tim.print(f"[{PALETTE_DARK}]{BUILD}")
    ptg.tim.print(f"[{PALETTE_LIGHT}]Goodbye!")

    if (OUTPUT['action'] == 'BUILD'):
        profile_name = OUTPUT['1']
        timezone = OUTPUT['4']
        CPU = OUTPUT['7']
        GPU = OUTPUT['9']
        Memoria = OUTPUT['11']
        create_profile(profile_name)
        # os.system('./scripts/build.sh')
    if (OUTPUT['action'] == 'RUN'):
        os.system('./sandbox/run.sh')


if __name__ == "__main__":
    while (OUTPUT['action'] != 'EXIT'):
        main()


# {'action': 'BUILD', '0': 'Container', '1': 'Nombre', '2': 'Container', '3': 'Container', '4': 'Timezone', '5': 
#   'Container', '6': 'Splitter', '7': True, '8': 'Splitter', '9': False, '10': 'Splitter', '11': True, '12': 'Container', '13': 'Splitter'}

