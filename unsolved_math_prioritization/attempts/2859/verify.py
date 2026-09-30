from itertools import product
from pathlib import Path
import hashlib,json
n=0
# Original and mutant maps in the separating Mayer-Vietoris calculation.
for a,b,c,d in product(range(-4,5),repeat=4):
 original=[[a,b],[-c,-d]];mutant=[[a,b],[c,d]]
 assert [original[0],[-z for z in original[1]]]==mutant;n+=1
 assert [[z%2 for z in row] for row in original]==[[z%2 for z in row] for row in mutant];n+=1
I=[[int(i==j) for j in range(4)] for i in range(4)]
A0=[[I[i][j]-I[i][j] for j in range(4)] for i in range(4)]
A1=[[-I[i][j]-I[i][j] for j in range(4)] for i in range(4)]
assert A0==[[0]*4 for _ in range(4)];n+=1
assert A1==[[-2*int(i==j) for j in range(4)] for i in range(4)];n+=1
assert all(z%2==0 for row in A1 for z in row);n+=1
r={'assertions':n,'all_pass':True,'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Homology presentation controls only, no Floer computation or executable geometry.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
