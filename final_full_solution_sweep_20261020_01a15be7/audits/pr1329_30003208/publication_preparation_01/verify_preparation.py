# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Alec Kriebel
"""Read-only audit of this frozen local preparation; not its independent review."""
from pathlib import Path
import json,hashlib,zipfile,io,gzip,subprocess,sys
P=Path(__file__).resolve().parent;S=P/'release/tail_generation_source'
def need(ok,m):
 if not ok:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(f):return json.loads(f.read_bytes())
def strict(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys() and all(strict(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
 return a==b
def zipread(b):
 z=zipfile.ZipFile(io.BytesIO(b));names=z.namelist();need(len(names)==len(set(names)),'duplicate ZIP paths')
 for n in names:need(not n.startswith('/') and '..' not in Path(n).parts,'ZIP traversal')
 need(sum(i.file_size for i in z.infolist())<8*1024*1024,'bounded ZIP expansion')
 return {n:z.read(n) for n in names}
def main():
 seal=obj(P/'MANIFEST.json')['files'];actual={f.relative_to(P).as_posix() for f in P.rglob('*') if f.is_file() and f!=P/'MANIFEST.json'}
 need(set(seal)==actual,'closed preparation members')
 for name,pin in seal.items():
  b=(P/name).read_bytes();need(len(b)==pin['bytes'] and sha(b)==pin['sha256'],'sealed member '+name)
 need(sum(f.stat().st_size for f in P.rglob('*') if f.is_file())<=8*1024*1024,'8MiB preparation cap')
 status=obj(P/'PREPARATION_STATUS.json');need(status['publication_ready']is False and status['new_publication_performed']is False,'readiness boundary')
 need(status['result_family_count']==1 and status['aliases']==['30003208','30002897'],'alias family')
 need(status['fresh_whole_package_review_complete']is False and status['root_final_package_adoption_complete']is False,'pending independent adoption')
 need(status['provider_write_calls']==0,'no provider writes')
 need((P/'note/main.tex').read_bytes()==(S/'main.tex').read_bytes(),'dedicated project and source archive source differ')
 need((P/'release/tail-generation.pdf').read_bytes()==(S/'paper.pdf').read_bytes(),'PDF selection')
 scientific=zipread((P/'release/tail-generation-source-and-verification.zip').read_bytes())
 wanted={'tail_generation_source/'+f.relative_to(S).as_posix():f.read_bytes() for f in S.rglob('*') if f.is_file()}
 need(scientific==wanted,'exact scientific ZIP bytes/member set')
 kit=zipread((P/'release/tail-generation-upload-kit.zip').read_bytes())
 need(set(kit)=={'tail-generation.pdf','tail-generation-source-and-verification.zip','zenodo-metadata.json','zenodo-deposit.json','README.txt'},'five-member upload kit')
 for name in ['tail-generation.pdf','tail-generation-source-and-verification.zip','zenodo-metadata.json','zenodo-deposit.json']:need(kit[name]==(P/'release'/name).read_bytes(),'kit member '+name)
 need(kit['README.txt']==(S/'UPLOAD_README.txt').read_bytes(),'kit instructions')
 metadata=obj(S/'zenodo-metadata.json');need(strict(metadata,obj(P/'release/zenodo-metadata.json')) and strict(metadata,obj(S/'zenodo-deposit.json')['metadata']),'metadata agreement')
 need('doi' not in metadata and 'prereserve_doi' not in metadata,'no DOI assignment')
 qa=obj(S/'PDF_VISUAL_QA.json');need(qa['pages']==4 and qa['every_page_rendered_and_visually_inspected'] and qa['pdf_sha256']==sha((S/'paper.pdf').read_bytes()),'final PDF QA receipt')
 final=obj(P/'FINAL_LEDGER_CHECK.json');need(final['numeric_gid']==1254632077 and final['column_count']==43 and final['metadata_stable'] and not any(x['exact_alias_hits'] for x in final['leads']),'final bounded duplicate receipt')
 raws={}
 for mode in ['metadata_before','metadata_after','UNFORMATTED_VALUE','FORMULA']:
  b=gzip.decompress((P/'private/ledger_final'/(mode+'.json.gz')).read_bytes());raws[mode]=json.loads(b);pin=next(x for x in final['captures'] if x['name']==mode);need(len(b)==pin['raw_bytes'] and sha(b)==pin['raw_sha256'],'raw GWS capture '+mode)
 need(strict(raws['metadata_before'],raws['metadata_after']),'metadata stability')
 need(raws['metadata_before']['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','book identity')
 need(strict(raws['UNFORMATTED_VALUE'],raws['FORMULA']),'typed formula/value identity')
 for mode in ['UNFORMATTED_VALUE','FORMULA']:need(raws[mode]['range']=="'Math Puzzles'!A1:AQ1178" and len(raws[mode]['values'])==191,'full ledger bound')
 r=subprocess.run([sys.executable,'-B',str(S/'reproduce.py')],capture_output=True);need(r.returncode==0,'scientific reproduction: '+r.stderr.decode());result=json.loads(r.stdout)
 print(json.dumps({'status':'PASS','publication_ready':False,'fresh_independent_review_required':True,'scientific_reproduction':result,'scientific_zip_members':len(scientific),'upload_kit_members':len(kit),'provider_write_calls':0},sort_keys=True,indent=2))
if __name__=='__main__':main()
