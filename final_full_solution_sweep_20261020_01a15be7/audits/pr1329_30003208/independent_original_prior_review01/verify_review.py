#!/usr/bin/env python3
"""Read-only stdlib verification of this closed independent review packet.
Does not use network, Git, source-author programs, or imports from PR/source data.
The replayed finite controls do not certify the universal mathematical theorem.
"""
import argparse,base64,gzip,hashlib,json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
G=0
def need(ok,msg):
    global G
    G+=1
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def readj(rel):return json.loads((P/rel).read_bytes())
def readgz(rel):return json.loads(gzip.decompress((P/rel).read_bytes()))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
    seal=P/'MANIFEST.json';sb=seal.read_bytes();need(sha(sb)==args.manifest_sha256,'external manifest SHA256')
    m=json.loads(sb);need(m['schema']=='closed-independent-review/v1','manifest schema')
    members=m['files'];names=[x['path'] for x in members]
    need(len(names)==len(set(names)),'no repeated inventory names')
    actual=[]
    for p in P.rglob('*'):
        need(not p.is_symlink(),'no symlinks')
        if p.is_file() and p!=seal:actual.append(p.relative_to(P).as_posix())
    need(set(names)==set(actual),'exact closed inventory; only top-level seal excluded')
    for x in members:
        rel=pathlib.PurePosixPath(x['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe inventory path')
        p=P.joinpath(*rel.parts);b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'member hash '+str(rel))
        need(x['private']==(rel.parts[0]=='private_sources'),'private body flag '+str(rel))
    need(sum(x['bytes'] for x in members)+len(sb)<8*1024*1024,'allocation cap')
    need('private_sources/' in (P/'.gitignore').read_text(),'private captures ignored')
    pins=readj('SOURCE_PINS.json');pr=readgz('private_sources/pr_files.json.gz')
    need(pins['head']=='46e2906b587bbd76091021807218e95419d3f9c0','pinned head')
    need(len(pr)==len(pins['files'])==8,'eight input blobs')
    bypath={x['path']:x for x in pr};need(len(bypath)==8,'unique source input paths')
    for x in pins['files']:
        v=bypath[x['path']];b=v['body'].encode();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        need(len(b)==x['bytes']==v['bytes'],'input body size')
        need(sha(b)==x['sha256']==v['sha256'],'input SHA256')
        need(blob==x['blob']==v['blob'],'immutable Git blob hash')
        need(x['private'] and v['private'],'source input private')
    proof=bypath['unsolved_math_prioritization/attempts/30003208/PROOF.md']['body']
    need('No separability, trace, faithfulness' in proof,'unrestricted theorem scope input')
    need('P_N F(x) P_N = P_N x P_N' in proof,'compression argument input')
    live=readj('private_sources/live_pr.json');receipt=readj('PR_CAPTURE_RECEIPT.json')
    need(live['head_sha']==pins['head']==receipt['head_sha'],'live head receipt')
    need(live['number']==1329 and live['changed_files']==8,'PR identity')
    need(sha(live['body'].encode())==receipt['body_sha256']=='ae458c41a7b85bd3c32beed1aa8e2c610120c250d6381a71939b3cfffb558356','PR body pin')
    ledger=readgz('private_sources/ledger_initial.json.gz');lr=json.loads(ledger['stdout']);lm=readj('INITIAL_LEDGER_CHECK.json')
    need(sha(ledger['stdout'].encode())==lm['sha256']=='fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1','fresh ledger receipt')
    need(lr['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','workbook')
    vr=lr['valueRanges'];need(len(vr)==1,'numeric filter single target')
    need(vr[0]['dataFilters']==[{'gridRange':{'endColumnIndex':43,'sheetId':1254632077,'startColumnIndex':0}}],'numeric gid all43')
    need(len(vr[0]['valueRange']['values'])==lm['rows']==191,'ledger rows')
    need(all(isinstance(i,int) for a in lm['leads'].values() for i in a),'public ledger metadata contains row numbers only')
    si=readj('SOURCE_INDEX.json');nsource=0;npdf=0;nblocked=0
    for x in si['entries']:
        vals=readgz(x['capture']);v=vals[x['index']];nsource+=1
        need(v['url']==x['url'] and v.get('status')==x.get('status'),'source capture locator/status')
        need(v['private'] and x['private'],'source body privacy')
        need(bool(x['read_scope']),'explicit actual reading scope')
        if 'base64' in v:
            b=base64.b64decode(v['base64'],validate=True)
            need(len(b)==v['bytes']==x['bytes'],'body byte size')
            need(sha(b)==v['sha256']==x['sha256'],'primary/metadata body pin')
            need(b.startswith(b'%PDF')==x['actual_pdf'],'actual PDF magic, not just status200')
            if x['actual_pdf']:npdf+=1
            if 'text' in v:need(sha(v['text'].encode())==x['text_sha256'],'derived exact text pin')
            else:need(not x['text_present'],'no invented extracted text')
            if not b:nblocked+=1
        else:
            need('error' in v and '403' in v['error'],'explicit inaccessible publisher capture');nblocked+=1
    need(nsource==28,'full primary source inventory')
    for fn in ['private_sources/citation_sources.json.gz','private_sources/publication_search.json.gz']:
        for v in readgz(fn):
            b=base64.b64decode(v['base64'],validate=True)
            need(len(b)==v['bytes'] and sha(b)==v['sha256'],'registry/citation exact capture')
            need(v['private'],'registry raw private')
    pub=readgz('private_sources/publication_search.json.gz');totals=[]
    for v in pub:totals.append(json.loads(base64.b64decode(v['base64']))['hits']['total'])
    need(totals==[0,1,0],'bounded public Zenodo query results')
    alias=readj('ALIASES.json');nr=readj('NO_ROW_PROPOSAL.json')
    need(alias['catalog_ids']==['30003208','30002897'] and alias['one_mathematical_result_family'],'alias dedup')
    need(alias['target_publication_doi'] is None and alias['target_zenodo_record'] is None,'no invented full-target publication')
    need(nr['cells'] is None and nr['append_authorized_in_this_packet'] is False,'no unjustified tracker row')
    need(alias['pr_url']==nr['pr_url']=='https://github.com/AlecKriebel/Math/pull/1329','exact PR identity')
    saved=[(P/f'CONTROL_RESULTS_{i}.json').read_bytes() for i in range(3)]
    need(saved[0]==saved[1]==saved[2],'normal/O/OO saved control output identity')
    need(sha(saved[0])=='dd42771b6734be444cc14a299af33d033a538360a60c0c8ccbf8035678b366ac','exact controls result pin')
    cr=json.loads(saved[0]);need(cr['explicit_guards']==82376 and cr['negative_rejections']==8,'control count')
    need(cr['author_code_executed'] is False and cr['universal_proof_from_finite_controls'] is False,'finite proof limits')
    replays=readj('CONTROL_REPLAYS.json')
    for i,flags in enumerate([[],['-O'],['-OO']]):
        rr=subprocess.run([sys.executable,'-B']+flags+[str(P/'check_controls.py')],cwd=P,capture_output=True,timeout=60)
        need(rr.returncode==0 and not rr.stderr,'fresh own-controls mode '+str(i))
        need(rr.stdout==saved[i],'fresh exact mode output '+str(i))
        rec=replays['runs'][i];need(rec['stdout_sha256']==sha(rr.stdout) and rec['stdout_bytes']==len(rr.stdout) and rec['stderr_empty'],'stored replay receipt')
    # Recheck bytes after executable replay: no writes may have occurred.
    for x in members:
        b=(P/x['path']).read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'post-replay unchanged '+x['path'])
    need(sha(seal.read_bytes())==args.manifest_sha256,'post-replay unchanged seal')
    print(json.dumps({'status':'PASS','manifest_sha256':args.manifest_sha256,'members':len(members),'private_members':sum(x['private'] for x in members),'source_captures':nsource,'actual_primary_pdfs':npdf,'inaccessible_body_captures':nblocked,'fresh_control_modes':[0,1,2],'control_guards_per_mode':cr['explicit_guards'],'integrity_guards':G,'author_code_executed':False,'universal_mathematical_proof':'written REPORT, not finite tests','service_writes':False},sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
