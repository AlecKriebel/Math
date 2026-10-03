"""Check all package bytes and rerun exact mathematical certificates.
Requires Python 3.10+ and a C++17 compiler called g++. Standard library only.
All generated files stay in an automatically removed temporary directory.
"""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,shutil,subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
manifest=load(HERE/'MANIFEST.json')
expected={r['path'] for r in manifest['files']}
actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*')
        if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
assert actual==expected and len(expected)==len(manifest['files'])
for r in manifest['files']:
    p=HERE/r['path']
    assert not p.is_symlink() and p.resolve().is_relative_to(HERE.resolve())
    b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
records=gzip.decompress((HERE/'certificates/30_action_records.txt.gz').read_bytes())
assert len(records)==15258431
assert sha(records)=='af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf'
assert len(records.splitlines())==90921
twenty=gzip.decompress((HERE/'certificates/20_full_actions.jsonl.gz').read_bytes())
rows=[json.loads(line) for line in twenty.splitlines()]
assert len(rows)==810 and len({tuple(r['word']) for r in rows})==810
def inv(w):return tuple(-x for x in reversed(w))
def reduce_word(w):
    stack=[]
    for x in w:
        if stack and stack[-1]==-x:stack.pop()
        else:stack.append(x)
    return tuple(stack)
def subst(w,tables):
    return reduce_word(v for x in w for v in (tables[x-1] if x>0 else inv(tables[-x-1])))
A=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),
   ((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),
   ((1,),(2,),(3,),(3,-2,1,4))]
assert len(A)==5 and all(len(table)==4 and all(isinstance(w,tuple) and all(isinstance(x,int) and 1<=abs(x)<=4 for x in w) for w in table) for table in A)
def action(word):
    images=tuple((j,) for j in range(1,5))
    for g in word:images=tuple(subst(w,A[g-1]) for w in images)
    return images
h=(5,4,3,2,1,1,2,3,4,5);target=action(h+h)
universe=set()
for start in range(6):
    def walk(pos,counts,w):
        if len(w)==20:
            if pos==start:universe.add((start+1,w))
            return
        for nxt in (pos-1,pos+1):
            if not 0<=nxt<6:continue
            edge=min(pos,nxt)
            if counts[edge]==4:continue
            nc=list(counts);nc[edge]+=1;walk(nxt,tuple(nc),w+(edge+1,))
    walk(start,(0,)*5,())
assert {(r['center'],tuple(r['word'])) for r in rows}==universe
survivors=set()
for r in rows:
    im=action(r['word'])
    assert tuple(tuple(w) for w in r['images'])==im
    assert r['survives']==(im==target)
    if r['survives']:survivors.add(tuple(r['word']))
assert survivors=={(h+h)[j:]+(h+h)[:j] for j in range(20)}
with tempfile.TemporaryDirectory(prefix='wajnryb-fixed-input-') as temporary:
    work=Path(temporary);candidate=work/'candidate'
    shutil.copytree(HERE/'reference',candidate)
    def execute(args):
        r=subprocess.run(list(map(str,args)),cwd=work,capture_output=True)
        assert r.returncode==0,(args,r.stderr.decode(errors='replace'))
        assert r.stderr==b'',(args,r.stderr)
        return r.stdout
    for n in range(1,5):
        assert execute([sys.executable,'-B',candidate/f'check_turn_{n}.py'])==(candidate/f'TURN_{n}_CHECKS.json').read_bytes()
    assert execute([sys.executable,'-B',candidate/'verify_turn_4_cpp.py'])==(candidate/'TURN_4_CPP_CHECKS.json').read_bytes()
    assert execute([sys.executable,'-B',candidate/'review/independent_check.py'])==(candidate/'review/INDEPENDENT_CHECKS.json').read_bytes()
    out=execute([sys.executable,'-B',candidate/'verify_publication.py'])
    assert out==b'PASS: all frozen public bytes, four Python receipts, C++ full stream, and independent review controls\n'
    executable=work/'direct_cpp'
    assert execute(['g++','-O3','-std=c++17',candidate/'check_turn_4.cpp','-o',executable])==b''
    streamed=execute([executable,'--stream'])
    lines=streamed.splitlines(keepends=True)
    assert b''.join(line for line in lines if line.startswith(b'S|'))==records
    terminal=json.loads(lines[-1])
    assert terminal=={'status':'PASS','reachable_states':234368,'outgoing_edges':711342,
                     'coaccessible_states':90921,'coaccessible_edges':261810}
    independent=work/'independent';independent.mkdir()
    for name in ('fullstreams','receipts'):(independent/name).mkdir()
    shutil.copyfile(HERE/'independent_20_30.py',independent/'independent_20_30.py')
    begin=datetime.now(timezone.utc)
    out=execute([sys.executable,'-B',independent/'independent_20_30.py'])
    finish=datetime.now(timezone.utc)
    actual_independent=json.loads(out)
    assert begin<=datetime.fromisoformat(actual_independent['utc'])<=finish
    expected_independent=load(HERE/'independent_expected.json')
    assert actual_independent.keys()==expected_independent.keys()
    assert {k:v for k,v in actual_independent.items() if k!='utc'}=={k:v for k,v in expected_independent.items() if k!='utc'}
    assert gzip.decompress((independent/'fullstreams/independent_backward_records.txt.gz').read_bytes())==records
    # A second independently authored true backward graph, across ranks1..6.
    snapshot=work/'snapshot/problems/11000151_artin_a5_quotient'
    snapshot.mkdir(parents=True)
    shutil.copyfile(candidate/'check_turn_4.cpp',snapshot/'check_turn_4.cpp')
    ranks=work/'rank_control';ranks.mkdir();(ranks/'receipts').mkdir()
    shutil.copyfile(HERE/'independent_ranks1_6.py',ranks/'independent_ranks1_6.py')
    begin=datetime.now(timezone.utc)
    out=execute([sys.executable,'-B',ranks/'independent_ranks1_6.py'])
    finish=datetime.now(timezone.utc)
    decoder=json.JSONDecoder();text=out.decode();values=[]
    while text.strip():
        value,end=decoder.raw_decode(text.lstrip());values.append(value)
        text=text.lstrip()[end:]
    expected_ranks=load(HERE/'independent_ranks_expected.json')
    assert len(values)==7 and values[:6]==expected_ranks['ranks']
    actual_ranks=values[-1]
    assert actual_ranks==load(ranks/'receipts/INDEPENDENT_FINITE_CONTROLS.json')
    assert actual_ranks.keys()==expected_ranks.keys()
    assert begin<=datetime.fromisoformat(actual_ranks['utc'])<=finish
    assert {k:v for k,v in actual_ranks.items() if k!='utc'}=={k:v for k,v in expected_ranks.items() if k!='utc'}
    for rank in range(1,7):
        expected_records=(gzip.decompress((HERE/f'certificates/rank{rank}_action_records.txt.gz').read_bytes()) if rank<6 else records)
        assert (ranks/f'private_streams/rank{rank}_all_coaccessible_actions.txt').read_bytes()==expected_records
    assert (ranks/'private_streams/all_810_F4_actions.jsonl').read_bytes()==twenty
print('PASS: complete package, all810 actions, all90921 records, author and both independent backward full replays')
