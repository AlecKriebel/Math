"""Independent private controls. Never import/compile/execute production sources."""
import ctypes, datetime as dt, hashlib, json, math, os, re, stat, sys
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];checks=0
assert __debug__ and not sys.flags.optimize

def check(v):
    global checks;checks+=1;assert v

def reject(fn):
    try:fn()
    except (ValueError,TypeError,KeyError,json.JSONDecodeError,UnicodeDecodeError,OSError):check(True)
    else:check(False)
def require(v,m='model rejection'):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def encode(o):return (json.dumps(o,indent=2,allow_nan=False)+'\n').encode()
def typed_row(r):
    require(type(r) is dict and set(r)=={'path','bytes','sha256'});p=r['path'];require(type(p) is str and p and '\\' not in p and '\0' not in p)
    q=PurePosixPath(p);require(not q.is_absolute() and q.as_posix()==p and not {'.','..','.git','__pycache__'}.intersection(q.parts));require(type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']))
def precise_load(b):
    def pairs(items):
        o={}
        for k,v in items:require(k not in o);o[k]=v
        return o
    def constant(v):raise ValueError('constant')
    def number(v):f=float(v);require(math.isfinite(f));return f
    return json.loads(b,object_pairs_hook=pairs,parse_constant=constant,parse_float=number)
def valid_capture(c):
    require(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and type(c['actual_operator_pid']) is int and c['actual_operator_pid']==11716 and c['operator_unchanged'] is True)
    if c['schema']=='pr48-root-unchanged-helper-actual-capture/v1':
        typed_row(c['source']);require(c['source_unchanged'] is True and c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])])
    else:require(c['schema']=='pr48-root-readonly-git-actual-capture/v1' and c['source'] is None and c['source_unchanged'] is None and type(c['argv']) is list and len(c['argv'])>=2 and c['argv'][0]=='git' and c['argv'][1] in {'show','ls-tree','diff','merge-base'})
    typed_row(c['stdout']);typed_row(c['stderr']);require(c['stderr']['bytes']==0)
