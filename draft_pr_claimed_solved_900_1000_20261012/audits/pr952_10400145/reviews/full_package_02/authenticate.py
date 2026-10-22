import datetime, hashlib, json, pathlib, subprocess, sys, zipfile

ROOT = pathlib.Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_claimed_solved_900_1000_20261012'
A = P / 'audits/pr952_10400145'
D = A / 'preprint'
R = A / 'reviews/full_package_02'
PIN = '87e6753c48153e6bbc82ad77181339dd4d4fe64e0c855be507da6b47b7438424'
INV = '86f04bba661b5036a0b3a2b958779569ed4b92543748071f7177ed6d60e6df97'
CORE = '888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8'
MAN = 'fe04fc51d308975f07b00ff788b12a719d8cce2ec5edddc738c8469cf49b30f2'
HEAD = '989a532ae1d50894190d010a0a02ba8c3d71ee05'

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p, pin=None):
    b=p.read_bytes()
    if pin: assert sha(b)==pin, str(p)
    return b
def fp(p):
    b=read(p);return {'bytes':len(b),'sha256':sha(b)}
def verify_map(base, mapping):
    for path, record in mapping.items():
        assert fp(base/path)=={k:record[k] for k in ['bytes','sha256']},path

phase=sys.argv[1]
fraw=read(D/'FREEZE.json',PIN); f=json.loads(fraw)
iraw=read(A/'publication/workflow/OPERATIONS_INVENTORY.json',INV); inv=json.loads(iraw)
read(D/'package/PACKAGE_MANIFEST.json',MAN)
read(D/'package/verify_package.py','ba18bdcd863c3dca65c86be711564527ce19e4c859204b66095e39d366f453d7')
read(D/'habiro-rank-interpolation-v1.0.pdf','f3b3f38a7f3a3a4be37482908b03ffa722879fc047925428c6bdedee83d882b6')
read(D/'habiro-rank-interpolation-verification-v1.0.zip','5fca36bc43c8b4f64ca236a417b036f4f36874f01476bfd216383e3fd05bbfae')
read(ROOT/'zenodo_deposit_tool/zenodo.py','a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca')
verify_map(D,f['files']);verify_map(ROOT,f['evidence_files']);verify_map(P,f['future_helpers']);verify_map(ROOT,inv['files'])
b=read(P/'accept_pr952.py',CORE)
n={'__name__':'review_auth_only','__file__':str(P/'accept_pr952.py')}
exec(compile(b,str(P/'accept_pr952.py'),'exec'),n)
context=n['capture_inventory'](INV)
freeze_result=n['freeze_check'](fraw,PIN,context)
original_result=n['original_check']()
(R/f'private_{phase}_core_auth.json').write_text(json.dumps({'inventory':context,'freeze':freeze_result,'original':original_result},indent=2,default=str)+'\n')
records=json.loads(read(A/'ORIGINAL_FILE_RECORDS.json'))['files']
originals={}
with zipfile.ZipFile(D/'habiro-rank-interpolation-verification-v1.0.zip') as z:
    for path,record in records.items():
        disk=read(A/'original'/path); git=subprocess.run(['git','show',HEAD+':'+path],cwd=ROOT,capture_output=True,check=True).stdout
        matches=[q for q in z.namelist() if q.endswith(path)]
        assert len(matches)==1,(path,matches)
        info=z.getinfo(matches[0]); archive=z.read(matches[0])
        assert disk==git==archive and len(disk)==record['bytes'] and sha(disk)==record['sha256'],path
        blob=subprocess.run(['git','hash-object','--stdin'],input=disk,cwd=ROOT,capture_output=True,check=True).stdout.decode().strip()
        assert blob==record['git_blob']
        mode=(info.external_attr>>16)&0o177777
        assert mode==0o100644,(path,oct(mode))
        originals[path]={**record,'archive_mode':'100644','disk_and_archive_match':True}
obs=R/f'private_{phase}_preflight';obs.mkdir(exist_ok=True)
args=[sys.executable,'-I','-S','-B',str(P/'accept_pr952.py'),'--operations-sha256',INV,'--freeze',PIN,'--preflight-only','--observation-dir',str(obs)]
proc=subprocess.run(args,cwd=ROOT,capture_output=True)
(R/f'{phase}_preflight.stdout.raw').write_bytes(proc.stdout)
(R/f'{phase}_preflight.stderr.raw').write_bytes(proc.stderr)
(R/f'{phase}_preflight_launch.json').write_text(json.dumps({'args':args,'returncode':proc.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')},indent=2)+'\n')
if proc.returncode: print('AUTHENTICATION_PREFLIGHT_FAILED_RETURN_CODE',proc.returncode);sys.exit(1)
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'original_pr_head':HEAD,'freeze_sha256':PIN,'package_manifest_sha256':MAN,'future_helpers':f['future_helpers'],'candidate_files':f['files'],'originals':originals,'evidence_files':f['evidence_files'],'inventory_dependencies':inv['files'],'mechanical_counts':{'payloads':len(f['files']),'evidence':len(f['evidence_files']),'dependencies':len(inv['files']),'originals':len(originals)}}
(R/f'AUTHENTICATION_{phase.upper()}.json').write_text(json.dumps(result,indent=2)+'\n')
print('AUTHENTICATION_PASS_SAFE_STATUS')
