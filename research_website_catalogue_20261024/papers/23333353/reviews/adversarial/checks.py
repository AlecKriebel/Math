"""Independent exact diagnostics and read-only original custody; no network or supplied code.

Run with the existing shared-math-runtime Python, without -O. The --verify-only
mode repeats the checks without any writes. Initial receipt mode writes only
two named fresh receipts in this script's own namespace; never rewrites them.
Finite diagnostics do not prove any all-word or infinite-copy statement.
"""
from pathlib import Path, PurePosixPath
import datetime
import hashlib
import json
import stat
import sys
import zipfile
import sympy as s

if sys.argv[1:] not in ([], ['--verify-only']):
    raise SystemExit('usage: checks.py [--verify-only]')
VERIFY_ONLY = sys.argv[1:] == ['--verify-only']
OUT = Path(__file__).resolve().parent
P = OUT.parents[3]
SRC = P / 'papers/23333353/sources'
checks = []


def need(name, condition, detail=None):
    if not condition:
        raise RuntimeError(name + ': ' + str(detail))
    checks.append({'name': name, 'verified': True, 'detail': detail})


def sha(data):
    return hashlib.sha256(data).hexdigest()


def binding(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}


def write_new(name, obj):
    with (OUT / name).open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


need('ordinary assertions-enabled runtime', sys.flags.optimize == 0)
expected = {
    'SOURCE_READY.json': '7ee6c2ca13b7f3222af3a5d323faa70956eb1aeb283c71194d43eda2e71c4d5f',
    'SOURCE_READY_MANIFEST.json': 'b295d697a9e43eab226f7dac7416ac854245486f071e5f1474ab1087c34b09a3',
    'SOURCE_READY_SEAL.json': '5a4e063a16235f413ed17859c7944a997a33ea761424f1ab0d97e1c431891c04',
}
for name, digest in expected.items():
    need('supplied source authentication: ' + name, sha((SRC / name).read_bytes()) == digest)
manifest = json.loads((SRC / 'SOURCE_READY_MANIFEST.json').read_text())
originals = []
for b in manifest['files']:
    pp = PurePosixPath(b['path'])
    need('original canonical path: ' + str(pp), not pp.is_absolute() and '..' not in pp.parts)
    path = SRC / pp
    got = binding(path)
    need('original bytes: ' + str(pp), got['bytes'] == b['bytes'] and got['sha256'] == b['sha256'])
    originals.append(got)
need('69 complete original bindings', len(originals) == manifest['file_count'] == 69)
record = json.loads((SRC / 'record.raw.json').read_text())
ready = json.loads((SRC / 'SOURCE_READY.json').read_text())
latest = json.loads((SRC / 'latest.raw.json').read_text())
versions = json.loads((SRC / 'versions.raw.json').read_text())
need('actual record/version/date identities', record['id'] == latest['id'] == 23333353
     and record['metadata']['version'] == '1.0'
     and record['metadata']['publication_date'] == '2026-10-12'
     and record['created'] == '2026-10-13T05:53:41.831316+00:00'
     and versions['hits']['total'] == 1)
need('two genuine published file objects', len(record['files']) == len(ready['all_actual_assets']) == 2)
for asset in ready['all_actual_assets']:
    obj = asset['api_file_object']
    need('complete asset file object: ' + obj['key'], obj in record['files'] and obj in latest['files'])
    data = (SRC / obj['key']).read_bytes()
    need('actual asset bytes and MD5: ' + obj['key'], len(data) == obj['size'] == asset['bytes']
         and sha(data) == asset['sha256']
         and 'md5:' + hashlib.md5(data).hexdigest() == obj['checksum'])
