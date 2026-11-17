"""Passive diagnostic magnification of supplied primary pixels; original remains unchanged."""
from pathlib import Path
from PIL import Image
base=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23137834/reviews')
source=base/'scope-sol/primary/verdure-13.png'
target=base/'verdure-convention-challenge-sol-20261117/verdure-printed87-diagnostic.png'
assert not target.exists()
with Image.open(source) as im:
    im.crop((150,890,900,1140)).resize((1500,500),Image.Resampling.NEAREST).save(target)
