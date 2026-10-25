"""Prepare, or explicitly execute, the root-authorized JC legacy article redirect.

This one-paper helper handles documented incorporation of an earlier manuscript.
It does not relax the separate generic exact-edition redirect helper. Default
operation is read-only preflight plus owned preview files. Execution requires a
reviewed dry-run plan and creates a separate-index commit from fresh origin/main;
it never writes the shared working tree, shared index, local branch, or HEAD.
"""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.request
import xml.etree.ElementTree as ET


PROGRAM = Path(__file__).resolve().parents[1]
REPO = PROGRAM.parent
REDIRECTS = PROGRAM / 'redirects'
OWNED = REDIRECTS / 'jc-incorporated-article-implementation-20261025'
PUBLIC = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
RID = '22089373'
SLUG = 'strong-tree-child-level-2-jukes-cantor-identifiability'
TITLE = 'Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for Level-2 Jukes-Cantor Networks'
PDF = 'Strong_Tree_Childness_Sharp_Level2_JC.pdf'
OLD_BASE = 'https://aleckriebel.github.io/Math/papers/s-tc-jc-sharp-boundary/'
DESTINATION = 'https://aleckriebel.com/research/' + SLUG + '/'
LEAF = 'docs/papers/s-tc-jc-sharp-boundary/index.html'
OLD_PDF = 'docs/papers/s-tc-jc-sharp-boundary/paper.pdf'
INDEX = 'docs/index.html'
SITEMAP = 'docs/sitemap.xml'
MAX_PATHS = {LEAF, INDEX, SITEMAP}
OLD_HTML_SHA = 'e6dadc68e6cecf64b2b9ac3d95c55a18d1a455c356b9d6da0797e17ff2faaedf'
OLD_PDF_SHA = '65f5a54f6858b091546bc2221cb36d77bf5e24722bb79d6420b98f429dadc810'
NEW_HTML_SHA = 'ab60bf2313a43fcd0033fa1d450464f16dee03e6cc2ac9d37e3eeb1f1b8f5a1d'
NEW_PDF_SHA = 'ae01c6beba01da624bba7060e9f3adfce74a5e568e5808f4db168300d7873084'
LINEAGE_SHA = '928bbd136734ad918c69af20e5dff213c9fd35068a016af3acc5dc214528dc5e'
PENDING_SHA = '790a2e876d17c2a36d80bd85e4dcd9f388bdf70cb92abb1ed6958a8c028de525'
REPORT_SHA = 'e25bdc87b5bfc2d305de36a12f47214e081e6b4b4158eac4de19320eef354020'
DECISION_SHA = 'd98389088ec094e709df386c85521c319d7e49d2495ed703efb6560fbcc46121'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def git(*argv, env=None, data=None):
    clean_env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    if env:
        clean_env.update(env)
    return subprocess.check_output(
        ['git', '-c', 'gc.auto=0', *argv], cwd=REPO, env=clean_env, input=data
    )


def remote_main():
    rows = git('ls-remote', '--exit-code', 'origin', 'refs/heads/main').decode().splitlines()
    require(len(rows) == 1, 'Expected one origin main ref')
    revision, ref = rows[0].split()
    require(ref == 'refs/heads/main' and re.fullmatch(r'[0-9a-f]{40}', revision), 'Invalid origin main ref')
    return revision


def local_state():
    index = Path(git('rev-parse', '--git-path', 'index').decode().strip())
    head_file = Path(git('rev-parse', '--git-path', 'HEAD').decode().strip())
    if not index.is_absolute():
        index = REPO / index
    if not head_file.is_absolute():
        head_file = REPO / head_file
    return {
        'branch': git('branch', '--show-current').decode().strip(),
        'head': git('rev-parse', 'HEAD').decode().strip(),
        'head_file_sha256': sha(head_file.read_bytes()),
        'shared_index_path': str(index),
        'shared_index_sha256': sha(index.read_bytes()),
        'docs': {str(p.relative_to(REPO)): sha(p.read_bytes())
                 for p in sorted((REPO / 'docs').rglob('*')) if p.is_file()},
    }


