import pathlib,json,hashlib,zipfile,subprocess,stat,datetime,sys
P=pathlib.Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012');ROOT=P.parent;A=P/'audits/pr952_10400145';D=A/'preprint';R=A/'reviews/full_package_03'
def sha(b):return hashlib.sha256(b).hexdigest()
def rec(path):
 b=path.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def check(paths,base):
 out={}
 for n,v in paths.items():
  p=base/n
  try: actual=rec(p);out[n]={'expected':v,'actual':actual,'match':actual=={k:v[k] for k in ('bytes','sha256')}}
  except Exception as e:out[n]={'error':str(e),'match':False}
 return out
f=json.loads((D/'FREEZE.json').read_bytes());o=json.loads((A/'publication/workflow/OPERATIONS_INVENTORY.json').read_bytes());orig=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_bytes()); out={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'boundary':sys.argv[1],'freeze':rec(D/'FREEZE.json'),'operations_inventory':rec(A/'publication/workflow/OPERATIONS_INVENTORY.json'),'core':rec(P/'accept_pr952.py'),'files':check(f['files'],D),'evidence_files':check(f['evidence_files'],ROOT),'dependencies':check(o['files'],ROOT),'original':{}}
with zipfile.ZipFile(D/'habiro-rank-interpolation-verification-v1.0.zip') as z:
 for n,v in orig['files'].items():
  p=A/'original'/n;b=p.read_bytes();disk=rec(p);mode=oct(stat.S_IMODE(p.stat().st_mode));git=subprocess.run(['git','show',orig['head']+':'+n],cwd=ROOT,capture_output=True);ls=subprocess.run(['git','ls-tree',orig['head'],'--',n],cwd=ROOT,capture_output=True);gb=git.stdout;zb=z.read('original/'+n);zi=z.getinfo('original/'+n)
  actual={'disk':disk,'disk_mode':mode,'git':{'bytes':len(gb),'sha256':sha(gb),'exit':git.returncode,'ls_tree':ls.stdout.decode().strip()},'zip':{'bytes':len(zb),'sha256':sha(zb),'mode':oct(stat.S_IMODE(zi.external_attr>>16))}}
  actual['match']=(disk=={k:v[k] for k in ('bytes','sha256')} and len(gb)==v['bytes'] and sha(gb)==v['sha256'] and len(zb)==v['bytes'] and sha(zb)==v['sha256'] and int(mode,8)==int(v['disk_mode'],8) and ls.stdout.decode().split()[0]==v['git_mode'] and ls.stdout.decode().split()[2]==v['git_blob'] and stat.S_IMODE(zi.external_attr>>16)==int(v['disk_mode'],8));out['original'][n]=actual
out['summary']={k:{'count':len(out[k]),'matches':sum(v['match'] for v in out[k].values())} for k in ('files','evidence_files','dependencies','original')}
(R/('AUTHENTICATION_'+sys.argv[1]+'.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']))
