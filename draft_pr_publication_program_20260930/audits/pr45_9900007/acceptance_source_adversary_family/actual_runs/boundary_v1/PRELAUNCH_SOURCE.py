"""Independent tiny hostile fixtures; never load production as Python code."""
from pathlib import Path, PurePosixPath
import argparse, copy, datetime as dt, hashlib, json, os, stat
H=Path(__file__).resolve().parent
def insist(value, label):
    if not value: raise ValueError(label)
def exact(x,y):
    if type(x) is not type(y): return False
    if type(x) is dict: return x.keys()==y.keys() and all(exact(x[k],y[k]) for k in x)
    if type(x) is list: return len(x)==len(y) and all(exact(a,b) for a,b in zip(x,y))
    return x==y
def relative(s):
    insist(type(s) is str and s and '\\' not in s and '\0' not in s,'path type')
    p=PurePosixPath(s)
    insist(not p.is_absolute() and p.as_posix()==s and not set(p.parts)&{'.','..','.git','__pycache__'},'path normalization')
    return p
def regular(base,name):
    relative(name);p=base/name
    insist(base.is_dir() and not base.is_symlink() and p.is_file() and not p.is_symlink(),'regular file')
    insist(p.resolve(strict=True).is_relative_to(base.resolve(strict=True)),'bounded root')
    q=p.parent
    while q!=base:
        insist(q.is_dir() and not q.is_symlink(),'real ancestor');q=q.parent
    return p
def closed(base,m):
    insist(type(m) is dict and set(m)=={'schema','self_excluded','files_count','files'},'whole schema')
    insist(m['schema']=='own-fixture/v1' and exact(m['self_excluded'],['SELF.json']),'sole self')
    insist(type(m['files_count']) is int and type(m['files']) is list and m['files_count']==len(m['files']),'count types')
    names={'SELF.json'}
    for z in m['files']:
        insist(type(z) is dict and set(z)=={'path','bytes','sha256'},'whole row schema');relative(z['path'])
        insist(z['path'] not in names and type(z['bytes']) is int and z['bytes']>=0,'member uniqueness/type');names.add(z['path'])
        b=regular(base,z['path']).read_bytes();insist(len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256'],'entire body')
    actual=set();dirs=set()
    for p in base.rglob('*'):
        name=p.relative_to(base).as_posix();relative(name);insist(not p.is_symlink() and (p.is_file() or p.is_dir()),'no special members')
        (actual if p.is_file() else dirs).add(name)
        if p.is_file():insist(stat.S_IMODE(p.stat().st_mode)==0o444,'literal fullmode')
    expected={x.as_posix() for n in names for x in PurePosixPath(n).parents if str(x)!='.'}
    insist(names==actual and dirs==expected,'entire topology')
def reject(fn,label,out):
    try:fn()
    except (ValueError,TypeError,KeyError):out.append(label);return
    raise ValueError('Hostile fixture escaped: '+label)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-tag',required=True);v=ap.parse_args();relative(v.run_tag)
    d=H/'boundary_fixtures';d.mkdir();f=d/'sub';f.mkdir();body=f/'body.txt';body.write_bytes(b'own inert body\n');body.chmod(0o444)
    m={'schema':'own-fixture/v1','self_excluded':['SELF.json'],'files_count':1,'files':[{'path':'sub/body.txt','bytes':len(body.read_bytes()),'sha256':hashlib.sha256(body.read_bytes()).hexdigest()}]}
    (d/'SELF.json').write_text(json.dumps(m)+'\n');(d/'SELF.json').chmod(0o444);closed(d,m);out=[]
    mutations=[]
    z=copy.deepcopy(m);z['self_excluded'].append('extra.json');mutations.append(('extra self exclusion',z))
    z=copy.deepcopy(m);z['files_count']=True;mutations.append(('boolean member count',z))
    z=copy.deepcopy(m);z['files'].append(copy.deepcopy(z['files'][0]));z['files_count']=2;mutations.append(('duplicate member',z))
    z=copy.deepcopy(m);z['files'][0]['bytes']=True;mutations.append(('boolean bytes',z))
    z=copy.deepcopy(m);z['files'][0]['annotation']='smuggled';mutations.append(('extra row key',z))
    z=copy.deepcopy(m);z['files'][0]['sha256']='0'*64;mutations.append(('body identity substitution',z))
    for label,z in mutations:reject(lambda z=z:closed(d,z),label,out)
    extra=d/'extra.txt';extra.write_text('own unlisted file\n');extra.chmod(0o444);reject(lambda:closed(d,m),'unlisted file',out);extra.unlink()
    empty=d/'empty';empty.mkdir();reject(lambda:closed(d,m),'unlisted empty directory',out);empty.rmdir()
    leaf=d/'leaf_link';leaf.symlink_to(body);reject(lambda:regular(d,'leaf_link'),'actual leaf symlink',out);leaf.unlink()
    ancestor=d/'ancestor_link';ancestor.symlink_to(f,target_is_directory=True);reject(lambda:regular(d,'ancestor_link/body.txt'),'actual ancestor symlink',out);ancestor.unlink()
    for mode in [0o644,0o1444,0o2444,0o4444]:
        body.chmod(mode);reject(lambda:closed(d,m),'actual hostile fullmode '+oct(mode),out)
    body.chmod(0o444);closed(d,m)
    old={'state':{'a':{'turns':1,'solved':False,'runtime':None}},'history':'complete prefix\n','inventory':[{'pr':44,'done':True}],'post':{'schema':'future45/v1','native13':[{'path':str(i),'mode':0o644} for i in range(13)]}}
    z=copy.deepcopy(old);z['state']['a']['turns']=True;reject(lambda:insist(exact(z,old),'full type boundary'),'entire old state bool substitution',out)
    z=copy.deepcopy(old);z['history']='prefix\n';reject(lambda:insist(exact(z,old),'complete prefix boundary'),'truncated whole history',out)
    z=copy.deepcopy(old);z['post']={'targets':36,'turns':44};reject(lambda:insist(exact(z,old),'whole post boundary'),'abbreviated post counters',out)
    z=copy.deepcopy(old);z['inventory'][0]['done']=1;reject(lambda:insist(exact(z,old),'whole inventory boundary'),'entire inventory type substitution',out)
    def approval(draft):
        insist(type(draft) is dict and set(draft)=={'root_read','source_adversary_read','utc','execution_approved'},'full approval schema')
        insist(draft['root_read'] is True and draft['source_adversary_read'] is True and draft['execution_approved'] is True,'genuine new approval')
        t=dt.datetime.fromisoformat(draft['utc']);insist(t.utcoffset()==dt.timedelta(0) and t<=dt.datetime.now(dt.timezone.utc),'aware actual UTC')
    reject(lambda:approval({'root_read':False,'source_adversary_read':False,'utc':None,'execution_approved':False}),'draft cannot approve',out)
    reject(lambda:approval({'root_read':True,'source_adversary_read':True,'utc':'2999-01-01T00:00:00+00:00','execution_approved':True}),'future UTC cannot approve',out)
    reject(lambda:approval({'root_read':True,'source_adversary_read':True,'utc':'2026-10-03T00:00:00','execution_approved':True}),'naive UTC cannot approve',out)
    result={'schema':'pr45-adversary-private-boundary-controls/v1','status':'PASS_PRIVATE_HOSTILE_FIXTURES_ONLY','actual_child_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'rejected':out,'healthy_before_and_after':True,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'fixtures_are_own_inert_models_not_production_runtime_tests':True}
    with(H/'BOUNDARY_CONTROL_RESULTS.json').open('x')as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
