"""Independent private OS/predicate controls; proposed production stays text only."""
import datetime as dt
import hashlib
import json
import math
import os
import stat
from pathlib import Path, PurePosixPath

F=Path(__file__).absolute().parent
R=F.parents[3]
V=F.parent/'acceptance_preparation_family_v3'
checks=0
rejections=[]
def need(v,label):
    global checks
    checks+=1
    if not v: raise ValueError(label)
def expect(label,callback):
    try: callback()
    except ValueError: rejections.append(label)
    else: raise AssertionError('Accepted negative '+label)
def sha(b): return hashlib.sha256(b).hexdigest()
def typed(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
    return a==b
def strict_json(b):
    def pairs(rr):
        d={}
        for k,v in rr:
            if k in d: raise ValueError('duplicate key')
            d[k]=v
        return d
    def floating(x):
        y=float(x)
        if not math.isfinite(y): raise ValueError('nonfinite float')
        return y
    def constant(x): raise ValueError('nonfinite constant')
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=constant)
def accepted_sealer(candidate,expected_parent,expected_sha):
    # Declarative identity: the same regular source at one allowed parent, with
    # every ancestor real. Never imports or launches the represented source.
    p=Path(candidate)
    need(p.is_absolute(),'absolute')
    need(p.parent==expected_parent and p.name=='seal_final_evidence.py','exact family and name')
    need(p.is_file() and not p.is_symlink(),'regular source')
    need(not any(q.is_symlink() for q in p.parents),'real ancestors')
    need(type(expected_sha) is str and sha(p.read_bytes())==expected_sha,'exact whole source')
    return str(p)
def all_native(expected,observed,allowed_body):
    need(set(expected)==set(observed) and len(expected)==13,'all13 domain')
    for name in expected:
        need(type(observed[name]['mode']) is int and observed[name]['mode']==expected[name]['mode'],'all13 full mode')
        if name not in allowed_body:
            need(observed[name]['body']==expected[name]['body'],'protected body')
def owned(name):
    return (name=='program/RESEARCH_LOG.md' or name in {'native/'+str(i) for i in range(13)} or
            name.startswith('audit48/') or name.startswith('canonical2961/'))
def foreign(names):
    need(type(names) is list and all(type(n) is str for n in names),'typed foreign')
    need(names==sorted(set(names)),'sorted unique')
    for name in names: need(not owned(name),'foreign not owned')
HEADER=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
def queue_edit(raw):
    lines=raw.decode().splitlines(keepends=True)
    header=[x for x in lines if x.startswith('| Rank | ID / code |')]
    need(len(header)==1 and [x.strip() for x in header[0].split('|')[1:-1]]==HEADER,'named columns')
    matched=[x for x in lines if len(x.split('|'))==14 and x.split('|')[2].strip()=='2961 / KP-4.85']
    need(len(matched)==1,'unique primary')
    need(not any(len(x.split('|'))==14 and x.split('|')[2].strip().startswith('30004403 / ') for x in lines),'no alias')
    row=matched[0]; parts=row.split('|')
    need(parts[8].strip()=='queued' and parts[9].strip()=='0/5','original primary status')
    parts[8]=' unsolved ';parts[9]=' 2/5 ';parts[11]=' qualified subgroup partial '
    patched='|'.join(parts); after=raw.replace(row.encode(),patched.encode(),1)
    need(after.replace(patched.encode(),row.encode(),1)==raw,'whole inverse')
    need({i for i,(a,b) in enumerate(zip(row.split('|'),parts)) if a!=b}=={8,9,11},'three named cells only')
    return after,row,patched
def closed_manifest(m,names):
    need(type(m) is dict and set(m)=={'schema','self_excluded','files_count','files'},'literal critical keys')
    need(m['schema']=='model/v1' and m['self_excluded']==['SELF_MANIFEST.json'],'exact self-only')
    need(type(m['files_count']) is int and m['files_count']==len(m['files']),'typed count')
    got=[]
    for n in m['files']:
        need(type(n) is str and n and PurePosixPath(n).as_posix()==n and not PurePosixPath(n).is_absolute() and not {'..','.git','__pycache__'}.intersection(PurePosixPath(n).parts),'canonical member')
        need(n!='SELF_MANIFEST.json','self excluded')
        got.append(n)
    need(len(set(got))==len(got) and set(got)|{'SELF_MANIFEST.json'}==names,'exact member closure')