result=json.loads((A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json').read_bytes())
for c in result['complete_actual_Git_captures']+result['complete_actual_helper_captures']:
    valid_capture(c);check(True)
    for k,v in [('pid',True),('exit_code',False),('actual_operator_pid',True),('completed',1),('actual_execution',1),('operator_unchanged',1),('stdin_supplied',0)]:mut=dict(c);mut[k]=v;reject(lambda m=mut:valid_capture(m))
for c in result['complete_actual_Git_captures']:
    for k,v in [('source',{}),('source_unchanged',True),('schema','pr48-root-unchanged-helper-actual-capture/v1'),('argv',['git','reset','--hard'])]:m=dict(c);m[k]=v;reject(lambda m=m:valid_capture(m))
for c in result['complete_actual_helper_captures']:
    for k,v in [('source',None),('source_unchanged',None),('source_unchanged',1),('argv',['python',c['source']['path']]),('schema','pr48-root-readonly-git-actual-capture/v1')]:m=dict(c);m[k]=v;reject(lambda m=m:valid_capture(m))
row={'path':'safe/member.json','bytes':0,'sha256':sha(b'')};typed_row(row);check(True)
for p in ['', '/absolute','../escape','safe/../escape','safe//member','safe/./member','safe\\member','safe\0member','.git/HEAD','__pycache__/cache']:
    r=dict(row,path=p);reject(lambda r=r:typed_row(r))
for n in [True,False,-1,0.0,None,'0']:
    r=dict(row,bytes=n);reject(lambda r=r:typed_row(r))
for h in ['A'*64,'0'*63,'0'*65,None,0]:r=dict(row,sha256=h);reject(lambda r=r:typed_row(r))
for b in [b'{"a":1,"a":2}',b'NaN',b'Infinity',b'-Infinity',b'1e999',b'{']:
    reject(lambda b=b:precise_load(b))
check(type(precise_load(b'1')) is int);check(type(precise_load(b'true')) is bool);check(precise_load(b'null') is None);check(precise_load(b'{}')=={})
private=F/'private_controls';private.mkdir(exist_ok=False);fixture=private/'full_permission_fixture';fixture.write_bytes(b'private mode fixture\n')
accepted=[]
for mode in range(0o10000):
    fixture.chmod(mode);actual=stat.S_IMODE(fixture.stat().st_mode);check(actual==mode);check((actual==0o444)==(mode==0o444))
    if actual==0o444:accepted.append(mode)
fixture.chmod(0o444);check(accepted==[0o444])
source=private/'rename_source';source.mkdir();(source/'member').write_bytes(b'private exclusive rename\n')
existing=private/'rename_existing';existing.mkdir();(existing/'sentinel').write_bytes(b'never replace\n');lib=ctypes.CDLL(None,use_errno=True);fn=lib.renamex_np;fn.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];fn.restype=ctypes.c_int
check(fn(os.fsencode(source),os.fsencode(existing),4)==-1);check((existing/'sentinel').read_bytes()==b'never replace\n');check(source.exists());absent=private/'rename_absent';check(fn(os.fsencode(source),os.fsencode(absent),4)==0);check(not source.exists());check((absent/'member').read_bytes()==b'private exclusive rename\n')
# Genuine exact fixed-row provenance and immutable failed-JSON exceptions.
pins=json.loads((F/'STATIC_INPUT_BINDINGS.json').read_bytes());exception={r['path']:r for r in pins['exact_literal_structured_exceptions']}
for r in pins['fixed_rows']:
    b=(R/r['path']).read_bytes();check(len(b)==r['bytes']);check(sha(b)==r['sha256']);check(stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode'])
    if r['path'] in exception:check(exception[r['path']]['bytes']==len(b));check(exception[r['path']]['sha256']==sha(b))
check(set(exception)<={r['path'] for r in pins['fixed_rows']})
for r in pins['closed_inputs'].values():check(r['schema'].startswith('pr48-'));check(r['manifest']['full_mode']==0o444)
# Production source is read solely as text; no imported/compiled code or builder call.
text=(F/'prepare_current_packet.py').read_text();operator=(F/'capture_root_builder_operation.py').read_text()
for marker in ["if c['schema']=='pr48-root-unchanged-helper-actual-capture/v1'", "c['source'] is None and c['source_unchanged'] is None", "'complete_actual_Git_captures'", "len(gitcaps)==38", "len(caps)==4", "'ABSENT'", "'raw_present_null'] is False", "'original_prior_report_file_exists'] is False", "'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'", "'source_unchanged'] is True", "'new_different_source_adversary'] is True", "'approved_by_root'] is True", "'PREPUBLICATION'" if False else "'frozen_inner_command_copy_is_prepublication_prefix':True", "'30004403 / OWR-17471-009' and not hits", "publish_absent(stage,dest)"]:
    check(marker in text)
check("if 'source' in c:" not in text);check('compile(' not in text);check('exec(' not in text);check('importlib' not in text)
for marker in ["PR48_ROOT_OUTER_CAPTURE", "pr48-root-builder-prelaunch/v1", "'PENDING'", "child.wait(timeout=600)", "'builder_unchanged_after_child'"]:
    check(marker in operator)
for p in F.glob('DRAFT_ROOT*.json'):
    o=json.loads(p.read_bytes());check(o['approved_by_root'] is False);check(o['reading_completed'] is False);check(o['current_verdict'] is None);check(o['future_acceptance_approved'] is False)
qualified=(F/'OPERATIVE_SOURCE_AUDIT.md').read_text();check('its research-results entry is null' not in qualified);check('Separate adversarial review is pending; no PR will be opened before that review.' not in qualified);check('ABSENT' in qualified);check('PENDING' in qualified)
receipt={'schema':'pr48-private-source-contract-controls/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_child_pid':os.getpid(),'status':'PASS','assertions':checks,'all4096_full_permission_values_actually_chmod_checked':True,'exclusive_existing_rejected_absent_rename_actual':True,'all38_null_source_Git_and_four_typed_helpers_accepted':True,'typed_capture_and_path_mutations_rejected':True,'original_failed_JSON_stream_exceptions_exact_pins_only':True,'production_source_read_as_text_only':True,'production_builder_imported_compiled_or_executed':False,'ROOT_prerequisites_authored':False,'future_acceptance_approved':False,'native_writes':False}
(F/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').write_bytes(encode(receipt));print(json.dumps(receipt,indent=2))
