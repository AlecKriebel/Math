import datetime,hashlib,json,pathlib
here=pathlib.Path(__file__).resolve().parent
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
ledger=[json.loads(line) for line in (here/'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
for r in ledger:
    for stream in ['stdout','stderr']:
        b=(here/r[stream+'_path']).read_bytes()
        assert len(b)==r[stream+'_bytes']
        assert hashlib.sha256(b).hexdigest()==r[stream+'_sha256']
assert len(ledger)==9
assert [r['exit'] for r in ledger if r['exit']!=0]==[2,2]
assert json.loads((here/'INDEPENDENT_RESULTS.json').read_text())['status']=='PASS'
assert json.loads((here/'COMPLETION_DEPENDENCE_RESULTS.json').read_text())['status']=='PASS'
first=json.loads((here/'FIRST_CONCLUSION.json').read_text())
assert hashlib.sha256((here/first['file']).read_bytes()).hexdigest()==first['sha256']
candidate=here/'original_replay/CANDIDATE.md'
assert hashlib.sha256(candidate.read_bytes()).hexdigest()=='fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698'
with (here/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+utc+': Independent endpoint-word/bitset graph checks passed 1,494,879 assertions; exhaustive all small partial-graph global completions matched local expectations; original controls reproduced with two preserved launch failures followed by corrected passes. Formal all-n theorem and exact tournament maximum written. Graph-family review completion estimate: 100%. Imported knot formula and priority remain outside this review. No native/Git/PR/publication mutation or outside contact.\n')
summary={'timestamp_utc':utc,'verdict':'conditional graph pass; prior-opinion-exposed',
         'candidate_sha256':'fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698',
         'completion_percent_graph_family':100,'graph_repairs_required':[],
         'graph_counterexamples_found':[], 'independent_assertions':1494879,
         'original_replay_graph_assertions':42684,'original_replay_jones_assertions':183,
         'procedural_exposure_preserved':True,
         'conditional_dependency':'Imported classical-knot v3 formula (4), normalization, source correspondence; priority unknown.',
         'bounded_receipt_cutoff':'009_completion_dependence_checks',
         'receipt_integrity_verified_through_cutoff':True}
(here/'AUDIT_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
(here/'ACTUAL_COMMANDS_BOUNDED.jsonl').write_bytes((here/'ACTUAL_COMMANDS.jsonl').read_bytes())
manifest=[]
for p in sorted(here.rglob('*')):
    if not p.is_file() or p.name in ['ARTIFACT_MANIFEST.json','ACTUAL_COMMANDS.jsonl']:
        continue
    b=p.read_bytes()
    assert len(b)<1048576
    manifest.append({'path':str(p.relative_to(here)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
assert sum(r['bytes'] for r in manifest)<1048576
(here/'ARTIFACT_MANIFEST.json').write_text(json.dumps({'timestamp_utc':utc,
    'scope':'Own audit folder files existing at finalization; excludes live append-only ACTUAL_COMMANDS.jsonl and manifest itself. Finalization execution receipt is subsequent to cutoff.',
    'receipt_cutoff':'009_completion_dependence_checks','files':manifest,
    'total_bytes':sum(r['bytes'] for r in manifest)},indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('Report SHA256 '+hashlib.sha256((here/'GRAPH_AUDIT_REPORT.md').read_bytes()).hexdigest())
print('Manifest SHA256 '+hashlib.sha256((here/'ARTIFACT_MANIFEST.json').read_bytes()).hexdigest())
