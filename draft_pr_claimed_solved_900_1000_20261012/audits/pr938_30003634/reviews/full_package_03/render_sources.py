import json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;P=R/'private';P.mkdir(exist_ok=True)
sources={x['name']:Path(x['source_file']) for x in json.loads((R/'SOURCE_PINS.json').read_text())['primary_downloads']}
for n,path in sources.items():subprocess.run(['pdftotext','-layout',str(path),str(P/(n+'.txt'))],check=True)
D=R.parents[1]/'publication'
subprocess.run(['pdftoppm','-scale-to','1250','-png',str(D/'output/pdf/note.pdf'),str(P/'paper')],check=True,capture_output=True)
for n,page in [('owr',35),('otto',6),('toffoli',31),('gg',28),('gg',35),('kawasaki2025',40),('calegari',42),('erle',5)]:
 subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1300','-singlefile','-png',str(sources[n]),str(P/(n+str(page)))],check=True,capture_output=True)
print('Rendered four paper pages and eight primary statement pages')
