from pathlib import Path
import subprocess
from .config import Component, BuildStep


class BuildError(Exception):
    pass


def build_component(component: Component):
    for step in component.steps:
        run_build_step(step, cwd=path)


def run_build_step(step: BuildStep, cwd: Path):
    # TODO: Small window with process output
    proc = subprocess.run(step.cmd, shell=True, cwd=str(cwd))
    if proc.returncode and step.break_on_error:
        # TODO: Make full process output visible
        raise BuildError(
            f'Step {step.name | step.cmd} failed with return code {proc.returncode}'
        )
