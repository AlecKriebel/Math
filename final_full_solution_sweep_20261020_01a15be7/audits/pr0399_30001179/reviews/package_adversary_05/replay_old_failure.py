#!/usr/bin/env python3
"""Preserve review04's four wrong-destination observations as OLD failures."""
import difflib,hashlib,json,sys,types
from pathlib import Path
O=Path(__file__).resolve().parent;A=O.parents[1];H=A/'ops_doi_destination_repair_20261021';D=H/'pre_destination_binding';P=A.parents[1]/'private/pr0399_package05'
def main():
    source=D/'reviews/package_adversary_04/operations_checks.py';raw=source.read_bytes();original=raw.decode()
    if hashlib.sha256(raw).hexdigest()!='08991cecd52cf1907d3b4bcd680e4f66de8cf207d6c70ba2d9c3aeee4201b936':raise RuntimeError('old program changed')
    body=original.replace("P=A.parents[1]/'private/pr0399_package04'","P=A.parents[1]/'private/pr0399_package05'")
    for variable in ['name','n']:body=body.replace("(A/("+variable+"+'.py')).read_bytes()","(Path("+repr(str(D))+")/("+variable+"+'.py')).read_bytes()")
    mode='optimized' if sys.flags.optimize else 'normal';output=P/('old_failure_'+mode);sys.argv=[str(source),'--output',str(output)]
    module=types.ModuleType('old04_exact');module.__file__=str(A/'reviews/package_adversary_04/operations_checks.py');exec(compile(body,str(source),'exec'),module.__dict__)
    if len(module.doi_findings)!=4 or len(module.results)!=55 or module.attempts:raise RuntimeError('historical observations differ')
    result={'optimization':sys.flags.optimize,'source_sha256':hashlib.sha256(raw).hexdigest(),'compiled_adapted_sha256':hashlib.sha256(body.encode()).hexdigest(),'old_other_controls':55,'old_wrong_destination_observations':module.doi_findings,'actual_provider_attempts':0,'classification':'Four observations under preserved356: they evidence OLD defects, never current successes.','only_adapter_changes':'Owned output custody plus old seven-helper read/hash lookup paths; expectations untouched.'}
    (O/('OLD_FAILURE_'+mode+'.json')).write_text(json.dumps(result,indent=2)+'\n');(O/'OLD_REPLAY_ADAPTATION.diff').write_text(''.join(difflib.unified_diff(original.splitlines(keepends=True),body.splitlines(keepends=True),fromfile='original_review04',tofile='owned_review05_old_replay')))
if __name__=='__main__':main()
