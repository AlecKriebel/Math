"""Read-only Poppler rendering for visual inspection; no manuscript authoring."""
from pathlib import Path
import hashlib, json, subprocess
from PIL import Image, ImageDraw
D=Path(__file__).resolve().parent; P=D.parents[3]; S=P/'papers/22395326/sources';W=D/'replay-work/visual'
W.mkdir(exist_ok=True)
items=[]
for name,count in [('Symmetry-Stratified_Level2_Identifiability.pdf',41),('Symmetry-Stratified_Level2_Identifiability_Supplement.pdf',14)]:
    prefix=W/('main' if count==41 else 'sup')
    command=['/opt/homebrew/bin/pdftoppm','-scale-to','900','-png',str(S/name),str(prefix)]
    run=subprocess.run(command,capture_output=True,text=True,timeout=60)
    if run.returncode:raise RuntimeError(run.stderr)
    pages=sorted(W.glob(prefix.name+'-*.png'))
    if len(pages)!=count:raise RuntimeError('wrong rendered page count')
    sheets=[]
    for first in range(0,count,12):
        sheet=Image.new('RGB',(1830,3280),'#cccccc');draw=ImageDraw.Draw(sheet)
        for k,p in enumerate(pages[first:first+12]):
            im=Image.open(p).convert('RGB');im.thumbnail((600,790))
            x=(k%3)*610;y=(k//3)*820
            sheet.paste(im,(x,y+24));draw.text((x+5,y+4),f'{prefix.name} PDF {first+k+1}',fill='black')
        out=W/f'{prefix.name}-contact-{first+1:02}.jpg';sheet.save(out,quality=88);sheets.append(str(out))
    items.append({'source':str(S/name),'source_sha256':hashlib.sha256((S/name).read_bytes()).hexdigest(),'pages':count,'command':command,'contact_sheets':sheets})
(D/'VISUAL_RENDER_RECEIPT.json').write_text(json.dumps(items,indent=2)+'\n')
print(json.dumps(items,indent=2))
