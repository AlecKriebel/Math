"""Read-only closure and retained-outcome replay. Caller MUST prehash this file.

Does not run lifecycle worlds, create authority, contact services or write files.
The complete manifest's SHA is supplied externally, never trusted from itself.
"""
from pathlib import Path
import argparse,ast,base64,gzip,hashlib,json,os,stat,sys
if sys.flags.optimize or not __debug__ or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Use Python -I -S -B optimize0')
E=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parsed(b):
    def pairs(items):
        out={}
        for k,v in items:need(k not in out,'duplicate JSON key');out[k]=v
        return out
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:need(False,'nonfinite JSON'))
def meta(p):
    s=p.lstat();return {'mode':s.st_mode,'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink,'inode':s.st_ino,'device':s.st_dev}
def check_manifest(wanted):
    raw=(E/'MANIFEST.json').read_bytes();need(sha(raw)==wanted,'externally pinned full closure manifest')
    mf=parsed(raw);need(mf['schema']=='SOURCE21-entire-preparation-closure-v1','closed schema')
    paths={'.':E,**{str(p.relative_to(E)):p for p in E.rglob('*')}}
    need(set(paths)==set(mf['entries']),'whole namespace including self reserve')
    for name,p in paths.items():
        record=mf['entries'][name];need(meta(p)==record['physical'],'full physical metadata '+name)
        need(not p.is_symlink(),'no symlink '+name)
        if name=='MANIFEST.json':need(record['self_reserved']is True,'self reserved manifest')
        elif p.is_file():
            b=p.read_bytes();need(record['bytes']==len(b)and record['sha256']==sha(b),'complete payload '+name)
        else:need(p.is_dir()and record['directory']is True,'regular file or directory '+name)
    need(mf['action_authority']is False and mf['publication_ready']is False,'no action endorsement')
    return mf
def native(path):
    n=parsed(gzip.decompress(path.read_bytes()))
    for key in ['stdout','stderr']:
        b=base64.b64decode(n[key+'_base64'],validate=True)
        need(len(b)==n[key+'_bytes']and sha(b)==n[key+'_sha256'],'complete native stream '+path.name)
    need(n['binary_outcome_preserved_before_interpretation']is True,'original binary before interpretation')
    need(n['original_argv'][1:4]==['-I','-S','-B'],'isolated child argv')
    return n,base64.b64decode(n['stdout_base64'])
def result_world(r):
    need(r['status']=='PASS'and r['error']is None,'complete final lifecycle outcome')
    need([v['action']for v in r['answers']]==['resume-stage','publish','verify-public','ledger'],'all four separately parsed lifecycle actions')
    need(r['native_calls']==['upload:finite-warm-thresholds.pdf','upload:finite-warm-thresholds-source-and-verification.zip','update','publish']and r['appends']==1,'known zero-create exact model effects')
    need(r['Git_writes']==[]and r['blocked_external_attempts']==[]and r['actual_service_effects']==0 and r['actual_AUTH_STATE_runtime_changes']is False,'no actual effects')
    need(r['readiness']is False and r['action_authority']is False,'no inferred readiness')
    names={v['name']for v in r['negative_controls']}
    for name in ['instance_shadow_authorize_wire','class_alias_authorize_wire','callback_alias_original_request','UI_need_helper_code_mutation','exact_initial_six_namespace_orphan','stage_known_reentry_consumed']:
        need(name in names,'required named final boundary control '+name)
def replay():
    external=parsed((E/'EXTERNAL_INPUTS21.json').read_bytes())
    for name,pin in external['files'].items():
        p=Path(name);b=p.read_bytes();need(len(b)==pin['bytes']and sha(b)==pin['sha256'],'complete selected immutable external input')
        need(meta(p)=={k:pin[k]for k in ['mode','mtime_ns','nlink','inode','device']},'selected external physical metadata')
    src=E/'source21';raw=(src/'SOURCE_MANIFEST21.json').read_bytes();mf=parsed(raw)
    need({p.name for p in src.iterdir()}==set(mf)|{'SOURCE_MANIFEST21.json'},'finite SOURCE21 namespace')
    for name,pin in mf.items():
        b=(src/name).read_bytes();need(pin=={'bytes':len(b),'sha256':sha(b)},'complete SOURCE21 body')
    entry=(E/'entry21.py').read_bytes();ns={'__file__':str(E/'entry21.py'),'__name__':'readonly21_closure_entry'};exec(compile(entry,str(E/'entry21.py'),'exec',dont_inherit=True,optimize=0),ns)
    need(ns['SOURCE21']==sha(raw),'entry actual source21 pin');ns['components']()
    for p in [E/'entry21.py',E/'native_step21.py',src/'overlay21.py']:ast.parse(p.read_bytes())
    outcome=parsed((E/'FINAL_CONTROL_SELECTION21.json').read_bytes());need(outcome['source21_sha256']==sha(raw),'operative source identity')
    for field,resultfile in [('world','INERT_WORLD_RESULT21.json'),('wiring','WIRING_CONTROLLER_RESULT21.json'),('authentication','AUTHENTICATION_RESULT21.json')]:
        p=E/outcome[field]['path'];need(sha(p.read_bytes())==outcome[field]['sha256'],'selected full original native pin')
        n,b=native(p);need(n['returncode']==0 and n['stderr_bytes']==0,'selected native complete success')
        need(n['caller_source_sha256']==sha((E/Path(n['caller_source_path']).name).read_bytes()),'selected exact executed test buffer')
        r=parsed(b);need(r==parsed((E/resultfile).read_bytes())and r['status']=='PASS','entire retained outcome equality')
        need(r['source21_sha256']==sha(raw),'selected native final source binding')
        if field in {'world','wiring'}:need(r['entry21_sha256']==sha(entry),'selected exact final entry binding')
        if field=='wiring':need(r['controller21_sha256']==sha((E/'native_step21.py').read_bytes()),'selected exact final controller binding')
        if field=='world':
            result_world(r);carrier=(E/'INERT_FULL_CAPTURE_CARRIER21.json.gz').read_bytes();need(sha(carrier)==r['complete_capture_carrier_sha256'],'complete readonly body carrier')
            c=parsed(gzip.decompress(carrier));bodies={k:base64.b64decode(v,validate=True)for k,v in c['bodies_base64'].items()}
            need(all(sha(v)==k for k,v in bodies.items())and all(k in bodies for k in c['paths'].values()),'full unique bodies and every original path')
            need(len(bodies)==r['complete_capture_bodies']and sum(map(len,bodies.values()))==r['complete_capture_raw_bytes'],'lossless carrier totals')
    # Active hash-consistent false expectations must be refused by the outcome
    # predicates independently of generic manifest or stream checks.
    r=parsed((E/'INERT_WORLD_RESULT21.json').read_bytes())
    for key,value in [('appends',2),('native_calls',['create']),('action_authority',True),('answers',[])]:
        bad=dict(r);bad[key]=value
        try:result_world(bad)
        except RuntimeError:pass
        else:raise RuntimeError('Accepted hash-consistent false world '+key)
    for p in (E/'templates').glob('*.json'):
        v=parsed(p.read_bytes());need(v['allowed_actions']==[]and v['expires_at']=='1970-01-01T00:00:00Z','inactive false example')
        for key in ['publication_ready','approved_for_actions','whole21_review_adopted','sole_entry20_authorized']:
            if key in v:need(v[key]is False,'false action flag '+key)
    need(not (E.parent/'known23592692_operations21_authority01').exists(),'no real SOURCE21 authority installed at preparation closure')
    need(not (E.parent/'root_actual21_known23592692_actions01').exists(),'no actual SOURCE21 native action OUT')
    return {'status':'PASS','source21_sha256':sha(raw),'entry21_sha256':sha(entry),'controller21_sha256':sha((E/'native_step21.py').read_bytes()),'external_selected_files':len(external['files']),'actual_service_effects':0,'action_authority':False,'publication_ready':False,'limits':'Retained qualified lifecycle model + entry spies + separate inert controller children; no fresh373 science rerun or actual production entry child world.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args();mf=check_manifest(a.manifest_sha256)
    need(os.statvfs(E).f_bavail*os.statvfs(E).f_frsize>=120*1024**2,'prospective readonly closure reserve')
    need(sum(q.lstat().st_blocks*512 for q in [E,*E.rglob('*')])<=40*1024**2,'own physical cap')
    result=replay();result.update(payload_entries=len(mf['entries']),manifest_sha256=a.manifest_sha256);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