def verify_gates():
    lineage_path = REDIRECTS / 'jc-legacy-root-lineage-disposition-20261025.json'
    require(sha(lineage_path.read_bytes()) == LINEAGE_SHA, 'Root lineage disposition changed; review required')
    lineage = read_json(lineage_path)
    require(lineage['status'] == 'ARTICLE_REDIRECT_AUTHORIZED_AFTER_ROOT_LINEAGE_REVIEW'
            and lineage['accepted_by'] == 'root' and str(lineage['record_id']) == RID,
            'Missing exact root lineage authorization')
    require(lineage['source'] == OLD_BASE and lineage['destination'] == DESTINATION,
            'Lineage source/destination mismatch')
    permitted = set(lineage['permitted_mutation'])
    require({LEAF, SITEMAP} <= permitted <= MAX_PATHS, 'Unexpected lineage mutation scope')
    require(lineage['historical_pdf_preserve_sha256'] == OLD_PDF_SHA
            and lineage['old_pdf_index_link_preserved'] is True
            and lineage['old_pending_receipt_preserved'] is True
            and lineage['target_already_root_browser_live_verified'] is True
            and lineage['no_new_scientific_clearance'] is True, 'Lineage preservation gate failed')
    report = REDIRECTS / 'jc-legacy-reconciliation-20261025/REPORT.md'
    decision = report.with_name('decision.json')
    pending = REDIRECTS / 'jc-legacy-correspondence-20261025.json'
    require(sha(report.read_bytes()) == lineage['report_sha256'] == REPORT_SHA, 'Lineage report mismatch')
    require(sha(decision.read_bytes()) == lineage['decision_sha256'] == DECISION_SHA, 'Lineage decision mismatch')
    require(sha(pending.read_bytes()) == PENDING_SHA, 'Historical pending receipt changed')
    paper = PROGRAM / 'papers' / RID
    publication = read_json(paper / 'publication.json')
    promotion = read_json(paper / 'promotion.json')
    proof = read_json(PROGRAM / 'verification/browser-root-disposition.json')['papers'][RID]
    require(publication['slug'] == SLUG and publication['title'] == TITLE
            and publication['pdf_filename'] == PDF
            and publication['doi'] == '10.5281/zenodo.' + RID, 'Publication identity mismatch')
    require(promotion['status'] == proof['status'] == 'PASS'
            and promotion['disposition_by'] == proof['accepted_by'] == 'root', 'Target root PASS gate missing')
    require(sha((paper / 'publication.json').read_bytes()) == proof['publication_sha256']
            and sha((paper / 'promotion.json').read_bytes()) == proof['promotion_sha256'], 'Target content/promotion changed')
    require(proof['html_sha256'] == NEW_HTML_SHA
            and proof['pdf_sha256'] == promotion['pdf_sha256'] == NEW_PDF_SHA, 'Accepted target hashes changed')
    clearance_path = PROGRAM / promotion['root_clearance_file']
    require(clearance_path == PROGRAM / 'verification/root-clearance-22089373-20261025.json', 'Unexpected scientific clearance path')
    require(sha(clearance_path.read_bytes()) == promotion['root_clearance_sha256'], 'Existing root clearance changed')
    clearance = read_json(clearance_path)
    require(clearance['status'] == 'PASS' and clearance['disposition_by'] == 'root'
            and clearance['pdf_sha256'] == NEW_PDF_SHA, 'Existing root clearance gate failed')
    browser_path = PROGRAM / proof['browser_receipt']
    require(sha(browser_path.read_bytes()) == proof['browser_receipt_sha256'], 'Accepted browser evidence changed')
    browser = read_json(browser_path)
    require(browser['status'] == 'PASS' and str(browser['record_id']) == RID
            and browser['full_pdf_url'] == DESTINATION + PDF
            and browser['full_pdf_observed_pages'] == 33
            and browser['reader_observed_pages'] == 7, 'Browser reader identity gate failed')
    live_path = PROGRAM / proof['live_receipt']
    live = read_json(live_path)
    require(live['passed'] is True, 'Accepted live receipt failed')
    for path, url, digest in [('research/' + SLUG + '/index.html', DESTINATION, NEW_HTML_SHA),
                              ('research/' + SLUG + '/' + PDF, DESTINATION + PDF, NEW_PDF_SHA)]:
        rows = [row for row in live['checks'] if row['path'] == path]
        require(len(rows) == 1 and rows[0]['passed'] is True and rows[0]['url'] == url
                and rows[0]['actual_sha256'] == rows[0]['expected_sha256'] == digest,
                'Accepted live payload identity mismatch: ' + path)
        require(sha((PUBLIC / path).read_bytes()) == digest, 'Current target asset changed: ' + path)
    paths = [lineage_path, report, decision, pending, paper / 'publication.json', paper / 'promotion.json',
             clearance_path, browser_path, live_path]
    return {'files': {str(p.relative_to(PROGRAM)): sha(p.read_bytes()) for p in paths},
            'selected_browser_root_proof_sha256': sha(json.dumps(proof, sort_keys=True).encode())}


