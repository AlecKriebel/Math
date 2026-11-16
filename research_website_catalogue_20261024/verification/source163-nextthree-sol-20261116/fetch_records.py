"""One ordinary HTTPS GET per fixed published native record; no retry or code execution."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
import subprocess

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
RECORDS = [23357329, 23203143, 23153134]


def acquire(record):
    source = P / 'papers' / str(record) / 'sources'
    assert source.is_dir()
    for suffix in ['response.body', 'response.headers', 'curl.stdout.txt', 'curl.stderr.txt', 'transport.json']:
        assert not (source / ('record.' + suffix)).exists()
    url = 'https://zenodo.org/api/records/' + str(record)
    command = ['curl', '--disable', '--silent', '--show-error', '--request', 'GET', '--proto', '=https', '--connect-timeout', '15', '--max-time', '45', '--max-filesize', '16777216', '--dump-header', str(source / 'record.response.headers'), '--output', str(source / 'record.response.body'), '--write-out', '%{json}', url]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command, cwd=source, capture_output=True)
    (source / 'record.curl.stdout.txt').write_bytes(result.stdout)
    (source / 'record.curl.stderr.txt').write_bytes(result.stderr)
    try:
        transport = json.loads(result.stdout)
    except ValueError:
        transport = None
    receipt = {'UTC_start': start, 'UTC_end': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'command': command, 'exit': result.returncode, 'curl_transport': transport, 'retries': 0, 'followed_redirects': False, 'literal_stdout': 'record.curl.stdout.txt', 'literal_stderr': 'record.curl.stderr.txt', 'literal_headers': 'record.response.headers', 'literal_body': 'record.response.body'}
    (source / 'record.transport.json').write_text(json.dumps(receipt, indent=2) + '\n')
    summary = {'record': record, 'exit': result.returncode, 'HTTP': None if transport is None else transport.get('http_code')}
    if summary['HTTP'] == 200:
        native = json.loads((source / 'record.response.body').read_bytes())
        assert native['id'] == record
        summary.update(title=native['metadata']['title'], files=[x['key'] for x in native['files']], links=native['links'])
    return summary


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        for summary in pool.map(acquire, RECORDS):
            print(json.dumps(summary, ensure_ascii=False), flush=True)
