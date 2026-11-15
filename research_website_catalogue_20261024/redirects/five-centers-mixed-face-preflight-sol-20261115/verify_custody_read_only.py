#!/usr/bin/env python3
"""Pure bounded correspondence closure: standard library reads only, no scientific replay."""
from pathlib import Path
import hashlib
import json
import re
import sys
import unicodedata

A=Path(__file__).resolve().parent
TERMINALS={'OWNED_MANIFEST.json','FINAL_CLOSURE.json','FINAL_SEAL.json'}
DOCS='f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3'
checks=0
def need(condition, message):
    global checks
    checks+=1
    if not condition: raise ValueError(message)
def load(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
def check(e):
    p=Path(e['path']); b=p.read_bytes()
    need(not p.is_symlink(),'symlink input '+str(p))
    need(len(b)==e['bytes'] and sha(b)==e.get('SHA256',e.get('sha256')),'byte binding '+str(p))
    return b
def git(kind,b): return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def native(role):
    x=load(A/'raw'/(role+'.json'))
    need(x['role']==role and x['result']['isError'] is False,'actual connector result '+role)
    return json.loads(x['result']['structuredContent']['content'])
def tree_hash(es):
    es=sorted(es,key=lambda e:(e['path']+('/' if e['type']=='tree' else '')).encode())
    return git('tree',b''.join(str(int(e['mode'])).encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in es))
def fold(s): return unicodedata.normalize('NFKC',s).casefold().translate(str.maketrans('‐‑‒–—−','------'))
def compact(s): return ''.join(c for c in fold(s) if c.isalnum())
def main():
    preseal=sys.argv[1:]==['--preseal']
    need(preseal or not sys.argv[1:],'only --preseal is accepted')
    need(preseal or (A/'FINAL_SEAL.json').is_file(),'default requires final seal')
    owned=load(A/'OWNED_MANIFEST.json')
    need(owned['exact_root_relative_terminal_exclusions']==sorted(TERMINALS),'exact terminal exclusions')
    for e in owned['files']: check(e)
    payloads={Path(e['path']).relative_to(A).as_posix() for e in owned['files']}
    need(len(payloads)==len(owned['files']),'no duplicate payload paths')
    actual={p.relative_to(A).as_posix() for p in A.rglob('*') if p.is_file()}
    need(not any(p.is_symlink() for p in A.rglob('*')),'no owned symlinks')
    expected=payloads|{'OWNED_MANIFEST.json'}
    if preseal: expected|={n for n in ['FINAL_CLOSURE.json','FINAL_SEAL.json'] if (A/n).exists()}
    else: expected|={'FINAL_CLOSURE.json','FINAL_SEAL.json'}
    need(actual==expected,'complete exact owner namespace')
    if not preseal:
        seal=load(A/'FINAL_SEAL.json')
        need(seal['status']=='FINAL_BOUNDED_NEGATIVES_NO_REDIRECT_AUTHORITY','literal final disposition')
        for e in seal['bindings'].values(): check(e)
        need(seal['redirect_or_publication_or_canonical_or_AA_authority'] is False,'no promotion authority')
    for e in load(A/'INPUT_MANIFEST.json')['files']: check(e)
    # The reused primary packet is also closed as an exact namespace, not basename-filtered.
    p=Path(load(A/'REUSE_AUTHENTICATION.json')['prior_current_packet']['path']).parent
    prior=load(p/'OWNED_MANIFEST.json'); ps=load(p/'FINAL_SEAL.json')
    check(ps['bindings']['OWNED_MANIFEST.json'])
    for e in prior['files']: check(e)
    need({q.relative_to(p).as_posix() for q in p.rglob('*') if q.is_file()}=={Path(e['path']).relative_to(p).as_posix() for e in prior['files']}|{'OWNED_MANIFEST.json','FINAL_CLOSURE.json','FINAL_SEAL.json'},'prior exact namespace')
    need(not any(q.is_symlink() for q in p.rglob('*')),'prior symlink absence')
    op,oc,ot=native('opening-main'),native('opening-commit'),native('opening-root')
    cp,cc,ct=native('closing-main'),native('closing-commit'),native('closing-root')
    for ref,commit,root in [(op,oc,ot),(cp,cc,ct)]:
        need(ref['ref']=='refs/heads/main' and ref['object']['type']=='commit','actual main ref')
        need(ref['object']['sha']==commit['sha'] and commit['tree']['sha']==root['sha'],'actual commit-root chain')
        need(root['truncated'] is False,'complete root response')
        es=[e for e in root['tree'] if e['path']=='docs']
        need(len(es)==1 and es[0]['type']=='tree' and es[0]['sha']==DOCS,'same docs subtree at boundary')
    tree=native('docs-recursive')
    need(tree['sha']==DOCS and tree['truncated'] is False,'complete native recursive docs tree')
    groups={'':[]}; hashes={'':DOCS}
    for e in tree['tree']:
        parent,_,name=e['path'].rpartition('/')
        groups.setdefault(parent,[]).append({**e,'path':name})
        if e['type']=='tree': groups.setdefault(e['path'],[]);hashes[e['path']]=e['sha']
    for path,es in groups.items(): need(tree_hash(es)==hashes[path],'native tree SHA '+path)
    current=load(A/'CURRENT_BLOB_BINDINGS.json'); by={e['path']:e for e in current}
    leaves=[e for e in tree['tree'] if e['type']=='blob']
    need(len(leaves)==254 and len(current)==254 and set(by)=={'docs/'+e['path'] for e in leaves},'entire 254 leaf membership')
    for e in leaves:
        b=by['docs/'+e['path']]; raw=check(b['reused_complete_body'])
        need((b['blob'],b['mode'],b['bytes'])==(e['sha'],e['mode'],e['size']),'typed leaf association')
        need(sha(raw)==b['SHA256'] and git('blob',raw)==b['blob'],'whole current Git blob')
    reps=load(A/'SEARCH_REPRESENTATIONS.json')
    need(len(reps)==260,'complete search interface')
    need({k:sum(e['kind']==k for e in reps) for k in ['raw_UTF8','decoded_HTML','complete_PDF_text']}=={'raw_UTF8':137,'decoded_HTML':47,'complete_PDF_text':76},'representation kinds')
    need(sum(e.get('pages',0) for e in reps)==854,'inherited page occurrence count')
    queries=load(A/'QUERY_DEFINITIONS.json')['queries']; actual_hits=[]
    for rep in reps:
        s=check(rep['text_file']).decode('utf8'); f=fold(s); c=compact(s)
        need(rep['blob']==by[rep['public_path']]['blob'],'representation-current blob identity')
        if rep['kind']=='raw_UTF8': need(git('blob',s.encode())==rep['blob'],'raw representation blob')
        if rep['kind']=='complete_PDF_text':
            z=rep['original_whole_PDF_extract_binding']
            need(z['pdf_blob']==rep['blob'] and z['pdf_sha256']==by[rep['public_path']]['SHA256'],'whole PDF-extract association')
        for q in queries:
            ms=list(re.finditer(re.escape(q['pattern']) if q['mode']=='compact_literal' else q['pattern'],c if q['mode']=='compact_literal' else f))
            if ms: actual_hits.append((q['record_id'],q['tier'],rep['public_path'],rep['kind'],len(ms)))
    saved=load(A/'SEARCH_RESULTS.json')
    need(actual_hits==[(h['record_id'],h['tier'],h['representation']['public_path'],h['representation']['kind'],h['match_count']) for h in saved['hits']],'complete search replay')
    need(len(actual_hits)==2 and all(h[0]=='23440943' and h[1]=='subject_source_control' for h in actual_hits),'only broad surname controls')
    path_hits=[]
    for e in current:
        for q in queries:
            s=compact(e['path']) if q['mode']=='compact_literal' else fold(e['path'])
            if re.search(re.escape(q['pattern']) if q['mode']=='compact_literal' else q['pattern'],s): path_hits.append((q['record_id'],e['path']))
    need(path_hits==[] and load(A/'PATHNAME_SEARCH_RESULTS.json')['hits']==[],'all path searches negative')
    extra=load(A/'PUNCTUATION_INSENSITIVE_SEARCH.json'); ch=[]
    for rep in reps:
        s=compact(check(rep['text_file']).decode('utf8'))
        for rid,signatures in extra['signatures'].items():
            for signature in signatures:
                if compact(signature) in s: ch.append((rid,signature,rep['public_path']))
    need(ch==[] and extra['hits']==[],'punctuation-insensitive identity search')
    targets=load(A/'TARGET_IDENTITIES.json')
    need([t['record_id'] for t in targets]==['23392409','23440943'],'exact two targets')
    for t in targets:
        rid=t['record_id']; c=load(A/'target-inputs'/rid/'publication.json'); s=load(A/'target-inputs'/rid/'SOURCE_READY.json')
        need(t['literal_config_identity']['title']==s['title']==c['title'],'title identity')
        need(c['canonical_url'] is None and c['AA'] is None and c['proposed_canonical_url'] is None,'literal historical nulls retained')
        need(t['source_version_field_present'] is (rid=='23440943'),'missing versus present native version')
        need(c['version']==('1.0.0' if rid=='23440943' else None),'literal version')
        need(c['slug']==('totally-mixed-face-posets' if rid=='23440943' else 'five-outgoing-centers-alpha16'),'proposal-only slug')
        for a in t['native_asset_comparisons']:
            asset=a['whole_original_source_asset']; raw=check(asset)
            need(hashlib.md5(raw).hexdigest()==asset['original_api_file_object']['checksum'].split(':')[1],'native MD5')
            equal=[e for e in current if (e['bytes'],e['SHA256'])==(asset['bytes'],asset['SHA256'])]
            need(equal==a['current_docs_equal_whole_assets']==[],'no exact native asset present')
    verdict=load(A/'VERDICT.json')
    need(verdict['redirects_prepared']==[] and verdict['genuine_corresponding_articles_located']==0,'literal bounded verdict')
    need(verdict['global_history_archive_or_image_absence_claim'] is False,'bounded limits')
    exclusions=load(A/'EXCLUSIONS.json')
    need(len(exclusions['items'])==2 and all(x['corresponding_target_article'] is False for x in exclusions['items']),'both concrete false hits disposed')
    print(json.dumps({'status':'PASS_PURE_READ_ONLY_CORRESPONDENCE_CLOSURE','mode':'preseal' if preseal else 'final','checks':checks,'current_whole_blob_paths':254,'complete_text_representations':260,'PDF_text_path_occurrences':76,'new_PDF_extractions':0,'genuine_corresponding_articles':0,'network_requests':0,'writes':0,'subprocesses':0,'project_imports':0,'scientific_programmes_executed':0},indent=2))
if __name__=='__main__': main()
