#!/usr/bin/env python3
"""Exact review04 program, frozen356 helper source and owned output custody."""
import hashlib,json,sys,types
from pathlib import Path
H=Path(__file__).resolve().parent;A=H.parent;O=H/'pre_destination_binding'
def main():
 source=O/'reviews/package_adversary_04/operations_checks.py';body=source.read_text()
 body=body.replace("P=A.parents[1]/'private/pr0399_package04'","P=A.parents[1]/'private/pr0399_doi_destination_repair'")
 for n in ['name','n']:body=body.replace("(A/("+n+"+'.py')).read_bytes()","(Path("+repr(str(O))+")/("+n+"+'.py')).read_bytes()")
 mode='optimized' if sys.flags.optimize else 'normal';out=A.parents[1]/'private/pr0399_doi_destination_repair'/('old_finding_'+mode);out.parent.mkdir(parents=True,exist_ok=True);prior=sys.argv;sys.argv=[str(source),'--output',str(out)]
 try:
  module=types.ModuleType('review04_frozen');module.__file__=str(A/'reviews/package_adversary_04/operations_checks.py');exec(compile(body,str(source),'exec'),module.__dict__)
 finally:sys.argv=prior
 result={'mode':mode,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'other_controls':len(module.results),'doi_observations':len(module.doi_findings),'provider_attempts':len(module.attempts),'source_changes':['owned private/public output custody','exact preserved356 helper reads and hash receipt lookup'],'expected_old_acceptances_changed':False}
 capture=H/('old_finding_'+mode);capture.mkdir(exist_ok=False)
 for file in out.glob('*.json'):(capture/file.name).write_bytes(file.read_bytes())
 (capture/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
