"""Small IO boundary; inputs are read-only and model access is explicit."""
import json
from pathlib import Path

def read_text(path: Path, max_bytes: int = 10_000_000) -> str:
    with path.open('rb') as handle:
        data = handle.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError(f'Input exceeds {max_bytes:,} bytes.')
    return data.decode('utf-8-sig')

def render_json(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)
