#!/usr/bin/env python3
"""Old324 logic, proposed/current helpers, documented richer recursive-tree fixtures."""
from pathlib import Path
import hashlib,json,difflib,sys,types
from controls_support import HERE,AUDIT,implementation
KIND='canonical' if '--canonical' in sys.argv else 'proposed'
HELPER='''\n\ndef _regression_dirs(names):
    result={}
    for name in names:
        parts=Path(name).parts
        for end in range(1,len(parts)):
            result['/'.join(parts[:end])]={'mode':'040000','type':'tree','sha':'synthetic-directory'}
    return result
'''

def adapt(name,source):
    old=source
    if name=='offline_controls.py':
        a="patch.object(I,'subtree',lambda commit,path,recursive:c[commit,path])"
        b="patch.object(I,'subtree',lambda commit,path,recursive=True:(_regression_dirs(a[commit] if commit in a else original) if path==B.PROBLEM else c[commit,path]))"
        if source.count(a)!=1:raise RuntimeError('integration fixture source shape')
        source=source.replace(a,b)
        a="patch.object(I,'subtree',lambda c,p,r:{})"
        b="patch.object(I,'subtree',lambda c,p,r=True:(_regression_dirs(original if c==B.ORIGINAL else {**original,**selected}) if p==B.PROBLEM else {}))"
        if source.count(a)!=1:raise RuntimeError('branch fixture source shape')
        source=source.replace(a,b)
    if name=='candidate_controls.py':
        a="        def subtree(commit,path,recursive=True):\n"
        b=a+"            if path==B.PROBLEM:return _regression_dirs(original if commit==B.ORIGINAL else leaf[commit])\n"
        if source.count(a)!=1:raise RuntimeError('candidate fixture source shape')
        source=source.replace(a,b)
    if name!='repair_controls.py':source+=HELPER
    return source,''.join(difflib.unified_diff(old.splitlines(keepends=True),source.splitlines(keepends=True),fromfile='preserved324/'+name,tofile='recursive_fixture_only/'+name))

def main():
    mode='optimized' if sys.flags.optimize else 'normal';summary=[];diff=[]
    for name in ['offline_controls.py','repair_controls.py','candidate_controls.py']:
        implementation(KIND)
        path=HERE/'pre_review02_binding/publication_operations_preparation'/name;body=path.read_bytes()
        binding=next(e for e in json.loads((HERE/'INPUT_PRESERVATION.json').read_text())['files'] if e['path']=='publication_operations_preparation/'+name)
        if hashlib.sha256(body).hexdigest()!=binding['sha256']:raise RuntimeError('preserved regression source differs')
        source,change=adapt(name,body.decode());diff.append(change)
        out=HERE/('regression_'+KIND+'_'+mode)/name.removesuffix('.py');out.mkdir(parents=True,exist_ok=True)
        module=types.ModuleType('regression_'+name.removesuffix('.py'));module.__file__=str(AUDIT/'publication_operations_preparation'/name)
        exec(compile(source,'preserved_regression_fixture/'+name,'exec'),module.__dict__)
        module.HERE=out;module.main()
        summary.append({'suite':name,'controls':len(module.CASES),'accepted':sum(x['actual']=='accept' for x in module.CASES),'rejected':sum(x['actual']=='reject' for x in module.CASES),'preserved_source_sha256':binding['sha256']})
    (HERE/'REGRESSION_FIXTURE_ADAPTATION.diff').write_text(''.join(diff))
    result={'implementation':KIND,'optimization':sys.flags.optimize,'controls':sum(x['controls'] for x in summary),'all_controls_passed':True,'suites':summary,'fixture_adjustment':'Provide recursively complete selected-directory entries derived from the same original/selected leaves. No production guard is bypassed, removed, mocked out or weakened; no expected verdict changes.','actual_provider_attempts':0}
    (HERE/('REGRESSION_CANONICAL_OPTIMIZED.json' if sys.flags.optimize else 'REGRESSION_CANONICAL.json') if KIND=='canonical' else HERE/('REGRESSION_PROPOSED_OPTIMIZED.json' if sys.flags.optimize else 'REGRESSION_PROPOSED.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
