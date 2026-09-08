"""Read-only PDF contact sheets and metadata for the referee round."""
from pathlib import Path
import io,json,re,subprocess
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source_snapshot'
OUT=HERE/'rendered'; OUT.mkdir(exist_ok=True)
documents={'main':'manuscript/main.pdf','supplement':'manuscript/supplement.pdf',
           'summary':'external_audit/theorem_summary.pdf','skeleton':'external_audit/proof_skeleton.pdf',
           'journal_main':'submission/journal/manuscript.pdf','journal_supplement':'submission/journal/supplement.pdf',
           'letter':'submission/journal/cover_letter_SIADS.pdf'}
inventory=[]
for name,relative in documents.items():
    path=SOURCE/relative
    info=subprocess.check_output(['pdfinfo',str(path)],text=True)
    count=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    (HERE/(name+'.txt')).write_bytes(subprocess.check_output(['pdftotext','-layout',str(path),'-']))
    images=[]
    for start in range(1,count+1,4):
        panels=[]
        for page in range(start,min(start+4,count+1)):
            raw=subprocess.check_output(['pdftoppm','-f',str(page),'-l',str(page),'-r','100','-singlefile','-png',str(path)])
            picture=Image.open(io.BytesIO(raw)).convert('RGB')
            panels.append((page,picture))
        w=max(p.width for _,p in panels);h=max(p.height for _,p in panels)
        sheet=Image.new('RGB',(w*2,(h+30)*2),'#b8b8b8');draw=ImageDraw.Draw(sheet)
        for k,(page,picture) in enumerate(panels):
            x=(k%2)*w;y=(k//2)*(h+30)
            draw.text((x+12,y+8),f'{name} / page {page}',fill='black')
            sheet.paste(picture,(x,y+30))
        filename=f'{name}_{start:02d}-{min(start+3,count):02d}.jpg'
        sheet.save(OUT/filename,quality=88)
        images.append(filename)
    inventory.append({'document':relative,'pages':count,'bytes':path.stat().st_size,'pdfinfo':info,'contact_sheets':images})
(HERE/'PDF_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n')
print(json.dumps({'documents':len(inventory),'pages':sum(d['pages'] for d in inventory),'contact_sheets':sum(len(d['contact_sheets']) for d in inventory)}))
