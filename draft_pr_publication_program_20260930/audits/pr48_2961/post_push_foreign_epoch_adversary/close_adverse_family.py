"""UNEXECUTED SOURCE: ROOT closes this adverse family, never recovery production."""
from pathlib import Path
import argparse,datetime as dt,os,sys
sys.dont_write_bytecode=True
import audit_common as c
def main():
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--personally-read-complete-source',action='store_true');p.add_argument('--ready-sha256',required=True);a=p.parse_args()
    c.need(a.execute and a.personally_read_complete_source and __debug__ and sys.flags.optimize==0,'ROOT explicit personally read invocation')
    os.umask(0o022);c.topology(False);c.ready(a.ready_sha256);obs=c.own_evidence();c.check_observed_inputs_before_closure(obs)
    rows=[c.row(c.F/n) for n in sorted(c.NAMES)]
    for n in sorted(c.NAMES):os.chmod(c.F/n,0o444)
    value=dict(schema='pr48-independent-post-push-adverse-SOURCE-family-closure/v1',status='CLOSED_REJECTED_SOURCE_AUDIT_ONLY',utc=dt.datetime.now(dt.timezone.utc).isoformat(),self_excluded=[c.SELF],files_count=len(rows),files=rows,source_only=True,recovery_production_executed=False,ROOT_acceptance_approved=False)
    target=c.F/c.SELF
    with target.open('xb') as f:f.write(c.encode(value));f.flush();os.fsync(f.fileno())
    os.chmod(target,0o444);c.topology(True)
    for z in rows:c.need(c.row(c.F/z['path'])==z and (c.F/z['path']).stat().st_mode&0o7777==0o444,'Whole closed payload/full0444')
    c.need(target.stat().st_mode&0o7777==0o444,'Closed self full0444');print(c.encode(dict(status=value['status'],self_manifest_sha256=c.sha(c.raw(target)),payload_count=len(rows),actual_child_pid=os.getpid())).decode(),end='')
if __name__=='__main__':main()
