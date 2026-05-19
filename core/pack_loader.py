import json
from pathlib import Path
PACKS_DIR = Path(__file__).resolve().parent.parent / 'packs'
def load_pack(slug: str) -> dict:
    path = PACKS_DIR / slug / 'pack.json'
    if not path.exists(): raise FileNotFoundError(f'Pack not found: {path}')
    with path.open('r', encoding='utf-8') as f: pack = json.load(f)
    for key in ['slug','title','subtitle','version','dimensions','dimension_weights','questions','bands','recommendation_templates']:
        if key not in pack: raise ValueError(f'Missing required key: {key}')
    return pack
