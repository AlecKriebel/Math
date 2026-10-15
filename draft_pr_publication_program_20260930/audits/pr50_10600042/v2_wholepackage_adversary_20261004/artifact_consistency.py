import hashlib, json, pathlib, re
from pypdf import PdfReader
import pdfplumber
from PIL import Image, ImageChops
root=pathlib.Path(__file__).resolve().parent
package=root.parent/'publication_package_v2'
ex=root/'private/extracted'
pdfs={}
for name,path in [('published',package/'even_strand_markov.pdf'),('rebuild',ex/'even_strand_markov.pdf')]:
    reader=PdfReader(path)
    links=[]
    for page in reader.pages:
        for ref in page.get('/Annots',[]):
            annot=ref.get_object()
            if annot.get('/A',{}).get('/URI'):
                links.append(str(annot['/A']['/URI']))
    with pdfplumber.open(path) as doc:
        text=[page.extract_text(x_tolerance=1,y_tolerance=3) for page in doc.pages]
        bounds=[{'page':i+1,'width':p.width,'height':p.height,'character_count':len(p.chars),
                 'chars_outside_media_box':sum(c['x0']<0 or c['x1']>p.width or c['top']<0 or c['bottom']>p.height for c in p.chars)} for i,p in enumerate(doc.pages)]
    pdfs[name]={'path':str(path.relative_to(root.parent)), 'bytes':path.stat().st_size,
                'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':len(reader.pages),
                'metadata':dict(reader.metadata),'links':links,'bounds':bounds,
                'text_sha256':hashlib.sha256('\f'.join(text).encode()).hexdigest()}
    (root/'private'/f'{name}_pdf_text.txt').write_text('\f'.join(text))
assert pdfs['published']['pages']==pdfs['rebuild']['pages']==5
assert pdfs['published']['text_sha256']==pdfs['rebuild']['text_sha256']
pixels=[]
for i in range(1,6):
    a=Image.open(root/'private'/f'published-{i}.png').convert('RGB')
    b=Image.open(root/'private'/f'rebuilt-{i}.png').convert('RGB')
    assert a.size==b.size
    diff=ImageChops.difference(a,b)
    box=diff.getbbox()
    pixels.append({'page':i,'size':a.size,'exactly_equal':box is None,'difference_bbox':box})
    assert box is None
assert (ex/'even_strand_markov.tex').read_bytes()==(package/'even_strand_markov.tex').read_bytes()
assert (root/'private/commands/checker.stdout').read_bytes()==(ex/'expected_results.json').read_bytes()
assert (ex/'even-strand-markov-verification-v2.zip').read_bytes()==(package/'even-strand-markov-verification-v2.zip').read_bytes()
deposit=json.loads((package/'zenodo-deposit.json').read_text())
assert deposit['metadata']['creators']==[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}]
assert deposit['metadata']['publication_type']=='preprint'
assert deposit['metadata']['access_right']=='open'
assert deposit['metadata']['license']=='cc-by-4.0'
assert 'MIT' in deposit['metadata']['description']
assert all(pathlib.PurePosixPath(f['path']).name==f['path'] for f in deposit['files'])
assert all((package/f['path']).is_file() for f in deposit['files'])
needles=[r'/Users/',r'/home/',r'ghp_[A-Za-z0-9]+',r'github_pat_',r'AKIA[A-Z0-9]{16}',r'-----BEGIN .*PRIVATE KEY',r'Bearer\s+[A-Za-z0-9._-]+',r'10\.5281/zenodo\.(?:0|XXXX)',r'localhost',r'file://']
hits=[]
for p in list(ex.glob('*'))+[package/'zenodo-deposit.json']:
    if p.is_file() and p.suffix not in ('.pdf','.zip','.log'):
        body=p.read_text(errors='replace')
        for pattern in needles:
            if re.search(pattern,body): hits.append({'file':p.name,'pattern':pattern})
assert not hits,hits
logs={n:[row for row in p.read_text().splitlines() if re.search('Overfull|Underfull|Undefined|Warning|Error',row,re.I)] for n,p in [('supplied',package/'even_strand_markov.log'),('rebuilt',ex/'even_strand_markov.log')]}
output={'status':'PASS_ARTIFACT_CONSISTENCY','pdfs':pdfs,'page_pixels':pixels,'tex_exact_member_equal':True,
        'checker_stdout_exact_expected_equal':True,'rebuilt_zip_exact_equal':True,'metadata_file_paths_resolve':True,
        'sensitive_path_or_token_pattern_hits':hits,'compile_diagnostics':logs,
        'scope':'No state-changing publication or native editor action performed'}
(root/'ARTIFACT_CONSISTENCY.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
