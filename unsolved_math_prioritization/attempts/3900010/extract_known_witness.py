"""Read Reid's credited bitmap as mathematical cell-boundary data.
Usage: python extract_known_witness.py /path/to/14omino02_66x84.gif
The original image is a local reading input, not redistributed in this packet.
"""
from pathlib import Path
import sys,json,hashlib
from PIL import Image
from tile_model import D4,normalize
path=Path(sys.argv[1]);im=Image.open(path).convert('RGB');W,H=84,66
assert im.size==(10*W+1,10*H+1)
left={(x,y) for x in range(W) for y in range(H)};tiles=[]
while left:
 root=min(left);left.remove(root);stack=[root];part=[]
 while stack:
  x,y=stack.pop();part.append((x,y))
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   z=x+dx,y+dy
   if z not in left:continue
   px=10*x+5+5*dx;py=10*y+5+5*dy
   if im.getpixel((px,py))==(255,255,255):left.remove(z);stack.append(z)
 assert len(part)==14
 q=normalize(part);assert q in D4
 tiles.append({'x':min(x for x,y in part),'y':min(y for x,y in part),'orientation':D4.index(q)})
out={'attribution':'Michael Reid, restored14omino02 rectangle diagram; this is a coordinate transcription and independent verification, not a new tiling.','source_url':'https://sicherman.net/mikereid/Images/14omino02_66x84.gif','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':W,'height':H,'number_of_tiles':len(tiles),'tiles':tiles}
assert len(tiles)==396
Path(__file__).with_name('known_even_witness.json').write_text(json.dumps(out,indent=2)+'\n')
print('Extracted and shape-checked396 tiles')
