"""Read only the exact QUEUE.md status row at each inventoried PR head."""
import collections
import datetime
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def rows(text):
    result = {}
    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if len(cells) < 8:
            continue
        match = re.match(r'^(\d+)\s*(?:/|$)', cells[1])
        if match:
            result[match.group(1)] = {'status': cells[7], 'row': line}
    return result


def run():
    path = ROOT / 'pr_inventory.json'
    inventory = json.loads(path.read_text())
    main = rows((REPO / QUEUE).read_text())
    counts = collections.Counter()
    eligible = []
    for pr in inventory['range_prs']:
        content = subprocess.run(
            ['git', 'show', pr['headRefOid'] + ':' + QUEUE], cwd=REPO,
            capture_output=True, text=True, check=True).stdout
        branch = rows(content)
        candidates = list(dict.fromkeys(
            candidate for candidate in re.findall(r'(?<!\d)\d{4,8}(?!\d)', pr['headRefName'])
            if candidate in branch))
        if len(candidates) != 1:
            raise ValueError((pr['number'], candidates))
        problem_id = candidates[0]
        pr['problem_id'] = problem_id
        pr['queue_status'] = branch[problem_id]['status']
        pr['head_queue_row'] = branch[problem_id]['row']
        pr['main_queue_status'] = main.get(problem_id, {}).get('status')
        pr.pop('main_queue_rows', None)
        pr.pop('problem_id_candidates', None)
        pr['disposition'] = ('eligible_pending_review' if pr['isDraft'] and
                             pr['queue_status'] == 'claimed_solved' else 'skipped_out_of_scope')
        counts[pr['queue_status']] += 1
        if pr['disposition'] == 'eligible_pending_review':
            eligible.append({key: pr[key] for key in (
                'number', 'problem_id', 'title', 'headRefOid', 'headRefName',
                'queue_status', 'main_queue_status')})
    inventory['status_screened_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    inventory['status_counts'] = dict(counts)
    path.write_text(json.dumps(inventory, indent=2) + '\n')
    (ROOT / 'status_screen.tsv').write_text(
        'pr\tproblem_id\tpr_head_status\tmain_status\tdisposition\n' + ''.join(
            f"{pr['number']}\t{pr['problem_id']}\t{pr['queue_status']}\t"
            f"{pr['main_queue_status']}\t{pr['disposition']}\n"
            for pr in inventory['range_prs']))
    print(json.dumps({'status_counts': dict(counts), 'eligible': eligible}, indent=2))


if __name__ == '__main__':
    run()
