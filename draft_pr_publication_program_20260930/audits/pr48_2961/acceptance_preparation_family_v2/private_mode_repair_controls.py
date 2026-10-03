"""Handwritten private filesystem/predicate models; never imports production."""
from pathlib import Path
import hashlib,json,os,stat,datetime as dt
F=Path(__file__).absolute().parent
R=F.parents[3]
OLD=F.parent/'acceptance_preparation_family'
COUNT=0
NEG=[]
def need(v,m):
    global COUNT
    COUNT+=1
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,o):
    with p.open('x') as f:f.write(json.dumps(o,sort_keys=True,indent=2)+'\n')
def reject(label,action):
    try:action()
    except ValueError:NEG.append(label)
    else:raise ValueError('Accepted negative '+label)
def mode(path):return stat.S_IMODE(path.stat().st_mode)
def reference(path):b=path.read_bytes();return {'path':path.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)}
def native_predicate(rows,files,allowed):
    need(type(rows) is list and len(rows)==13 and len({z['path'] for z in rows})==13,'Entire thirteen distinct mode domain')
    for row in rows:
        need(type(row['worktree_mode']) is int and 0<=row['worktree_mode']<=0o7777,'Typed full mode')
        p=files[row['path']]
        need(mode(p)==row['worktree_mode'],'All thirteen modes, including allowed body paths')
        if row['path'] not in allowed:need(p.read_bytes()==row['original'],'Only allowed bodies may differ')
def independent_replacement(path,body):
    before=mode(path);stage=path.with_name(path.name+'.private-stage')
    with stage.open('xb') as h:
        h.write(body);h.flush();os.fchmod(h.fileno(),before);os.fsync(h.fileno())
    os.replace(stage,path)
    need(path.read_bytes()==body and mode(path)==before,'Actual complete body and full mode preserved')
def old_loss_model(path,body):
    stage=path.with_name(path.name+'.old-private-stage')
    with stage.open('xb') as h:h.write(body);h.flush();os.fsync(h.fileno())
    os.replace(stage,path)
def main():
    before_mask=os.umask(0o022)
    try:
        d=F/'private_mode_models_v2';d.mkdir(exist_ok=False);observations=[]
        for value in [0o600,0o644,0o1600,0o2600,0o4600,0o7644]:
            p=d/('preserve_'+oct(value)+'.bin');p.write_bytes(b'original body\n');os.chmod(p,value);need(mode(p)==value,'Actual selected full preimage mode')
            old=reference(p);old_mode=mode(p);independent_replacement(p,b'changed complete body\n');observations.append({'before':old,'after':reference(p),'before_mode':old_mode,'after_mode':mode(p),'expected_mode':value,'actual_umask':0o022})
        bad=d/'old_loss0600.bin';bad.write_bytes(b'original body\n');os.chmod(bad,0o600);old_loss_model(bad,b'correct new body\n');need(mode(bad)==0o644 and bad.read_bytes()==b'correct new body\n','Actual V1 mode-loss countermodel reproduced privately')
        nominal=d/'old_nominal0644.bin';nominal.write_bytes(b'original body\n');os.chmod(nominal,0o644);old_loss_model(nominal,b'correct new body\n');need(mode(nominal)==0o644,'Nominal0644 old model remains qualified')
        files={};rows=[];allowed={'native0','native1','native2','native3'}
        for i in range(13):
            n='native'+str(i);p=d/(n+'.bin');p.write_bytes(('original'+str(i)).encode());os.chmod(p,0o600 if i%2==0 else 0o644);files[n]=p;rows.append({'path':n,'original':p.read_bytes(),'worktree_mode':mode(p)})
        for n in allowed:independent_replacement(files[n],b'allowed changed native body')
        native_predicate(rows,files,allowed)
        for n in sorted(allowed):
            p=files[n];value=mode(p);os.chmod(p,0o644 if value==0o600 else 0o600);reject('allowed_body_mode_'+n,lambda:native_predicate(rows,files,allowed));os.chmod(p,value)
        for value in [True,420.0,None,-1,0o10000]:
            mutant=[dict(z) for z in rows];mutant[0]['worktree_mode']=value;reject('malformed_full_mode_'+repr(value),lambda:native_predicate(mutant,files,allowed))
        reject('missing_thirteenth_mode',lambda:native_predicate(rows[:-1],files,allowed))
        changed=files['native4'];old=changed.read_bytes();changed.write_bytes(b'undeclared body');reject('nonallowed_body_change',lambda:native_predicate(rows,files,allowed));changed.write_bytes(old)
        native_predicate(rows,files,allowed)
        # Text is inspected, never imported/compiled/executed as production.
        source=(F/'pr48_guards.py').read_text();writer=source.split('def write(p,raw,exclusive=False):\n',1)[1].split('\n\ndef dump(',1)[0];fresh=source.split('def fresh_check(pre,allowed=()):\n',1)[1].split('\n\ndef native_git_snapshot',1)[0]
        need(writer.index('s.write(raw); s.flush()')<writer.index('os.fchmod(')<writer.index('os.fsync(s.fileno())')<writer.index('os.replace(tmp,p)')<writer.index("'Full existing permission mode changed during replacement'"),'Exact operative staged/full-mode ordering read as text')
        need('native_modes(all_native)' in fresh and 'native_modes(remaining)' not in fresh and 'check(R,remaining)' in fresh and 'len(all_native)==13' in fresh,'Exact operative all13 mode/allowed-body separation read as text')
        helpers=['integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']
        for n in helpers:need((F/n).read_bytes()==(OLD/n).read_bytes(),'Unrelated operative source unchanged')
        roots=['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json']
        for n in roots:need((F/n).read_bytes()==(OLD/n).read_bytes(),'False/null ROOT drafts unchanged')
        result={'schema':'pr48-private-mode-preservation-repair-controls/v2','status':'PASS_PRIVATE_HANDWRITTEN_MODELS_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'assertions':COUNT,'expected_negative_controls':NEG,'selected_actual_full_modes':[0o600,0o644,0o1600,0o2600,0o4600,0o7644],'actual_umask':0o022,'all_thirteen_private_mode_checks':True,'allowed_body_mode_mutations_rejected':4,'old0600_loss_countermodel_reproduced':True,'old_nominal0644_domain_not_disproved':True,'replacement_models':observations,'modes_are_actual_at_private_model_epoch_not_after_SOURCE_closure':True,'production_imported_compiled_executed':False,'independent_SOURCE_review_supplied':False,'actual_PR47_predecessor_completed':False,'new_substantive_attempts':0,'audit_turns':0,'paper_or_new_DOI_or_tracker':False}
        dump(F/'PRIVATE_MODE_REPAIR_RESULT.json',result);print(json.dumps(result,sort_keys=True))
    finally:os.umask(before_mask)
if __name__=='__main__':main()
