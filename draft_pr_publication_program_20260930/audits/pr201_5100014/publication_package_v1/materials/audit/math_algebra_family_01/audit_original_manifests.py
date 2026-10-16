"""Hash/size, assertion-bytecode and exact count audit, explicit enforcement."""
import ast,hashlib,json,dis,types
from pathlib import Path
HERE=Path(__file__).resolve().parent; ORIGINAL=HERE.parent/'original_submitted_head'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,m):
    if not c:raise RuntimeError(m)
def assertops(c):
    return sum(i.opname=='LOAD_ASSERTION_ERROR' for i in dis.get_instructions(c))+sum(assertops(x) for x in c.co_consts if isinstance(x,types.CodeType))
def main():
    files=sorted(p for p in ORIGINAL.rglob('*') if p.is_file())
    need(len(files)==24,'original file count differs')
    need(sum(p.stat().st_size for p in files)==54661,'original bytes differ')
    frozen=json.loads((ORIGINAL/'FROZEN_MANIFEST.json').read_text()); entries=[]
    for name,r in frozen['files'].items():
        p=ORIGINAL/name;need(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'author manifest mismatch '+name)
        entries.append({'name':name,'sha256':sha(p),'bytes':p.stat().st_size})
    reviewer=json.loads((ORIGINAL/'independent_review/MANIFEST.json').read_text());rentries=[]
    need(sha(ORIGINAL/'CANDIDATE.md')==reviewer['author_candidate_sha256'],'review candidate identity mismatch')
    need(sha(ORIGINAL/'FROZEN_MANIFEST.json')==reviewer['author_manifest_sha256'],'review author manifest mismatch')
    for name,h in reviewer['files'].items():
        p=ORIGINAL/'independent_review'/name;need(sha(p)==h,'review manifest mismatch '+name);rentries.append(name)
    stats=[]
    for name in ('turn1_exact.py','turn1_generic_six.py','independent_review/independent_check.py'):
        code=(ORIGINAL/name).read_text();normal=compile(code,name,'exec',optimize=0);optimized=compile(code,name,'exec',optimize=1)
        stats.append({'file':name,'assert_statement_sites':sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(code))),'normal_assert_opcodes':assertops(normal),'optimized_assert_opcodes':assertops(optimized)})
    receipt=json.loads((ORIGINAL/'independent_review/independent_receipt.json').read_text())
    need(sum(receipt['exact_groups'].values())==receipt['exact_assertions']==1757,'claimed exact counter sum mismatch')
    need(sum(receipt['numerical_groups'].values())==receipt['numerical_diagnostics']==26568,'claimed numerical counter sum mismatch')
    out={'status':'PASS','original_files':len(files),'original_bytes':sum(p.stat().st_size for p in files),'author_manifest_entries':len(entries),'review_manifest_entries':len(rentries),'all_hashes_sizes_match':True,'author_manifest_sha256':sha(ORIGINAL/'FROZEN_MANIFEST.json'),'candidate_sha256':sha(ORIGINAL/'CANDIDATE.md'),'assertion_enforcement_audit':stats,'important':'Reviewer counter names retain 1757 and26568 under -O, but their assert conditions are stripped. Optimized PASS is not evidence of enforced checks. Exact author script has zero assertions; it is a calculator. Generic author script asserts closure only.','frozen_entries':entries,'review_entries':rentries}
    (HERE/'original_manifest_assertion_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
