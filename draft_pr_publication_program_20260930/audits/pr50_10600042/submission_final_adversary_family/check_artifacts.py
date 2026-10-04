#!/usr/bin/env python3
"""Read exact final submission inputs; create only a private extracted copy."""
from pathlib import Path
import hashlib, json, re, zipfile
base=Path(__file__).absolute().parent
package=base.parent/'publication_package_v1'
checks=0
def need(ok,msg):
    global checks
    if not ok: raise ValueError(msg)
    checks+=1
def binding(path):
    need(path.is_file() and not path.is_symlink(), 'regular input '+str(path))
    body=path.read_bytes()
    return {'path':str(path),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}

members=('LICENSE-CODE.txt','LICENSE-TEXT.md','README.md','SHA256SUMS','SOURCE_QUALIFICATIONS.md',
         'VERIFICATION_RECORD.json','build_verification_zip.py','even_strand_markov.tex',
         'expected_results.json','verify_even_calculus.py')
extract=base/'extracted'
need(not extract.exists(),'no reuse of prior private extraction')
extract.mkdir()
archive=package/'even-strand-markov-verification-v1.zip'
pins=[binding(package/n) for n in ('even_strand_markov.tex','even_strand_markov.pdf',archive.name,'zenodo-deposit.json')]
with zipfile.ZipFile(archive) as z:
    need(z.namelist()==list(members), 'exact ordered ten member set')
    need(z.testzip() is None,'all member CRCs')
    for name in members:
        info=z.getinfo(name)
        need(info.external_attr>>16==0o100644,'normalized regular member mode')
        need(info.date_time==(1980,1,1,0,0,0),'normalized archive timestamp')
        body=z.read(name)
        need(body==(package/name).read_bytes(), 'whole member equals submitted sidecar '+name)
        (extract/name).write_bytes(body)
sha={}
for line in (extract/'SHA256SUMS').read_text().splitlines():
    h,n=line.split('  ',1)
    need(n not in sha and bool(re.fullmatch('[0-9a-f]{64}',h)), 'checksum row')
    sha[n]=h
need(set(sha)==set(members)-{'SHA256SUMS'},'all nonself checksums exactly')
for n,h in sha.items(): need(hashlib.sha256((extract/n).read_bytes()).hexdigest()==h, 'extracted checksum '+n)
record=json.loads((extract/'VERIFICATION_RECORD.json').read_bytes())
for p,key in (('verify_even_calculus.py','checker_binding'),('expected_results.json','expected_result_binding')):
    b=binding(extract/p)
    need({k:b[k] for k in ('bytes','sha256')}==record[key], 'record '+key)
tex=(extract/'even_strand_markov.tex').read_bytes()
need(hashlib.sha256(tex).hexdigest()=='cd141a55da2241764d4fbbe8a145d8d4be29370803e24704e645c60cf8f2d0dc','assigned final source pin')
need(record['manuscript_provenance']['submission_tex_binding']=={'bytes':len(tex),'sha256':hashlib.sha256(tex).hexdigest()}, 'record final tex')
old=base.parent/'preprint_v1'/'even_strand_markov.tex'
oldbody=old.read_bytes()
need(hashlib.sha256(oldbody).hexdigest()==record['manuscript_provenance']['reviewed_preprint_v1_tex_sha256'],'old source pin')
stripped=tex.replace(b'\\hypersetup{\n pdftitle={An even-strand Markov calculus for classical and virtual links},\n pdfauthor={Alec Kriebel}\n}\n',b'',1)
stripped=stripped.replace(b'\\begingroup\n\\small\n\\begin{thebibliography}',b'\\begin{thebibliography}',1)
stripped=stripped.replace(b'\\end{thebibliography}\n\\endgroup\n',b'\\end{thebibliography}\n',1)
need(stripped==oldbody,'only PDF metadata and bibliography sizing change')
meta=json.loads((package/'zenodo-deposit.json').read_bytes())
need(set(meta)=={'metadata','files'}, 'top-level manifest schema')
m=meta['metadata']
need(m['title']=='An even-strand Markov calculus for classical and virtual links','exact title')
need(m['upload_type']=='publication' and m['publication_type']=='preprint','publication type')
need(m['creators']==[{'name':'Kriebel, Alec','orcid':'0009-0001-9320-500X'}],'exact creator/ORCID no invented affiliation')
need(m['access_right']=='open' and m['license']=='cc-by-4.0','record license')
need(meta['files']==[{'path':'even_strand_markov.pdf','name':'even_strand_markov.pdf'},
                     {'path':archive.name,'name':archive.name}],'only complete actual PDF and ZIP')
for f in meta['files']: need((package/f['path']).is_file(),'upload file exists')
need(not ({'doi','prereserve_doi','deposit_id','publication_date'} & set(m)),'no invented publication fields')
need('unrefereed' in m['description'] and 'no human peer review' in m['description'] and 'MIT' in m['description'], 'metadata disclosures/licensing')
need('present openness are not claimed' in m['description'],'metadata scope qualification')
need('MIT License' in (extract/'LICENSE-CODE.txt').read_text() and 'CC BY 4.0' in (extract/'LICENSE-TEXT.md').read_text(),'portable licenses')
need(tex.count(b'\\begin{document}')==1 and tex.count(b'\\end{document}')==1,'standalone manuscript')
need(b'\\input' not in tex and b'\\include' not in tex and b'\\includegraphics' not in tex,'no missing source dependency')
need(b'no human peer review or formal proof certification is claimed' in tex,'manuscript disclosure')
native=json.loads((base.parent/'publication_operations/ROOT_NATIVE_COMPILER_RESPONSE.json').read_bytes())
response=json.loads(native['response']['content'][0]['text'])
need(native['source_sha256']==hashlib.sha256(tex).hexdigest() and response['kind']=='success' and response['path']==str(package/'even_strand_markov.tex'),'recorded native compiler source/result')
need(native['compiler_process_pid_not_reported'] is True,'no invented native PID')
out={'schema':'pr50-final-review-artifact-readback/v1','status':'PASS_EXACT_PORTABLE_ARTIFACTS','checks':checks,
     'input_pins':pins,'member_pins':[binding(extract/n) for n in members],
     'source_math_unchanged_from_reviewed_v1':True,'private_extraction_path':str(extract),
     'publication_or_mathematical_approval_not_conferred':True}
(base/'FINAL_INPUT_BINDINGS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
