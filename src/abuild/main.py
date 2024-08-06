#!/usr/bin/env python
import typer
from pathlib import Path
from .config import Config
from .state import state_update
from .build import build_component

app = typer.Typer()


@app.callback()
def main():
    # Set global options here
    pass


@app.command()
def build(config: str = 'abuild.yaml'):
    """Build components listed in the config file"""
    cfg = Config.from_file(Path(config))
    for component in cfg.components:
        with state_update(component.path, cfg.state_file) as need_rebuild:
            if need_rebuild:
                print(f'Building component: {component.display_name}')
                build_component(component)


@app.command()
def parse():
    pass


if __name__ == '__main__':
    app.run()
