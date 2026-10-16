"""Dated, bounded read-only provider searches and public-record custody."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'root_priority_current_private';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(label,args):
 j={'argv':args,'cwd':str(D),'started_utc':utc()};(D/(label+'.spec.json')).write_text(json.dumps(j,indent=2)+'\n')
 r=subprocess.run(args,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 for k,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  (D/(label+'.'+k+'.bin')).write_bytes(b);j[k]={'bytes':len(b),'sha256':sha(b)}
 j.update(ended_utc=utc(),exit_code=r.returncode);(D/(label+'.execution.json')).write_text(json.dumps(j,indent=2)+'\n')
 if r.returncode: return {'failed_exit':r.returncode,'stderr':r.stderr.decode(errors='replace')}
 try:return json.loads(r.stdout)
 except Exception:return {'parse_failed':True,'stdout_bytes':len(r.stdout)}
gh={}
for name,q in [('raw_id','repo:AlecKriebel/Math is:pr "5100034"'),('amr_id','repo:AlecKriebel/Math is:pr "AMR-050-0034"'),('target_title','repo:AlecKriebel/Math is:pr "focal-pedal" "equality"')]:
 j=run('github_'+name,['/opt/homebrew/bin/gh','api','-X','GET','search/issues','-f','q='+q,'-f','per_page=100'])
 gh[name]={'query':q,'total_count':j.get('total_count'),'incomplete_results':j.get('incomplete_results'),'hits':[{'number':i['number'],'title':i['title'],'url':i['html_url'],'created_at':i['created_at']} for i in j.get('items',[])],'failure':j.get('failed_exit')}
records={}
for rid,name in [(23079799,'recent0021'),(23089778,'recent0027'),(23088516,'recent0014')]:
 j=run('zenodo_'+str(rid),['/usr/bin/curl','-q','--fail','--location','--max-time','60','https://zenodo.org/api/records/'+str(rid)])
 records[name]={'id':rid,'created':j.get('created'),'updated':j.get('updated'),'doi':j.get('doi'),'publication_date':j.get('metadata',{}).get('publication_date'),'version':j.get('metadata',{}).get('version'),'title':j.get('metadata',{}).get('title'),'files':[{'key':f['key'],'size':f['size'],'checksum':f['checksum']} for f in j.get('files',[])],'failure':j.get('failed_exit')}
 p=A/'root_priority_recent_private'/(name+'.pdf');records[name]['website_pdf']={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'md5':hashlib.md5(p.read_bytes()).hexdigest()}
catalog=(A/'root_priority_recent_private/catalog.html').read_bytes()
j={'utc':utc(),'status':'READ_ONLY_BOUNDED_PROVENANCE_CHECK_NO_PRIORITY_VERDICT','github':gh,'zenodo':records,'catalog_exact_target_id_count':catalog.count(b'AMR-050-0034'),'limitations':['GitHub issue searches index titles/body/comments, not all files or unpublished/unindexed work; incomplete_results and failures retained.','Current downloaded website manuscripts may have later updates; compare exact public-record file checksums and dates before treating complete body as prior publication.','No matching exact catalog ID is not a proof of no prior theorem.','Only bibliographic provenance and target-specific search metadata are inspected here; unrelated PR statuses/results are not processed.']}
(A/'ROOT_PRIORITY_CURRENT_PROVENANCE.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
