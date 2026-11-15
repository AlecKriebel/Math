#!/usr/bin/env python3
"""Verify this audit and replay new-only read-only checks; writes no files.
Never invokes the renderer, preparation, compatibility or writer fault harness.
"""
from pathlib import Path,PurePosixPath
import difflib,hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent;P=A.parents[1]
E=P/'verification/local-banach-mtp2-stage-sol-20261025/resume'
STAGE_SEAL='c697767fba940a0a36c38dd2aafa68097d0af34243953b04b213958ce2a57487'
def require(v,s):
 if not v:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*flags):
 r=subprocess.run([sys.executable,'-B',*flags,str(script)],capture_output=True,text=True,check=True)
 require(not r.stderr,'Unexpected stderr: '+str(script));return json.loads(r.stdout)
def main():
 require(len(sys.argv)==1,'No overrides accepted')
 seal=json.loads((A/'SEAL.json').read_text());require(sha(A/'MANIFEST.json')==seal['manifest_sha256'],'Own manifest seal')
 manifest=json.loads((A/'MANIFEST.json').read_text());names=set()
 for x in manifest['files']:
  q=PurePosixPath(x['path']);require(not q.is_absolute() and '..' not in q.parts and str(q)==x['path'] and x['path'] not in names,'Unsafe or duplicate own path');names.add(x['path'])
  p=A/x['path'];require(p.is_file() and not p.is_symlink() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Own bytes changed: '+str(p))
 actual={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file()}
 require(actual==names|{'MANIFEST.json','SEAL.json'},'Own file set changed')
 require(sha(E/'SEAL.json')==STAGE_SEAL,'Different writer final stage seal')
 for name,w in json.loads((A/'FINAL_INPUT_BINDINGS.json').read_text())['files'].items():
  p=Path(name);require(p.stat().st_size==w['bytes'] and sha(p)==w['sha256'],'Final external binding changed: '+name)
 for name in ['render_page','final-content-check']:
  original=(P/('scripts/render_page.py' if name=='render_page' else 'verification/final-content-check.py')).read_text();proposed=(E/(name+'.proposed.py')).read_text()
  expected=''.join(difflib.unified_diff(original.splitlines(True),proposed.splitlines(True),fromfile='installed/'+name+'.py',tofile='proposed/'+name+'.py'))
  require(expected==(E/(name+'.diff')).read_text(),'Diff does not describe actual current baseline: '+name)
 stage=run(E/'verify_read_only.py');require(stage==json.loads((A/'STAGE_VERIFIER.json').read_text()),'Stage read-only replay changed')
 native=run(A/'source_native/verify_packet.py');require(native==json.loads((A/'NATIVE_PACKET_VERIFIER.json').read_text()),'Native read-only replay changed')
 contract=run(A/'independent_contract.py');require(contract==json.loads((A/'CONTRACT.json').read_text()),'Independent contract replay changed')
 normal=run(A/'semantic_campaign.py');require(normal==json.loads((A/'SEMANTIC_NORMAL.json').read_text()),'Normal new-only replay changed')
 optimized=run(A/'semantic_campaign.py','-O');require(optimized==json.loads((A/'SEMANTIC_OPTIMIZED.json').read_text()),'Optimized new-only replay changed')
 n=dict(normal);o=dict(optimized);n.pop('optimized');o.pop('optimized');require(n==o,'Normal and optimized outcomes differ')
 print(json.dumps({'assessment':'SEALED_INDEPENDENT_CODE_EDITORIAL_AUDIT_SUPPORTED','owned_files_verified':len(names),'writer_final_seal_sha256':STAGE_SEAL,'external_bindings_verified':len(json.loads((A/'FINAL_INPUT_BINDINGS.json').read_text())['files']),'independent_contract_controls':contract['controls'],'independent_semantic_cases_each_mode':normal['total'],'native_controls':native['native_checks'],'native_rejection_controls':native['in_memory_negative_controls'],'production_public_files':stage['production_public_files'],'hypothetical_public_files':stage['hypothetical_integrated_files'],'index_items':stage['index_items'],'sitemap_entries':stage['sitemap_entries'],'old69_campaign_repeated':False,'installation_or_publication_authority':False},sort_keys=True,indent=2))
if __name__=='__main__':main()
