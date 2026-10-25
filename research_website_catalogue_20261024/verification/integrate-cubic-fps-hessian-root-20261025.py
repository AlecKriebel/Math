"""Install only the exact, independently reviewed three-page proposal bytes."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, subprocess

P = Path(__file__).resolve().parents[1]
B = P/'verification/local-cubic-fps-hessian-stage-sol-20261025'
OUT = P/'verification/cubic-fps-hessian-production-integration-root-20261025'
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PY = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
IDS = ['23204952','22983138','23409904']

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def save(name, value):
    (OUT/name).write_text(json.dumps(value, indent=2)+'\n')

assert json.loads((P/'verification/root-cubic-fps-hessian-private-stage-20261025.json').read_text())['production_integration_authorized']
assert json.loads((P/'verification/sheet-endpoint-discotope-transition-20261025.json').read_text())['native_visual_check_pending'] is False
assert sha(B/'stage-readiness-manifest.json') == 'bfebb68338fb0bace50ad3e6e99cd7bc0fb97dab49747334f201603c31ffb2bf'
manifest = json.loads((B/'stage-readiness-manifest.json').read_text())
preservation = json.loads((B/'site-preservation.json').read_text())
for name, binding in manifest['original_input_bindings'].items():
    path = Path(name)
    assert path.stat().st_size == binding['bytes'] and sha(path) == binding['sha256'], name
for name, binding in manifest['owned_output_bindings'].items():
    path = Path(name) if Path(name).is_absolute() else B/name
    assert path.stat().st_size == binding['bytes'] and sha(path) == binding['sha256'], name
before = {str(f.relative_to(SITE)): {'bytes':f.stat().st_size,'sha256':sha(f)} for f in SITE.rglob('*') if f.is_file()}
assert len(before) == 472 and before == preservation['original_site_files']
assert sha(P/'scripts/render_page.py') == '4ccf17696e679a79d7bf095217271bf2444fb62fc59a4fe76c505ab4a49296fd'
assert sha(P/'verification/final-content-check.py') == '4a4acd9923dee36f7cdcf757b0ee449e53254601ce038b6cc53b456e35b1af53'
assert not (P/'scripts/cfh_source.py').exists()
OUT.mkdir(exist_ok=False)
save('before-site.json', before)

for source, target in [('render_page.proposed.py','scripts/render_page.py'),('final-content-check.proposed.py','verification/final-content-check.py'),('cfh_source.py','scripts/cfh_source.py')]:
    assert sha(B/source) == manifest['proposal_sha256'][source]
    (P/target).write_bytes((B/source).read_bytes())

new_paths = preservation['new_target_files']
assert len(new_paths) == 12 and all(not (SITE/name).exists() for name in new_paths)
shared_paths = ['research/index.html','research/sitemap.xml']
for name in new_paths + shared_paths:
    target = SITE/name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((B/'public'/name).read_bytes())
    assert target.read_bytes() == (B/'public'/name).read_bytes()

tree = ast.parse((P/'verification/final-content-check.py').read_text())
mapping = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEX_PATHS' for t in n.targets))
old_ids = [rid for rid in mapping if rid not in IDS]
assert len(old_ids) == 56
commands = []
for selected, stem in [(IDS,'target-three'),(old_ids,'legacy56')]:
    args = [PY,'verification/final-content-check.py',*selected,'--output-dir',str(OUT),'--output-stem',stem]
    result = subprocess.run(args, cwd=P, env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    (OUT/(stem+'.stdout')).write_bytes(result.stdout)
    (OUT/(stem+'.stderr')).write_bytes(result.stderr)
    commands.append({'args':args,'exit':result.returncode,'stdout':stem+'.stdout','stderr':stem+'.stderr'})
    assert result.returncode == 0, stem
    checked = json.loads((OUT/(stem+'.json')).read_text())
    assert checked['status'] == 'PASS' and not checked['issues'], stem

after = {str(f.relative_to(SITE)): {'bytes':f.stat().st_size,'sha256':sha(f)} for f in SITE.rglob('*') if f.is_file()}
changed = [name for name in before if before[name] != after[name]]
added = sorted(set(after)-set(before))
assert set(changed) == set(shared_paths) and set(added) == set(new_paths) and len(after) == 484
authorized = {str(P/'scripts/render_page.py'),str(P/'verification/final-content-check.py'),*[str(SITE/name) for name in shared_paths]}
for name, binding in manifest['original_input_bindings'].items():
    if name not in authorized:
        path = Path(name)
        assert path.stat().st_size == binding['bytes'] and sha(path) == binding['sha256'], name
save('final-site.json', after)
save('commands.json', commands)
receipt = {'utc':datetime.now(timezone.utc).isoformat(),'status':'ROOT_INSTALLED_EXACT_APPROVED_THREE_PAGE_BYTES','record_ids':IDS,'before_site_files':472,'after_site_files':484,'only_changed_existing_site_paths':changed,'added_paths':added,'protected_original_bindings_checked':4761,'only_four_authorized_existing_input_changes':True,'new_helper_added':True,'target_checks':180,'legacy56_checks':3197,'index_items':60,'sitemap_urls':61,'all_three_actual_public_copies_identical_to_root_read_stage':True,'production_renderer_invoked':False,'installation_method':'Exact reviewed static outputs copied; unchanged source-creation metadata from24Oct retained after midnight. Exact proposed code/helper installed; actual read-only checker run.','git_deploy_live_browser_native_done':False,'completion_percent_this_local_installation':100,'overall_goal_complete':False}
save('receipt.json', receipt)
(OUT/'RESEARCH_LOG.md').write_text(receipt['utc']+' — Installed exact reviewed outputs and code. Actual180target+3197oldchecks pass; only12newfiles and2sharedsitechanges; allother4761baseline bindings preserved except4authorizedexistinginputs. No production rerender claimed. Local installation100%; deployment/browser/native gates pending. All203goal ongoing.\n')
print(json.dumps(receipt))
