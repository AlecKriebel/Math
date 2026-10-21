#!/usr/bin/env python3
"""Build proposed seven-helper copies from frozen156 bytes. No canonical writes."""
from pathlib import Path
import difflib,json
H=Path(__file__).resolve().parent;O=H/'pre_record_url_binding';P=H/'proposed_helpers'
NAMES=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py','publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']

def main():
    P.mkdir(exist_ok=True);diff=[]
    for name in NAMES:
        old=(O/name).read_text();new=old
        if name=='ops_binding.py':
            line="_RECORD=re.compile(r'https?://(?:www\\.)?zenodo\\.org/(?:api/)?records?/([0-9]+)')\n"
            if new.count(line)!=1:raise RuntimeError('Frozen record-regex source shape')
            new=new.replace(line,'')
            start=new.index('def _review_names(');end=new.index('\n\ndef _decode',start)
            body='''def _review_names(text):
    lowered=ascii_lower(text)
    result={'10.5281/zenodo.'+m.group(1) for m in _FRAGMENT.finditer(lowered)
            if _bounded_token(lowered,m.start(),m.end()) and (not m.start() or lowered[m.start()-1]!='/')}
    return result|_official_record_url_leads(text)
'''
            new=new[:start]+(H/'record_url_identity.py').read_text()+'\n\n'+body+new[end:]
            short="re.search(r'(?<![a-z0-9.])10/[a-z0-9]+(?:$|[\\s?#.,;)])',ascii_lower(current))"
            if new.count(short)!=1:raise RuntimeError('Frozen shortDOI source shape')
            new=new.replace(short,'_unresolved_short_name(current)')
        if name=='record_publication_ledger.py':
            start=new.index('def matches(');end=new.index('\n\ndef append_verified',start)
            body="""def matches(rows,identifier,family_ids=()):
    found=[]
    for i,row in enumerate(rows[1:],2):
        is_target=target_in_row(row,identifier,family_ids)
        if PATTERN.search(' '.join(row)) or is_target:found.append((i,row))
    return found
"""
            new=new[:start]+body+new[end:]
        (P/name).write_text(new)
        diff.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='preserved156/'+name,tofile='PROPOSED_record_url/'+name))
    (H/'PROPOSAL.diff').write_text(''.join(diff));print(json.dumps({'proposed_helpers':7,'canonical_writes':False}))
if __name__=='__main__':main()
