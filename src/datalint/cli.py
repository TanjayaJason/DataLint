import csv
from pathlib import Path
import typer
import yaml
from .core import inspect, markdown
from .support import render_json
app = typer.Typer(help='Deterministic, read-only CSV quality checks.', add_completion=False)
@app.command()
def check(path: Path, config: Path | None = None, json: bool = False, fail_on_error: bool = False):
    """Profile CSV and explain findings. Optional CI exit code 2 for error findings."""
    try:
        report = inspect(path, config)
        typer.echo(render_json(report) if json else markdown(report))
        if fail_on_error and any(f['severity']=='error' for f in report['findings']):
            raise typer.Exit(2)
    except (ValueError, OSError, csv.Error, yaml.YAMLError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1)