def live_get(url, digest, media_type):
    request = urllib.request.Request(url, headers={'User-Agent': 'JCArticleRedirectPreflight/1.0'})
    with urllib.request.urlopen(request, timeout=45) as response:
        data = response.read()
        require(response.status == 200 and response.url == url, 'Live status or URL changed: ' + url)
        require(response.headers.get_content_type() == media_type, 'Live media type changed: ' + url)
    require(sha(data) == digest, 'Live bytes changed: ' + url)
    return {'url': url, 'status': 200, 'bytes': len(data), 'sha256': sha(data),
            'verified_utc': datetime.now(timezone.utc).isoformat()}


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.hrefs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.hrefs.append(dict(attrs).get('href', ''))


def prepare(parent):
    before = {path: git('show', parent + ':' + path) for path in MAX_PATHS}
    require(sha(before[LEAF]) == OLD_HTML_SHA, 'Fresh-origin old HTML differs from authorized bytes')
    require(sha(git('show', parent + ':' + OLD_PDF)) == OLD_PDF_SHA, 'Fresh-origin historical PDF changed')
    require(sha((REPO / LEAF).read_bytes()) == OLD_HTML_SHA
            and sha((REPO / OLD_PDF).read_bytes()) == OLD_PDF_SHA, 'Local historical article/PDF changed')
    redirect = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Earlier JC manuscript incorporated | Alec Kriebel</title>
