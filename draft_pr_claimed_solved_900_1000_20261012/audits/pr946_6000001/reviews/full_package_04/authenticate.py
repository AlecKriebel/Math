#!/usr/bin/env python3
"""Independent read-only scope and byte authentication. Writes only this review."""
import datetime, hashlib, json, os, pathlib, stat, subprocess, sys, zipfile
R = pathlib.Path(__file__).resolve().parent
ROOT = R.parents[4]
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = R.parents[1]
D = A / 'preprint'
HEAD = '7d3adb0e500b0414a49a449e7981d34ade329427'
FREEZE = '4a5ad29c194c353bd1a8fe502767673d8cd335e9b60b9135b88e031b03cebad3'
MANIFEST = '52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec'
INV = '6bed3df36abd6e2740664e86375e6adf441ec474e511a8b0735295629d8a2ca5'
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def run(*a): return subprocess.check_output(a, cwd=ROOT)
def need(c,m):
    if not c: raise RuntimeError(m)
def load(p): return json.loads(p.read_bytes())
def rec(p):
    b=p.read_bytes(); return {'bytes':len(b),'sha256':sha(b)}
def blob(ref,p): return run('git','show',ref+':'+p)
def gh(path): return json.loads(run('gh','api',path))
def main():
    began=utc()
    need(run('git','branch','--show-current').strip()==b'main','branch')
    need(sha((D/'FREEZE.json').read_bytes())==FREEZE,'external freeze pin')
    f=load(D/'FREEZE.json')
    need(f['revision_candidate']==4 and len(f['files'])==223 and len(f['evidence_files'])==48,'freeze counts')
    files={}
    for k,v in f['files'].items():
        x=rec(D/k); need(x==v,'candidate '+k); files[k]=x
    evidence={}
    for k,v in f['evidence_files'].items():
        x=rec(ROOT/k); need(x==v,'external evidence '+k); evidence[k]=x
    need(sha((A/'OPERATIONS_INVENTORY.json').read_bytes())==INV,'inventory pin')
    inv=load(A/'OPERATIONS_INVENTORY.json'); future={}
    for k,v in inv['files'].items():
        need(rec(ROOT/k)==v,'operation '+k)
        if pathlib.Path(k).parent.name==P.name: future[pathlib.Path(k).name]=v
    need(future==f['future_helpers'] and len(future)==6,'six helper equality')
    pr=gh('repos/AlecKriebel/Math/pulls/946')
    need(pr['number']==946 and pr['state']=='open' and pr['draft'] is True and pr['base']['ref']=='main' and pr['head']['sha']==HEAD and pr['merged_at'] is None,'live scope')
    need(pr['body'].encode()==(D/'ORIGINAL_PR_DESCRIPTION.md').read_bytes(),'unchanged original live body')
    changed=gh('repos/AlecKriebel/Math/pulls/946/files?per_page=100')
    need(pr['changed_files']==len(changed)==34,'changed paths count')
    prefix='unsolved_math_prioritization/attempts/6000001/'
    need(set(x['filename'] for x in changed)==set(load(A/'ORIGINAL_SNAPSHOT.json')['files'])|{'unsolved_math_prioritization/QUEUE.md'},'exact changed paths')
    queue=blob(HEAD,'unsolved_math_prioritization/QUEUE.md').decode()
    rows=[l for l in queue.splitlines() if l.startswith('|') and any(c.strip().split(' / ')[0]=='6000001' for c in l.split('|'))]
    need(len(rows)==1,'immutable queue row uniqueness')
    cells=[c.strip() for c in rows[0].strip('|').split('|')]
    need('claimed_solved' in cells and '4/5' in cells,'immutable exact claimed_solved scope')
    mainref=gh('repos/AlecKriebel/Math/git/ref/heads/main')['object']['sha']
    subprocess.run(['git','fetch','--no-write-fetch-head','origin',mainref],cwd=ROOT,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    catalog=json.loads(blob(mainref,'unsolved_math_prioritization/catalog.json'))
    target=[x for x in catalog if str(x.get('id'))=='6000001'];need(len(target)==1,'fresh source uniqueness');t=target[0]
    need(t['present'] is True and t['holds']==[] and t['statement_hash']=='04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd' and t['review_hash']=='f8584e1f273da5d42d94704da74c51cf5aa9f0100b44e2bc9b2096c45eabf4fb','fresh source pins')
    groups=json.loads(blob(mainref,'unsolved_math_prioritization/review_v2/related_target_groups.json'))['groups']
    membership={str(i):g for i,g in enumerate(groups) if '6000001' in [str(x) for x in g['ids']]}
    need(membership=={},'fresh related groups')
    z=zipfile.ZipFile(D/'global_hessian_verification.zip'); names=z.namelist();am=load(D/'ARCHIVE_MANIFEST.json')
    need(len(names)==len(set(names))==220 and len(am['files'])==219,'outer closure counts')
    need(set(names)==set(am['files'])|{'ARCHIVE_MANIFEST.json'},'outer closed members')
    need(z.read('ARCHIVE_MANIFEST.json')==(D/'ARCHIVE_MANIFEST.json').read_bytes(),'archive manifest')
    for k,v in am['files'].items():
        b=z.read(k);need({'bytes':len(b),'sha256':sha(b)}==v,'zip '+k)
        need(b==(D/k).read_bytes(),'zip disk '+k)
        need(z.getinfo(k).external_attr>>16==0o100644,'zip regular mode '+k)
    m=load(D/'package/PACKAGE_MANIFEST.json');need(sha((D/'package/PACKAGE_MANIFEST.json').read_bytes())==MANIFEST,'manifest external pin')
    need(len(m['files'])==207 and set(m['explicit_public_allowlist'])==set(m['files']),'inner count/allowlist')
    actual={str(p.relative_to(D/'package')) for p in (D/'package').rglob('*') if p.is_file()}
    need(actual==set(m['files'])|{'PACKAGE_MANIFEST.json'},'inner closure')
    for k,v in m['files'].items():need(rec(D/'package'/k)=={q:v[q] for q in ['bytes','sha256']},'inner '+k)
    originals={}
    for k,h in load(A/'ORIGINAL_SNAPSHOT.json')['files'].items():
        b=blob(HEAD,k);ls=run('git','ls-tree',HEAD,'--',k).decode().strip();mode,kind,tail=ls.split(' ',2);oid=tail.split('\t')[0]
        d=D/'package/original'/k;an='package/original/'+k;zb=z.read(an)
        need((A/'original'/k).read_bytes()==b and stat.S_IMODE((A/'original'/k).stat().st_mode)==0o644,'separate original disk '+k)
        need(sha(b)==h and d.read_bytes()==b==zb and mode=='100644' and kind=='blob','actual original '+k)
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid,'git blob OID '+k)
        need(stat.S_IMODE(d.stat().st_mode)==0o644 and z.getinfo(an).external_attr>>16==0o100644,'original modes')
        originals[k]={'bytes':len(b),'sha256':h,'git_blob':oid,'git_mode':mode,'disk_mode':'0644','archive_mode':'100644','disk_and_archive_match':True}
    out={'status':'PASS','utc':utc(),'started_utc':began,'original_pr_head':HEAD,'freeze_sha256':FREEZE,'package_manifest_sha256':MANIFEST,'operations_inventory_sha256':INV,'future_helpers':future,'candidate_files':files,'evidence_files':evidence,'payloads':219,'archive_members':220,'originals':originals,'inner_payloads':207,'inner_files':208,'actual_live_pr':{'number':946,'state':pr['state'],'draft':pr['draft'],'head':pr['head']['sha'],'base':pr['base']['ref'],'body_sha256':sha(pr['body'].encode()),'changed_paths':[x['filename'] for x in changed]},'immutable_queue_row':rows[0],'source_gate':{'remote_main':mainref,'present':True,'holds':[],'statement_hash':t['statement_hash'],'review_hash':t['review_hash'],'related_target_membership':membership}}
    dest=R/(sys.argv[1] if len(sys.argv)>1 else 'AUTHENTICATION_START.json');dest.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','utc':out['utc'],'destination':str(dest),'candidate':223,'evidence':48,'originals':len(originals),'source_main':mainref}))
if __name__=='__main__':main()
