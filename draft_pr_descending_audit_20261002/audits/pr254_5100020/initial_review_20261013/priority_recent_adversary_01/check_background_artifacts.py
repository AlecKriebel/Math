from pathlib import Path
import subprocess,json,base64,hashlib,datetime,urllib.request,urllib.parse
ROOT=Path(__file__).resolve().parent; S=ROOT/'sources'; R=ROOT/'receipts'
gh='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
def api(endpoint,name,optional=False):
 p=subprocess.run([gh,'api',endpoint],capture_output=True,text=True)
 (R/name).write_text(p.stdout); (R/(name+'.stderr')).write_text(p.stderr)
 if p.returncode:
  if optional: return None
  raise RuntimeError(name)
 return json.loads(p.stdout)
results=[]
for n,id in [(140,5100023),(223,5100024),(224,5100035),(227,5100038),(228,5100036),(110,5100034)]:
 d=api(f'repos/AlecKriebel/Math/pulls/{n}',f'background_pr{n}.json')
 commits=api(f'repos/AlecKriebel/Math/pulls/{n}/commits?per_page=100',f'background_pr{n}_commits.json')
 earlier=[c for c in commits if c['commit']['committer']['date']<'2026-10-01T10:55:00Z']
 if not earlier: results.append({'PR':n,'id':id,'created_at':d['created_at'],'earlier_commit_found':False}); continue
 sha=earlier[-1]['sha']
 proof=None
 for prefix in ['unsolved_math_prioritization/attempts','attempts']:
  path=f'{prefix}/{id}/PROOF.md'
  proof=api(f'repos/AlecKriebel/Math/contents/{path}?ref={sha}',f'background_pr{n}_proof_{prefix.split("/")[0]}.json',True)
  if proof: break
 if proof:
  data=base64.b64decode(proof['content']); (S/f'pr{n}_earlier_PROOF.md').write_bytes(data)
  results.append({'PR':n,'id':id,'created_at':d['created_at'],'ref':sha,'committer_date':earlier[-1]['commit']['committer']['date'],'path':path,'blob':proof['sha'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 else: results.append({'PR':n,'id':id,'created_at':d['created_at'],'ref':sha,'proof_at_guessed_paths':False})
url='https://zenodo.org/api/records?'+urllib.parse.urlencode({'q':'antipedal','size':100,'sort':'mostrecent'})
try:
 with urllib.request.urlopen(url,timeout=45) as p: raw=p.read()
 (S/'zenodo_antipedal_search.json').write_bytes(raw); d=json.loads(raw)
 search={'url':url,'total':d['hits']['total'],'records':[{'id':x['id'],'title':x['metadata']['title'],'created':x['created']} for x in d['hits']['hits']]}
except Exception as e: search={'url':url,'error':repr(e)}
(R/'BACKGROUND_SOURCE_AUTHENTICATION.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PRs':results,'zenodo_search':search},indent=2)+'\n')
print(json.dumps({'PRs':results,'zenodo_search':search},indent=2))
