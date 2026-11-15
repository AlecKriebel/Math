#!/usr/bin/env python3
"""One-time local-byte reuse and identity search; no network/Git/science execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import unicodedata

A = Path(__file__).resolve().parent
P = A.parents[1]
B = P / 'redirects/nash-quotient-robinson-preflight-sol-20261115'
C = P / 'redirects/cellularization-tree-lefschetz-link-preflight-sol-20261115'
DOCS = 'f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'
if (A / 'FINAL_SEAL.json').exists():
    raise RuntimeError('immutable final already exists')

def now(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'SHA256': sha(b)}
def put(n, x):
    p = A / n
    if not p.resolve().is_relative_to(A): raise ValueError('write outside new namespace')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
def check(e):
    p = Path(e['path']); b = p.read_bytes()
    if len(b) != e['bytes'] or sha(b) != e.get('SHA256', e.get('sha256')):
        raise ValueError('input bytes changed: ' + str(p))
    return b
def git_hash(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()
def native(role):
    x = load(A / 'raw' / (role + '.json'))
    if x['result']['isError']: raise ValueError('connector error')
    return json.loads(x['result']['structuredContent']['content'])
def tree_hash(es):
    es = sorted(es, key=lambda e: (e['path'] + ('/' if e['type']=='tree' else '')).encode())
    return git_hash('tree', b''.join(str(int(e['mode'])).encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in es))
def fold(s): return unicodedata.normalize('NFKC', s).casefold().translate(str.maketrans('‐‑‒–—−', '------'))
def compact(s): return ''.join(c for c in fold(s) if c.isalnum())

external = {}
def bind(p):
    e = pin(p); external[e['path']] = e; return e

# Authenticate the previously adopted exact current corpus without importing its code.
# The actual final seal is bound literally below; its adopted root receipt is a separate input.
for q in [B/'FINAL_SEAL.json', B/'OWNED_MANIFEST.json',
          P/'redirects/root-nash-quotient-robinson-negative-adoption-20261115.json',
          C/'FINAL_SEAL.json', C/'CURRENT_BLOB_BINDINGS.json', C/'REPORT.md',
          P/'redirects/root-cellularization-tree-lefschetz-link-negative-adoption-20261115.json']:
    bind(q)
prior = load(B/'OWNED_MANIFEST.json'); se = load(B/'FINAL_SEAL.json')
check(se['bindings']['OWNED_MANIFEST.json'])
for e in prior['files']: check(e)
expected_names = {Path(e['path']).relative_to(B).as_posix() for e in prior['files']} | {'OWNED_MANIFEST.json','FINAL_CLOSURE.json','FINAL_SEAL.json'}
actual_names = {p.relative_to(B).as_posix() for p in B.rglob('*') if p.is_file()}
if actual_names != expected_names or any(p.is_symlink() for p in B.rglob('*')):
    raise ValueError('prior exact namespace changed')
for n in ['CURRENT_BODY_MANIFEST.json','SEARCH_REPRESENTATIONS.json','REUSED_EXTERNAL_BYTE_MANIFEST.json','DOCS_REUSE_PROOF.json','CORPUS_RECEIPT.json']:
    bind(B/n)

op = native('opening-main'); co = native('opening-commit'); ro = native('opening-root'); tr = native('docs-recursive')
if co['sha'] != op['object']['sha'] or ro['sha'] != co['tree']['sha'] or ro['truncated'] is not False:
    raise ValueError('opening native boundary broken')
de = [e for e in ro['tree'] if e['path']=='docs']
if len(de)!=1 or de[0]['type']!='tree' or de[0]['sha']!=DOCS or tr['sha']!=DOCS or tr['truncated'] is not False:
    raise ValueError('docs tree changed: stop reuse')
groups = {'': []}; trees = {'': DOCS}
for e in tr['tree']:
    parent, _, name = e['path'].rpartition('/')
    groups.setdefault(parent, []).append({**e, 'path': name})
    if e['type']=='tree': groups.setdefault(e['path'], []); trees[e['path']]=e['sha']
for path, es in groups.items():
    if tree_hash(es) != trees[path]: raise ValueError('tree reconstruction: '+path)
leaves = [e for e in tr['tree'] if e['type']=='blob']
current = load(B/'CURRENT_BODY_MANIFEST.json'); bc = {e['path']:e for e in current}
whole = load(C/'CURRENT_BLOB_BINDINGS.json'); wc = {e['path']:e for e in whole}
if len(leaves)!=254 or set(bc)!=set(wc) or set(bc)!={'docs/'+e['path'] for e in leaves}:
    raise ValueError('complete corpus membership changed')
body_records=[]
for e in leaves:
    p='docs/'+e['path']; old=bc[p]; w=wc[p]
    if (e['sha'], e['mode'], e['size']) != (old['blob'],old['mode'],old['bytes']): raise ValueError('current leaf mismatch')
    if (w['blob'],w['bytes'],w['SHA256']) != (old['blob'],old['bytes'],old['SHA256']): raise ValueError('prior packets disagree')
    q=Path(w['current_body_path']); b=q.read_bytes()
    if len(b)!=old['bytes'] or sha(b)!=old['SHA256'] or git_hash('blob',b)!=e['sha']:
        raise ValueError('existing whole body changed: '+p)
    body_records.append({'path':p,'mode':e['mode'],'blob':e['sha'],'bytes':len(b),'SHA256':sha(b),'reused_complete_body':bind(q)})
put('CURRENT_BLOB_BINDINGS.json',body_records)
representations=load(B/'SEARCH_REPRESENTATIONS.json')
for e in representations:
    check(e['text_file']); bind(Path(e['text_file']['path']))
    if e['blob']!=bc[e['public_path']]['blob']: raise ValueError('text-to-current-blob association')
    if e['kind']=='raw_UTF8' and git_hash('blob',check(e['text_file']))!=e['blob']: raise ValueError('raw body association')
    if e['kind']=='complete_PDF_text':
        z=e['original_whole_PDF_extract_binding']
        if z['pdf_blob']!=e['blob'] or z['pdf_sha256']!=bc[e['public_path']]['SHA256']: raise ValueError('PDF binding')
if len(representations)!=260: raise ValueError('search interface changed')
put('SEARCH_REPRESENTATIONS.json',representations)

targets=[]
for rid, textrel, expectedroot, expectedsrc in [
    ('23392409','published-pdf-text.txt','0cfd2378fcd36e8813b9f6fb37a9218d91037f1cc20a7ee143e736b8cfe382b6','388fbf673c3f14886f9da3628be04a1f7c019b0d6d1c6c936fb084d8a245d972'),
    ('23440943','inputs/published-pdf-text.txt','2778005501abc4ae691c0b17e75915edf91917f36c8180021b1a3030c5553da1','928fb2b26bd31a0678fc3954c29f8a7897a3d6352e9b5dab791224a72a828235')]:
    paper=P/'papers'/rid; ed=paper/'reviews/editorial'; sp=paper/'sources/SOURCE_READY.json'; rp=P/'verification'/('root-clearance-'+rid+'-20261115.json')
    if pin(rp)['SHA256']!=expectedroot or pin(sp)['SHA256']!=expectedsrc: raise ValueError('authority pin')
    src=load(sp); config=load(ed/'publication.json'); root=load(rp)
    check(root['original_README']); bind(Path(root['original_README']['path']))
    for q,n in [(rp,'ROOT_CLEARANCE.json'),(sp,'SOURCE_READY.json'),(ed/'publication.json','publication.json'),(ed/'SEAL.json','EDITORIAL_SEAL.json'),(ed/'MANIFEST.json','EDITORIAL_MANIFEST.json'),(ed/textrel,'published-pdf-text.txt')]:
        b=q.read_bytes(); dest=A/'target-inputs'/rid/n; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b); bind(q)
    manifest=load(ed/'MANIFEST.json')
    editorial_seal=load(ed/'SEAL.json')
    manifest_pin=dict(editorial_seal['manifest']); manifest_pin['path']=str(ed/'MANIFEST.json'); check(manifest_pin)
    # Bind actual config and extract through the exact sealed editorial manifest.
    entries=manifest.get('files',manifest.get('owned_payloads',[]))
    if not entries: raise ValueError('unknown editorial manifest interface')
    for q in [ed/'publication.json', ed/textrel]:
        found=[e for e in entries if (e.get('path')==str(q) or e.get('path')==q.relative_to(ed).as_posix() or e.get('relative_path')==q.relative_to(ed).as_posix())]
        if len(found)!=1: raise ValueError('missing editorial manifest item '+str(q))
        z=dict(found[0]); z['path']=str(q); check(z)
    identity={k:config[k] for k in ['title','slug','doi','publication_date','version','printed_version','canonical_url','AA','proposed_canonical_url','pdf_filename','supplement_filename'] if k in config}
    if identity['title']!=src['title'] or identity['doi']!=src['DOI'] or config['canonical_url'] is not None or config['AA'] is not None:
        raise ValueError('target identity or historical publication boundary')
    assets=[]
    for asset in src['all_native_assets_in_original_order']:
        b=check(asset); bind(Path(asset['path']))
        if hashlib.md5(b).hexdigest()!=asset['original_api_file_object']['checksum'].split(':')[1]: raise ValueError('native asset checksum')
        assets.append({'whole_original_source_asset':asset,'current_docs_equal_whole_assets':[e for e in body_records if (e['bytes'],e['SHA256'])==(asset['bytes'],asset['SHA256'])]})
    targets.append({'record_id':rid,'sheet_row':src['sheet_row'],'literal_config_identity':identity,'source_version_field_present':src['version_field_present'],'native_conceptrecid_whole_field':src['native_conceptrecid_whole_field'],'whole_original_native_assets_in_original_order':src['all_native_assets_in_original_order'],'native_asset_comparisons':assets,'authoritative_root_clearance':bind(rp),'source_ready':bind(sp),'sealed_editorial_config':bind(ed/'publication.json'),'sealed_editorial_seal':bind(ed/'SEAL.json'),'existing_complete_PDF_text_read_for_identity_only':bind(ed/textrel),'future_proposal_only_not_live_canonical_or_AA':True})
put('TARGET_IDENTITIES.json',targets)

specs={
 '23392409': [('distinctive_alias',r'five[ _-]+(?:outgoing[ _-]+)?cent(?:er|re)s|16[ _-]+realization|five_centers|five-outgoing-centers-alpha16'),('subject_source_control',r'cube[ _-]+(?:moves?|flips?)|miquel|ramassamy|melotti|th[eé]venin|10\.4171/aihpd/163')],
 '23440943': [('distinctive_alias',r'totally[ _-]+mixed|mixed[ _-]+face[ _-]+posets?|30004231|owr[ _-]*17135[ _-]*028'),('subject_source_control',r'\bpayne\b|shellab|minkowski[ _-]+(?:sums?|addition)|d[ _-]?4\s*[×x]\s*i')]
}
queries=[]
for t in targets:
    rid=t['record_id']; c=t['literal_config_identity']
    queries += [{'record_id':rid,'tier':'record_DOI_concept','mode':'regex','pattern':'|'.join(re.escape(s) for s in [rid,str(t['native_conceptrecid_whole_field']['original_value']),c['doi']])}, {'record_id':rid,'tier':'exact_title_compact','mode':'compact_literal','pattern':compact(c['title'])}]
    queries += [{'record_id':rid,'tier':tier,'mode':'regex','pattern':pattern} for tier,pattern in specs[rid]]
put('QUERY_DEFINITIONS.json',{'normalization':'NFKC/casefold/six dash variants; exact title additionally drops nonalphanumeric characters','queries':queries})
hits=[]; paths=[]
def search(text, rep):
    f=fold(text); cp=compact(text)
    for q in queries:
        matches=list(re.finditer(re.escape(q['pattern']) if q['mode']=='compact_literal' else q['pattern'],cp if q['mode']=='compact_literal' else f))
        if matches:
            hits.append({'record_id':q['record_id'],'tier':q['tier'],'representation':rep,'match_count':len(matches),'all_matches':[{'normalized_start':m.start(),'matched':m.group(),'context':(cp if q['mode']=='compact_literal' else f)[max(0,m.start()-350):m.end()+550]} for m in matches]})
for rep in representations: search(check(rep['text_file']).decode('utf8'),rep)
for e in body_records:
    for q in queries:
        s=compact(e['path']) if q['mode']=='compact_literal' else fold(e['path'])
        m=list(re.finditer(re.escape(q['pattern']) if q['mode']=='compact_literal' else q['pattern'],s))
        if m: paths.append({'record_id':q['record_id'],'tier':q['tier'],'public_path':e['path'],'matches':[x.group() for x in m]})
put('SEARCH_RESULTS.json',{'UTC':now(),'representations_searched':len(representations),'all_complete_representations_searched':True,'hits':hits})
put('PATHNAME_SEARCH_RESULTS.json',{'paths_searched':len(body_records),'hits':paths})
compact_signatures={
 '23392409':['five outgoing centers','five centers','16-realization','cube moves','alpha-realizations','23392409','23392408'],
 '23440943':['totally mixed','mixed face poset','30004231','OWR-17135-028','23440943','23440942']}
compact_hits=[]
for rep in representations:
    s=compact(check(rep['text_file']).decode('utf8'))
    for rid, signatures in compact_signatures.items():
        for signature in signatures:
            if compact(signature) in s: compact_hits.append({'record_id':rid,'signature':signature,'representation':rep})
put('PUNCTUATION_INSENSITIVE_SEARCH.json',{'mechanism':'NFKC/casefold then all nonalphanumerics removed; each entire representation searched','signatures':compact_signatures,'representations':len(representations),'hits':compact_hits,'second_search_mechanism_not_independent_reviewer':True})
put('INPUT_MANIFEST.json',{'UTC':now(),'files':list(external.values()),'no_new_PDF_text_extractions':True,'no_new_native_asset_GETs':True,'no_old_helper_imports_or_execution':True})
put('CORPUS_RECEIPT.json',{'UTC':now(),'docs_tree':DOCS,'opening_main':op['object']['sha'],'opening_root':ro['sha'],'recursive_entries':len(tr['tree']),'whole_blob_path_occurrences':len(body_records),'unique_blobs':len({e['blob'] for e in body_records}),'whole_body_bytes_path_occurrences':sum(e['bytes'] for e in body_records),'all_native_tree_hashes_reconstructed':len(groups),'complete_text_representations':len(representations),'raw_UTF8':sum(e['kind']=='raw_UTF8' for e in representations),'decoded_HTML':sum(e['kind']=='decoded_HTML' for e in representations),'PDF_text_path_occurrences':sum(e['kind']=='complete_PDF_text' for e in representations),'unique_PDF_text_files':len({e['text_file']['path'] for e in representations if e['kind']=='complete_PDF_text'}),'PDF_pages_path_occurrences_not_new_full_reading':sum(e.get('pages',0) for e in representations),'new_PDF_extractions':0,'new_network_body_acquisitions_of_corpus_or_native_assets':0,'opaque_binary_paths_without_prose_search':sorted(set(bc)-{e['public_path'] for e in representations}),'archive_expansions':0,'hit_rows':len(hits),'pathname_hits':len(paths),'native_asset_exact_matches':sum(len(a['current_docs_equal_whole_assets']) for t in targets for a in t['native_asset_comparisons'])})
print(json.dumps({'status':'LOCAL_BYTE_REUSE_AND_IDENTITY_SEARCH_COMPLETE','hit_rows':len(hits),'pathname_hits':len(paths),'hits':[{'record':h['record_id'],'tier':h['tier'],'path':h['representation']['public_path'],'kind':h['representation']['kind'],'matches':h['match_count']} for h in hits]},indent=2))
