import pathlib,subprocess,hashlib,json
from pypdf import PdfReader
from PIL import Image
h=pathlib.Path(__file__).resolve().parent
paths=[h/'tmp/unpacked/output/pdf/totally-mixed-face-posets.pdf',h/'tmp/compiled/main.pdf']
readers=[PdfReader(p) for p in paths]
if any(len(r.pages)!=4 for r in readers):raise RuntimeError('page count')
result=[]
for j,p in enumerate(paths):
 subprocess.run(['pdftoppm','-r','110','-png',str(p),str(h/'tmp'/('frozen' if j==0 else 'rebuilt'))],capture_output=True,check=True)
for i,(a,b) in enumerate(zip(readers[0].pages,readers[1].pages),1):
 ta,tb=a.extract_text(),b.extract_text()
 ca,cb=a.get_contents().get_data(),b.get_contents().get_data()
 im=[Image.open(h/'tmp'/('%s-%d.png'%(s,i))).convert('RGB') for s in ('frozen','rebuilt')]
 if ta!=tb or ca!=cb or im[0].size!=im[1].size or im[0].tobytes()!=im[1].tobytes():raise RuntimeError('PDF difference page '+str(i))
 result.append({'page':i,'text_sha256':hashlib.sha256(ta.encode()).hexdigest(),'drawing_stream_sha256':hashlib.sha256(ca).hexdigest(),'pixels_sha256':hashlib.sha256(im[0].tobytes()).hexdigest(),'size':im[0].size,'identical':True})
log=(h/'tmp/compiled/main.log').read_text()
if 'Overfull' in log or 'undefined references' in log:raise RuntimeError('LaTeX warning')
(h/'evidence/PDF_COMPARISON.json').write_text(json.dumps({'page_count':4,'pages':result,'byte_identity':paths[0].read_bytes()==paths[1].read_bytes(),'frozen_sha256':hashlib.sha256(paths[0].read_bytes()).hexdigest(),'rebuilt_sha256':hashlib.sha256(paths[1].read_bytes()).hexdigest()},indent=2)+'\n')
print(json.dumps(result,indent=2))