members = []
with zipfile.ZipFile(SRC / 'verification_package.zip') as z:
    need('all ZIP CRCs', z.testzip() is None)
    names = set()
    for info in z.infolist():
        pp = PurePosixPath(info.filename)
        mode = info.external_attr >> 16
        need('safe original member: ' + info.filename,
             not info.is_dir() and not pp.is_absolute() and '..' not in pp.parts
             and str(pp) == info.filename and info.filename not in names
             and not stat.S_ISLNK(mode))
        names.add(info.filename)
        data = z.read(info)
        extracted = SRC / 'published-source' / pp
        need('member exact extracted bytes: ' + info.filename,
             extracted.read_bytes() == data and len(data) == info.file_size)
        members.append({'name': info.filename, 'bytes': len(data), 'sha256': sha(data), 'CRC': info.CRC})
need('60 complete regular ZIP members', len(members) == 60 and sum(x['bytes'] for x in members) == 233585)

primary_base = P / 'papers/23333353/reviews/scope/cache/primary'
primary_expected = {
    'owr2009-09.pdf': 'b3c4037dd84c3dccae4fd3b941a11fb3b9957865671ee940879be489e54c7aeb',
    'dkw-v3.pdf': 'c7349b4d3b185ec25bbf6c67e57fee504e7f94c624754ff44972ea2703992e72',
    'crismale-fidaleo.pdf': '3844909c51cad99d516d83179442c5704fa5340211b6fc3c76637faa3584833a',
}
primaries = []
for name, digest in primary_expected.items():
    b = binding(primary_base / name)
    need('actual primary: ' + name, b['sha256'] == digest)
    primaries.append(b)

prior_expected = {
    'papers/23074543/reviews/adversarial': '289a69d2eb79c2f907b584bf3eb34e16d5e7e04a98669e4052ac87ccfaf49aa7',
    'verification/cfh-independent-code-audit-sol-20261025': '08df6760943ae91c7fb4f22b5bc6952aea2325bc87ae1b1623a47af5dbdb984f',
    'papers/23442760/reviews/adversarial': '97745de4ecdbbfd9cdd465150871285f42a484668e12f88ea4852b48e33e5518',
    'papers/23395703/reviews/adversarial': 'cfa3ba1ab7d58027bca29c4e443afc24bd1e5da956107876c9d91f163fcf2ece',
}
prior = []
for rel, digest in prior_expected.items():
    d = P / rel
    seal = json.loads((d / 'FINAL_SEAL.json').read_text())
    need('prior exact seal: ' + rel, sha((d / 'FINAL_SEAL.json').read_bytes()) == digest)
    mf = d / seal['manifest']
    need('prior exact manifest: ' + rel, sha(mf.read_bytes()) == seal['manifest_sha256'])
    files = json.loads(mf.read_text())['files']
    if isinstance(files, dict):
        files = [dict(v, path=k) for k, v in files.items()]
    gotfiles = []
    for b in files:
        f = d / b['path']
        got = binding(f)
        need('prior owned evidence: ' + str(f), got['bytes'] == b['bytes'] and got['sha256'] == b['sha256'])
        gotfiles.append(got)
    prior.append({'namespace': str(d), 'seal': binding(d / 'FINAL_SEAL.json'),
                  'manifest': binding(mf), 'owned_files': gotfiles})

# Exact diagnostics: rational/surd arithmetic only, no random sampling.
one = s.ones(4, 1)
pv = s.Matrix([0, 0, 1, 1])
qv = s.Matrix([0, 1, 0, 1])
pqv = pv.multiply_elementwise(qv)
need('four-point basis determinant', abs(s.Matrix.hstack(one, pv, qv, pqv).det()) == 1)
need('scalar B/C intersection', s.Matrix.hstack(one, pv, -one, -qv).rank() == 3)
p, q = s.diag(*pv), s.diag(*qv)
u = s.Matrix([1, 0, 0, 1]) / s.sqrt(2)
rho = u * u.T
need('pure coherent density', rho * rho == rho and s.trace(rho) == 1 and rho.rank() == 1)
need('exact diagonal restriction', [rho[i, i] for i in range(4)] == [s.Rational(1, 2), 0, 0, s.Rational(1, 2)])
need('four necessary moments', [(u.T * a * u)[0] for a in [p, q, p*q, q*p]] == [s.Rational(1, 2)] * 4)
need('algebras distinct proper', s.Matrix.hstack(one, pv, qv).rank() == 3 and s.Matrix.hstack(one, pv).rank() == 2)
ut = s.Matrix([s.sqrt(3)/2, 0, 0, s.Rational(1, 2)])
need('quarter-weight coherent control', (ut.T * ut)[0] == 1 and (ut.T * p*q * ut)[0] == s.Rational(1, 4))
need('endpoints are characters', all((s.eye(4)[:, i].T * p*q * s.eye(4)[:, i])[0] == t for i, t in [(0, 0), (3, 1)]))

