from __future__ import annotations
import sys
from types import TracebackType
import pytermgui as ptg
import subprocess
import os
import time
 
from scripts.manage_profiles import create_profile
from scripts.manage_profiles import get_profiles
# from scripts.manage_profiles import run_profile


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
    ptg.Button.set_char("delimiter", [""] * 2)

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


def create_button(caption):
    return ptg.Button(caption, lambda *_, c=caption: create_profile(c), centered=True)


def _run_profile(manager: ptg.WindowManager) -> None:


    container = ptg.Container(static_width=50)

    modal = ptg.Window(
        "[app.title]Select profile",
        "",
    ).center()
    
    profiles = get_profiles()
    for caption in profiles:
        button = create_button(caption)
        container.lazy_add(button)

    # print(f"{container.get_lines()}")
    # time.sleep(5)
    
    modal.lazy_add(container)

    container_cancel = ptg.Container(
            ptg.Button("Cancel", lambda *_: modal.close()),
        )

    modal.lazy_add(container_cancel)

    manager.add(modal)


def _generate_profile(manager: ptg.WindowManager) -> None:

    modal = ptg.Window(
        # "[app.title]Generate Profile",
        # "",
        ptg.Container(
            ptg.InputField("", prompt="Profile Name: "),
        static_width=80,
        ),
        "[app.title]CPU",
        ptg.Container(
            ptg.Splitter(
                ptg.InputField(value="1", prompt="Qty: "),
                ptg.InputField(value="50000", prompt="Quota: "),
                "(μs)",
                ptg.InputField(value="100000", prompt="Period: "),
                "(μs)",
            ),
        ),
        "[app.title]Memory",
        ptg.Container(
            ptg.Splitter(
                ptg.InputField(value="1", prompt="Memory: "),
                "(Gb)",
                ptg.InputField(value="2", prompt="Swap: "),
                "(Gb)",
            ),
        ),
        "[app.title]Timezone",
        ptg.Container(
            ptg.InputField("Etc/Greenwich", prompt="Timezone: "),
        ),
        # ptg.Container(
        #     "",
        #     ptg.Splitter(
        #         ptg.Label("  CPU         "), 
        #         ptg.Toggle(("False", "True")),
        #     ),
        #     ptg.Splitter(
        #         ptg.Label("  GPU         "), 
        #         ptg.Toggle(("False", "True")),
        #     ),
        #     ptg.Splitter(
        #         ptg.Label("  Memoria     "), 
        #         ptg.Toggle(("False", "True")),
        #     ),
        # static_width=30,
        # ),
        "",
        ptg.Container(
            ptg.Splitter(
                ["Build", lambda *_: submit_build(manager, modal)],
                ptg.Button("Cancel", lambda *_: modal.close()),
            ),
        ),
    ).center().set_title("[app.title]Generate profile")


    modal.select(0)
    manager.add(modal)


def _confirm_quit(manager: ptg.WindowManager) -> None:

    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                # ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("Yes", lambda *_: _confirm_exit(manager)),
                ptg.Button("No", lambda *_: modal.close()).set_char("delimiter", [""] * 2),
            ),
        ),
    ).center()

    modal.select(0)
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

    # ptg.tim.print(f"[{PALETTE_LIGHT}]{OUTPUT}")
    if (OUTPUT['action'] == 'BUILD'):
        ptg.tim.print(f"[{PALETTE_LIGHT}]{OUTPUT}")
        profile_name = OUTPUT['1']
        cpu_qty = OUTPUT['4']
        cpu_quota = OUTPUT['5']
        cpu_period = OUTPUT['6']
        # GPU = OUTPUT['9']
        mem = OUTPUT['9']
        swap = OUTPUT['10']
        tz = OUTPUT['12']
        create_profile(profile_name, 
                       cpu_qty=cpu_qty,
                       cpu_quota=cpu_quota,
                       cpu_period=cpu_period,
                       mem=mem,
                       swap=swap,
                       tz=tz)
        # os.system('./scripts/build.sh')
    # if (OUTPUT['action'] == 'RUN'):
    #     os.system('./sandbox/run.sh')


if __name__ == "__main__":
    while (OUTPUT['action'] != 'EXIT'):
        main()

    ptg.tim.print(f"")
    ptg.tim.print(f"")
    ptg.tim.print(f"[{PALETTE_LIGHT}]Thank for use MiddleFingerprint! [app.header]  ╭ᥥ╮(´• ᴗ •`˵)╭ᥥ╮  ")
    ptg.tim.print(f"")



# {'action': 'BUILD', '0': 'Container', '1': 'Mimi', '2': 'Container', '3': 'Splitter', '4': '1', '5': '50000', '6': '100000', 
#  '7': 'Container', '8': 'Splitter', '9': '1', '10': '2', '11': 'Container', '12': 'Etc/Greenwich', '13': 'Container', '14': 'Splitter'}

