"""Handwritten independent models, not imported or compiled production code."""
from pathlib import Path,PurePosixPath
from fractions import Fraction
import copy,datetime as dt,hashlib,json,math,os,stat
F=Path(__file__).resolve().parent
S=F.parent/'acceptance_preparation_family_v2'
checks=0;negatives=[];actual_modes=[]
def need(ok,message='independent control failed'):
    global checks
    checks+=1
    if not ok:raise ValueError(message)
def reject(label,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):negatives.append(label)
    else:raise ValueError('Accepted mutation: '+label)
def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def parse(raw):
    def pairs(items):
        obj={}
        for k,v in items:
            need(k not in obj,'duplicate JSON');obj[k]=v
        return obj
    def floating(s):v=float(s);need(math.isfinite(v),'nonfinite float');return v
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('nonfinite constant')))
for raw in [b'{"count":0,"count":0}',b'NaN',b'Infinity',b'-Infinity',b'1e999']:
    reject('strict-json-'+raw.decode(),lambda raw=raw:parse(raw))
need(same(parse(b'{"count":0,"attempts":[]}'),{'count':0,'attempts':[]}))
need(not same(False,0) and not same(True,1) and not same(0,0.0))
source_names=['pr49_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']
bodies={n:(S/n).read_bytes() for n in source_names};text={n:b.decode() for n,b in bodies.items()}
guard=text['pr49_guards.py'];operator=text['capture_root_final_operation.py'];integration=text['integrate_reviewed_partial.py']
for token in ["native_modes(all_rows)","check(R,remaining)","len(all_rows)==13", "pr48-acceptance-source-closure/v3", "p48/'acceptance_preparation_family_v3/ROOT_POST_CONTRACT.json'", "load(sm)['schema']=='pr48-acceptance-source-closure/v3'", "type(z.get('worktree_mode')) is int", "old_mode=stat.S_IMODE(old_stat.st_mode)","os.fchmod(s.fileno(),old_mode)","os.replace(tmp,p)","stat.S_IMODE(p.lstat().st_mode)==old_mode", "source_verification_responses' not in ledger", "regular(base,'prior_report.json').read_bytes()==b'null\\n'", "all(k" if False else "set(allowed)<=NATIVE"]:
    need(token in guard,'Source correspondence: '+token)
need(guard.index('os.fchmod(s.fileno(),old_mode)')<guard.index('os.replace(tmp,p)'))
need(operator.index('for ancestor in [script.parent,*script.parent.parents]')<operator.index('dest.mkdir(mode=0o700)'))
need("script.parent == A / 'acceptance_preparation_family_v2'" in operator)
need("set(changed)=={8,11}" in integration and "cells[9]==row.split('|')[9]" in integration)
names=[f'native/{i}' for i in range(13)];allowed=set(names[:4]);old=[dict(path=n,body=('old'+n).encode(),mode=0o644) for n in names]
def fresh(actual):
    need(len(actual)==13 and {r['path'] for r in actual}==set(names),'exact native13')
    for before,after in zip(old,actual):
        need(type(after['mode']) is int and 0<=after['mode']<=0o7777 and after['mode']==before['mode'],'complete permission identity')
        if before['path'] not in allowed:need(after['body']==before['body'],'unchanged nonallowed body')
ok=copy.deepcopy(old)
for r in ok[:4]:r['body']=b'allowed changed body'
fresh(ok)
for i in range(13):
    for mode in range(0o10000):
        need((type(mode) is int and 0<=mode<=0o7777 and mode==old[i]['mode'])==(mode==0o644),'fullmode predicate')
    bad=copy.deepcopy(ok);bad[i]['mode']=0o600
    reject('native-mode-every-path-'+str(i),lambda bad=bad:fresh(bad))
for i in range(4,13):
    bad=copy.deepcopy(ok);bad[i]['body']=b'forbidden'
    reject('native-body-nonallowed-'+str(i),lambda bad=bad:fresh(bad))
