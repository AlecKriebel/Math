#!/usr/bin/env python3
"""Recheck separately supplied public inputs without publishing their contents."""
import argparse, hashlib, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def require(condition, label):
    if not condition:raise AssertionError(label)
def digest(data):return hashlib.sha256(data).hexdigest()
def git_blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def dump(value):return json.dumps(value,indent=2,sort_keys=True)+'\n'

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--catalog',type=Path,required=True,help='Complete catalog.json')
ap.add_argument('--problems',type=Path,required=True,help='Complete problems.json')
ap.add_argument('--research-results',type=Path,required=True,help='Complete research_results.json')
ap.add_argument('--queue-script',type=Path,required=True,help='Pinned repository queue.py')
ap.add_argument('--pdf-dir',type=Path,required=True,help='Directory with PDFs named as SOURCE_AUDIT.json specifies')
ap.add_argument('--author-zip',type=Path,required=True,help='Unmodified author-safe freeze ZIP')
ap.add_argument('--write',action='store_true',help='Write the deterministic verification result instead of comparing')
args=ap.parse_args()
meta=json.loads((ROOT/'SOURCE_AUDIT.json').read_text())
objects={}; corpus_results=[]
inputs={'catalog.json':args.catalog,'problems.json':args.problems,'research_results.json':args.research_results}
for pin in meta['full_corpora']:
    data=inputs[pin['filename']].read_bytes()
    require(len(data)==pin['bytes'],pin['filename']+' byte count')
    require(digest(data)==pin['sha256'],pin['filename']+' digest')
    objects[pin['filename']]=json.loads(data)
    corpus_results.append({**pin,'matches_author_pin':True,'entire_file_read':True})
catalog=[x for x in objects['catalog.json'] if str(x.get('id'))=='30005024']
problems=[x for x in objects['problems.json'] if str(x.get('id'))=='30005024']
require(len(catalog)==len(problems)==1,'unique problem identity')
c,p=catalog[0],problems[0]
require(c['rank']==meta['rank']==787,'rank')
require(c['problem_number']==p['problem_number']==meta['problem_number'],'problem code')
statement=p['statement'].encode()
require(len(statement)==meta['statement_utf8_bytes'],'statement byte count')
require(digest(statement)==c['statement_hash']==meta['statement_sha256'],'statement digest')
reports=objects['research_results.json']
require(p['problem_number'] not in reports,'exact-code research record absence')
review=digest(json.dumps([p,reports.get(p['problem_number'],{})],sort_keys=True).encode())
require(review==c['review_hash']==meta['review_hash'],'review hash')
queue=args.queue_script.read_bytes();qpin=meta['review_hash_definition_source']
require(len(queue)==qpin['bytes'] and digest(queue)==qpin['sha256'],'queue source content pin')
require(git_blob(queue)==qpin['git_blob_sha'],'queue source Git blob pin')
require(b'review_hash=digest(json.dumps([p,r],sort_keys=True))' in queue,'review hash serialization rule')
require(b"reports.get(p['problem_number'],{})" in queue,'research lookup rule')
pdfs=[]
for pin in meta['source_pdfs']:
    name=pin['local_pdf_basename'];require(Path(name).name==name,'safe PDF basename')
    data=(args.pdf_dir/name).read_bytes()
    require(data.startswith(b'%PDF-'),'PDF signature '+name)
    require(len(data)==pin['bytes'] and digest(data)==pin['sha256'],'PDF pin '+name)
    require(pin['author_hash_match'] and pin['author_bytes_match'],'recorded author PDF match '+name)
    pdfs.append({'name':name,'bytes':len(data),'sha256':digest(data),'matches_author_pin':True})
archive=args.author_zip.read_bytes()
require(len(archive)==19304,'author ZIP size')
require(digest(archive)=='0f5e6dfb82fa255889d917eba93535e1912785787276f5a3f63e85a9abddc144','author ZIP pin')
with zipfile.ZipFile(args.author_zip) as z:
    names=z.namelist()
    require(len(names)==len(set(names))==10,'author ZIP member identity')
    local={x.relative_to(ROOT/'author').as_posix() for x in (ROOT/'author').rglob('*') if x.is_file()}
    require(set(names)==local,'author extracted file set')
    for name in names:require(z.read(name)==(ROOT/'author'/name).read_bytes(),'unchanged author member '+name)
manifest=(ROOT/'author/MANIFEST.json').read_bytes()
require(digest(manifest)=='6e85d6ff39d8c353145140f1122f00861c95ed200f0f35a5445a007dfda2c825','author manifest pin')
receipt=json.loads((ROOT/'AUTHOR_FREEZE_RECEIPT.json').read_text())
require(receipt['zip_sha256']==digest(archive) and receipt['zip_bytes']==len(archive),'author receipt ZIP pins')
require(receipt['manifest_sha256']==digest(manifest),'author receipt manifest pin')
result={
 'status':'PASS_EXTERNAL_PROVENANCE',
 'problem_id':30005024,'problem_number':p['problem_number'],'rank':c['rank'],
 'full_corpora':corpus_results,
 'selected_catalog_matches':1,'selected_problem_matches':1,
 'statement_utf8_bytes':len(statement),'statement_sha256':digest(statement),
 'review_hash':review,'review_hash_recomputed_from_complete_inputs':True,
 'research_exact_code_record_present':False,
 'queue_rule_git_blob_sha':git_blob(queue),'queue_rule_sha256':digest(queue),
 'source_pdf_count':len(pdfs),'source_pdfs':pdfs,
 'author_zip_bytes':len(archive),'author_zip_sha256':digest(archive),
 'author_manifest_sha256':digest(manifest),'author_files_byte_identical':True,
 'source_payload_published':False,
 'limitations':['External-file verification checks supplied bytes, not fresh network retrieval.',
                'Retrieval and inspection history is separately recorded in SOURCE_AUDIT.json.',
                'Prior-attempt searches are bounded observations, not independently reconstructed by this offline script.']}
serialized=dump(result);target=ROOT/'PROVENANCE_RESULTS.json'
if args.write:target.write_text(serialized)
else:require(target.read_text()==serialized,'recorded provenance result')
print(json.dumps({k:result[k] for k in ['status','problem_id','rank','source_pdf_count','review_hash','author_files_byte_identical']}))
