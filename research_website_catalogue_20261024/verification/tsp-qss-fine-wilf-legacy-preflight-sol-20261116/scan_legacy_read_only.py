#!/usr/bin/env python3
"""Offline read-only fixed139/140/141 identity lookup; no project-code imports.
Authenticates whole old bytes/text by reference, never old findings or helpers.
No network, Git, PDF extraction, writes, science tests or redirect operation.
"""
from pathlib import Path, PurePosixPath
from collections import Counter
import hashlib, json, re, stat, sys, unicodedata
A = Path(__file__).resolve().parent

def need(ok, why):
    if not ok: raise ValueError(why)
def whole(p):
    p = Path(p)
    need(p.is_absolute() and '..' not in p.parts and all(not q.is_symlink() for q in (p,) + tuple(p.parents)), 'ordinary absolute reference')
    need(stat.S_ISREG(p.stat().st_mode), 'regular reference')
    return p.read_bytes()
def load(p): return json.loads(whole(p))
def check(r):
    b = whole(r['path'])
    need(len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r.get('SHA256', r.get('sha256')), 'whole pin: ' + r['path'])
    return b
def obj(kind,b): return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tree(entries):
    need(len(entries) == len({e['path'] for e in entries}), 'unique tree names')
    b = b''
    for e in sorted(entries, key=lambda e: (e['path']+('/' if e['type']=='tree' else '')).encode()):
        need('/' not in e['path'] and e['path'] not in ('','.','..') and e['type'] in ('tree','blob'), 'direct tree entry')
        b += e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha'])
    return obj('tree',b)
def norm(s): return ''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if c.isalnum())
def queries(text,t):
    compact = norm(text)
    return {'exact':[s for s in t['exact_queries'] if s.casefold() in text.casefold()],
            'normalized':[s for s in t['normalized_aliases'] if norm(s) in compact],
            'whole_word':[s for s in t['case_insensitive_whole_word_aliases'] if re.search(r'(?<!\w)'+re.escape(s)+r'(?!\w)',text,re.I)]}
def actual(name):
    w = load(A/name)
    need(w['actual_tool']=='mcp__codex_apps__github_fetch' and w['whole_returned_wrapper']['isError'] is False, 'actual public GitHub read')
    need(w['whole_returned_wrapper']['structuredContent']['url']==w['actual_URL'], 'actual returned URL')
    return json.loads(w['whole_returned_wrapper']['structuredContent']['content'])

