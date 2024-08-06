from pathlib import Path
import subprocess
from .config import Component, BuildStep


class BuildError(Exception):
    pass


def build_component(component: Component):
    for step in component.steps:
        print(f'Running step: {step.display_name}')
        run_build_step(step, cwd=component.path)


def run_build_step(step: BuildStep, cwd: Path):
    # TODO: Small window with process output
    proc = subprocess.run(
        step.cmd,
        shell=True,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print('Output:')
    print(proc.stdout.decode('utf-8'))
    if proc.returncode and step.break_on_error:
        # TODO: Make full process output visible
        raise BuildError(
            f'Step {step.display_name} failed with return code {proc.returncode}'
        )
