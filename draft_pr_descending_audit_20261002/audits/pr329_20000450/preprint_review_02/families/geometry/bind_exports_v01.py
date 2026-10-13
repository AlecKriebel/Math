from pathlib import Path
import hashlib,json,difflib,ast,datetime
root=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450')
own=Path(__file__).resolve().parent
archive=root/'preprint_review_02/phase3/archive_replay'
port=json.loads((archive/'PORTABILITY.json').read_text())
out={}
print('UTC_START',datetime.datetime.now(datetime.timezone.utc).isoformat())
for name in ['geometry_source','geometry_quotient','geometry','geometry_primitivity']:
    record=port['programs'][name]
    original=root/record['original_path']
    public=archive/'programs'/(name+'.py')
    o=original.read_bytes();e=public.read_bytes()
    oh=hashlib.sha256(o).hexdigest();eh=hashlib.sha256(e).hexdigest()
    assert len(o)==record['original_bytes']
    assert oh==record['original_sha256']
    assert eh==record['exported_sha256']
    diff=''.join(difflib.unified_diff(o.decode().splitlines(keepends=True),e.decode().splitlines(keepends=True),fromfile=str(original),tofile=str(public)))
    tree=ast.parse(e)
    asserts=sum(isinstance(n,ast.Assert) for n in ast.walk(tree))
    checks=[n.args[0].value for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['check','equal'] and n.args and isinstance(n.args[0],ast.Constant)]
    out[name]={'original_path':str(original),'original_bytes':len(o),'original_sha256':oh,'exported_path':str(public),'exported_bytes':len(e),'exported_sha256':eh,'declared_changes':record['changes'],'full_diff':diff,'static_assert_statements':asserts,'static_named_exact_checks':checks}
    print(name,'ORIGINAL',oh,'EXPORTED',eh,'STATIC_ASSERTS',asserts,'NAMED_CHECK_CALLS',len(checks))
    print(diff)
(own/'export_binding.json').write_text(json.dumps(out,indent=2)+'\n')
print('UTC_END',datetime.datetime.now(datetime.timezone.utc).isoformat())
