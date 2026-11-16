"""Source-only reference intake and exact candidate oracle. No old code or live reads."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import os
import stat

N=Path(__file__).absolute().parent
P=N.parent.parent
V=P/'verification'

def need(ok,why):
    if not ok:raise ValueError(why)

def read(p):
    need(p.is_relative_to(P) and '.git' not in p.parts and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary source-only input')
    return p.read_bytes()

def desc(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def extent(root):
    files,dirs=[],[]
    def walk(d):
        for e in os.scandir(d):
            q=Path(e.path);r=q.relative_to(root).as_posix();m=q.lstat().st_mode
            if stat.S_ISDIR(m):dirs.append(r);walk(q)
            else:need(stat.S_ISREG(m),'no link/special');files.append(r)
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary source root');walk(root)
    return sorted(files),sorted(dirs)

def new(name,value):
    with (N/name).open('xb') as f:f.write((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())

def main():
    auth=V/'root-supported-cycle-focal-v2-adoption-20261115.json';ab=read(auth)
    need(desc(ab)=={'bytes':24418,'SHA256':'408b6cb8660952c23e54f803d543eb82d3f226338371558871c76e59701cbc20'},'actual root408b adoption')
    a=json.loads(ab);need(a['root_complete_current_code_and_output_adopted'] is True and a['separate_bounded_production_mechanism_preparation_authorized'] is True and a['production_installation_authorized'] is False,'preparation only')
    specs=[('supported-cycle-focal-private-stage-sol-20261115','edf8e4e64ea345e950f6d94e678b4d6c8530df37089e80ef6681a519b7fedf54','OWNED_MANIFEST.json','old'),('supported-cycle-focal-independent-code-audit-sol-20261115','780e71570c61a0604c582b2a851b4fe8165105652ddf46446c06182995f36412','FINAL_MANIFEST.json','old_audit'),('supported-cycle-focal-private-stage-v2-sol-20261115','e3cdadbcddc446632a52e21b7d5d9f2b9de4901c62cb065770bdc5c1186700f6','OWNED_MANIFEST.json','v2'),('supported-cycle-focal-v2-integration-audit-sol-20261115','a5f46ca67692ebe8d67a25a54a5ebb3663adb66d685fdd653b6805162da28ca9','MANIFEST.json','audit')]
    packets=[]
    for folder,expected,mname,kind in specs:
        root=V/folder;sb=read(root/'FINAL_SEAL.json');need(desc(sb)['SHA256']==expected,'same-buffer exact prior seal');s=json.loads(sb);mb=read(root/mname)
        mh=s['MANIFEST_SHA256'] if kind=='old_audit' else s['manifest']['SHA256'] if kind in ('old','audit') else s['manifest_SHA256']
        need(desc(mb)['SHA256']==mh,'same-buffer actual manifest');m=json.loads(mb)
        rows=m['payloads'] if kind in ('old','v2') else {r['path']:{k:r[k] for k in ('bytes','SHA256')} for r in m['files']}
        need(extent(root)==(sorted(list(rows)+[mname,'FINAL_SEAL.json']),m['directories']),'strict whole old/audit/V2 namespace')
        for n,r in rows.items():need(desc(read(root/n))=={k:r[k] for k in ('bytes','SHA256')},'whole retained reference')
        packets.append({'root':str(root),'kind':kind,'seal_name':'FINAL_SEAL.json','seal':desc(sb),'manifest_name':mname,'manifest':desc(mb),'payload_files':len(rows),'directories':m['directories']})
    old=V/specs[0][0];stage=V/specs[2][0];source=json.loads(read(old/'SOURCE_INPUTS.json'));mapping={r['path']:r for r in source['files']}
    originals={};namespaces={}
    for r in source['files']:
        b=read(Path(r['path']));need(b==read(old/r['blob']) and desc(b)=={k:r[k] for k in ('bytes','SHA256')},'actual source/context whole identity');originals[r['path']]={'path':r['path'],**desc(b)}
    for ns in source['complete_original_namespaces']:namespaces[ns['path']]=ns
    for rid in ('23578142','23306203'):
        e=P/'papers'/rid/'reviews/editorial';protected=json.loads(read(old/mapping[str(e/'PROTECTED_INPUTS.json')]['blob']))
        need(len(protected['core_files'])==18,'qualified17original plus405b')
        for r in protected['files']:
            b=read(Path(r['path']));need(desc(b)=={k:r[k] for k in ('bytes','SHA256')},'actual frozen source/science/root/core');originals[r['path']]={'path':r['path'],**desc(b)}
        for ns in protected['whole_original_namespaces']:namespaces[ns['path']]=ns
    for root,ns in namespaces.items():need(extent(Path(root))==(ns['files'],ns['directories']),'every complete source/editorial/science/root namespace')
    oracle=[]
    for r in a['adopted_exact10_manifest']['files']:
        n=r['path'];b=read(stage/'candidate-a/public'/n);need(b==read(stage/'candidate-b/public'/n) and desc(b)=={k:r[k] for k in ('bytes','SHA256')},'root-adopted exact whole output oracle')
        oracle.append({'path':n,'source':str(stage/'candidate-a/public'/n),**desc(b),'action':'replace' if n in ('research/index.html','research/sitemap.xml') else 'add'})
    need(len(oracle)==10 and sum(r['action']=='add' for r in oracle)==8,'exact10 eightleaves/twoaggregates')
    new('INPUT_ORACLE.json',{'UTC':datetime.now(timezone.utc).isoformat(),'root_adoption':{'path':str(auth),**desc(ab)},'closed_reference_packets':packets,'frozen_original_files':list(originals.values()),'closed_original_namespaces':list(namespaces.values()),'exact10':oracle,'old_baseline_reference':str(old/'WEBSITE_BASELINE.json'),'raw_index_reference':str(old/'private/shared-index.before'),'prior_qualified_pattern':{'root':str(V/'five-centers-mixed-face-production-integration-preparation-v2-sol-20261115'),'six_bodies_read_bytes':76890},'corpus_copied':False,'production_authority':False,'native_context_only':107})
    new('INITIAL_EXPECTATIONS.json',{'UTC':datetime.now(timezone.utc).isoformat(),'claim':'Prepare only exact10 installer/checkedcommit/surgicalsharedindex/guardednonforcepush mechanism; never execute production during preparation.','stage_full_root_adopted':True,'new_mechanism_root_adopted':False,'future_root_install_and_separate_commitapproval_required':True,'baseline':[623,94,95],'proposal':[631,96,97],'actual_expected_BASE':'0880af3e389248dbcd098ac275a880d93e09ea99','actual_expected_index':'35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6','actual_expected_raw_records':58563,'protected_records':58561,'unrelated_public_paths':621,'false_template_authorities':True,'no_future_prefix_exemptions':True,'finite_external_runtime_only_after_actualrootauthority':True,'no_W_read_yet':True,'production_authority':False,'AA':None,'canonical_url':None,'follow_up':None,'completion_percent':20})
    new('INITIAL_SEAL.json',{'UTC':datetime.now(timezone.utc).isoformat(),'INPUT_ORACLE':desc(read(N/'INPUT_ORACLE.json')),'INITIAL_EXPECTATIONS':desc(read(N/'INITIAL_EXPECTATIONS.json')),'before_mechanism_authoring_and_live_reads':True,'production_authority':False})
    print(json.dumps({'status':'INITIAL_REFERENCE_AND_EXACT10_ORACLE_FROZEN','original_files':len(originals),'closed_original_namespaces':len(namespaces),'closed_packets':len(packets),'oracle_outputs':len(oracle),'no_live_reads_or_corpuscopy':True}))

if __name__=='__main__':main()
