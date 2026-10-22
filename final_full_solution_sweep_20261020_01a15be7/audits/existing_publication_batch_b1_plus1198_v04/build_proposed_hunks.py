"""Generate and syntax-check policy-only hunks; never install production sources."""
from pathlib import Path
import difflib
A=Path(__file__).resolve().parent
def once(text,old,new):
    if text.count(old)!=1:raise RuntimeError('Unique source context required: '+old[:80])
    return text.replace(old,new)

def main():
    old_core=(A/'frozen_proposal/VERSION03_CORE.py.txt').read_text()
    old_runner=(A/'frozen_proposal/VERSION03_RUNNER.py.txt').read_text()
    core=once(old_core,'def identity_hits(rows,item):',
              (A/'PROPOSED_PR_PARSER.py.txt').read_text()+'\n\ndef identity_hits(rows,item):')
    core=once(core,"matched=[];arxiv_ids=arxiv_identifiers_in_text(text)",
              "matched=[];arxiv_ids=arxiv_identifiers_in_text(text);pr_ids=associated_pr_numbers_in_text(text)")
    core=once(core,"            if arxiv is not None:ok=arxiv in arxiv_ids",
              "            pr_number=associated_pr_alias_number(value)\n            if kind=='pr_reference':require(pr_number is not None,'Malformed associated PR URL alias')\n            if pr_number is not None:ok=pr_number in pr_ids\n            elif arxiv is not None:ok=arxiv in arxiv_ids")
    runner=once(old_runner,'canonical_arxiv_identifier,expected_same_paper_arxiv_ids,typed_equal,compare_1198_record)',
                'canonical_arxiv_identifier,expected_same_paper_arxiv_ids,typed_equal,compare_1198_record,associated_pr_alias_number)')
    runner=once(runner,"    require(sum(len(x['associated_prs']) for x in items)==17,'Lost associatedPR')",
                "    associated=[n for x in items for n in x['associated_prs']]\n    require(len(associated)==len(set(associated))==17 and all(type(n) is int and n>0 for n in associated),'Lost, duplicated or mistyped associated PR inventory')")
    runner=once(runner,"        accepted_item=next(x for x in accepted_identity['items'] if x['pr']==item['pr'])",
                "        accepted_item=next(x for x in accepted_identity['items'] if x['pr']==item['pr'])\n        expected_associations=accepted_item.get('associated_prs',[accepted_item['pr']])\n        require(typed_equal(item['associated_prs'],expected_associations),'Frozen known associated PR inventory drift')\n        alias_numbers=[associated_pr_alias_number(a['value']) for a in item['identity_leads'] if a['kind']=='pr_reference']\n        require(all(n is not None for n in alias_numbers) and sorted(alias_numbers)==sorted(expected_associations),'Missing, duplicate or extraneous known associated PR alias')")
    compile(core,'PROPOSED_V04_CORE_NOT_INSTALLED','exec')
    compile(runner,'PROPOSED_V04_RUNNER_NOT_INSTALLED','exec')
    diff=''.join(difflib.unified_diff(old_core.splitlines(True),core.splitlines(True),
        fromfile='version03/ops_core.py',tofile='proposed_version04/ops_core.py'))
    diff+=''.join(difflib.unified_diff(old_runner.splitlines(True),runner.splitlines(True),
        fromfile='version03/append_reviewed_rows.py',tofile='proposed_version04/append_reviewed_rows.py'))
    (A/'PROPOSED_SOURCE_HUNKS.diff').write_text(diff)
    print('Syntax-checked proposal only; production hashes deliberately remain version03 pending adoption.')

if __name__=='__main__':main()
