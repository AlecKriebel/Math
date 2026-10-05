"""Exact Zenodo identity and controlled unauthenticated public HTTP reads."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit
import hashlib, json, subprocess, sys, os
if sys.flags.optimize:
    raise RuntimeError("Optimized Python is forbidden for publication identity checks.")

utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()

def identity(record, required=True):
    rid = record['id']
    assert type(rid) is int and rid > 0, 'Invalid record ID'
    expected = '10.5281/zenodo.' + str(rid)
    doi = record.get('doi')
    if required or doi is not None:
        assert doi == expected, 'DOI does not identify the exact record'
        assert record['doi_url'] == 'https://doi.org/' + expected
    if required or record.get('record_url') is not None:
        assert record['record_url'] == 'https://zenodo.org/records/' + str(rid)
    return rid

def resolution_binding(resolution, rid):
    assert type(rid) is int and rid > 0
    assert resolution['status'] == 'resolved' and resolution['http_status'] == 200
    assert resolution['url'] == 'https://doi.org/10.5281/zenodo.' + str(rid)
    p = urlsplit(resolution['resolved_url'])
    assert p.scheme == 'https' and p.netloc == 'zenodo.org'
    assert not p.query and not p.fragment
    assert p.path in {f'/records/{rid}', f'/records/{rid}/', f'/record/{rid}', f'/record/{rid}/'}, 'DOI resolves to a different record'

def public_request(directory, label, url, head=False):
    p = urlsplit(url)
    assert p.scheme == 'https' and p.netloc in {'zenodo.org', 'doi.org'}
    assert not p.query and not p.fragment
    assert Path(label).name == label
    # -q MUST be the first option. No configuration, netrc, cookies, user,
    # client certificate, or origin authorization can enter this request.
    argv = ['/usr/bin/curl', '-q', '--fail', '--silent', '--show-error',
        '--location', '--proto', '=https', '--proto-redir', '=https',
        '--no-netrc', '--header', 'Authorization:', '--header', 'Cookie:',
        '--max-time', '55', '--user-agent', 'Math-Zenodo-Deposit-Tool/1.0']
    if head:
        argv += ['--head', '--output', '/dev/null', '--write-out', '%{json}']
    argv.append(url)
    directory = Path(directory)
    assert not (directory/(label+'.execution.json')).exists()
    start = utc()
    timed_out = False
    try:
        run = subprocess.run(argv, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired as e:
        timed_out = True
        run = subprocess.CompletedProcess(argv,124,e.stdout or b'',e.stderr or b'')
    for stream, raw in [('stdout', run.stdout), ('stderr', run.stderr)]:
        (directory/(label+'.'+stream)).write_bytes(raw)
    native = dict(argv=argv, cwd=os.getcwd(), orchestrator_sha256=sha(Path(__file__).read_bytes()), started_utc=start, finished_utc=utc(),
        exit_code=run.returncode, timed_out=timed_out, stdout_bytes=len(run.stdout),
        stdout_sha256=sha(run.stdout), stderr_bytes=len(run.stderr),
        stderr_sha256=sha(run.stderr), automatic_retry=False,
        default_configuration_disabled=True, origin_credentials_absent=True)
    (directory/(label+'.execution.json')).write_text(json.dumps(native, indent=2)+'\n')
    assert run.returncode == 0 and not run.stderr, native
    return run.stdout, native

def resolve_exact(directory, rid):
    assert type(rid) is int and rid > 0
    url = 'https://doi.org/10.5281/zenodo.' + str(rid)
    raw, native = public_request(directory, 'exact_doi_resolution', url, head=True)
    result = json.loads(raw)
    resolution = dict(status='resolved', http_status=result['http_code'],
        url=url, resolved_url=result['url_effective'], native=native,
        controlled_unauthenticated_fresh_request=True)
    resolution_binding(resolution, rid)
    return resolution
