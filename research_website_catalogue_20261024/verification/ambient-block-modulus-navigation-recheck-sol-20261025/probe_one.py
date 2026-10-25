"""One bounded actual checker execution with a retained exact HTML read.

No HTML is copied or edited. All Python writes are confined to this new packet.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import builtins, hashlib, io, json, runpy

O = Path(__file__).resolve().parent
P = O.parents[1]
S = P/'verification/local-ambient-block-modulus-stage-sol-20261025'
A = P/'verification/audit-ambient-block-modulus-code-sol-20261025'
C = P/'verification/ambient-block-modulus-navigation-correction-sol-20261025'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

rid, case, mode = sys.argv[1:4]
need(rid in {'23333353','23416806','23441617'}, 'unauthorized record')
need(case in {'pristine','h1_valid_but_wrong_href','Research_valid_but_wrong_href'}, 'unauthorized case')
need(mode in {'normal','optimized'}, 'unauthorized mode')
need(sys.flags.optimize == (1 if mode == 'optimized' else 0), 'actual optimization mode mismatch')
candidate = C/'final-content-check.proposed.py'
need(hashlib.sha256(candidate.read_bytes()).hexdigest() == '60fdabc716e9dbf887f197aa1d5e726df8675cb646404ba79603995e54ed6a80', 'candidate byte pin')
executable = C/'final-content-check.stage.py'
old_root = 'R=Path(__file__).resolve().parents[1]\n'
need(executable.read_text() == candidate.read_text().replace(old_root, 'R=Path('+repr(str(P))+')\n'), 'private executable override')
config = json.loads((P/'papers'/rid/'publication.json').read_text())
target = S/'public/research'/config['slug']/'index.html'
original = target.read_bytes()
sample = None
if case == 'pristine':
    changed = original
else:
    sample = A/'navigation-fault-samples'/f'{rid}-{case}.html'
    changed = sample.read_bytes()
    retained = json.loads((A/'mutations'/f'{rid}-{case}-{mode}.json').read_text())
    need(hashlib.sha256(changed).hexdigest() == retained['changed_read_SHA256'], 'retained fault bytes differ')
    need(hashlib.sha256(original).hexdigest() == retained['original_SHA256'], 'pristine original differs')
    need(changed != original, 'fault is not a change')

base_bytes, base_text = Path.read_bytes, Path.read_text
reads = []
def overridden_bytes(path):
    if path == target:
        reads.append({'API':'read_bytes','sha256':hashlib.sha256(changed).hexdigest(),'bytes':len(changed)})
        return changed
    return base_bytes(path)
def overridden_text(path, encoding=None, errors=None):
    if path == target:
        reads.append({'API':'read_text','sha256':hashlib.sha256(changed).hexdigest(),'bytes':len(changed)})
        return changed.decode(encoding or 'utf-8', errors or 'strict')
    return base_text(path, encoding=encoding, errors=errors)
Path.read_bytes, Path.read_text = overridden_bytes, overridden_text

real_open = builtins.open
def guarded_open(file, mode='r', *args, **kwargs):
    if isinstance(file, (str, bytes, Path)) and any(x in mode for x in 'wax+'):
        need(Path(file).resolve().is_relative_to(O), 'write outside new recheck namespace: '+str(file))
    return real_open(file, mode, *args, **kwargs)
builtins.open = guarded_open
io.open = guarded_open
sys.path[:0] = [str(S), str(P/'scripts')]
sys.argv = [str(S/'stage_reader.py'), str(executable), rid,
            '--site', str(S/'public'), '--output-dir', str(O/'qa'/mode),
            '--output-stem', rid+'-'+case]
exit_code = 0
try:
    runpy.run_path(str(S/'stage_reader.py'), run_name='__main__')
except SystemExit as error:
    exit_code = error.code if isinstance(error.code, int) else 1
finally:
    modules = {}
    for name in ('ambient_block_modulus_source','abm_body_contract','published_assets','bosonic_source',
                 'dipole_source','cfh_source','cylinder_discotope_source','spanning_sos_gin_source'):
        module = sys.modules.get(name)
        if module is not None and getattr(module,'__file__',None):
            path = Path(module.__file__)
            data = base_bytes(path)
            modules[name] = {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    observation = {'record_id':rid,'case':case,'mode':mode,'actual_optimize_flag':sys.flags.optimize,
                   'target_HTML_path':str(target),'retained_sample_path':str(sample) if sample else None,
                   'pristine_sha256':hashlib.sha256(original).hexdigest(),
                   'actual_override_sha256':hashlib.sha256(changed).hexdigest(),
                   'actual_override_bytes':len(changed),'target_read_calls':reads,
                   'actual_imported_source_modules':modules,'HTML_written':False,
                   'candidate_proposed_sha256':hashlib.sha256(base_bytes(candidate)).hexdigest(),
                   'actual_private_executable_sha256':hashlib.sha256(base_bytes(executable)).hexdigest(),
                   'checker_exit_code':exit_code}
    (O/'read-observations'/f'{rid}-{case}-{mode}.json').write_text(json.dumps(observation,indent=2)+'\n')
need(bool(reads), 'no actual target HTML read occurred')
raise SystemExit(exit_code)
