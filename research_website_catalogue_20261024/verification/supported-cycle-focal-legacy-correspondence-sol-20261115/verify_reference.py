"""Pure reference authentication only; no old helper/search/science execution.
Stdlib reads; no project imports, network, subprocess, website/Git access or writes.
"""
import hashlib
import json
import os
from pathlib import Path
import stat

N=Path(__file__).absolute().parent
TERMINALS={'FINAL_SEAL.json','OWNED_MANIFEST.json'}
COUNT=0

def need(ok,why):
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(why)

def sha(b):return hashlib.sha256(b).hexdigest()

def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real input '+str(p));return p.read_bytes()

def pin(p,d):
    b=read(p);need(len(b)==d['bytes'] and sha(b)==d['SHA256'],'whole held buffer '+str(p));return b

def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary namespace root')
    files,dirs=[],[]
    def walk(d):
        with os.scandir(d) as rows:
            for e in rows:
                p=Path(e.path);r=p.relative_to(root).as_posix();m=p.lstat().st_mode
                if stat.S_ISDIR(m):dirs.append(r);walk(p)
                else:need(stat.S_ISREG(m),'reject link or special');files.append(r)
    walk(root);return sorted(files),sorted(dirs)

def main():
    r=json.loads(read(N/'REFERENCE.json'));old=Path(r['existing_pair_specific_packet_root'])
    sb=pin(old/'FINAL_SEAL.json',r['seal']);s=json.loads(sb)
    need(sha(sb)=='3756a8ddc8b671692ec7f058d597050fbdbd349be1fdd647557940e1a552480d','exact existing pair-specific seal')
    mb=pin(old/'OWNED_MANIFEST.json',r['manifest']);need(sha(mb)==s['bindings']['OWNED_MANIFEST.json']['SHA256'],'same-buffer authenticated old manifest');m=json.loads(mb)
    names=sorted(x['path'] for x in m['files']);oldterm=['FINAL_CLOSURE.json','FINAL_SEAL.json','OWNED_MANIFEST.json']
    need(extent(old)==(sorted([*names,*oldterm]),m['directories']),'whole old ordinary-file AND directory namespace')
    need(len(names)==53 and len(m['directories'])==5,'literal prior extent')
    for d in m['files']:pin(old/d['path'],d)
    for d in s['bindings'].values():pin(Path(d['path']),d)
    for key in ('report','verdict','target_identities','prior_helper_full_body_read_not_executed'):pin(Path(r[key]['path']),r[key])
    v=json.loads(pin(old/'VERDICT.json',r['verdict']));targets=json.loads(pin(old/'TARGET_IDENTITIES.json',r['target_identities']))
    need([x['record_id'] for x in targets]==['23578142','23306203'],'exact requested record pair')
    for t in targets:
        # Native JSON wrappers only, never a scientific source body or programme.
        record=json.loads(pin(Path(t['native_record_pin']['path']),t['native_record_pin']))
        ready=json.loads(pin(Path(t['SOURCE_READY_pin']['path']),t['SOURCE_READY_pin']))
        seal=json.loads(pin(Path(t['source_seal_pin']['path']),t['source_seal_pin']))
        need(str(record['id'])==t['record_id'] and record['metadata']['title']==ready['title']==t['title'] and record['metadata']['doi']==ready['DOI']==t['DOI'],'whole native record identity')
        need(seal['SOURCE_READY_SHA256']==t['SOURCE_READY_pin']['SHA256'],'original READY seal')
    need(v['docs_subtree_SHA']=='f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3' and v['whole_blob_paths']==254 and v['whole_text_representations']==260,'exact reported search extent')
    need(v['genuine_corresponding_articles_located']==0 and v['global_absence_claim'] is False and v['redirects_prepared']==[] and v['redirects_written']==[],'literal bounded negative with no redirect')
    current=json.loads(read(N/'VERDICT.json'));need(current['fresh_remote_check_performed'] is False and current['redirect_authority'] is False and current['corresponding_article_URLs']==[],'new qualified reuse only')
    sealed=(N/'FINAL_SEAL.json').exists()
    if sealed:
        ss=json.loads(read(N/'FINAL_SEAL.json'));mm=pin(N/'OWNED_MANIFEST.json',ss['manifest']);own=json.loads(mm)
        need(extent(N)==(sorted([*own['files'],*TERMINALS]),own['directories']),'exact new files/directories; only two root terminals')
        for name,d in own['files'].items():pin(N/name,d)
    print(json.dumps({'status':'PASS_REFERENCE_AUTHENTICATION_ONLY','checks':COUNT,'sealed':sealed,'old_payload_files':53,'old_directories':5,'native_record_metadata_matches':2,'prior_reported_docs_paths':254,'prior_reported_representations':260,'prior_reported_corresponding_articles':0,'fresh_remote_check':False,'whole_corpus_search_replayed':False,'old_code_executed':False,'production_mutation':False},sort_keys=True))

if __name__=='__main__':main()
