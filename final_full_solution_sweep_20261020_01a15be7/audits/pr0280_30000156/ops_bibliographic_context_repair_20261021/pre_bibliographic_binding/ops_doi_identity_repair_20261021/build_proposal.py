#!/usr/bin/env python3
"""Produce reviewable proposed copies only. Never opens canonical files for writing."""
from pathlib import Path
import difflib
import hashlib
import json
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
FROZEN=HERE/'pre_review03_binding'
OUT=HERE/'proposed_helpers'


def replace_once(text,old,new):
    if text.count(old)!=1:raise RuntimeError('Unexpected frozen source shape')
    return text.replace(old,new)


def main():
    OUT.mkdir(exist_ok=True)
    sources={n:(FROZEN/(n+'.py')).read_text() for n in ['ops_binding','prepublication_check','publication_live_gates','record_publication_ledger']}
    recognizer=(HERE/'doi_identity_proposal.py').read_text()
    sources['ops_binding'] += '\n\n# Shared conservative DOI identity recognizer.\n'+recognizer[recognizer.index('_ASCII_LOWER='):]
    sources['prepublication_check']=replace_once(sources['prepublication_check'],
        "and re.search(r'zenodo[./]'+str(expected_deposit_id)+r'(?!\\d)',' '.join(r)))]",
        "and target_in_row(r,expected_deposit_id))]")
    sources['publication_live_gates']=replace_once(sources['publication_live_gates'],
        """has_current_doi=(expected_deposit_id is not None and
            '10.5281/zenodo.'+str(expected_deposit_id) in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(row))))""",
        "has_current_doi=(expected_deposit_id is not None and target_in_row(row,expected_deposit_id))")
    s=sources['record_publication_ledger']
    s=replace_once(s,"or any(doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',v)) for v in r)]","or target_in_row(r,identifier)]")
    s=replace_once(s,"doi_rows=[r for r in before[1:] if doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(r)))]","doi_rows=[r for r in before[1:] if target_in_row(r,identifier)]")
    s=replace_once(s,"or doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(r)))]","or target_in_row(r,identifier)]")
    s=replace_once(s,"if sum(doi in set(re.findall(r'10\\.5281/zenodo\\.\\d+',' '.join(r))) for r in after)!=1:","if sum(target_in_row(r,identifier) for r in after)!=1:")
    sources['record_publication_ledger']=s
    p=sources['prepublication_check']
    p=replace_once(p,"    pr = read_command([", """    identity_ids=(record_identity_ids(next(r for r in full['records'] if int(r['id'])==expected_deposit_id),expected_deposit_id)
                  if expected_deposit_id is not None else [])
    ledger_matches=[{'row':i,'values':r} for i,r in enumerate(rows,1) if PATTERN.search(' '.join(r))
                    or (expected_deposit_id is not None and target_in_row(r,expected_deposit_id,identity_ids))]
    pr = read_command([""")
    p=replace_once(p,"'read_only':True,'expected_pr_head':expected_head,", "'read_only':True,'expected_identity_record_ids':identity_ids,'expected_pr_head':expected_head,")
    sources['prepublication_check']=p
    g=sources['publication_live_gates']
    g=replace_once(g,"    target_rows=[]", """    identity_ids=(record_identity_ids(records[expected_deposit_id],expected_deposit_id) if expected_deposit_id is not None else [])
    if gate.get('expected_identity_record_ids',identity_ids)!=identity_ids:
        raise RuntimeError('Target concept/version-parent identity evidence changed')
    target_rows=[]""")
    g=replace_once(g,"target_in_row(row,expected_deposit_id)","target_in_row(row,expected_deposit_id,identity_ids)")
    g=g.replace('Current target DOI/row','Current target DOI/identity lead').replace('Current target DOI appears','Current target DOI/identity lead appears')
    sources['publication_live_gates']=g
    d=sources['record_publication_ledger']
    d=d.replace('def matches(rows,identifier):','def matches(rows,identifier,family_ids=()):')
    d=d.replace('target_in_row(r,identifier)','target_in_row(r,identifier,family_ids)')
    d=d.replace("    operation=uuid.uuid4().hex", "    family_ids=gate.get('expected_identity_record_ids',[identifier])\n    operation=uuid.uuid4().hex")
    d=d.replace('matches(before,identifier)','matches(before,identifier,family_ids)').replace('matches(after,identifier)','matches(after,identifier,family_ids)')
    d=d.replace('Current target DOI/row','Current target DOI/identity lead').replace('Existing DOI appears','Existing DOI/identity lead appears').replace('DOI is duplicated','DOI/identity lead is duplicated')
    sources['record_publication_ledger']=d
    i=(FROZEN/'repository_integration.py').read_text()
    directory_code="""

def verify_directory_overlay(base,integrated,added_names,original=None):
    def inventory(commit):
        result={n:(v['mode'],v['type']) for n,v in subtree(commit,PROBLEM).items() if v['type']=='tree'}
        if any(v!=('040000','tree') for v in result.values()):
            raise RuntimeError('Unexpected selected directory mode/type')
        return result
    expected=inventory(base)
    if original is not None:expected.update(inventory(original))
    for name in added_names:
        parts=PurePosixPath(name).parts
        for end in range(1,len(parts)):expected['/'.join(parts[:end])]=('040000','tree')
    if inventory(integrated)!=expected:
        raise RuntimeError('Selected subtree directory inventory changed outside exact overlay')
"""
    i=replace_once(i,'\ndef verify_integrated_tree(',directory_code+'\ndef verify_integrated_tree(')
    i=replace_once(i,"    expected.update(added)\n", "    expected.update(added)\n    verify_directory_overlay(base,integrated,added,ORIGINAL)\n")
    i=replace_once(i,"        if leaves(new,PROBLEM)!=expected:","        verify_directory_overlay(ORIGINAL,new,selected)\n        if leaves(new,PROBLEM)!=expected:")
    sources['repository_integration']=i
    diff=[]
    for name,code in sources.items():
        (OUT/(name+'.py')).write_text(code)
        diff.extend(difflib.unified_diff((FROZEN/(name+'.py')).read_text().splitlines(keepends=True),code.splitlines(keepends=True),
                                        fromfile='frozen_review03/'+name+'.py',tofile='PROPOSED_ONLY/'+name+'.py'))
    (HERE/'PROPOSED.diff').write_text(''.join(diff))
    print(json.dumps({'proposal_files':list(sources),'canonical_edits':False}))


if __name__=='__main__':main()