bad=copy.deepcopy(ok);bad[0]['mode']=True;reject('bool-native-mode',lambda:fresh(bad))
bad=copy.deepcopy(ok);bad[-1]['path']=bad[0]['path'];reject('duplicate-native-path',lambda:fresh(bad))
fixture=F/'fixtures';fixture.mkdir(exist_ok=True)
for mode in [0,0o600,0o644,0o1000,0o1600,0o2000,0o2600,0o4000,0o4600,0o7777]:
    p=fixture/('mode_'+oct(mode)+'.bin');p.write_bytes(b'old');p.chmod(mode)
    old_mode=stat.S_IMODE(p.stat().st_mode);need(old_mode==mode)
    tmp=p.with_suffix('.tmp')
    with tmp.open('xb+') as stream:
        stream.write(b'new');stream.flush();os.fchmod(stream.fileno(),old_mode);os.fsync(stream.fileno())
        os.replace(tmp,p);stream.seek(0)
        need(stream.read()==b'new' and stat.S_IMODE(p.stat().st_mode)==mode)
    actual_modes.append(dict(requested=mode,observed=stat.S_IMODE(p.stat().st_mode),body_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    p.chmod(0o644)
def parent_gate(path):
    need(path.is_absolute() and path.is_file() and not path.is_symlink(),'exact leaf')
    for ancestor in [path.parent,*path.parent.parents]:need(not ancestor.is_symlink(),'no symlink ancestors')
    need(path.parent==fixture/'acceptance_preparation_family_v2' and path.name=='seal_final_evidence.py','exact reviewed parent and basename')
exact=fixture/'acceptance_preparation_family_v2';exact.mkdir();(exact/'seal_final_evidence.py').write_bytes(b'private inert fixture only\n')
parent_gate(exact/'seal_final_evidence.py')
older=fixture/'acceptance_preparation_family';older.mkdir();(older/'seal_final_evidence.py').write_bytes(b'private inert fixture only\n')
reject('older-parent',lambda:parent_gate(older/'seal_final_evidence.py'))
reject('relative-parent',lambda:parent_gate(Path('acceptance_preparation_family_v2/seal_final_evidence.py')))
target=fixture/'alternate';target.mkdir();(target/'seal_final_evidence.py').write_bytes(b'private inert fixture only\n')
saved=fixture/'saved';exact.rename(saved);exact.symlink_to(target,target_is_directory=True)
reject('exact-parent-symlink',lambda:parent_gate(exact/'seal_final_evidence.py'));exact.unlink();saved.rename(exact)
leaf=exact/'seal_final_evidence.py';leaf.rename(exact/'retained_leaf.bin');leaf.symlink_to(exact/'retained_leaf.bin')
reject('exact-leaf-symlink',lambda:parent_gate(leaf));leaf.unlink();(exact/'retained_leaf.bin').rename(leaf)
closure_keys={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'}
good=dict(schema='pr48-acceptance-source-closure/v3',status='CLOSED_SOURCE_ONLY',utc=dt.datetime.now(dt.timezone.utc).isoformat(),self_excluded=['PREPARATION_MANIFEST.json'],files_count=0,files=[],source_only=True,proposed_helpers_imported_compiled_executed=False,future_acceptance_or_ROOT_approval_claimed=False)
def predecessor(o):
    need(type(o) is dict and set(o)==closure_keys,'exact closure9')
    need(o['schema']=='pr48-acceptance-source-closure/v3','exact successor version')
    need(type(o['files_count']) is int and o['files_count']==len(o['files']),'plain count')
    need(o['source_only'] is True and o['proposed_helpers_imported_compiled_executed'] is False and o['future_acceptance_or_ROOT_approval_claimed'] is False,'SOURCE cannot self approve')
predecessor(good)
for key,value,label in [('schema','pr48-acceptance-source-closure/v1','old-V1'),('schema','pr48-acceptance-source-closure/v2','old-V2'),('files_count',False,'bool-count'),('future_acceptance_or_ROOT_approval_claimed',True,'invented-future-approval'),('source_only',1,'integer-for-source-bool')]:
    bad=copy.deepcopy(good);bad[key]=value;reject(label,lambda bad=bad:predecessor(bad))
bad=copy.deepcopy(good);bad['future_EXECUTE']=True;reject('critical-extension',lambda:predecessor(bad))
def owned(n):return n.startswith('audit49/') or n.startswith('attempt30000703/') or n=='program/RESEARCH_LOG.md' or n in names
for n in ['program/RESEARCH_LOG.md','audit49/ROOT_RESEARCH_LOG.md','attempt30000703/science.md',*names]:reject('owned-not-foreign-'+n,lambda n=n:need(not owned(n)))
for n in ['unrelated/paper/log.txt','program/other_effort/log.md']:need(not owned(n))
header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
row='| 1 | 30000703 / OWR-1460-009 | boundary | 7 | 8 | 3 | 2007 | queued | 0/5 | preserve chat | preserve findings | preserve DOI |\n'
before=('foreign-before\n| '+' | '.join(header)+' |\n'+row+'foreign-after\n').encode()
def edit(raw):
    need(raw.count(row.encode())==1,'unique literal selected row');cells=row.split('|');need(cells[8].strip()=='queued' and cells[9]==' 0/5 ')
    cells[8]=' already_solved ';cells[11]=' credited known theorem ';new='|'.join(cells)
    need({i for i,(a,b) in enumerate(zip(row.split('|'),cells)) if a!=b}=={8,11});need(cells[9]==row.split('|')[9] and cells[10]==row.split('|')[10] and cells[12]==row.split('|')[12])
    out=raw.replace(row.encode(),new.encode(),1);need(out.replace(new.encode(),row.encode(),1)==raw);return out
edit(before);reject('queue-duplicate',lambda:edit(before+row.encode()))
ledger=parse((S/'EXPECTED_ORIGINAL_LEDGER.json').read_bytes());need(type(ledger['id']) is int and ledger['id']==30000703 and ledger['count']==0 and type(ledger['count']) is int and ledger['substantive_attempts']==[])
need('source_verification_responses' not in ledger)
scope=parse((S/'SCIENTIFIC_SCOPE.json').read_bytes())
need(scope['literal_target_status']=='already_solved' and scope['prior_publication_doi']=='10.1007/s11854-007-0009-x')
for k in ['project_solved','novelty_claimed','angular_only_sufficient','global_injectivity_claimed','finite_Blaschke_claimed','whole_circle_continuation_claimed','derivative_one_claimed','human_peer_review_claimed','formal_certification','paper_or_new_doi_or_tracker']:need(scope[k] is False)
for k in ['original_substantive_attempts','new_substantive_attempts','audit_turns']:need(type(scope[k]) is int and scope[k]==0)
need(scope['original_source_response_count'] is None and scope['original_response_field_absent'] is True)
prior={str(i):{'id':str(i),'turns_used':(47 if i==0 else 0),'turn_limit':50,'nested':['preserve',i]} for i in range(39)}
after=copy.deepcopy(prior);after['30000703']={'id':'30000703','turns_used':0,'turn_limit':5,'status':'already_solved'}
need(len(after)==40 and sum(z['turns_used'] for z in after.values())==47 and all(same(after[k],v) for k,v in prior.items()))
need(Fraction(39*100,180)==Fraction(65,3))
# Affine example along z=1-t^2+i*t: disk membership and exact distorted ratio.
for denominator in range(2,102):
    t=Fraction(1,denominator);x=t*t;y=t
    disk=2*x-x*x-y*y;ratio=2*disk/(4*x-x*x-y*y)
    need(disk>0 and ratio==2*(1-t*t)/(3-t*t) and ratio<Fraction(2,3))
result=dict(schema='pr49-fresh-independent-source-private-controls/v1',status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_pid=os.getpid(),assertions=checks,negative_controls=negatives,actual_descriptor_mode_cases=actual_modes,zero_permission_body_readback_via_retained_open_descriptor=True,all4096_modes_predicate_checked_for_each_of13_paths=True,source_bindings={n:dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest()) for n,b in bodies.items()},production_imported_compiled_executed=False,formal_certification=False,ROOT_approval_created=False,future_acceptance_approved=False,native_index_ref_remote_write=False)
(F/'PRIVATE_CONTROLS_RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps(result,sort_keys=True,indent=2))
