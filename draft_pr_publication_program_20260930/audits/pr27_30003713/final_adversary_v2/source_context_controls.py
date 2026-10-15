"""Fresh read-only pinned source, exact prior, duplicate scope, and administration checks."""
from pathlib import Path
from urllib.request import Request,urlopen
import datetime,hashlib,json,re,sqlite3,subprocess
P=Path(__file__).resolve().parent;A=P.parent;R=P.parents[3];Q=R/'unsolved_math_prioritization';sha=lambda b:hashlib.sha256(b).hexdigest();pin='37e53eabe540fb458758e198be61634bd02ee008'
manifest=json.loads((Q/'manifest.json').read_text());assert manifest['revision']==pin;cache={};bindings=[]
for name,v in manifest['files'].items():
 b=(Q/'cache'/name).read_bytes();assert sha(b)==v['sha256'] and len(b)==v['bytes'];cache[name]=json.loads(b);bindings.append({'file':name,'sha256':sha(b),'bytes':len(b)})
raw=cache['problems.json'];assert len(raw)==15458;target=[x for x in raw if x['id']==30003713];assert len(target)==1;source=target[0];assert source['problem_number']=='OWR-15987-026'
prior=cache['research_results.json'].get(source['problem_number'],{});assert prior=={}
con=sqlite3.connect('file:'+str(Q/'cache/catalog.sqlite')+'?mode=ro',uri=True);db=con.execute('SELECT payload,report FROM records WHERE key=?',('30003713',)).fetchall();con.close();assert len(db)==1 and json.loads(db[0][0])==source and json.loads(db[0][1])==prior
assert source==json.loads((A/'source_snapshot/source_record.json').read_text())
context=sha(json.dumps([source,prior],sort_keys=True).encode());assert context=='0fb4d607f5e9cce2db158be17ff5c02f3b64ff2510ea911ed9b5c18490812ca6';assert json.loads((A/'reviewed_candidate/readiness.json').read_text())['review_hash']==context
matches=[]
for s in raw:
 t=(s.get('title','')+' '+s.get('statement','')).lower()
 if ('square-zero' in t or 'square zero' in t or 'e^2=0' in t) and 'lie' in t and 'homology' in t:matches.append({'id':s['id'],'code':s['problem_number'],'title':s['title']})