def main():
    need(not sys.argv[1:], 'offline read-only default only')
    check({'path':str(A/'INITIAL_SEAL.json'),'bytes':419,'SHA256':'e0adb981048dea328aea3dc67b17fd3aa6f54ced39a7d275e378ea950e5e8bfe'})
    initial = json.loads(check(load(A/'INITIAL_SEAL.json')['initial']))
    targets = initial['targets']
    need([(t['record_id'],t['sheet_row']) for t in targets]==[('23204250',139),('23133607',140),('23130727',141)], 'fixed targets')
    for t in targets:
        s,n,r = (json.loads(check(t[k])) for k in ('source_ready','native_record','root_editorial_adoption'))
        need(str(s['record_id'])==t['record_id'] and s['sheet_row']==t['sheet_row'] and all(s[k]==v for k,v in t['identity'].items()), 'source identity/date/version')
        need(n['metadata']['description']==t['native_description_whole'] and [f['key'] for f in n['files']]==t['native_asset_keys_in_order'], 'whole native identity context')
        need(r['status']==t['root_editorial_status'] and r['proposed_slug']==t['future_target_path_proposal'], 'root proposal identity')
    branch,root = actual('open-branch.connector.json'),actual('open-root.connector.json')
    need(branch['name']=='main' and branch['commit']['sha'].startswith(initial['root_supplied_main_prefix_before_observation']), 'opening main identity')
    need(root['sha']==branch['commit']['commit']['tree']['sha'] and root['truncated'] is False and tree(root['tree'])==root['sha'], 'complete actual root')
    docs = [e for e in root['tree'] if e['path']=='docs']
    need(len(docs)==1 and docs[0]['type']=='tree' and docs[0]['sha']==initial['previous_docs_subtree_reference_only'], 'current docs subtree unchanged')
    corpus = json.loads(check(initial['corpus_interface_reference']))
    need(corpus['current_docs_subtree']==corpus['docs_tree_reconstructed']==docs[0]['sha'], 'exact reusable corpus')
    refs = {Path(r['path']).name:r for r in corpus['reference_bindings']}
    need(len(refs)==len(corpus['reference_bindings'])==5, 'finite corpus references')
    for r in refs.values(): check(r)
    blobs,reps = corpus['whole_blob_bindings'],corpus['whole_text_representations']
    need(blobs==json.loads(check(refs['CURRENT_BLOB_BINDINGS.json'])) and reps==json.loads(check(refs['SEARCH_REPRESENTATIONS.json'])), 'complete original body/text interfaces')
    recursive = json.loads(json.loads(check(refs['docs-recursive.json']))['result']['structuredContent']['content'])
    need(recursive['sha']==docs[0]['sha'] and recursive['truncated'] is False, 'complete recursive docs object')
    children = {}
    for e in recursive['tree']:
        p = PurePosixPath(e['path']);need(not p.is_absolute() and '..' not in p.parts, 'safe recursive path')
        parent = '' if str(p.parent)=='.' else str(p.parent)
        children.setdefault(parent,[]).append({**e,'path':p.name})
    for e in recursive['tree']:
        if e['type']=='tree': need(tree(children[e['path']])==e['sha'], 'reconstructed child tree')
    need(tree(children[''])==docs[0]['sha'], 'reconstructed docs root')
    bypath = {r['path']:r for r in blobs};native = [e for e in recursive['tree'] if e['type']=='blob']
    need(len(blobs)==len(bypath)==len(native)==254 and len(reps)==260 and set(bypath)=={'docs/'+e['path'] for e in native}, 'complete254paths/260representations')
    for e in native:
        r = bypath['docs/'+e['path']];b = check(r['reused_complete_body'])
        need(obj('blob',b)==r['blob']==e['sha'] and len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['SHA256'] and r['mode']==e['mode'], 'whole immutable blob/mode/size')
    hits,pathhits = [],[]
    for r in reps:
        b = check(r['text_file']);text = b.decode('utf-8')
        need(r['public_path'] in bypath and r['blob']==bypath[r['public_path']]['blob'], 'text belongs to current blob')
        if r['kind']=='raw_UTF8': need(obj('blob',b)==r['blob'], 'entire original UTF8')
        if r['kind']=='complete_PDF_text':
            ex = r['original_whole_PDF_extract_binding']
            need(ex['pdf_blob']==r['blob'] and ex['pdf_sha256']==bypath[r['public_path']]['SHA256'] and check(ex)==b, 'historical PDF text provenance; identity only')
        for t in targets:
            q = queries(text,t)
            if any(q.values()): hits.append({'record_id':t['record_id'],'public_path':r['public_path'],'kind':r['kind'],'blob':r['blob'],'matched':q,'text_reference':r['text_file'],'whole_original_body_reference':bypath[r['public_path']]['reused_complete_body']})
    for p in sorted(bypath):
        for t in targets:
            q = queries(p,t)
            if any(q.values()): pathhits.append({'record_id':t['record_id'],'public_path':p,'matched':q})
    html = {p for p in bypath if p.casefold().endswith(('.html','.htm'))}
    need(len(html)==47 and all(sorted(r['kind'] for r in reps if r['public_path']==p)==['decoded_HTML','raw_UTF8'] for p in html), 'all47HTML complete raw/decoded coverage')
    print(json.dumps({'status':'BOUNDED_SCAN_COMPLETE','commit':branch['commit']['sha'],'root_tree':root['sha'],'root_entries':len(root['tree']),'docs_subtree':docs[0]['sha'],'docs_tree_objects':1+sum(e['type']=='tree' for e in recursive['tree']),
      'whole_paths':254,'complete_text_representations':260,'representation_kinds':dict(Counter(r['kind'] for r in reps)),'HTML_paths':47,'text_paths':len({r['public_path'] for r in reps}),'opaque_paths':len(set(bypath)-{r['public_path'] for r in reps}),
      'hits':hits,'pathname_hits':pathhits,'writes':0,'network_Git_new_PDF_extraction_or_science_tests':False},ensure_ascii=False,sort_keys=True))

if __name__=='__main__': main()
