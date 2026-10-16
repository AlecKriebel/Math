from pathlib import Path
import hashlib,json,stat,subprocess,datetime,sys
BASE=Path('/Users/alec/Documents/Math')
AUDIT=BASE/'draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616'
OUT=AUDIT/'reviews/exact_priority_falsifier_01'
HEAD='b356dec5cb01e5f536b9cfeece56ad08844c03cb'
R=AUDIT/'ORIGINAL_FILE_RECORDS.json'
expected='610351fbb778f78ce53cda03ea715f38615abb5710690987c214f8093bda13ae'
def sha(b): return hashlib.sha256(b).hexdigest()
assert sha(R.read_bytes())==expected
rec=json.loads(R.read_bytes()); assert rec['head']==HEAD and len(rec['files'])==26
entries={}
for rel,w in rec['files'].items():
    p=AUDIT/'original'/rel; b=p.read_bytes(); s=p.lstat()
    assert stat.S_ISREG(s.st_mode)
    blob=subprocess.check_output(['git','-C',str(BASE),'cat-file','blob',HEAD+':'+rel])
    tree=subprocess.check_output(['git','-C',str(BASE),'ls-tree',HEAD,'--',rel]).decode().strip()
    mode,kind,blob_id=tree.split('\t')[0].split()
    got={'bytes':len(b),'sha256':sha(b),'git_blob':blob_id,'git_mode':mode,'disk_mode':f'{stat.S_IMODE(s.st_mode):04o}'}
    assert got==w,(rel,got,w)
    assert b==blob,(rel,'git disk mismatch')
    entries[rel]={**got,'git_disk_content_equal':True}
actual={str(p.relative_to(AUDIT/'original')) for p in (AUDIT/'original').rglob('*') if p.is_file()}
assert actual==set(rec['files']), (actual-set(rec['files']),set(rec['files'])-actual)
result={'actual_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records_sha256':expected,'submitted_head':HEAD,'files':entries,'file_count':len(entries),'total_bytes':sum(e['bytes'] for e in entries.values()),'all_exact':True}
path=OUT/('INTAKE_AUTHENTICATION.json' if len(sys.argv)==1 else sys.argv[1]); path.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({k:v for k,v in result.items() if k!='files'}))