<meta http-equiv="refresh" content="0; url={escape(DESTINATION)}">
<link rel="canonical" href="{escape(DESTINATION)}">
</head><body>
<h1>Earlier manuscript incorporated into a later paper</h1>
<p>The result in <i>Full-Dimensional Jukes–Cantor Ambiguity in Weakly Tree-Child Level-2 Networks</i> is incorporated into the later paper <a href="{escape(DESTINATION)}">{escape(TITLE)}</a>.</p>
<p><a href="{escape(DESTINATION)}">Read the current paper on AlecKriebel.com.</a></p>
<p><a href="./paper.pdf">Read the unchanged historical edition (10-page PDF).</a> This earlier manuscript has a narrower scope than the later paper.</p>
</body></html>
'''.encode()
    index = before[INDEX].decode()
    old_article_href = './papers/s-tc-jc-sharp-boundary/'
    article_hrefs = [href for href in Links(index).hrefs if href in
                     {old_article_href, OLD_BASE, '/Math/papers/s-tc-jc-sharp-boundary/'}]
    require(len(article_hrefs) <= 1, 'Multiple old index article links require review')
    old_pdf_hrefs = [href for href in Links(index).hrefs if 's-tc-jc-sharp-boundary/' in href and href.endswith('.pdf')]
    if article_hrefs:
        literal = 'href="' + article_hrefs[0] + '"'
        require(index.count(literal) == 1, 'Unexpected index href spelling')
        index = index.replace(literal, 'href="' + DESTINATION + '"', 1)
    require([href for href in Links(index).hrefs if 's-tc-jc-sharp-boundary/' in href and href.endswith('.pdf')]
            == old_pdf_hrefs, 'Historical index PDF links changed')
    sitemap, removed = re.subn(r'  <url>\s*<loc>' + re.escape(OLD_BASE) + r'</loc>.*?</url>\n',
                               '', before[SITEMAP].decode(), flags=re.S)
    require(removed == 1, 'Expected exactly one old sitemap URL')
    before_entries = list(ET.fromstring(before[SITEMAP]))
    after_entries = list(ET.fromstring(sitemap))
    retained = [entry for entry in before_entries
                if next((child.text for child in entry if child.tag.endswith('}loc')), None) != OLD_BASE]
    require([ET.tostring(entry) for entry in after_entries] == [ET.tostring(entry) for entry in retained],
            'Another sitemap entry changed')
    after = {LEAF: redirect, INDEX: index.encode(), SITEMAP: sitemap.encode()}
    changed = sorted(path for path in MAX_PATHS if before[path] != after[path])
    require(set(changed) == ({LEAF, SITEMAP, INDEX} if article_hrefs else {LEAF, SITEMAP}), 'Unexpected changed paths')
    return before, after, changed, {'remote_article_href_count': len(article_hrefs),
                                  'historical_pdf_hrefs_before': old_pdf_hrefs,
                                  'historical_pdf_hrefs_after': old_pdf_hrefs,
                                  'remote_index_unchanged': before[INDEX] == after[INDEX]}


def tree_entries(tree):
    return dict(row.split('\t', 1)[::-1] for row in git('ls-tree', '-r', tree, '--', 'docs').decode().splitlines())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--dry-run', action='store_true')
    mode.add_argument('--execute', action='store_true')
    parser.add_argument('--approved-plan', type=Path)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    require(not any(name in os.environ for name in ['GIT_INDEX_FILE', 'GIT_WORK_TREE', 'GIT_DIR', 'GIT_COMMON_DIR']),
            'Unexpected inherited Git overrides')
    require(Path(git('rev-parse', '--show-toplevel').decode().strip()) == REPO, 'Wrong repository')
    require(git('remote', 'get-url', 'origin').decode().strip() in
            {'git@github.com:AlecKriebel/Math.git', 'https://github.com/AlecKriebel/Math.git'}, 'Unexpected remote')
    initial = local_state()
    require(initial['branch'] == 'main', 'Shared branch must remain main')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = (args.output_dir or OWNED / (('execution-' if args.execute else 'dry-run-') + stamp)).resolve()
    require(out.is_relative_to(OWNED.resolve()) and out != OWNED.resolve(), 'Output must be a new owned subdirectory')
    out.mkdir(parents=True, exist_ok=False)
    write_json(out / 'local-state-before.json', initial)
    try:
        gates = verify_gates()
        actual_live = [live_get(DESTINATION, NEW_HTML_SHA, 'text/html'),
                       live_get(DESTINATION + PDF, NEW_PDF_SHA, 'application/pdf')]
        if args.execute:
            require(args.approved_plan is not None, 'Execution requires the root-reviewed dry-run plan')
            approved = read_json(args.approved_plan)
            require(approved['mode'] == 'dry_run' and approved['status'] == 'READY_FOR_ROOT_REVIEW'
                    and approved['script_sha256'] == sha(Path(__file__).read_bytes()), 'Invalid reviewed plan or changed helper')
            git('fetch', '--no-tags', 'origin', 'main')
        else:
            require(args.approved_plan is None, '--approved-plan is only used for execution')
        parent = remote_main()
        git('cat-file', '-e', parent + '^{commit}')  # Dry-run never fetches or writes Git objects.
        before, after, changed, index_proof = prepare(parent)
        docs_before = tree_entries(parent)
        docs_planned = dict(docs_before)
        for path in changed:
            mode, kind, _ = docs_before[path].split()
            # Without -w this computes an object ID without writing a Git object.
            blob = git('hash-object', '--stdin', data=after[path]).decode().strip()
            docs_planned[path] = mode + ' ' + kind + ' ' + blob
        require({path for path in docs_before if docs_before[path] != docs_planned[path]} == set(changed),
                'Planned docs tree changed another object')
        require(docs_before[OLD_PDF] == docs_planned[OLD_PDF], 'Planned historical PDF object changed')
        write_json(out / 'origin-docs-before.json', docs_before)
        write_json(out / 'planned-docs-after.json', docs_planned)
        plan = {'schema': 'jc-incorporated-article-redirect-v1', 'mode': 'execute' if args.execute else 'dry_run',
                'status': 'READY_FOR_ROOT_REVIEW', 'utc': datetime.now(timezone.utc).isoformat(),
                'script_sha256': sha(Path(__file__).read_bytes()), 'parent': parent, 'record_id': RID,
                'source': OLD_BASE, 'destination': DESTINATION, 'changed_paths': changed,
                'before_sha256': {path: sha(data) for path, data in before.items()},
                'after_sha256': {path: sha(data) for path, data in after.items()},
                'historical_pdf_sha256': OLD_PDF_SHA, 'index_proof': index_proof,
                'gates': gates, 'fresh_target_live': actual_live, 'working_tree_writes': False,
                'scientific_clearance': 'existing root decision only; no new scientific review'}
        for side, values in [('before', before), ('after', after)]:
            for path, data in values.items():
                target = out / side / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        patch = ''.join(''.join(difflib.unified_diff(before[path].decode().splitlines(True),
                                                   after[path].decode().splitlines(True),
                                                   fromfile='a/' + path, tofile='b/' + path)) for path in changed)
        (out / 'proposed.patch').write_text(patch)
        write_json(out / 'index-preservation.json', {**index_proof,
                   'remote_before_sha256': sha(before[INDEX]), 'remote_after_sha256': sha(after[INDEX]),
                   'local_before_sha256': initial['docs'][INDEX],
                   'note': 'Local and origin index may differ; only any actual article href may change remotely. PDF hrefs stay exact.'})
        require(verify_gates() == gates, 'Authorization or accepted target evidence changed during preparation')
        require(remote_main() == parent, 'Fresh-origin race; rerun dry-run and review the new diff')
        if args.execute:
            for key in ['schema', 'script_sha256', 'parent', 'source', 'destination', 'changed_paths',
                        'before_sha256', 'after_sha256', 'historical_pdf_sha256', 'index_proof', 'gates']:
                require(plan[key] == approved[key], 'Reviewed plan changed: ' + key)
            with tempfile.TemporaryDirectory(prefix='jc-article-separate-index-') as temp:
                env = {'GIT_INDEX_FILE': str(Path(temp) / 'index')}
                git('read-tree', parent, env=env)
                for path in changed:
                    mode = git('ls-tree', parent, '--', path).decode().split()[0]
                    blob = git('hash-object', '-w', '--stdin', data=after[path]).decode().strip()
                    git('update-index', '--add', '--cacheinfo', mode, blob, path, env=env)
                require(sorted(git('diff', '--cached', '--name-only', parent, env=env).decode().splitlines()) == changed,
                        'Separate index contains unexpected paths')
                git('diff', '--cached', '--check', parent, env=env)
                tree = git('write-tree', env=env).decode().strip()
                old_tree, new_tree = tree_entries(parent), tree_entries(tree)
                require(set(old_tree) == set(new_tree), 'Docs paths added or removed unexpectedly')
                require({path for path in old_tree if old_tree[path] != new_tree[path]} == set(changed),
                        'Another docs object changed')
                require(git('show', tree + ':' + OLD_PDF) == git('show', parent + ':' + OLD_PDF), 'Historical PDF tree object changed')
                commit = git('-c', 'commit.gpgsign=false', 'commit-tree', tree, '-p', parent,
                             data=b'Redirect incorporated earlier JC manuscript to canonical paper page\n').decode().strip()
            require(verify_gates() == gates and remote_main() == parent, 'Pre-push evidence/origin race')
            require(local_state() == initial, 'Shared local state changed before push; no push performed')
            plan.update(status='PREPARED_NOT_PUSHED', commit=commit, tree=tree)
            write_json(out / 'plan.json', plan)
            write_json(out / 'push-intent.json', {'utc': datetime.now(timezone.utc).isoformat(),
                       'parent': parent, 'commit': commit, 'ref': 'refs/heads/main', 'force': False,
                       'note': 'If transport fails, inspect the remote ref before any retry; never assume push outcome.'})
            # Ordinary fast-forward push; a race after this check is rejected by Git.
            pushed = git('push', '--porcelain', 'origin', commit + ':refs/heads/main').decode()
            plan.update(status='PUSHED_PENDING_LIVE_REDIRECT_VERIFICATION', commit=commit, tree=tree, push_output=pushed)
        write_json(out / 'plan.json', plan)
        print(json.dumps({'output': str(out), 'status': plan['status'], 'parent': parent, 'changed_paths': changed}))
    finally:
        final = local_state()
        write_json(out / 'local-state-after.json', final)
        write_json(out / 'shared-state-preservation.json', {'unchanged': final == initial,
                   'branch_main': final['branch'] == 'main', 'local_head_unchanged': final['head'] == initial['head'],
                   'shared_index_unchanged': final['shared_index_sha256'] == initial['shared_index_sha256'],
                   'all_local_docs_unchanged': final['docs'] == initial['docs'],
                   'local_docs_index_before_sha256': initial['docs'][INDEX],
                   'local_docs_index_after_sha256': final['docs'][INDEX]})
        require(final == initial, 'Shared working tree, index, branch or local HEAD changed')


if __name__ == '__main__':
    main()