R = s.Matrix([[s.Rational(1,2), s.Rational(1,2), 0], [s.Rational(1,2), s.Rational(1,2), 0], [0,0,0]])
S = R + s.diag(0,0,1)
Omega = s.Matrix([1,0,0])
v = R * Omega
need('null-vector/operator negative control', R*R == R and S*S == S and R != S
     and R*Omega == S*Omega and R*v == S*v == v)

# A two-copy quotient: first copy id, second copy tau(p)=q,tau(q)=p.
# The orbit-supported state is extreme invariant on the quotient by proof,
# and quotient descent proves the pullback extreme. These finite equalities
# authenticate the construction, while DERIVATIONS.md proves all laws.
tau = s.zeros(4)
for i, j in enumerate([0,2,1,3]):
    tau[i,j] = 1
psi = s.Matrix([[0, s.Rational(1,2), s.Rational(1,2), 0]])
need('two-copy equivariant involution', tau*tau == s.eye(4) and tau*pv == qv and tau*qv == pv and psi*tau == psi)
need('two-copy correct B1/C2 full-law generators', tau*qv == pv and (psi*pv)[0] == s.Rational(1,2))
need('two-copy differs on untested same-copy pq', (psi*pqv)[0] == 0)
need('zero/invertible CS obstruction', s.det(s.Matrix([[0,1],[1,s.symbols('m', real=True)]])) == -1)
need('fixed-marginal decomposition constituents excluded', s.Matrix([[1,0,0,0]]) != s.Matrix([[s.Rational(1,2),0,0,s.Rational(1,2)]])
     and s.Matrix([[0,0,0,1]]) != s.Matrix([[s.Rational(1,2),0,0,s.Rational(1,2)]]))

utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
custody = {'utc': utc, 'status': 'ALL_BOUND_ORIGINAL_AND_PRIMARY_AND_PRIOR_PACKET_BYTES_VERIFIED',
           'source_authentication': [binding(SRC / n) for n in expected],
           'whole_original_bindings': originals, 'original_archive_members': members,
           'primary_bindings': primaries, 'prior_packet_bindings': prior,
           'scope_primary_receipt': binding(P / 'papers/23333353/reviews/scope/primary-fetch-receipts.json'),
           'originals_or_prior_files_modified': False}
if not VERIFY_ONLY:
    write_new('ORIGINAL_BINDINGS.json', custody)
result = {'utc': utc, 'status': 'EXACT_DIAGNOSTICS_AND_CUSTODY_COMPLETED',
          'python': sys.version, 'sympy': s.__version__, 'checks': checks,
          'finite_diagnostics_are_universal_proofs': False,
          'universal_proof_artifact': 'DERIVATIONS.md',
          'supplied_or_historical_code_executed': False,
          'writes': ['ORIGINAL_BINDINGS.json', 'CHECK_RESULTS.json']}
if not VERIFY_ONLY:
    write_new('CHECK_RESULTS.json', result)
print(json.dumps({'checks': len(checks), 'originals': len(originals), 'members': len(members),
                  'primaries': len(primaries), 'prior_packets': len(prior), 'status': result['status']}))
