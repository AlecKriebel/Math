#!/usr/bin/env python3
"""Build exact reviewable copies from preserved PR399 sources; no canonical writes."""
from pathlib import Path
import difflib,json
HERE=Path(__file__).resolve().parent
FROZEN=HERE/'pre_review02_binding'
OUT=HERE/'proposed_helpers'

def replace(text,old,new):
    if text.count(old)!=1:raise RuntimeError('Unexpected preserved source shape: '+old[:120])
    return text.replace(old,new)

def main():
    OUT.mkdir(exist_ok=True)
    names=['ops_binding','prepublication_check','publication_live_gates','repository_integration','publication_lifecycle','record_publication_ledger','verify_published_files']
    sources={name:(FROZEN/(name+'.py')).read_text() for name in names}
    recognizer=(HERE/'doi_identity.py').read_text()
    sources['ops_binding']+='\n\n# Shared ASCII DOI identities and conservative review leads; no URI-equivalence claim.\n'+recognizer[recognizer.index('_ASCII_LOWER='):]
    s=sources['prepublication_check']
    start=s.index('    ledger_matches =');end=s.index('    client =',start)
    s=s[:start]+"    # Evaluate every cell even before an ID exists: unresolved short aliases block.\n    for row in rows:row_identity_names(row)\n"+s[end:]
    old="    pr = read_command(["
    new="""    identity_ids=(record_identity_ids(next(r for r in full['records'] if r['id']==expected_deposit_id),expected_deposit_id)
                  if expected_deposit_id is not None else [])
    for record in full['records']:
        if record['id'] in identity_ids:targets[record['id']]=record
    ledger_matches=[{'row':i,'values':r} for i,r in enumerate(rows,1)
                    if PATTERN.search(' '.join(r)) or (expected_deposit_id is not None
                    and target_in_row(r,expected_deposit_id,identity_ids))]
    pr = read_command(["""
    s=replace(s,old,new)
    s=replace(s,"'read_only':True,'expected_pr_head':expected_head,", "'read_only':True,'expected_identity_record_ids':identity_ids,'expected_pr_head':expected_head,")
    sources['prepublication_check']=s
    s=sources['publication_live_gates']
    s=replace(s,'    target_rows=[]',"""    identity_ids=(record_identity_ids(records[expected_deposit_id],expected_deposit_id) if expected_deposit_id is not None else [])
    if gate.get('expected_identity_record_ids',identity_ids)!=identity_ids:
        raise RuntimeError('Target concept/version-parent identity evidence changed')
    target_rows=[]""")
    s=replace(s,"""has_current_doi=(expected_deposit_id is not None and
            '10.5281/zenodo.'+str(expected_deposit_id) in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(row))))""", """row_identity_names(row)
        has_current_doi=(expected_deposit_id is not None and target_in_row(row,expected_deposit_id,identity_ids))""")
    sources['publication_live_gates']=s
    s=sources['record_publication_ledger']
    s=replace(s,'def matches(rows,identifier):','def matches(rows,identifier,family_ids=()):')
    s=replace(s,"or any(doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',v)) for v in r)]","or target_in_row(r,identifier,family_ids)]")
    s=replace(s,'    operation=uuid.uuid4().hex',"    family_ids=gate.get('expected_identity_record_ids',[identifier])\n    operation=uuid.uuid4().hex")
    s=replace(s,"doi_rows=[r for r in before[1:] if doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(r)))]", "# Independently inspect every returned cell before exemptions or mutation.\n    for value in before:row_identity_names(value)\n    doi_rows=[r for r in before[1:] if target_in_row(r,identifier,family_ids)]")
    s=replace(s,"or doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(r)))]","or target_in_row(r,identifier,family_ids)]")
    s=replace(s,"if sum(doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(r))) for r in after)!=1:","if sum(target_in_row(r,identifier,family_ids) for r in after)!=1:")
    s=s.replace('matches(before,identifier)','matches(before,identifier,family_ids)').replace('matches(after,identifier)','matches(after,identifier,family_ids)')
    # No pattern short circuit may hide a later unresolved alias at readback.
    s=replace(s,"    after=read('ledger_after_append',operation)","    after=read('ledger_after_append',operation)\n    for value in after:row_identity_names(value)")
    sources['record_publication_ledger']=s
    s=sources['repository_integration']
    directory='''\n\ndef verify_directory_overlay(base,integrated,added_names,original=None):
    def inventory(commit):
        entries=subtree(commit,PROBLEM)
        result={name:(entry['mode'],entry['type']) for name,entry in entries.items() if entry['type']=='tree'}
        for name,identity in result.items():
            safe_file(Path('/synthetic'),name)
            if identity!=('040000','tree'):
                raise RuntimeError('Unexpected selected directory mode/type')
        return result
    expected=inventory(base)
    if original is not None:expected.update(inventory(original))
    for name in added_names:
        safe_file(Path('/synthetic'),name)
        parts=PurePosixPath(name).parts
        for end in range(1,len(parts)):expected['/'.join(parts[:end])]=('040000','tree')
    if inventory(integrated)!=expected:
        raise RuntimeError('Selected subtree directory inventory changed outside exact overlay')
'''
    s=replace(s,'\ndef verify_integrated_tree(',directory+'\ndef verify_integrated_tree(')
    s=replace(s,'    expected.update(added)\n','    expected.update(added)\n    verify_directory_overlay(base,integrated,added,ORIGINAL)\n')
    s=replace(s,'        if leaves(new,PROBLEM)!=expected:', '        verify_directory_overlay(ORIGINAL,new,selected)\n        if leaves(new,PROBLEM)!=expected:')
    sources['repository_integration']=s
    diff=[]
    for name,body in sources.items():
        (OUT/(name+'.py')).write_text(body)
        diff.extend(difflib.unified_diff((FROZEN/(name+'.py')).read_text().splitlines(keepends=True),body.splitlines(keepends=True),fromfile='preserved_review02/'+name+'.py',tofile='repaired_proposal/'+name+'.py'))
    (HERE/'PROPOSED.diff').write_text(''.join(diff))
    print(json.dumps({'proposed_helpers':len(sources),'canonical_files_written':False}))
if __name__=='__main__':main()
