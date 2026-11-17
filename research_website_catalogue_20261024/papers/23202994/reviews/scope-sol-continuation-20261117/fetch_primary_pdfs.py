"""Bounded passive official-primary PDF copy; no repository/scientific execution."""
import datetime, hashlib, json, pathlib, urllib.request
OWN = pathlib.Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23202994/reviews/scope-sol-continuation-20261117')
PIN = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'
ITEMS = [
 ('MAIN.pdf', 'https://raw.githubusercontent.com/openai/math/' + PIN + '/preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/paper.pdf', 792444, '50daa477c52b1f3e179764794506f0037d26c2ec130d1d6e817626f4e0b689f3'),
 ('ATOMIC.pdf', 'https://raw.githubusercontent.com/openai/math/' + PIN + '/preprints/An-atomic-certificate-for-triangular-lattice-universal-optimality-September-26-2026/paper.pdf', 481427, '83e0d874119abae56db94fb1ecd6ebb794753d4982464b4f9788e5158708be93'),
 ('HardinSaff-math-ph0311024v3.pdf', 'https://arxiv.org/pdf/math-ph/0311024v3', 325401, 'd031e7c826b8400440d0681da9c4d4297e56eb8765b1f335b0dd3dd10fd57167'),
]
receipts = []
for name, url, expected_bytes, expected_sha in ITEMS:
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    target = OWN / 'primary' / name
    assert not target.exists()
    request = urllib.request.Request(url, headers={'User-Agent': 'Independent mathematical source review'})
    with urllib.request.urlopen(request, timeout=45) as response:
        raw = response.read(2000001)
        final_url = response.url
        headers = dict(response.headers)
        status = response.status
    assert len(raw) <= 2000000 and raw.startswith(b'%PDF-')
    target.write_bytes(raw)
    actual_sha = hashlib.sha256(raw).hexdigest()
    matched = len(raw) == expected_bytes and actual_sha == expected_sha
    receipt = dict(name=name, requested_url=url, final_url=final_url, status=status, headers=headers, start_UTC=start, end_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), bytes=len(raw), SHA256=actual_sha, recorded_native_bytes=expected_bytes, recorded_native_SHA256=expected_sha, exact_native_match=matched)
    receipts.append(receipt)
    print(json.dumps(receipt), flush=True)
    if name in ('MAIN.pdf', 'ATOMIC.pdf'):
        assert matched
with (OWN / 'PDF_FETCH_RECEIPTS.json').open('x') as stream:
    json.dump(receipts, stream, indent=2)
    stream.write('\n')
