from pathlib import Path
import datetime, hashlib, json, stat

R = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23137834/reviews/root-initial-20261117')
S = R.parent.parent/'sources'
def digest(b): return hashlib.sha256(b).hexdigest()
assert digest((S/'assets/pentagonal-torsion-note.pdf').read_bytes()) == '0325be9bc4b754ad1d94baadf2f1b88af587e9443b9d242a2d7af7b2dda79420'
assert digest((S/'published-source/container-001/tree/manuscript.tex').read_bytes()) == '3338be58c5c6250a826f2a2af772db5a3838dad1d45c6c4a847c62cc00b4f9df'
assert digest((S/'record.response.body').read_bytes()) == '29efcc4628bba1134f51923a9c41bc6128321f7c45e8d98095be0e0a29198b6f'
assert len(list((R/'pages').glob('page-*.png'))) == 7
initial = json.loads((R/'INITIAL.json').read_text())
assert initial['raster_pages_viewed'] == 7 and initial['support_code_results_current_peer_primary_bodies_read'] is False
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (R/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n{now}: root personally viewed all7freshownPDFpages after all482TeXlines/fullnativeAPI/all7textpages. Original-only INITIAL35% complete; mathematicalverdict withheld. Twelve independenthanddeductions recorded; actualprimary/support/currentfamilies still unread. Checkpoint this frozen INITIAL before those interfaces. No scientific program executed. Programme144/203scientific/native dispositions,59remaining,70.935961%; active/incomplete.\n')
terminals = {'INITIAL_MANIFEST.json','INITIAL_SEAL.json'}
assert not any((R/n).exists() for n in terminals)
payload = []
dirs = []
for p in [R,*sorted(R.rglob('*'))]:
    s = p.lstat();assert not p.is_symlink()
    rel = str(p.relative_to(R))
    if stat.S_ISDIR(s.st_mode):
        dirs.append({'path':rel,'mode':'0555','empty':not any(p.iterdir())})
    else:
        assert stat.S_ISREG(s.st_mode)
        b = p.read_bytes()
        payload.append({'path':rel,'bytes':len(b),'SHA256':digest(b),'mode':'0444','empty':not b})
manifest = {'schema':'finite-root-original-only-initial-v1','UTC':now,'root':str(R),'root_mode':'0555','regular_files':len(payload)+2,'child_directories':len(dirs)-1,'payload_files':payload,'directories':dirs,'exact_terminal_recursive_hash_exclusions':sorted(terminals),'terminal_modes':{n:'0444' for n in sorted(terminals)},'other_exclusions':[]}
(R/'INITIAL_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
seal = {'UTC':now,'status':'ORIGINAL_ONLY_INITIAL_FROZEN_NO_VERDICT','record':'23137834','files':len(payload)+2,'child_directories':len(dirs)-1,'manifest_SHA256':digest((R/'INITIAL_MANIFEST.json').read_bytes()),'completion_percent_of_review':35,'original_TeX_text_API_and7rasters_personally_read':True,'scientific_support_current_peer_and_primary_bodies_unread':True,'scientific_program_runs':0,'checkpoint_before_any_scientific_continuation_pending':True,'programme_goal_complete':False}
(R/'INITIAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for p in R.rglob('*'):
    p.chmod(0o555 if p.is_dir() else 0o444)
R.chmod(0o555)
assert all(stat.S_IMODE(p.stat().st_mode)==(0o555 if p.is_dir() else 0o444) for p in [R,*R.rglob('*')])
for x in payload:
    p=R/x['path'];assert len(p.read_bytes())==x['bytes'] and digest(p.read_bytes())==x['SHA256']
print(json.dumps({'files':len(payload)+2,'child_directories':len(dirs)-1,'INITIAL_SEAL_SHA256':digest((R/'INITIAL_SEAL.json').read_bytes()),'INITIAL_MANIFEST_SHA256':digest((R/'INITIAL_MANIFEST.json').read_bytes()),'original_only_review_percent':35,'mathematical_verdict':None}))
