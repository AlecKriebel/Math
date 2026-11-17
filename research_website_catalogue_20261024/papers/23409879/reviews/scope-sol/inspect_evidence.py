"""Read-only data inspection; no import or execution of project/scientific code."""
from pathlib import Path
from decimal import Decimal
from html.parser import HTMLParser
import hashlib
import json
import stat
from datetime import datetime, timezone

R = Path(__file__).resolve().parent
S = R.parents[1] / 'sources'

def pin(p, root):
    st = p.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise RuntimeError('not an ordinary file: ' + str(p))
    b = p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(), bytes=len(b),
                SHA256=hashlib.sha256(b).hexdigest(), mode=oct(stat.S_IMODE(st.st_mode)))

def whole(root):
    files, dirs = [], []
    for p in sorted(root.rglob('*')):
        st = p.lstat()
        if stat.S_ISDIR(st.st_mode):
            dirs.append(dict(path=p.relative_to(root).as_posix(), mode=oct(stat.S_IMODE(st.st_mode))))
        elif stat.S_ISREG(st.st_mode):
            files.append(pin(p, root))
        else:
            raise RuntimeError('unexpected filesystem object: ' + str(p))
    return files, dirs

custody = json.loads((R / 'SOURCE_CUSTODY.json').read_text())
sf, sd = whole(S)
if sf != custody['files'] or sd != custody['directories']:
    raise RuntimeError('source byte/mode/namespace drift')
if oct(stat.S_IMODE(S.lstat().st_mode)) != custody['root_mode']:
    raise RuntimeError('source root mode drift')
initial = json.loads((R / 'INITIAL_MANIFEST.json').read_text())
for p in initial['payload_files']:
    if pin(R / p['path'], R) != p:
        raise RuntimeError('initial payload drift: ' + p['path'])
for name, digest in {
    'INITIAL_MANIFEST.json':'040ca9503d696d1360130388457a5a4ca18640cff8967ccfc2278fbba70e2a70',
    'INITIAL_SEAL.json':'833bc2dc68db3cb011a51ef1c9e59c45396825a79fde8871fc3efc416148b3b2'
}.items():
    if pin(R / name, R)['SHA256'] != digest:
        raise RuntimeError('initial terminal-control drift: ' + name)
for d in initial['directories']:
    if oct(stat.S_IMODE((R / d['path']).lstat().st_mode)) != d['mode']:
        raise RuntimeError('initial directory mode drift')

native = S / 'published-source/container-001/tree/verification/parity_controls.py'
copy = R / 'native-run/parity_controls.py'
if native.read_bytes() != copy.read_bytes():
    raise RuntimeError('executed copy differs from original')
if (R / 'native-run/stderr.txt').read_bytes() != b'':
    raise RuntimeError('native stderr was nonempty')
data = json.loads((R / 'native-run/results/parity_controls_results.json').read_text())
if (data['precision_decimal_digits'], data['mpmath_version'], data['sympy_version']) != (100, '1.3.0', '1.14.0'):
    raise RuntimeError('native dependency/precision mismatch')
if data['exact'] != {'symbolic_factorization':'exact zero residual', 'rational_divisor_cases_N_3_to_100':1521}:
    raise RuntimeError('unexpected exact result')
rows = data['numeric']
if len(rows) != 117 or len({(v['k'],v['N'],v['tau']) for v in rows}) != 117:
    raise RuntimeError('unexpected numeric case extent')
positive, negative = [], []
for v in rows:
    p, m = (Decimal(v[k]) for k in ('relative_phase_spread_focus_plus','relative_phase_spread_focus_minus'))
    residual = Decimal(v['tangent_formula_max_relative_residual'])
    swap = Decimal(v['antipodal_phase_swap_max_log_error'])
    if not (residual < Decimal('1e-85') and swap < Decimal('1e-85')):
        raise RuntimeError('output residual exceeded declared threshold')
    if v['N'] % 4 == 0:
        if not (p < Decimal('1e-85') and m < Decimal('1e-85')):
            raise RuntimeError('positive-case output threshold failed')
        positive.append((p, m))
    else:
        if not (p > Decimal('1e-70') and m > Decimal('1e-70')):
            raise RuntimeError('negative-case output threshold failed')
        negative.append((p, m))

class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.row = None
        self.rows = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'figure' and a.get('id') in ('T1','T2','T3'):
            self.current = a['id']
        if self.current and tag == 'tr':
            self.row = []
        if self.current and tag == 'math' and self.row is not None:
            self.row.append(a.get('alttext'))
    def handle_endtag(self, tag):
        if tag == 'tr' and self.current and self.row is not None:
            self.rows.append({'table':self.current,'math_alttext':self.row})
            self.row = None
        if tag == 'figure':
            self.current = None

t = Tables()
t.feed((R / 'primaries/dlmf22.4.html').read_text())
out = dict(UTC=datetime.now(timezone.utc).isoformat(),
    status='DATA_GUARDS_AND_ALL_OUTPUT_RECORDS_INSPECTED',
    source_regular_files=len(sf), source_child_directories=len(sd), source_all_bytes_modes_exact=True,
    original_INITIAL_25_files_preserved=True,
    native_copy=pin(copy,R), native_exit=0, native_stderr_empty=True,
    native_scientific_invocations=1, native_result_records_read_as_data=len(rows),
    exact_result=data['exact'], numeric_positive_cases=len(positive), numeric_negative_cases=len(negative),
    max_positive_relative_spread=str(max(x for pair in positive for x in pair)),
    min_negative_relative_spread=str(min(x for pair in negative for x in pair)),
    max_tangent_relative_residual=str(max(Decimal(x['tangent_formula_max_relative_residual']) for x in rows)),
    max_phase_swap_log_error=str(max(Decimal(x['antipodal_phase_swap_max_log_error']) for x in rows)),
    DLMF_selected_tables=t.rows,
    primary_pins=[pin(R/'primaries'/x,R) for x in ('stachel2105.03624.pdf','ferudun.pdf','dlmf22.4.html')],
    numerical_samples_are_universal_proof=False,
    current174root_peer_opinions_accessed=False)
print(json.dumps(out, indent=2))
