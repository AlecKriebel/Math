"""Independent closed archive and exact captured750-stage replay, read-only."""
from pathlib import Path
import collections, datetime, hashlib, io, json, os, shutil, subprocess, sys, zipfile, zlib
sys.dont_write_bytecode=True
HERE=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1080_11000150/root_reproduction/whole04_20261016');BASE=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1080_11000150');D=BASE/'preprint_v1_0';K=D/'verification_kit';R=BASE/'repairs/archive_wording01'
def need(x,s):
    if not x:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p):return json.loads(p.read_text())
def matches(p,r):return p.is_file() and not p.is_symlink() and p.stat().st_size==r.get('bytes',r.get('size')) and sha(p)==r['sha256']
def main():
    pins=obj(R/'CURRENT_INPUT_PINS.json')['files'];need(len(pins)==750,'stage750 count')
    stage=HERE/'captured750';stage.mkdir()
    for r in pins:
        p=BASE/r['path'];need(matches(p,r),'current captured750 pin '+r['path'])
        q=stage/r['path'];q.parent.mkdir(parents=True,exist_ok=True);os.link(p,q)
    copied=[]
    for p in R.rglob('*'):
        if not p.is_file() or p.is_symlink():continue
        q=stage/p.relative_to(BASE);q.parent.mkdir(parents=True,exist_ok=True);os.link(p,q)
        copied.append({'path':str(p.relative_to(BASE)),'bytes':p.stat().st_size,'sha256':sha(p)})
    argv=[sys.executable,'-B','-I',str(stage/'repairs/archive_wording01/verify_repair.py'),'--check']
    result=subprocess.run(argv,cwd=stage,capture_output=True,text=True,timeout=120)
    (HERE/'CAPTURED750_CHECK_RECEIPT.json').write_text(json.dumps({'argv':argv,'cwd':str(stage),'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'scope':'Exact captured750 paths, each current logical byte rehashed before hardlinking; completed immutable repair artifacts hardlinked separately. --check is read-only. New ROOT and review records intentionally outside historical750. No patch to checker or canonical stage.'},indent=2)+'\n')
    need(result.returncode==0,'captured750 sealed read-only stage replay')
    names=obj(K/'ALLOWLIST.json')['members'];manifest=obj(K/'MANIFEST.json')['files']
    need(len(names)==267 and len(manifest)==266,'closed count')
    need(names==sorted(p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()),'closed inventory')
    need([r['path'] for r in manifest]==[n for n in names if n!='MANIFEST.json'],'manifest excludes only self')
    payload={n:(K/n).read_bytes() for n in names}
    rebuilt=io.BytesIO()
    with zipfile.ZipFile(rebuilt,'w',compression=0) as z:
        for n in names:
            i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=0;z.writestr(i,payload[n])
    need(rebuilt.getvalue()==(D/'verification_kit.zip').read_bytes(),'independent entire ZIP byte equality')
    with zipfile.ZipFile(D/'verification_kit.zip') as z:
        need(z.namelist()==['verification_kit/'+n for n in names] and z.comment==b'' and z.testzip() is None,'ZIP order/comment/CRC')
        for n,i in zip(names,z.infolist()):
            need(z.read(i)==payload[n] and i.CRC==zlib.crc32(payload[n])&0xffffffff,'payload/CRC')
            need(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.compress_type==0 and i.extra==b'' and i.comment==b'' and i.flag_bits==0,'complete member header')
    archives=[{'path':n,'bytes':len(payload[n]),'sha256':hashlib.sha256(payload[n]).hexdigest()} for n in names if n.endswith('.zip')]
    need(len(archives)==3 and len({r['sha256'] for r in archives})==2,'retained historical duplicate archives')
    for r in archives:
        for readme in [D/'README.md',K/'README.md']:need(r['path'] in readme.read_text() and r['sha256'] in readme.read_text(),'globally disclosed archive exception')
    need((D/'metadata.json').read_bytes()==(K/'metadata.json').read_bytes(),'native byte equality')
    upload=obj(D/'deposit_metadata.json');need(upload=={'metadata':obj(D/'metadata.json'),'files':[{'path':'preprint.pdf','name':'preprint.pdf'},{'path':'verification_kit.zip','name':'verification_kit.zip'}]},'native exact schema/attachments')
    binding=obj(D/'EXTERNAL_BINDING.json');s=binding['current_archive_wording_status'];need(matches(D/s['filename'],s),'outer current status separately bound');need((D/s['filename']).read_bytes()==(K/s['filename']).read_bytes(),'inside outside current status')
    status=obj(D/s['filename']);need(status['whole_reviews_completed']==3 and status['minimum_whole_reviews']==2 and status['latest_review_actionable_counts']=={'P0':0,'P1':0,'P2':0,'P3':1} and status['required_next_review']=='NEW complete whole04','current staged review accounting')
    need(all(status[k] is False for k in ['publication_ready','issues_resolved','published','root_integrity_adopted']) and status['services_held_at']==1032,'readiness/service hold')
    # Six originals authenticate against submitted frozen bytes without Git.
    originals=[]
    for p in sorted((BASE/'submitted').iterdir()):
        if p.is_file() and (K/'originals/submitted'/p.name).exists():
            q=K/'originals/submitted'/p.name;need(p.read_bytes()==q.read_bytes(),'six original copy '+p.name);originals.append({'name':p.name,'sha256':sha(p)})
    need(len(originals)==6 and not any(Path(r['name']).suffix=='.py' for r in originals),'six original files, no executable')
    summary={'status':'PASS','captured_stage_files':750,'read_only_sealed_stage_check':True,'stage_repair_files':len(copied),'archive_members':267,'manifest_payloads':266,'all_member_headers_payloads_CRC_closed':True,'independent_zip_byte_equal':True,'historical_archives':archives,'native_schema_exact':True,'six_originals':originals,'stage_check_summary':json.loads(result.stdout)}
    (HERE/'CUSTODY_RESULTS.json').write_text(json.dumps(summary,indent=2)+'\n')
    # Read-only hardlinks are disposable, never modified in place.
    rows=[{'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(stage.rglob('*')) if p.is_file()]
    with (HERE/'CLEANUP_RECEIPTS.jsonl').open('a') as f:f.write(json.dumps({'operation':'remove-own-read-only-captured750-hardlinks','files':rows})+'\n')
    shutil.rmtree(stage)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['stage_check_summary','six_originals']},indent=2))
if __name__=='__main__':main()
