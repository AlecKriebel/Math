"""Date the second bounded priority checkpoint without accepting priority."""
from pathlib import Path
import datetime, hashlib, json
A = Path(__file__).resolve().parent
P = A.parent.parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'mode': p.stat().st_mode & 0o7777}
out = A / 'ROOT_PRIORITY_PROGRESS_002.json'
assert not out.exists()
assert not json.loads((P / 'SHARED_GIT_WINDOW_STATUS.json').read_text())['shared_git_writes_paused']
stamp = now()
record = {'utc': stamp, 'status': 'PRELIMINARY_CLASSICAL_ATTRIBUTION_CONFIRMED_EXACT_APPLICATION_PRIORITY_OPEN',
          'report': pin(A / 'ROOT_PRIORITY_CLASSICAL_COMPARISON_UPDATE.md'),
          'mathematics_percent': 100, 'priority_percent_estimate': 40, 'pr_workflow_percent_estimate': 30,
          'full_priority_accepted': False, 'paper_prepared': False, 'merged': False, 'published': False,
          'shared_git_window': 'PR55 follow-up explicitly released and root independently verified',
          'root_reading_scope': {'pries_ulmer2021': 'all35 pages', 'pries_ulmer2024_correction': 'all5 pages',
                                 'pries_ulmer2022': 'all13 pages', 'hoshi2026': 'all9 PDFpages',
                                 'oort_author_manuscript': 'selected23/80:1–9,12–20,40–43,77',
                                 'muller_yu2026v2': 'selected28/50:1–7,13–23,41–50',
                                 'chai_oort2020': 'indexed example lead only; native403 retained; fullreading not claimed',
                                 'kraft1975_original': 'not retrieved/read', 'chai2025_notes': 'not retrieved/read'},
          'program': pin(Path(__file__))}
out.write_text(json.dumps(record, indent=2) + '\n')
entry = ('\n### ' + stamp + ' — exact classical attribution and expanded priority comparison\n\n'
         'Root finished all13 published Pries–Ulmer2022 pages and read23 selected Oort author-manuscript pages and28 selected Muller–Yu2026v2 pages. Native portable convention comparison passed all six maps and complement/rotation checks. Exact2020 Chai–Oort word/filtration lead remains under investigation; actualHTTP403 failures preserved and no fullreading claimed. Classical object/non-self-duality attribution is required; exact qss filtration/Witt lift priority remains open. Mathematics100%, priority estimated40%, workflow30%. No paper, merge or publication. Shared PR55 follow-up released and exact d6bf1f8bd45c786d786a8f2dce3bb4002964ceb1 main/remote and all six foreign bodies/modes independently verified.\n')
for path in [A / 'ROOT_PRIORITY_WORK_LOG.md', A / 'RESEARCH_LOG.md', P / 'RESEARCH_LOG.md']:
    with path.open('a') as f: f.write(entry)
print(json.dumps(record, indent=2))
