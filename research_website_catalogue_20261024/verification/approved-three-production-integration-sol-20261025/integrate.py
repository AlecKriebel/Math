"""Execute only the root-authorized exact three-paper production integration."""
from pathlib import Path
import datetime, difflib, hashlib, json, shutil, subprocess, sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
D = P/'verification/local-bosonic-stage-sol-20261025'
E = Path(__file__).resolve().parent
PY = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
RECORDS = ['23306332', '23203100', '22089807']

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while data := stream.read(1048576):
            h.update(data)
    return h.hexdigest()

def snapshot():
    return {str(x.relative_to(S)): {'sha256': sha(x), 'bytes': x.stat().st_size}
            for x in sorted((S/'public').rglob('*')) if x.is_file()}

def save(name, value):
    target = E/name
    assert not target.exists(), target
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')

baseline = json.loads((E/'premutation-custody.json').read_text())
assert baseline['issues'] == []
assert snapshot() == baseline['site_baseline'], 'Public site changed after last custody check'
assert not (E/'integration-command-results.json').exists(), 'Integration already attempted'
for cwd, expected in [(P, 'main'), (S, 'master')]:
    assert subprocess.check_output(['git', 'branch', '--show-current'], cwd=cwd, text=True).strip() == expected

proposals = [
    ('render_page.proposed.py', 'scripts/render_page.py', 'proposed-shared-renderer.diff'),
    ('bosonic_source.proposed.py', 'scripts/bosonic_source.py', 'proposed-new-source-adapter.diff'),
    ('final-content-check.proposed.py', 'verification/final-content-check.py', 'proposed-shared-checker.diff'),
]
for source, relative, patch in proposals:
    target = P/relative
    binding = baseline['proposal_bindings'][relative]
    assert sha(D/source) == binding['sha256']
    assert (sha(target) if target.exists() else None) == binding['baseline_sha256']
    old = target.read_text() if target.exists() else ''
    new = (D/source).read_text()
    compile(new, str(target), 'exec')
    actual = ''.join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True), fromfile='a/'+relative if old else '/dev/null', tofile='b/'+relative))
    assert actual == (D/patch).read_text(), relative
    assert 'stage.py' not in new and '/verification/local-' not in new
for rid in RECORDS:
    c = json.loads((P/'papers'/rid/'publication.json').read_text())
    assert not (S/'public/research'/c['slug']).exists()

# Preserve before-bytes only inside this assignment's new evidence folder.
for relative in ['scripts/render_page.py', 'verification/final-content-check.py']:
    target = E/'before/programme'/relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(P/relative, target)
for relative in ['public/research/index.html', 'public/research/sitemap.xml', 'public/research/research.css', 'public/robots.txt']:
    target = E/'before/site'/relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(S/relative, target)
save('git-before.json', {label: {'head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=cwd,text=True).strip(), 'branch': subprocess.check_output(['git','branch','--show-current'],cwd=cwd,text=True).strip()} for label,cwd in [('math',P),('site',S)]})

# The full .proposed.py bytes are the production authority, never stage copies.
for source, relative, patch in proposals:
    (P/relative).write_bytes((D/source).read_bytes())
    assert sha(P/relative) == baseline['proposal_bindings'][relative]['sha256']

results = []
for rid in RECORDS:
    command = [PY, '-B', str(P/'scripts/render_page.py'), rid]
    run = subprocess.run(command, cwd=P, text=True, capture_output=True)
    (E/('render-'+rid+'.stdout.txt')).write_text(run.stdout)
    (E/('render-'+rid+'.stderr.txt')).write_text(run.stderr)
    results.append({'record_id': rid, 'command': command, 'returncode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr})
    if run.returncode:
        save('integration-command-results.json', {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status':'STOPPED_RENDER_ERROR', 'results':results})
        raise SystemExit(run.returncode)
save('integration-command-results.json', {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status':'RENDER3_COMPLETE', 'results':results})
save('immediate-after-site.json', snapshot())
print(json.dumps({'status':'RENDER3_COMPLETE', 'records':RECORDS, 'render_exit_codes':[x['returncode'] for x in results]}))
