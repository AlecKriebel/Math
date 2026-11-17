from pathlib import Path
import datetime, hashlib, json, stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P / 'verification'
D = V / 'd4-root-custody-sol-20261117'
def sha(b): return hashlib.sha256(b).hexdigest()
def write(p, x):
    assert not p.exists(), str(p)
    p.write_text(json.dumps(x, indent=2) + '\n')
def identity(p):
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode), str(p)
    b = p.read_bytes()
    return {'bytes': len(b), 'SHA256': sha(b), 'mode': f'{stat.S_IMODE(s.st_mode):04o}'}

assert sha((D/'FINAL.json').read_bytes()) == '101d6e8cfb772037645c9c97e1c14128a52c43c5dbcfef4e4673d381d0eafa85'
assert sha((D/'MANIFEST.json').read_bytes()) == '5d621b7f74896018761443bc073bcd7050dd4b176dcbf2f05c5afe4a181fa4db'
m = json.loads((D/'MANIFEST.json').read_text())
expected = {x['path'] for x in m['payload_files']} | {'FINAL.json', 'MANIFEST.json'}
assert {x.name for x in D.iterdir()} == expected and len(expected) == 9
assert f'{stat.S_IMODE(D.stat().st_mode):04o}' == m['root_mode']
observed = {name: identity(D/name) for name in sorted(expected)}
for x in m['payload_files']:
    assert observed[x['path']] == {k: x[k] for k in ['bytes','SHA256','mode']}, x['path']
assert all(x['mode'] == '0644' for x in observed.values())
review = P/'papers/23439776/reviews/root-continuation-20261117/ROOT_REVIEW.md'
ri = identity(review)
assert ri['bytes'] == 11832 and ri['SHA256'] == '4836979d83da2747da766a2defc76bc0e5bbd6b48b25025c0de434aefd580e62'
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt = {'UTC': now, 'status': 'ACCEPTED_FINITE_CUSTODY_AND_ROOT_SCIENTIFIC_DISPOSITION',
           'owned_files_authenticated': observed, 'protected_input_files': 237,
           'protected_input_child_directories': 14, 'actual_REPORT_FINAL_and_root_review_read': True,
           'scientific_execution_by_this_reader': False, 'root_review': ri,
           'custody_completion_percent': 100, 'goal_complete': False}
rp = V/'root-d4-final-adoption-20261117.json'
write(rp, receipt)
clearance = {'UTC': now, 'record_id': '23439776', 'sheet_row': 171,
 'status': 'PASS_ORIGINAL_HISTORICAL_CANONICAL_W_COUNTEREXAMPLE',
 'scientific_review_completion_percent': 100, 'full_original_manuscript_read': True,
 'root_independent_original_and_primary_checkpoints': True,
 'independent_families': ['adversarial-sol','scope-sol'],
 'fresh_independent_convention_challenge': 'convention-challenge-sol-20261117/CHALLENGE.md',
 'central_defect_or_unsupported_inference': None, 'native_API_version': '1.0',
 'declared_publication_date': '2026-10-17', 'review': str(review.relative_to(P)),
 'review_SHA256': ri['SHA256'], 'finite_custody_receipt': str(rp.relative_to(P)),
 'finite_custody_SHA256': sha(rp.read_bytes()),
 'scope': 'D4 stated canonical-X potential: 22 facets, two exponent -2 terms; historical necessary converse only',
 'exclusions': ['later string-coordinate converse','coefficient criterion','KS sufficient-theorem conclusion','exclusive priority'],
 'credit': 'Schumann historical OWR claim; KS/GKS construction; earlier Mironov Case267 full string support',
 'root_scientific_executions': 0, 'family_native_attempts': 2, 'family_native_exits': [0,0],
 'no_formal_or_human_certificate': True, 'follow_up': None,
 'prepare_factual_private_page_authorized': True, 'publication_or_AA_or_redirect_certificate': False,
 'native_sheet_transition_pending': True, 'scientific_dispositions': 144,
 'scientific_passes': 136, 'deferred': 8, 'scientific_remaining': 59,
 'programme_percent': 100*144/203, 'goal_complete': False}
cp = V/'root-clearance-23439776-20261117.json'
write(cp, clearance)
progress = P/'PROGRESS.json'
p = json.loads(progress.read_text())
assert p['current_scientific_inventory']['dispositions'] == 143
assert p['native_sheet_reviewed_or_deferred_count'] == 143
p['updated_utc'] = now
p['actual_scientific_disposed_count'] = p['root_scientific_dispositions'] = 144
p['actual_scientific_disposed_percent'] = p['root_scientific_percent'] = 100*144/203
p['scientific_reviews_remaining'] = 59
p['current_scientific_inventory'].update(dispositions=144, passed=136, remaining=59, percent=100*144/203)
p['actual_scientific_dispositions_pending_native_update'] = ['23439776']
p['native_review_transition_pending_rows'] = [171]
p['local_scientific_dispositions_pending_tracker'] = ['23439776']
p['root_clearance_23439776'] = str(cp.relative_to(P))
p['note'] = '144/203 scientific dispositions:136 passes,8 deferred,59 remain. Native Sheet143 pending D4 row171 after evidence checkpoint:123 verified,10 deployed pending actual UI,2 preparing,8 in review,50 queued,2 holds,8 deferred;36 exclusions/6 aliases. Three new pages live at4cc09/245a,15 hashes and closing local guards passed; independent post-audit pending. All10 pending AA remain blank. Goal active/incomplete.'
progress.write_text(json.dumps(p, indent=2) + '\n')
with (P/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n\n## {now} — D4 original counterexample review completed\n\nRoot disposition PASS for record23439776 historical canonical-W claim with exact coordinate and priority exclusions. Two independent native routes exit0, root science executions0; original sources, actual primary interfaces and a fresh independent convention challenge were read. Finite custody237files/14dirs authenticated by independent reader; root9-file packet adopted. No follow-up. Scientific144/203 (136pass8defer59remain), {100*144/203:.6f}%; native143 pending checkpoint/row171. Programme active/incomplete.\n')
print(json.dumps({'clearance': identity(cp), 'custody_adoption': identity(rp), 'scientific_reviewed': 144, 'native_reviewed': 143}))
