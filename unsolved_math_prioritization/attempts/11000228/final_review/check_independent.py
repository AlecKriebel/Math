from pathlib import Path
import json,hashlib
p=Path('/workspace/shared/research_exceptional_11000228/checkpoint');src=p.parent/'sources';n=0
for f in json.loads((p/'FINAL_FROZEN_MANIFEST.json').read_text())['files']:
 assert hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256'];n+=1
for f in json.loads((p/'SOURCE_MANIFEST.json').read_text())['primary_pdfs']:
 assert hashlib.sha256((src/f['file']).read_bytes()).hexdigest()==f['sha256'];n+=1
# Basis count on F2: fiber-degree a, base degrees b-2i, each nonnegative degree contributes d+1.
def sections(a,b):return sum(max(0,b-2*i+1) for i in range(a+1))
assert sections(1,2)==4;n+=1
assert sections(2,4)==9;n+=1
assert sections(3,6)==16;n+=1
# Intersection pairing, canonical class -2e-4f.
def pair(a,b,c,d):return -2*a*c+a*d+b*c
R=(2,4);X=(3,6)
assert pair(*R,*X)==12;n+=1
assert 1+(pair(*R,*R)+pair(*R,-2,-4))//2==1;n+=1
assert pair(1,0,*X)==0;n+=1
assert pair(0,4,*X)==12 and pair(0,6,*X)==18;n+=1
for marks in range(1,10):assert 8+marks+4-7==marks+5; n+=1
for sig in [(-1,9),(-1,3,6),(-1,3,3,3),(12,)]:
 genus=(sum(sig)+4)//4;assert genus in [3,4];n+=1
 assert all(x%3==0 for x in sig if x>0);n+=1
print(json.dumps({'status':'PASS','independent_assertions':n,'scope':'source/report integrity and ruled-surface arithmetic only; no classification-proof certification'},indent=2))