assert len(matches)==1 and matches[0]['id']==30003713
related=(Q/'review_v2/related_target_groups.json').read_text();assert '30003713' not in related and 'OWR-15987-026' not in related
# Exact selected-id/code joins across raw reports and main-tree paths.
raw_code_match=[k for k in cache['research_results.json'] if k in ['30003713','OWR-15987-026']];assert raw_code_match==[]
state=json.loads((Q/'state.json').read_text());history=[json.loads(x) for x in (Q/'history.jsonl').read_text().splitlines() if x];assert len(state)==len(history)==17;assert sum(x.get('turns_used',0) for x in state.values())==18;assert '30003713' not in state and all(str(x['id'])!='30003713' for x in history)
assert all(x['event'] in ['acceptance_mirror_import','acceptance_duplicate_mirror_import'] and not x['evidence']['historical_transitions_asserted'] for x in history)
cat=next(x for x in json.loads((Q/'catalog.json').read_text()) if str(x['id'])=='30003713');assert cat['local_status']=='queued' and cat['turns_used']==0 and cat['eligible'];assert cat['review_hash']==context
assess=json.loads((Q/'assessments.json').read_text());assert '30003713' in assess
qrows=[x for x in (Q/'QUEUE.md').read_text().splitlines() if '| 30003713 / OWR-15987-026 |' in x];assert len(qrows)==1;cols=[x.strip() for x in qrows[0].split('|')[1:-1]];assert len(cols)==12 and cols[7:9]==['queued','0/5']
turns=[json.loads(x) for x in (A/'source_snapshot/turns.jsonl').read_text().splitlines() if x];assert len(turns)==1 and turns[0]['turn']==1
queuecode=(Q/'queue.py').read_text();assert "args.status in ['ready','in_progress']" in queuecode and "Readiness evidence required" in queuecode;assert "'| Rank | ID / code | Problem | EV | Difficulty | Proposed | Status | Turns |'" in queuecode
mainpaths=subprocess.check_output(['git','ls-tree','-r','--name-only','main'],cwd=R,text=True).splitlines();target_main=[x for x in mainpaths if '/30003713/' in x];assert target_main==[]
# Fresh authenticated PR read; all writes restricted to own receipt.
live=json.loads(subprocess.check_output(['gh','pr','view','27','--repo','AlecKriebel/Math','--json','number,url,state,isDraft,baseRefName,baseRefOid,headRefOid,headRefName,body,files,mergeCommit,mergedAt'],cwd=R,text=True));assert live['headRefOid']=='84d7f6103b087e431d7afb751501380ebd7ffd42' and live['isDraft'] and live['state']=='OPEN' and live['baseRefName']=='main' and live['mergedAt'] is None
frozen=json.loads((A/'snapshot_manifest.json').read_text());assert [x['path'] for x in live['files']]==frozen['changed_paths'];assert live['body']==(A/'reviewed_candidate/pr_body.md').read_text()
(P/'LIVE_PR_RECEIPT.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'live':live,'body_equals_candidate':True,'exact_original_head_and_paths':True,'future_merge_canonical_not_blessed':True},indent=2)+'\n')
# Pinned LFS metadata independently binds cached source bytes to same remote revision.
u='https://huggingface.co/api/datasets/ulamai/UnsolvedMath/tree/'+pin+'?recursive=false&expand=true';b=urlopen(Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read();(P/'ignoredtmp/primary/pinned_dataset_metadata.json').write_bytes(b);meta=json.loads(b);lfs=[]
for name,v in manifest['files'].items():
 m=next(x for x in meta if x['path']==name);assert m['size']==v['bytes'] and m['lfs']['oid']==v['sha256'];lfs.append({'file':name,'size':m['size'],'oid':m['lfs']['oid']})
# Bibliographic primary metadata; published body deliberately not inferred.
u2='https://api.crossref.org/works/10.1080%2F10586458.2025.2608243';b2=urlopen(Request(u2,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read();(P/'ignoredtmp/primary/crossref.json').write_bytes(b2);cross=json.loads(b2)['message'];assert cross['published-online']['date-parts']==[[2026,3,4]]
admin_bindings=[{'file':x,'sha256':sha((Q/x).read_bytes()),'bytes':(Q/x).stat().st_size} for x in ['state.json','history.jsonl','catalog.json','assessments.json','QUEUE.md','queue.py','policy.json','review_v2/related_target_groups.json']]
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FRESH_SOURCE_CONTEXT_ADMIN','pin':pin,'cache_bindings':bindings,'lfs_metadata_sha256':sha(b),'remote_lfs_bindings':lfs,'raw_source_sqlite_snapshot_equal':True,'records':len(raw),'exact_prior':prior,'exact_prior_code_matches':raw_code_match,'context_digest':context,'context_digest_is_not_math_review_sha':True,'full_target_predicate_matches':matches,'bounded_duplicate_scope':True,'related_exact_id_code_match':False,'mirror_states':len(state),'mirror_histories':len(history),'original_consumed':18,'duplicate_usage_added':sum(x.get('turns_used',0) for x in history if x['event']=='acceptance_duplicate_mirror_import'),'target_state_history_absent':True,'main_target_paths':target_main,'current_queue_row':qrows[0],'queue_columns':len(cols),'static_catalog':{k:cat[k] for k in ['local_status','turns_used','eligible','review_hash']},'assessment_is_desk_prior':True,'manual_readiness_reopen_requires_source_bound_evidence':True,'legacy_generator_eight_columns_would_erase_current_twelve':True,'generator_never_invoked':True,'administration_bindings':admin_bindings,'current_mirror_is_PR27_acceptance':False,'future_canonical_or_queue_bytes_blessed':False,'crossref_sha256':sha(b2),'published_online':cross['published-online'],'doi':cross['DOI'],'published_body_compared':False,'original_substantive_attempts':1,'limit':5,'new_substantive_attempts':0}
(P/'SOURCE_CONTEXT_ADMIN_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['administration_bindings','cache_bindings','remote_lfs_bindings']},indent=2))
