"""Data-only one-shot terminal sealing of this owned finite correspondence packet."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat

O = Path(__file__).resolve().parent
def sha(data): return hashlib.sha256(data).hexdigest()
def encode(obj): return (json.dumps(obj, indent=2, ensure_ascii=False)+'\n').encode()
def put(name, obj):
    with (O/name).open('xb') as f: f.write(encode(obj))
def pin(name):
    p=O/name; data=p.read_bytes()
    return {'path':name,'bytes':len(data),'SHA256':sha(data),'mode':stat.S_IMODE(p.stat().st_mode)}

assert not (O/'FINAL.json').exists() and not (O/'OWNED_MANIFEST.json').exists()
now=datetime.now(timezone.utc).isoformat()
c=json.loads((O/'CORRESPONDENCE.json').read_bytes())
assert c['status']=='GENUINE_CURRENT_COMMITTED_ARTICLE_CORRESPONDENCE'
assert all(x['matches'] for x in c['checksum_checks'])
assert all(x['byte_identical'] for x in c['native_asset_comparisons'] if x['file']!='SHA256SUMS.txt')
put('COMPLETION.json',{'UTC':now,'completion_percent':100,
    'scope':'Bounded current committed legacy correspondence only',
    'scientific_verdict':'Inherited clearance; no new verdict',
    'future_condition':'User-authorized routine redirect only after exact new target is live and verified',
    'live_UI_or_new_target_certified':False})
with (O/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n- '+now+' — Terminal checkpoint: current legacy identity and exact native PDF/ZIP correspondence established; independent bounded data review complete. All 10 checksum entries pass. Finite packet sealed; no further writes planned. Completion estimate: 100% of this bounded correspondence task; live replacement and redirect remain outside this packet.\n')

files=[]; dirs=[]
for p in sorted(O.rglob('*')):
    assert not p.is_symlink()
    rel=p.relative_to(O).as_posix()
    if p.is_dir(): dirs.append({'path':rel,'mode':stat.S_IMODE(p.stat().st_mode)})
    elif p.is_file(): files.append(pin(rel))
    else: raise RuntimeError('Non-regular object '+rel)
manifest={'schema':'finite-owned-packet-manifest-v1','UTC':now,'root':str(O),
    'root_mode':stat.S_IMODE(O.stat().st_mode),'files':files,'directories':dirs,
    'exact_terminal_exclusions':['OWNED_MANIFEST.json','FINAL.json'],
    'no_future_or_subtree_exclusions':True}
put('OWNED_MANIFEST.json',manifest)
final={'schema':'bounded-legacy-correspondence-final-v1','UTC':now,'row':184,'record':22983519,
    'status':c['status'],'completion_percent':100,'frozen':True,
    'remote_main_at_capture':c['remote_main_at_capture'],'docs_tree':c['current_docs_tree'],
    'legacy_URL':c['legacy_URL'],'current_HTML_path':c['current_HTML_path'],
    'HTML':next(x for x in c['objects'] if x['path'].endswith('/index.html')),
    'eventual_website_canonical':c['eventual_website_canonical'],
    'native_PDF_and_source_ZIP_byte_identical':True,'all_ten_checksum_entries_match':True,
    'site_and_native_checksum_files_have_different_coverage':True,
    'independent_adversarial_data_check':pin('INDEPENDENT_CHECK.md'),
    'clearance_SHA256':c['clearance_SHA256'],'clearance_commit':c['clearance_commit'],
    'scientific_clearance_inherited':True,'new_scientific_runs':0,
    'preserved_mistakes':['locator-attempt.tool-result.json','capture-attempt.tool-result.json'],
    'first_capture_reexecuted':False,'continuation_exit':0,
    'report':pin('REPORT.md'),'correspondence':pin('CORRESPONDENCE.json'),
    'execution':pin('EXECUTION.json'),'manifest':pin('OWNED_MANIFEST.json'),
    'manifest_payload_files':len(files),'total_owned_files_including_terminals':len(files)+2,
    'owned_child_directories':len(dirs),
    'live_UI_or_target_certified':False,'redirect_executed':False,'fetches':0,'mutating_Git_commands':0,
    'external_contact_or_individual_outreach_prepared':False,
    'scope_limit':'Current committed docs identity; no global/historical absence or priority claim',
    'routine_future_redirect':'Authorized by overall goal only after exact new target is live and verified; parent workflow revalidates then-current legacy article'}
put('FINAL.json',final)

# Terminal finite-file and digest validation. No subprocess or Git calls.
expected={x['path'] for x in files}|{'OWNED_MANIFEST.json','FINAL.json'}
actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}
assert expected==actual
for item in files: assert pin(item['path'])==item
assert pin('OWNED_MANIFEST.json')==final['manifest']
print(json.dumps({'status':'FROZEN_AND_VALIDATED','total_files':len(actual),
    'child_directories':len(dirs),'FINAL':pin('FINAL.json'),
    'manifest':pin('OWNED_MANIFEST.json'),'REPORT':pin('REPORT.md')},indent=2))