def main():
    source={n:(V/n).read_text() for n in ['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']}
    op=source['capture_root_final_operation.py']; guard=source['pr48_guards.py']
    need("script.parent == A / 'acceptance_preparation_family_v3'" in op,'actual V3 literal folder')
    need(op.index('assert all(not parent.is_symlink()')<op.index('dest.mkdir')<op.index('proc = subprocess.Popen(argv'),'path checks before capture and source launch')
    need('native_modes(all_native)' in guard and 'check(R,remaining); native_modes(all_native); foreign_check(pre)' in guard,'actual full mode domain independent body exclusions')
    block=guard[guard.index('def write('):guard.index('def dump(')]
    need(block.index('s.flush()')<block.index('os.fchmod(')<block.index('os.fsync(s.fileno())')<block.index('os.replace('),'actual flush then mode then sync then replace')
    need('stat.S_IMODE(p.stat().st_mode)==previous_mode' in block,'actual postreplacement fullmode assertion')
    for name in ['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py']:
        text=source[name]
        need('pr48_guards' in text or 'def require' in text,'personally inspected production role text')
    fixture=F/'private_fixtures'; fixture.mkdir(exist_ok=False)
    observations=[]
    # Exercise real descriptor/rename permission semantics, without importing
    # proposed write(). Historical non-preserving model is a negative witness.
    for mode in [0o600,0o640,0o644,0o744,0o444,0o1644,0o2640,0o4600,0o7644]:
        old=fixture/('mode_'+oct(mode)); old.write_bytes(b'old');old.chmod(mode)
        fd=os.open(str(fixture/('staged_'+oct(mode))),os.O_CREAT|os.O_EXCL|os.O_RDWR,0o600)
        staged=fixture/('staged_'+oct(mode))
        try:
            need(os.write(fd,b'complete replacement body')==25,'whole private write')
            os.fchmod(fd,mode);os.fsync(fd)
            os.replace(staged,old)
            need(stat.S_IMODE(os.fstat(fd).st_mode)==mode and stat.S_IMODE(old.stat().st_mode)==mode,'real descriptor/rename fullmode')
            os.lseek(fd,0,os.SEEK_SET);need(os.read(fd,100)==b'complete replacement body','entire replacement descriptor body')
            observations.append({'mode':mode,'result':'preserved','bytes':25})
        finally: os.close(fd)
        old.chmod(0o600) # Keep inspectable owned private fixtures after observation.
    target=fixture/'m1_old_mode';target.write_bytes(b'old');target.chmod(0o600)
    tmp=fixture/'m1_nonpreserving';tmp.write_bytes(b'new');tmp.chmod(0o644);os.replace(tmp,target)
    need(stat.S_IMODE(target.stat().st_mode)!=0o600,'M1 actual negative witness')
    expected={'native/'+str(i):{'mode':0o600 if i%2 else 0o644,'body':bytes([i])} for i in range(13)}
    allowed={'native/'+str(i) for i in [0,1,7,12]}
    all_native(expected,expected,allowed)
    for n in expected:
        changed={k:dict(v) for k,v in expected.items()};changed[n]['mode']^=0o100
        expect('native_mode_'+n,lambda changed=changed:all_native(expected,changed,allowed))
        for bit in [0o1000,0o2000,0o4000]:
            changed={k:dict(v) for k,v in expected.items()};changed[n]['mode']^=bit
            expect('native_special_mode_'+n+'_'+oct(bit),lambda changed=changed:all_native(expected,changed,allowed))
    for n in expected:
        changed={k:dict(v) for k,v in expected.items()};changed[n]['body']=b'permitted body'
        if n in allowed: all_native(expected,changed,allowed)
        else: expect('protected_native_body_'+n,lambda changed=changed:all_native(expected,changed,allowed))
    wrong=dict(expected);wrong.pop('native/2');expect('missing_native_domain',lambda:all_native(expected,wrong,allowed))
    sealer=V/'seal_final_evidence.py'; sealer_sha=sha(sealer.read_bytes())
    need(accepted_sealer(sealer,V,sealer_sha)==str(sealer),'actual V3 path positive without launch')
    for p in [V.parent/'acceptance_preparation_family/seal_final_evidence.py',V.parent/'acceptance_preparation_family_v2/seal_final_evidence.py',V/'../acceptance_preparation_family_v3/seal_final_evidence.py',V/'integrate_reviewed_partial.py',Path('seal_final_evidence.py'),V/'unknown/seal_final_evidence.py']:
        expect('path_'+str(p),lambda p=p:accepted_sealer(p,V,sealer_sha))
    expect('wrong_source_sha',lambda:accepted_sealer(sealer,V,'0'*64))
    for x in [None,True,1,'']:
        expect('malformed_source_sha_'+repr(x),lambda x=x:accepted_sealer(sealer,V,x))
    local=fixture/'real_parent';local.mkdir();stub=local/'seal_final_evidence.py';stub.write_bytes(b'private source fixture, never executed')
    local_sha=sha(stub.read_bytes());link=fixture/'alias_parent';link.symlink_to(local,target_is_directory=True)
    expect('symlink_expected_parent',lambda:accepted_sealer(link/'seal_final_evidence.py',link,local_sha));link.unlink()
    direct=local/'direct.py';direct.symlink_to(stub)
    expect('direct_source_symlink_wrong_name',lambda:accepted_sealer(direct,local,local_sha));direct.unlink()
    original=stub.read_bytes();stub.unlink();stub.symlink_to(sealer)
    expect('exact_name_source_symlink',lambda:accepted_sealer(stub,local,sealer_sha));stub.unlink();stub.write_bytes(original)
    foreign(['another_problem/log.md'])
    for bad in [['program/RESEARCH_LOG.md'],['native/4'],['audit48/private.md'],['canonical2961/PARTIAL.md'],['z','a'],['a','a'],[True]]:
        expect('foreign_'+repr(bad),lambda bad=bad:foreign(bad))
    for raw in [b'{"a":1,"a":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}',b'{"x":-Infinity}']:
        expect('json_'+raw.decode(),lambda raw=raw:strict_json(raw))
    need(strict_json(b'{"a":null,"b":1,"c":true}')=={'a':None,'b':1,'c':True},'valid typed JSON positive')
    for a,b in [(True,1),(False,0),(None,{}),(1,1.0),({'a':1},{'a':True}),([1],[True])]:need(not typed(a,b),'type mutant rejects')
    header='| '+' | '.join(HEADER)+' |\n'
    values=['1','2961 / KP-4.85','literal target','EV','8','hard','2020','queued','0/5','KEEP_CHAT','old finding','KEEP_DOI']
    row='| '+' | '.join(values)+' |\n';other='| '+' | '.join(['2','42 / OTHER','other problem','EV','4','low','2020','queued','0/5','OTHER_CHAT','other finding','OTHER_DOI'])+' |\n'
    whole=('prefix\n'+header+row+other+'suffix\n').encode(); after,before_row,after_row=queue_edit(whole)
    need(other.encode() in after and b'KEEP_CHAT' in after and b'KEEP_DOI' in after and after.count(b'qualified subgroup partial')==1,'full other bytes/chat/DOI')
    for label,raw in [('duplicate_primary',whole+row.encode()),('alias',whole+row.replace('2961 / KP-4.85','30004403 / OWR-17471-009').encode()),('missing_primary',whole.replace(row.encode(),b'')),('wrong_header',whole.replace(b'| Status |',b'| STATUS |')),('wrong_turns',whole.replace(b'| 0/5 | KEEP_CHAT',b'| 2/5 | KEEP_CHAT'))]:expect('queue_'+label,lambda raw=raw:queue_edit(raw))
    mf={'schema':'model/v1','self_excluded':['SELF_MANIFEST.json'],'files_count':2,'files':['REPORT.md','nested/a']};names={'REPORT.md','nested/a','SELF_MANIFEST.json'};closed_manifest(mf,names)
    for key,value in [('self_excluded',['SELF_MANIFEST.json','extra']),('files_count',True),('files',['REPORT.md','REPORT.md']),('files',['REPORT.md','../outside']),('files',['REPORT.md','SELF_MANIFEST.json']),('schema','unknown/v1')]:
        bad=dict(mf);bad[key]=value;expect('closure_'+key+'_'+repr(value),lambda bad=bad:closed_manifest(bad,names))
    expect('closure_extra_member',lambda:closed_manifest(mf,names|{'extra'}))
    # Exact prior-state/history/accounting relation independent of native code.
    before={str(i):{'turns_used':1,'status':'old'} for i in range(38)};before['0']['turns_used']=8
    next_state={**before,'2961':{'turns_used':2,'status':'unsolved'}}
    need(len(before)==38 and sum(v['turns_used'] for v in before.values())==45,'predecessor state dimensions')
    need(len(next_state)==39 and sum(v['turns_used'] for v in next_state.values())==47 and all(typed(next_state[k],v) for k,v in before.items()) and '30004403' not in next_state,'one primary shared2/5, preserve prior states')
    old_history=b'{"old":1}\n';event=b'{"id":"2961","turns_used":2}\n';need((old_history+event).startswith(old_history),'full history prefix')
    need(38*100/180==21.11111111111111 and 37*100/180==20.555555555555557,'program percentage arithmetic')
    # Six repeated entries do NOT prove six distinct roles; ROOT remains owner.
    need(len(['preflight']*6)==6 and len(set(['preflight']*6))!=6,'automatic role-count limitation exposed')
    result={'schema':'pr48-v3-fresh-private-controls/v1','status':'PASS_PRIVATE_MODELS_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'assertions':checks,'expected_negative_controls':rejections,'real_OS_fullmode_cases':observations,'M1_old_model_actual_failure_witness':True,'six_role_count_not_distinct_role_guarantee':True,'production_imported_compiled_executed':False,'sealer_launched':False,'future_acceptance_approved':False}
    with (F/'PRIVATE_CONTROLS_RESULT.json').open('x') as h:json.dump(result,h,indent=2,sort_keys=True);h.write('\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
