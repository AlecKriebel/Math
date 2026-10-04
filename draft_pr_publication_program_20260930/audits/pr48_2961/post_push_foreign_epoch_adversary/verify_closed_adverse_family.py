"""UNEXECUTED SOURCE: separate read-only verification of the closed adverse audit."""
from pathlib import Path
import argparse,os,sys
sys.dont_write_bytecode=True
import audit_common as c
def main():
    p=argparse.ArgumentParser();p.add_argument('--self-manifest-sha256',required=True);a=p.parse_args();c.topology(True);b=c.raw(c.F/c.SELF);c.need(c.sha(b)==a.self_manifest_sha256,'ROOT exact actual self pin');m=c.parse(b)
    c.need(set(m)=={'schema','status','utc','self_excluded','files_count','files','source_only','recovery_production_executed','ROOT_acceptance_approved'} and m['schema']=='pr48-independent-post-push-adverse-SOURCE-family-closure/v1' and m['status']=='CLOSED_REJECTED_SOURCE_AUDIT_ONLY' and m['self_excluded']==[c.SELF] and type(m['files_count']) is int and m['files_count']==len(m['files'])==len(c.NAMES) and m['source_only'] is True and m['recovery_production_executed'] is False and m['ROOT_acceptance_approved'] is False,'Exact typed adverse-only closure')
    c.need({z['path'] for z in m['files']}==c.NAMES and len({z['path'] for z in m['files']})==len(c.NAMES),'Exact self-only payload')
    for z in m['files']:c.need(c.row(c.F/c.safe(z['path']))==z and (c.F/z['path']).stat().st_mode&0o7777==0o444,'Entire closed payload/full0444')
    c.need((c.F/c.SELF).stat().st_mode&0o7777==0o444,'Closed self full0444');c.own_evidence()
    # Input observations are dated. A later preserved repair version cannot be
    # rejected solely because its live sources differ from this adverse version.
    print(c.encode(dict(status='PASS_READONLY_CLOSED_REJECTED_SOURCE_AUDIT_ONLY',actual_child_pid=os.getpid(),payload_count=len(c.NAMES),future_source_approval=False)).decode(),end='')
if __name__=='__main__':main()
