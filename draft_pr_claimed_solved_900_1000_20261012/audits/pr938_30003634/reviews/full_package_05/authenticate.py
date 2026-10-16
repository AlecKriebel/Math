import hashlib,json,stat,subprocess,zipfile,sys
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent; ROOT=R.parents[4];P=ROOT/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr938_30003634';D=A/'publication';C=D/'reviewed_candidates/candidate05'
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b';PRE='unsolved_math_prioritization/attempts/30003634/';PIN='76e645150f6fa525448a99c189f6eb535e1318fef15e086088dc052bc2dbb82a'
def need(v,s):
 if not v: raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(a):return subprocess.run(a,cwd=ROOT,check=True,capture_output=True).stdout
def fp(p):
 b=p.read_bytes();need(stat.S_ISREG(p.lstat().st_mode),'nonregular '+str(p));return {'bytes':len(b),'sha256':sha(b)}
def main():
 f=json.loads((D/'PREPUBLICATION_FREEZE.json').read_bytes());need(sha((D/'PREPUBLICATION_FREEZE.json').read_bytes())==PIN,'freeze pin');need((C/'PREPUBLICATION_FREEZE.json').read_bytes()==(D/'PREPUBLICATION_FREEZE.json').read_bytes(),'snapshot freeze')
 for n,v in f['files'].items():need(fp(D/n)==v and fp(C/n)==v,'current/snapshot '+n)
 for n,v in f['future_helpers'].items():need(fp(P/n)==v and fp(C/'future_helpers'/n)==v,'helper '+n)
 snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_bytes());need(snap['head']==HEAD and len(snap['files'])==44,'snapshot inventory')
 ls=run(['git','ls-tree','-r',HEAD,'--',PRE]).decode().splitlines();tree={line.split('\t')[1]:line.split('\t')[0].split() for line in ls};need(set(tree)==set(snap['files']),'actual exact subtree')
 orig={}
 with zipfile.ZipFile(D/'deep-derived-pure-braids-source-verification-v1.0.zip') as z:
  names=z.namelist();need(len(names)==213 and len(names)==len(set(names)),'archive members');raw=z.read('PACKAGE_MANIFEST.json');need(sha(raw)==f['package_manifest_sha256'],'manifest pin');m=json.loads(raw);need(len(m['files'])==212 and set(names)==set(m['files'])|{'PACKAGE_MANIFEST.json'},'closed manifest')
  for i in z.infolist():
   need(stat.S_ISREG(i.external_attr>>16),'nonregular archive');need(i.filename!='' and not i.filename.startswith('/') and '\\' not in i.filename and all(x not in ['','.','..'] for x in i.filename.split('/')),'path')
   if i.filename!='PACKAGE_MANIFEST.json':need({'bytes':len(z.read(i)),'sha256':sha(z.read(i))}==m['files'][i.filename],'payload')
  for n,h in snap['files'].items():
   mode,kind,blob=tree[n];b=run(['git','cat-file','blob',blob]);disk=A/'original'/n;an='original_packet/'+n[len(PRE):];i=z.getinfo(an)
   need(mode=='100644' and kind=='blob' and sha(b)==h and disk.read_bytes()==b and z.read(an)==b,'git disk zip '+n);need(stat.S_IMODE(disk.stat().st_mode)==0o644 and i.external_attr>>16==0o100644,'modes')
   orig[n]={'git_blob':blob,'git_mode':mode,'bytes':len(b),'sha256':h,'disk_mode':'0644','archive_mode':'100644','disk_and_archive_match':True}
  need(z.read('note.pdf')==(D/'output/pdf/note.pdf').read_bytes(),'pdf equality')
 result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','original_pr_head':HEAD,'freeze_sha256':PIN,'package_manifest_sha256':f['package_manifest_sha256'],'candidate_files':f['files'],'future_helpers':f['future_helpers'],'archive_members':213,'payloads':212,'originals':orig}
 out=R/('AUTHENTICATION_END.json' if '--end' in sys.argv else 'AUTHENTICATION_START.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','output':out.name,'candidate_files':len(f['files']),'helpers':len(f['future_helpers']),'originals':len(orig)}))

if __name__=='__main__':main()
