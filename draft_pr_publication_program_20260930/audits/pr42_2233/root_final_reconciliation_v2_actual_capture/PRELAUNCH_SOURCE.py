#!/usr/bin/env python3
"""Future root administrative reconciliation only; no scientific helper execution."""
import argparse
import ctypes
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import pr42_guards as g


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root-bindings',required=True); p.add_argument('--root-bindings-sha256',required=True); p.add_argument('--execute',action='store_true'); p.add_argument('--plan',required=True); p.add_argument('--plan-sha256',required=True); p.add_argument('--preparation-manifest-sha256',required=True); p.add_argument('--output',required=True)
    a=p.parse_args(); g.require(a.execute,'Root explicit execution required')
    g.require(g.git('branch','--show-current')=='main','Stay on main for actual root reconciliation')
    g.manifest(g.HERE,'PREPARATION_MANIFEST.json',a.preparation_manifest_sha256,frozen=True)
    plan=g.regular(g.R,a.plan); g.require(plan.resolve().is_relative_to(g.A.resolve()) and not plan.resolve().is_relative_to(g.C.resolve()) and not plan.resolve().is_relative_to(g.HERE.resolve()),'Root plan outside closed packages required')
    g.require(g.sha(plan.read_bytes())==g.digest(a.plan_sha256),'Genuine root plan pin differs')
    scope=g.load(plan); refs=g.plan_scope(scope,a.preparation_manifest_sha256,a.root_bindings,a.root_bindings_sha256)
    output=g.A/g.relative(a.output); g.require(output.parent==g.A and not output.exists() and not output.is_symlink(),'New adjacent absent-only final directory required')
    target=output; stage=g.A/(".pr42-final-stage-"+str(os.getpid())+"-"+g.stamp().replace(":",""));stage.mkdir(exist_ok=False);output=stage
    g.dump(output/'ROOT_REVIEWED_SCOPE.json',scope,exclusive=True)
    _,after=g.basis(a.root_bindings,a.root_bindings_sha256); g.require(g.equal(after,refs),'Entire immutable evidence changed during reconciliation')
    receipt={'schema':'pr42-actual-final-reconciliation/v1','utc':g.stamp(),'status':'PASS','actual_root_reconciliation':True,'pr':42,'problem_id':2233,'preparation_manifest_sha256':a.preparation_manifest_sha256,'entire_scope':scope,'bindings_before':refs,'bindings_after':after,'root_reviewed_plan':g.pin(plan),'reconciliation_source':g.pin(g.HERE/'seal_final_evidence.py'),'science_helpers_executed':False,'new_substantive_attempts':0,'audit_turns':0,'shared_mutations':False}
    g.dump(output/'ROOT_FINAL_RECONCILIATION.json',receipt,exclusive=True)
    rr=[{'path':n,'bytes':len((output/n).read_bytes()),'sha256':g.sha((output/n).read_bytes())} for n in ['ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json']]
    g.dump(output/'FINAL_MANIFEST.json',{'schema':'pr42-final-root-two-member-closure/v1','utc':g.stamp(),'self_excluded':['FINAL_MANIFEST.json'],'files_count':2,'files':rr},exclusive=True)
    g.manifest(output,'FINAL_MANIFEST.json',count=2)
    for f in output.iterdir(): f.chmod(0o444)
    g.manifest(output,'FINAL_MANIFEST.json',count=2,frozen=True)
    g.require(sys.platform=='darwin','Reviewed macOS absent-only directory publication required');libc=ctypes.CDLL(None,use_errno=True);rename=libc.renamex_np;rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
    if rename(os.fsencode(stage),os.fsencode(target),4)!=0:
        error=ctypes.get_errno();raise OSError(error,os.strerror(error),str(target))
    output=target
    print(g.encode({'status':'PASS','final_receipt_sha256':g.sha((output/'ROOT_FINAL_RECONCILIATION.json').read_bytes()),'final_manifest_sha256':g.sha((output/'FINAL_MANIFEST.json').read_bytes()),'science_helpers_executed':False,'shared_mutations':False}).decode(),end='')


if __name__=='__main__': main()
