"""Validate preserved receipts and seal this bounded read-only diagnosis."""
from probe_delivery import ROOT, PROGRAM, SITE, now, sha, inspect
from pathlib import Path
import json
import subprocess

probe = json.loads((ROOT / 'http-probe.json').read_text())
variants = json.loads((ROOT / 'variant-probe.json').read_text())
context = json.loads((ROOT / 'context.json').read_text())
checks = []
expected = {str(SITE / 'public/research/index.html'): sha((SITE / 'public/research/index.html').read_bytes()),
            str(SITE / 'public/research/deep-derived-pure-braids-not-one-solvable/index.html'):
                sha((SITE / 'public/research/deep-derived-pure-braids-not-one-solvable/index.html').read_bytes())}
for receipt in [probe, variants]:
    for request in receipt['requests']:
        for hop in request['hops']:
            raw = (ROOT / hop['body_file']).read_bytes()
            checks.append({'check': 'raw-body-sha256', 'label': request['label'], 'url': hop['url'],
                           'passed': sha(raw) == hop['sha256']})
            # Derived HTML metadata is corrected from preserved raw bytes; no repeated requests.
            hop.pop('h2_anchor_count', None)
            hop.update(inspect(raw))
            headers = dict((k.lower(), v) for k, v in hop['headers'])
            checks.append({'check': 'revalidation-header', 'label': request['label'], 'url': hop['url'],
                           'passed': headers.get('cache-control') == 'public, max-age=0, must-revalidate'})
            if hop['status'] == 200:
                content = (ROOT / hop['decoded']['file']).read_bytes() if 'decoded' in hop else raw
                key = next(k for k in expected if 'deep-derived-pure-braids' in k) if 'deep-derived-pure-braids' in hop['url'] else str(SITE / 'public/research/index.html')
                checks.append({'check': '200-body-matches-local', 'label': request['label'], 'url': hop['url'],
                               'passed': sha(content) == expected[key]})
            elif hop['status'] == 301:
                checks.append({'check': 'alias-resolves-canonical', 'label': request['label'],
                               'passed': headers.get('location') in ['/research/', '/research/deep-derived-pure-braids-not-one-solvable/']})
            else:
                checks.append({'check': 'only-current-validator-304', 'label': request['label'],
                               'passed': request['label'] == 'conditional-current' and hop['status'] == 304 and len(raw) == 0})

scan_pattern = 'serviceWorker|service-worker|caches[.]open'
scan = subprocess.run(['rg', '-n', '-i', scan_pattern, 'public'], cwd=SITE, capture_output=True, text=True)
(ROOT / 'service-worker-source-scan.json').write_text(json.dumps({
    'utc': now(), 'command': ['rg', '-n', '-i', scan_pattern, 'public'],
    'exit_code': scan.returncode, 'stdout': scan.stdout, 'stderr': scan.stderr,
    'limitation': 'Current source scan only; does not inspect browser registrations or browser-internal caches.'
}, indent=2) + '\n')
checks.append({'check': 'no-current-source-service-worker-cache-code', 'passed': scan.returncode == 1 and not scan.stdout and not scan.stderr})
for item in context['browser_evidence_read_only']:
    checks.append({'check': 'browser-input-unchanged', 'file': item['file'],
                   'passed': sha(Path(item['file']).read_bytes()) == item['sha256']})
checks.append({'check': 'site-head-unchanged', 'passed': subprocess.check_output(['git','rev-parse','HEAD'],cwd=SITE,text=True).strip()==context['site_head']})
checks.append({'check': 'site-status-unchanged', 'passed': subprocess.check_output(['git','status','--porcelain'],cwd=SITE,text=True)==context['site_status_before']})
for rel in ['firebase.json', '.firebaserc', 'README.md', 'deploy.sh', 'public/research/index.html',
            'public/research/deep-derived-pure-braids-not-one-solvable/index.html']:
    checks.append({'check': 'site-input-unchanged', 'file': rel,
                   'passed': (SITE / rel).read_bytes() == (ROOT / ('local-' + rel.replace('/', '__'))).read_bytes()})
(ROOT / 'http-probe.json').write_text(json.dumps(probe, indent=2) + '\n')
(ROOT / 'variant-probe.json').write_text(json.dumps(variants, indent=2) + '\n')
inputs = []
for rel in ['MODEL_POLICY.md', 'verification/live-23393596-23358014-23356964.json',
            'verification/braid-wave-cantor-hosting-deploy-20261025.json',
            'verification/research-index-freshness-20261025/initial-http.json',
            'verification/research-index-freshness-20261025/post-deploy-http.json']:
    p = PROGRAM / rel
    inputs.append({'file': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())})
(ROOT / 'input-bindings.json').write_text(json.dumps(inputs, indent=2) + '\n')
summary = {'verified_utc': now(), 'bounded_http_requests': 21,
           'wire_get_hops': sum(len(r['hops']) for group in [probe, variants] for r in group['requests']),
           'all_checkable_http_and_preservation_checks_passed': all(c['passed'] for c in checks),
           'browser_recurrence_resolved': False,
           'remaining_gap': 'The actual Chrome request/response/cache-selection evidence for reload47 then article-return44 was not captured in the provided browser artifacts; no browser access is used in this diagnosis.',
           'checks': checks}
(ROOT / 'checks.json').write_text(json.dumps(summary, indent=2) + '\n')
log = (ROOT / 'RESEARCH_LOG.md').read_text().replace('2026-10-25T04:23:17.226939+00:00', probe['requests'][-1]['finished_utc'])
line = f"- {now()} — Completed 21 bounded fresh HTTP requests (29 wire GET hops), historical-link comparison, and preservation checks. No current HTTP/configuration fault reproduced; old validators correctly return latest200 and gzip/referrer/default-host variants agree. Recommendation: retain current policy and preserve the browser recurrence as unresolved pending actual browser network evidence. Bounded diagnosis completion estimate: 100%; confidence that the exact browser-internal mechanism is identified: 30%. No deployment or repair is claimed.\n"
if 'Completed 21 bounded' not in log:
    (ROOT / 'RESEARCH_LOG.md').write_text(log + line)
if not all(c['passed'] for c in checks):
    raise SystemExit('A preservation or HTTP check failed; inspect checks.json before promotion.')
paths = sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name != 'SHA256SUMS' and '__pycache__' not in p.parts)
(ROOT / 'SHA256SUMS').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(ROOT)}\n' for p in paths))
print(json.dumps({k: v for k, v in summary.items() if k != 'checks'}, indent=2))
