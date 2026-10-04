from pathlib import Path
import hashlib,json,zipfile,subprocess,datetime
P=Path(__file__).absolute().parent.parent/'publication_package_v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):b=p.read_bytes();return {'path':p.name,'bytes':len(b),'sha256':sha(b)}
expected={}
for row in (P/'SHA256SUMS').read_text().splitlines():
    h,n=row.split('  ',1);assert n not in expected;expected[n]=h
with zipfile.ZipFile(P/'even-strand-markov-verification-v1.zip') as z:
    assert set(z.namelist())==set(expected)|{'SHA256SUMS'} and len(z.namelist())==10
    assert z.testzip() is None
    for n in z.namelist():
        b=z.read(n);assert b==(P/n).read_bytes()
        if n!='SHA256SUMS':assert sha(b)==expected[n]
assert sha((P/'even_strand_markov.tex').read_bytes())=='cd141a55da2241764d4fbbe8a145d8d4be29370803e24704e645c60cf8f2d0dc'
info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(P/'even_strand_markov.pdf')],capture_output=True,check=True)
assert info.stderr==b'' and b'Pages:           4' in info.stdout
assert b'An even-strand Markov calculus for classical and virtual links' in info.stdout
assert b'Alec Kriebel' in info.stdout
compiler=json.loads((Path(__file__).parent/'ROOT_NATIVE_COMPILER_RESPONSE.json').read_bytes())
assert compiler['response']['isError'] is False
assert json.loads(compiler['response']['content'][0]['text'])['kind']=='success'
report={'schema':'pr50-root-final-artifact-readback/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FULL_FINAL_ARTIFACT_READBACK','files':[pin(P/n) for n in ['even_strand_markov.tex','even_strand_markov.pdf','even-strand-markov-verification-v1.zip','zenodo-deposit.json']],'zip_members_exact_full_body_readback':10,'pdfinfo_full_stdout':info.stdout.decode(),'pdfinfo_full_stderr':info.stderr.decode(),'root_personally_viewed_all_four_rendered_pages':True,'visual_observation':'All four rendered pages were personally viewed by ROOT in this same task; equations, move rules and five bibliography entries are legible, with no clipping or overlaps.','render_images':['tmp/pdfs/submission_v1/page-'+str(i)+'.png' for i in range(1,5)],'native_compiler_response_reference':'ROOT_NATIVE_COMPILER_RESPONSE.json','pdf_export_actual_capture':'../../pr45_9900007/root_pr50_submission_pdf_export_actual_capture/CAPTURE.json','mathematical_review_or_publication_approval_not_conferred_by_this_check':True}
out=Path(__file__).parent/'ROOT_FINAL_ARTIFACT_READBACK.json'
with out.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(report,indent=2))
