#!/usr/bin/env python3
"""Read-only byte preservation, link, inventory and restricted-content audit.
Accepts reader and original research roots; output never contains original paths.
This is packaging verification, not a new mathematical proof pass.
"""
import argparse, ast, hashlib, json, re
from pathlib import Path
from urllib.parse import urlsplit, unquote

def h(b): return hashlib.sha256(b).hexdigest()
def require(x,msg):
    if not x: raise RuntimeError(msg)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('reader',type=Path); ap.add_argument('original',type=Path); ap.add_argument('--source-evidence-root',type=Path,action='append',default=[]); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
    r=a.reader.resolve(); o=a.original.resolve(); files=sorted(p for p in r.rglob('*') if p.is_file()); require(not any(p.is_symlink() for p in r.rglob('*')),'symlink')
    # Hash all originals only internally; report document IDs and hashes, never storage paths.
    orig={}
    for root in [o]+a.source_evidence_root:
        for p in root.rglob('*'):
            if p.is_file(): orig.setdefault(h(p.read_bytes()),[]).append(p)
    manifest=json.loads((r/'FILE_MANIFEST.json').read_text()); listed={x['path'] for x in manifest['files']}
    require(len(listed)==len(manifest['files']),'duplicate manifest member')
    require(listed=={str(p.relative_to(r)) for p in files}-set(manifest['manifest_exclusions']),'manifest coverage')
    for x in manifest['files']:
        b=(r/x['path']).read_bytes(); require(len(b)==x['bytes'] and h(b)==x['sha256'],'manifest pin '+x['path'])
    sums=[]
    for line in (r/'SHA256SUMS').read_text().splitlines():
        pin,rel=line.split('  ',1); require(h((r/rel).read_bytes())==pin,'checksum '+rel); sums.append(rel)
    require(set(sums)=={str(p.relative_to(r)) for p in files}-{'SHA256SUMS'},'checksum coverage')
    inv=json.loads((r/'PRESERVATION_INVENTORY.json').read_text()); san=json.loads((r/'SANITIZATION_INVENTORY.json').read_text()); records=inv['proofs_and_qualifications']+inv['reviews']; rd={x['id']:x for x in records}; rows=[]; transformation_rows=[]
    for x in records:
        d=x['derivative']; b=(r/d['path']).read_bytes(); require(h(b)==d['sha256'] and len(b)==d['bytes'],'derivative '+x['id']); candidates=[p for p in orig.get(x['original']['sha256'],[]) if p.name==x['source_document']]; require(candidates,'original missing '+x['id']); original=candidates[0].read_bytes(); require(len(original)==x['original']['bytes'],'original size '+x['id']); v=original
        for op in [op for op in san['operations'] if op['document_id']==x['id']]:
            require(h(v)==op['input_sha256_before_operation'],'transform input '+x['id']); off=op['byte_offset_before_operation']; n=op['removed_bytes']; removed=v[off:off+n]; replacement=b[off:off+op['replacement_bytes']] if op['operation']=='replace' else b''
            require(h(removed)==op['removed_text_sha256'] and h(replacement)==op['replacement_text_sha256'],'transform slice '+x['id']); v=v[:off]+replacement+v[off+n:]
            transformation_rows.append({'id':x['id'],'operation':op['operation'],'byte_offset':off,'removed_bytes':n,'replacement_bytes':len(replacement),'slice_pins_match':True})
        require(v==b,'transformation final '+x['id']); acceptance=[]
        for aid in x.get('acceptance_ids',[]):
            txt=(r/rd[aid]['derivative']['path']).read_text(); require(x['original']['sha256'] in txt,'missing acceptance pin '+x['id']+' '+aid); acceptance.append(aid)
        rows.append({'id':x['id'],'path':d['path'],'original_sha256':h(original),'derivative_sha256':h(b),'original_bytes':len(original),'derivative_bytes':len(b),'exact_transformation_match':True,'acceptance_pins_present':acceptance})
    checks=json.loads((r/'CHECK_INVENTORY.json').read_text())['checks']; check_rows=[]
    for x in checks:
        b=(r/x['script']).read_bytes(); e=(r/x['expected']).read_bytes(); require(h(b)==x['script_sha256'] and len(b)==x['script_bytes'],'check pin');require(h(e)==x['expected_sha256'] and len(e)==x['expected_bytes'],'expected pin');require(h(b) in orig and h(e) in orig,'check original not found '+x['id']); asserts=sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(b)));require(bool(asserts)==x['uses_python_assertions'],'assert classification '+x['id']); require(not asserts or x['modes']==['normal'],'assert optimization '+x['id']);check_rows.append({'id':x['id'],'script_sha256':h(b),'expected_sha256':h(e),'assert_statement_count':asserts,'modes':x['modes'],'original_script_and_result_bytes_match':True})
    # Only file-suffix Markdown targets count as file links. Bracket notation such
    # as [5](T) in the mathematical originals is algebra, not an intended file.
    links=[]; excluded_algebra=[]; public=set(); markers=[]
    patterns=[r'/workspace/',r'/home/',r'/root/',r'file://',r'sandbox:',r'codex://',r'chatgpt\.com/(?:c|g|share)/',r'PRIVATE_PASS_LEDGER',r'(?i)(?:token|signature|credential|password)\s*[=:]\s*[A-Za-z0-9_-]{12,}',r'(?i)(?:sk-[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})']
    for p in files:
        b=p.read_bytes();require(not b.startswith(b'%PDF'),'PDF payload');require(p.suffix in {'.md','.json','.py','.txt',''} and p.name!='.DS_Store','unexpected file type '+p.name); txt=b.decode('utf8')
        if p.suffix=='.json': json.loads(txt)
        for pattern in patterns:
            if re.search(pattern,txt): markers.append({'path':str(p.relative_to(r)),'pattern':pattern})
        public.update(u.rstrip('.,;\"') for u in re.findall(r'https?://[^\s<>`\)\]]+',txt))
        if p.suffix!='.md': continue
        for m in re.finditer(r'\[[^\]\n]+\]\(([^\s)]+)(?:\s+[^)]*)?\)',txt):
            t=m.group(1)
            if urlsplit(t).scheme: continue
            if not re.search(r'\.(?:md|json|py|txt)(?:#.*)?$',t): excluded_algebra.append({'path':str(p.relative_to(r)),'target':t});continue
            q=(p.parent/unquote(t.split('#')[0])).resolve();require(q.is_relative_to(r),'escaping link '+t);require(q.is_file(),'broken link '+t);links.append({'path':str(p.relative_to(r)),'target':t,'exists':True})
    require(not markers,'restricted marker hits')
    refs=json.loads((r/'REFERENCES.json').read_text())['sources']; refrows=[]
    for s in refs:
        v={'id':s['id'],'public_url':s['public_url'],'has_retained_pdf_pin':bool(s.get('retained_pdf'))}
        if s.get('retained_pdf'):
            pin=s['retained_pdf']; matches=orig.get(pin['sha256'],[]); v.update({'sha256':pin['sha256'],'bytes':pin['bytes'],'matching_original_source_bytes_available':any(p.stat().st_size==pin['bytes'] for p in matches)})
        refrows.append(v)
    out={'status':'PASS','kind':'independent read-only packaging and preservation verification; no new mathematical pass','reader_manifest_sha256':h((r/'FILE_MANIFEST.json').read_bytes()),'reader_sha256sums_sha256':h((r/'SHA256SUMS').read_bytes()),'file_count':len(files),'manifest_members':len(listed),'checksum_entries':len(sums),'preserved_document_count':len(rows),'proof_count':sum(x['kind']=='proof' for x in records),'qualification_count':sum(x['id'].startswith('L') for x in records),'review_count':len(inv['reviews']),'transformation_count':len(transformation_rows),'check_count':len(checks),'expected_execution_count':sum(len(x['modes']) for x in checks),'intended_local_markdown_link_count':len(links),'excluded_algebraic_bracket_expressions':excluded_algebra,'local_links':links,'documents':rows,'transformations':transformation_rows,'checks':check_rows,'source_pins':refrows,'public_urls':sorted(public),'restricted_marker_hits':markers,'source_pin_limit':'An unavailable matching file is not reported as independently byte-verified; public metadata remains traceable to original records.'}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if not isinstance(v,list)},indent=2))
if __name__=='__main__': main()
