"""Pure owned synthetic tests. Never imports any actual project source module."""
import sys
from pathlib import Path
import hashlib
import json
import os
import stat
import types

HERE = Path(__file__).absolute().parent
TARGET = HERE.parent / 'root_lifecycle_runner_01/run_lifecycle206_v3.py'
SOURCE = TARGET.read_bytes()
assert len(SOURCE) == 11168
assert hashlib.sha256(SOURCE).hexdigest() == '8d0aed332228ce340d09105ff9e85126d4f26f42da8cc620ed8e19f409053ecc'
assert stat.S_IMODE(TARGET.stat().st_mode) == 0o444
SCENARIO = sys.argv[1]
ROOT = HERE / 'final_dispatcher_fixtures' / SCENARIO / 'ROOT'
A = ROOT / 'draft_pr_publication_program_20260930/audits/pr206_5100062'
D = A / 'root_lifecycle_runner_01'
D.mkdir(parents=True)

def put(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    path.chmod(0o444)

def pin(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}

def enc(obj):
    return (json.dumps(obj, sort_keys=True) + '\n').encode()

DISPATCHER = D / 'run_lifecycle206_v3.py'
put(DISPATCHER, SOURCE)
M = types.ModuleType('audit_dispatcher')
M.__file__ = str(DISPATCHER)
exec(compile(SOURCE, str(DISPATCHER), 'exec'), M.__dict__)

if SCENARIO.startswith('checked_'):
    path = ROOT / 'input'
    body = b'safe fixture\n'
    want = pin(body)
    if SCENARIO == 'checked_fifo':
        os.mkfifo(path, 0o444)
    elif SCENARIO == 'checked_symlink':
        put(ROOT / 'referent', body)
        path.symlink_to(ROOT / 'referent')
    elif SCENARIO == 'checked_directory':
        path.mkdir()
    elif SCENARIO == 'checked_oversize':
        put(path, b'x' * 2000001)
    else:
        put(path, body)
        if SCENARIO == 'checked_fifo_swap':
            original_open = M.os.open
            def swap_open(p, *args, **kwargs):
                if p == path:
                    path.rename(ROOT / 'preserved_regular')
                    os.mkfifo(path, 0o444)
                return original_open(p, *args, **kwargs)
            M.os.open = swap_open
        if SCENARIO == 'checked_writable':
            path.chmod(0o644)
        if SCENARIO == 'checked_dotdot':
            (ROOT / 'subdir').mkdir()
            path = ROOT / 'subdir/../input'
    try:
        value = M.checked(path, want)
        print(json.dumps({'accepted': True, 'bytes': len(value)}))
    except BaseException as exc:
        print(json.dumps({'accepted': False, 'type': type(exc).__name__, 'message': str(exc)}))
    raise SystemExit(0)

F = types.ModuleType('audit_fixture')
F.events = []
F.installed = False
F.nodes = []
F.adapter = None
F.alias_reads = []
F.alias_writes = []
F.closed = 0
F.created = 0
F.secret = 'SYNTHETIC_CREDENTIAL_SENTINEL_206_AUDIT'
sys.modules['audit_fixture'] = F

def original_api(*aa, **kw):
    raise AssertionError('Synthetic API must not be called')

F.original_api = original_api

class Alias:
    def __init__(self, index):
        self.index = index
        self._api = original_api
    @property
    def api(self):
        F.alias_reads.append(self.index)
        if F.installed and SCENARIO == 'alias_read_failure' and self.index == 2:
            raise RuntimeError(F.secret)
        return self._api
    @api.setter
    def api(self, value):
        F.alias_writes.append((self.index, 'original' if value is original_api else 'cache'))
        if F.installed and SCENARIO in ('alias_restore_failure', 'chained_exception_uncaught') and self.index == 2 and value is original_api:
            raise RuntimeError(F.secret)
        self._api = value

def make_nodes(h):
    nodes = [h] + [Alias(i) for i in range(1, 6)]
    h.m = nodes[1]
    nodes[1].m = nodes[2]
    nodes[2].h = nodes[3]
    nodes[3].m = nodes[4]
    nodes[4].m = nodes[5]
    F.nodes = nodes
    return nodes

F.make_nodes = make_nodes

def method(owner, action, *args):
    F.events.append(['method', owner, action, list(args)])
    if SCENARIO in ('phase_exception', 'phase_exception_uncaught', 'chained_exception_uncaught'):
        raise RuntimeError(F.secret)
    return {'owner': owner, 'action': action, 'args': list(args)}

F.method = method
support = b'''import sys
F=sys.modules['audit_fixture']
F.events.append('support_compile')
def configure_authority(wanted):F.events.append('authority')
def writer_protocol():return {'synthetic_offline':True}
def gate(pin):F.events.append('gate')
def baseline_custody():F.events.append('custody')
def originals():F.events.append('originals')
def queue_rows():F.events.append('queue')
def generation(name):F.events.append(['generation',name])
def configure_backend(c,h):F.events.append('configure_backend')
'''
ready = b'''import sys
F=sys.modules['audit_fixture']
F.events.append('ready_compile')
def configure(s):F.events.append('ready_configure')
def inputs(pin):F.events.append('ready_inputs')
def bind(*a):return F.method('ready','bind',*a)
def prepare(*a):return F.method('ready','prepare',*a)
def verify(*a):return F.method('ready','verify',*a)
def accept(*a):return F.method('ready','accept',*a)
def sync(*a):return F.method('ready','sync',*a)
def pointer(*a):return F.method('ready','pointer',*a)
'''
lifecycle = b'''import sys
F=sys.modules['audit_fixture']
F.events.append('lifecycle_compile')
def configure(s,r,n):F.events.append('lifecycle_configure')
def bind(*a):return F.method('lifecycle','bind',*a)
def prepare(*a):return F.method('lifecycle','prepare',*a)
def verify(*a):return F.method('lifecycle','verify',*a)
def accept(*a):return F.method('lifecycle','accept',*a)
def sync(*a):return F.method('lifecycle','sync',*a)
def pointer(*a):return F.method('lifecycle','pointer',*a)
'''
native = b'''import sys
F=sys.modules['audit_fixture']
F.events.append('native_compile')
def configure(s):F.events.append('native_configure')
'''
sources = {'support206.py': support, 'ready206.py': ready,
           'lifecycle206.py': lifecycle, 'make_native206.py': native}
source_pins = {}
for name, body in sources.items():
    relative = M.OWN + '/' + name
    put(A / relative, body)
    source_pins[relative] = pin(body)

backend_pins = {}
legacy = b'''# synthetic inert exact-edit fixture
if TREE_CACHE_PATH.exists():
 for key,rows in json.loads(TREE_CACHE_PATH.read_text())['trees'].items():
  verify_tree_object(key,rows);native_tree_cache[key]={n:tuple(x) for n,x in rows.items()}
atexit.register(persist_authenticated_tree_cache)
'''
hbody = b'''import sys, types, importlib.util
F=sys.modules['audit_fixture'];F.events.append('h_compile')
api=F.original_api
TREE_CACHE={}
F.h_globals=globals()
def lookup():return TREE_CACHE
_self=types.SimpleNamespace()
_nodes=F.make_nodes(_self)
m=_nodes[1]
m.native_tree_cache=TREE_CACHE
F.nodes[0]=sys.modules['audit_dispatcher']._h_proxy if hasattr(sys.modules['audit_dispatcher'],'_h_proxy') else _self
'''
# h is not inserted into sys.modules by native(); use a frame-free holder and
# replace only its first node reference during adapter installation below.
hbody = hbody.replace(b"F.nodes[0]=sys.modules['audit_dispatcher']._h_proxy if hasattr(sys.modules['audit_dispatcher'],'_h_proxy') else _self\n", b'')
if SCENARIO.startswith('guard_'):
    call = {'guard_relative': "importlib.util.spec_from_file_location('bad','relative.py')",
            'guard_outside': "importlib.util.spec_from_file_location('bad','/outside.py')",
            'guard_kwargs': "importlib.util.spec_from_file_location('bad',__file__,loader=None)"}[SCENARIO]
    hbody += (call + '\n').encode()
adapter = b'''import sys
F=sys.modules['audit_fixture'];F.events.append('adapter_compile');F.adapter=sys.modules.get(__name__)
class TreeCache:
 def __init__(self):
  F.events.append('cache_init');F.created+=1;self.stats={'synthetic':True}
  if F.scenario=='constructor_failure':raise RuntimeError(F.secret)
 def close(self):
  F.events.append('cache_close');F.closed+=1
  if F.scenario=='close_failure':raise RuntimeError(F.secret)
F.original_init=TreeCache.__init__
F.cache_class=TreeCache
def install_loaded(c,h):
 F.events.append('install')
 if F.scenario=='install_before_constructor':raise RuntimeError(F.secret)
 cache=TreeCache()
 F.nodes[0]=h
 for obj in F.nodes:obj.api=cache
 F.installed=True
 if F.scenario=='install_after_aliases':raise RuntimeError(F.secret)
 return cache,lambda:None
'''
F.scenario = SCENARIO
for relative in sorted(M.BACKENDS):
    if relative.endswith('pr179_10800007/prepare_final_scoped_merge.py'):
        body = legacy
    elif relative.endswith('pr191_5000005/lifecycle_common.py'):
        body = b"import sys\nsys.modules['audit_fixture'].events.append('c_compile')\n"
    elif relative.endswith('pr190_5000007/prepare_final_scoped_merge.py'):
        body = hbody
    elif relative.endswith('immutable_tree_transport_01/tree_transport.py'):
        body = adapter
    else:
        body = b"raise AssertionError('Unused synthetic backend executed')\n"
    path = ROOT / relative
    put(path, body)
    backend_pins[relative] = {'original': pin(body), 'execution': pin(M.execution_buffer(path, body)), 'readonly': True}

gate = b'{"synthetic_gate":true}\n'
put(A / 'ROOT_PUBLICATION_GATE_01.json', gate)
adopt = {'schema': 'pr206-root-lifecycle-source-adoption-v1',
         'evidence_scope': 'ACTUAL_ROOT_RECEIPT',
         'accepted_preparation_only': True, 'PR': 206,
         'original_head': '488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7',
         'external_dispatcher_owns_authenticated_direct8_adapter_and_all_alias_cache_cleanup': True,
         'dispatcher_pin': pin(SOURCE), 'sources': source_pins,
         'loader_sources': backend_pins,
         'expected_publication_gate': {'path': 'ROOT_PUBLICATION_GATE_01.json', **pin(gate)},
         'program_view_writer_protocol': {'synthetic_offline': True}}
if SCENARIO == 'bad_graph':
    adopt['loader_sources']['fake'] = adopt['loader_sources'].pop(sorted(backend_pins)[0])
if SCENARIO == 'bad_dispatcher_pin':
    adopt['dispatcher_pin']['sha256'] = '0' * 64
if SCENARIO == 'bad_backend_pin':
    adopt['loader_sources'][sorted(backend_pins)[-1]]['original']['sha256'] = '0' * 64
if SCENARIO == 'bad_source_pin':
    adopt['sources'][sorted(source_pins)[-1]]['sha256'] = '0' * 64
if SCENARIO == 'bad_gate_pin':
    adopt['expected_publication_gate']['sha256'] = '0' * 64
adopt_bytes = enc(adopt)
put(A / M.ADOPTION, adopt_bytes)
if SCENARIO == 'bad_adoption_pin':
    adopt_bytes += b'corruption'

phase, action = 'ready', 'prepare'
if SCENARIO.startswith('route_'):
    _, phase, action = SCENARIO.split('_')
elif SCENARIO == 'preflight':
    action = 'preflight'
elif SCENARIO == 'bind':
    action = 'bind'

sys.modules['audit_dispatcher'] = M
old_aliases = {}
for alias in ['Root_support206', 'Root_ready206', 'Root_native206', 'Root_lifecycle206']:
    sentinel = types.ModuleType('prior_' + alias)
    sys.modules[alias] = sentinel
    old_aliases[alias] = sentinel
old_spec = M.importlib.util.spec_from_file_location
sys.argv = [str(DISPATCHER), '--adoption', M.ADOPTION,
            '--adoption-bytes', str(len(adopt_bytes)), '--adoption-sha256', pin(adopt_bytes)['sha256'],
            phase, action, 'synthetic_generation']
if phase != 'ready':
    sys.argv += ['--ack-path', 'ROOT_PR_METADATA_ACKNOWLEDGEMENT_01.json', '--ack-bytes', '1', '--ack-sha256', '0' * 64]

def run():
    M.main()

if SCENARIO in ('phase_exception_uncaught', 'chained_exception_uncaught'):
    M.entry()
else:
    caught = None
    try:
        run()
    except BaseException as exc:
        caught = {'type': type(exc).__name__, 'message': str(exc)}
    node_original = []
    for i, obj in enumerate(F.nodes):
        try:
            value = F.h_globals['api'] if i == 0 else (obj._api if isinstance(obj, Alias) else obj.api)
            node_original.append(value is original_api)
        except BaseException:
            node_original.append(False)
    print(json.dumps({'scenario': SCENARIO, 'exception': caught, 'events': F.events,
                      'alias_reads': F.alias_reads, 'alias_writes': F.alias_writes,
                      'alias_original': node_original, 'created': F.created, 'closed': F.closed,
                      'constructor_restored': not hasattr(F, 'cache_class') or F.cache_class.__init__ is F.original_init,
                      'spec_restored': M.importlib.util.spec_from_file_location is old_spec,
                      'module_aliases_restored': all(sys.modules[k] is v for k, v in old_aliases.items())}, sort_keys=True))
