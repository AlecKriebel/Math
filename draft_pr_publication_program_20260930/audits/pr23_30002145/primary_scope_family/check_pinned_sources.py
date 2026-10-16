#!/usr/bin/env python3
"""Read-only exact-head/source-corpus provenance replay; writes only this family."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
HEAD='ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d'
PREFIX='unsolved_math_prioritization/'
ID=30002145
CODE='OWR-12008-005'
TITLE='Rigidity of Symmetric-Gradient Differential Inclusions'

def sha(b): return hashlib.sha256(b).hexdigest()
def gitfile(p): return subprocess.check_output(['git','show',HEAD+':'+p],cwd=REPO)
def values(x):
    if isinstance(x,dict):
        for v in x.values(): yield from values(v)
    elif isinstance(x,list):
        for v in x: yield from values(v)
    else: yield str(x)

manifest=json.loads(gitfile(PREFIX+'manifest.json'))
corpus={}
data={}
for name in ('problems.json','research_results.json'):
    b=(REPO/PREFIX/'cache'/name).read_bytes()
    assert sha(b)==manifest['files'][name]['sha256']
    assert len(b)==manifest['files'][name]['bytes']
    data[name]=json.loads(b)
    corpus[name]={'path':str(REPO/PREFIX/'cache'/name),'sha256':sha(b),'bytes':len(b),'entries':len(data[name])}
problems=data['problems.json'];reports=data['research_results.json']
matches=[p for p in problems if p.get('id')==ID]
assert len(matches)==1
record=json.loads((ROOT.parent/'source_snapshot/source_record.json').read_bytes())
assert record==matches[0]
norm=lambda v: re.sub(r'\s+',' ',v).strip().casefold()
duplicates=[{'id':p['id'],'title':p['title']} for p in problems if p['id']!=ID and norm(p.get('statement',''))==norm(record['statement'])]
report_queries={needle:[k for k,v in reports.items() if needle in k or any(needle in t for t in values(v))] for needle in (str(ID),CODE,TITLE)}
code_matches=[{'id':p['id'],'title':p['title']} for p in problems if p.get('problem_number')==CODE]
semantic_matches=[{'id':p['id'],'title':p['title'],'problem_number':p['problem_number']}
                  for p in problems if re.search(r'symmetric.?grad|symmetri[sz]ed.?grad|bounded deformation|fixed.polar|rank.one.line',p.get('statement','')+' '+p.get('title',''),re.I)]
group_bytes=gitfile(PREFIX+'review_v2/related_target_groups.json')
group_contains=any(str(ID) in v or CODE in v or TITLE in v for v in values(json.loads(group_bytes)))
state=json.loads(gitfile(PREFIX+'state.json')).get(str(ID),{})
history=[json.loads(x) for x in gitfile(PREFIX+'history.jsonl').decode().splitlines() if str(ID) in x]
assessment=json.loads(gitfile(PREFIX+'assessments.json')).get(str(ID),{})
catalog=[p for p in json.loads(gitfile(PREFIX+'catalog.json')) if str(p['id'])==str(ID)]
queue=[line for line in gitfile(PREFIX+'QUEUE.md').decode().splitlines() if str(ID) in line]
snapshot=json.loads((ROOT.parent/'snapshot_manifest.json').read_bytes())
binding=[]
for entry in snapshot['files']:
    rel=entry['path'];b=(ROOT.parent/'source_snapshot'/rel).read_bytes()
    h=gitfile(PREFIX+'attempts/'+str(ID)+'/'+rel)
    ok=sha(b)==entry['sha256'] and len(b)==entry['bytes'] and b==h
    assert ok
    binding.append({'path':rel,'sha256':sha(b),'bytes':len(b),'equals_git_head':True})
default=('queued' if assessment.get('decision')=='candidate' else 'unreviewed')
if assessment.get('resolution')=='already_solved':default='already_solved'
result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'script_sha256':sha(Path(__file__).read_bytes()),'head':HEAD,
        'revision':manifest['revision'],'corpus':corpus,
        'snapshot_record_equals_pinned_record':True,'numeric_id_matches':len(matches),
        'matching_problem_codes':code_matches,'normalized_statement_duplicates':duplicates,
        'report_queries':report_queries,'semantic_statement_title_queries':semantic_matches,
        'related_target_groups_contains_id_code_or_title':group_contains,
        'exact_head':{'state':state,'history':history,'assessment':assessment,'catalog':catalog,'queue_rows':queue,
                      'status_generator_default_from_unchanged_candidate_assessment':default,
                      'legacy_durability_warning':'Do not run generator on manually preserved operational queue. Canonical machine state has no selected-target disposition; the current queue row is nevertheless explicit scoped evidence.'},
        'snapshot_binding':binding,'snapshot_all_14_files_match_head':len(binding)==14,
        'limits':'No report under these exact identity queries and no duplicate under stated checks; this is not a theorem that no differently worded related mathematical target exists.'}
(ROOT/'pinned_corpus_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':True,'head':HEAD,'files_bound':len(binding),'report_hits':report_queries,
                  'normalized_duplicates':duplicates,'state':state,'history':history,
                  'default_status':default,'semantic_matches':semantic_matches},indent=2))
