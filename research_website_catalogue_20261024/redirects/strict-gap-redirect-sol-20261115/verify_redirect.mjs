// Pure local verification/planning: reads only; no network, Git or publication calls.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const A = path.dirname(fileURLToPath(import.meta.url));
const DEST = 'https://aleckriebel.com/research/strict-dirichlet-gap/';
const LEAF = 'docs/papers/strict-dirichlet-gap/index.html';
const OLD = 'b9705a518f76839427ff4f1e0bded6bdf95a7894';
const names = ['tree-root.json', 'tree-docs.json', 'tree-papers.json', 'tree-leaf.json'];
const childNames = ['docs', 'papers', 'strict-dirichlet-gap', 'index.html'];
const need = (ok, why) => { if (!ok) throw new Error(why); };
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const hash = (algorithm, b) => crypto.createHash(algorithm).update(b).digest('hex');
const gitHash = (type, b) => hash('sha1', Buffer.concat([Buffer.from(`${type} ${b.length}\0`), b]));
const native = x => {
  need(x.isError !== true, 'connector failure');
  return x.structuredContent?.content !== undefined ? JSON.parse(x.structuredContent.content) : x;
};
const content = x => x.structuredContent?.content ?? x.content;
const tuple = e => [e.path, e.mode, e.type, e.sha];

function checkPin(p) {
  const stat = fs.lstatSync(p.path);
  need(stat.isFile() && !stat.isSymbolicLink(), 'nonregular pinned file');
  const b = fs.readFileSync(p.path);
  need(b.length === p.bytes && hash('sha256', b) === p.SHA256, 'pinned bytes changed: ' + p.path);
}
function pinWalk(x) {
  if (!x || typeof x !== 'object') return 0;
  if (typeof x.path === 'string' && typeof x.bytes === 'number' && typeof x.SHA256 === 'string') {
    checkPin(x); return 1;
  }
  return Object.values(x).reduce((n, v) => n + pinWalk(v), 0);
}
function ownFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => {
    const p = path.join(dir, e.name);
    need(!e.isSymbolicLink(), 'unexpected symlink');
    return e.isDirectory() ? ownFiles(p) : [p];
  });
}
function custody() {
  const inputs = pinWalk(json(path.join(A, 'INPUT_MANIFEST.json')));
  let owned = 0;
  if (fs.existsSync(path.join(A, 'OWNED_MANIFEST.json'))) {
    const manifest = json(path.join(A, 'OWNED_MANIFEST.json'));
    const terminal = new Set(['OWNED_MANIFEST.json', 'FINAL_CLOSURE.json', 'FINAL_SEAL.json'].map(n => path.join(A, n)));
    const actual = ownFiles(A).filter(p => !terminal.has(p)).sort();
    const expected = manifest.files.map(e => e.path).sort();
    need(JSON.stringify(actual) === JSON.stringify(expected), 'owned exact membership');
    owned = pinWalk(manifest.files);
  }
  if (fs.existsSync(path.join(A, 'FINAL_SEAL.json'))) pinWalk(json(path.join(A, 'FINAL_SEAL.json')).bindings);
  return { input_pins_checked: inputs, owned_payloads_checked: owned };
}

function treeHash(tree) {
  need(tree.truncated === false, 'truncated tree');
  const entries = [...tree.tree];
  need(new Set(entries.map(e => e.path)).size === entries.length, 'duplicate tree names');
  entries.forEach(e => {
    need(!e.path.includes('/') && !e.path.includes('\0') && e.path !== '' &&
         /^[0-9a-f]{40}$/.test(e.sha), 'invalid immediate tree entry');
    need(({ tree: '040000', commit: '160000' })[e.type] === e.mode ||
         (e.type === 'blob' && ['100644', '100755', '120000'].includes(e.mode)), 'mode/type');
  });
  entries.sort((a, b) => Buffer.compare(Buffer.from(a.path + (a.type === 'tree' ? '/' : '')),
                                         Buffer.from(b.path + (b.type === 'tree' ? '/' : ''))));
  const payload = Buffer.concat(entries.map(e => Buffer.concat([
    Buffer.from(`${Number(e.mode).toString()} ${e.path}\0`), Buffer.from(e.sha, 'hex')
  ])));
  return gitHash('tree', payload);
}

function redirectContract(html) {
  need(/<html lang="en">/.test(html), 'language');
  need(html.match(/<link rel="canonical" href="([^"]+)">/g)?.length === 1 &&
       html.includes(`<link rel="canonical" href="${DEST}">`), 'canonical');
  need(html.includes(`<a href="${DEST}">Nonattainment in the Harrell–Stubbe Dirichlet gap inequality</a>`), 'visible fallback');
  need(html.includes(`<noscript><meta http-equiv="refresh" content="0; url=${DEST}"></noscript>`), 'noncompeting no-script refresh');
  need(html.match(/http-equiv="refresh"/g)?.length === 1, 'refresh count');
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  need(scripts.length === 1 && !/<script\s/.test(html), 'single inline script');
  need(!/\bsrc=|<iframe|<base\b|<form\b/.test(html), 'unnecessary resource or alternate navigation');
  const cases = ['', '?utm_source=legacy', '#result', '?utm_source=legacy#result',
    '?x=1&x=2#main', '?q=a+b&raw=%2523&raw=%2F#section%202',
    '?next=https%3A%2F%2Fevil.example%2F%3Fx%3D1#https://evil.example/',
    '?a=%23%3F%26%3D&empty=#fragment?x=1&x=2', '?q=%E2%88%86#%E2%88%86',
    '?x=1&&x=2#result', '?x=%00%0A%2B#part%2Ftwo', '?x=1#'];
  for (const tail of cases) {
    const old = new URL('https://aleckriebel.github.io/Math/papers/strict-dirichlet-gap/' + tail);
    const calls = [];
    const location = Object.freeze({ search: old.search, hash: old.hash, replace: u => calls.push(u) });
    vm.runInNewContext(scripts[0][1], { URL, window: Object.freeze({ location }) }, { timeout: 100 });
    need(calls.length === 1, 'exactly one replacement');
    need(calls[0] === DEST + old.search + old.hash, 'query/hash loss, duplication or wrong target');
  }
  return cases.length;
}

function makePlan(dir, html) {
  const ref = native(json(path.join(dir, 'remote-ref.json')));
  const end = native(json(path.join(dir, 'remote-ref-end.json')));
  const commit = native(json(path.join(dir, 'remote-commit.json')));
  const trees = names.map(n => native(json(path.join(dir, n))));
  need(ref.ref === 'refs/heads/main' && end.ref === ref.ref &&
       ref.object.type === 'commit' && ref.object.sha === end.object.sha &&
       commit.sha === ref.object.sha, 'capture is not one stable main parent');
  need(commit.tree.sha === trees[0].sha, 'parent tree association');
  trees.forEach((t, i) => {
    need(treeHash(t) === t.sha, 'native tree does not hash to its claimed SHA');
    const e = t.tree.find(v => v.path === childNames[i]);
    need(e && (i === 3 ? e.mode === '100644' && e.type === 'blob' && e.sha === OLD :
      e.mode === '040000' && e.type === 'tree' && e.sha === trees[i + 1].sha), 'path ancestry/old-leaf guard');
  });
  const oldBody = Buffer.from(content(json(path.join(dir, 'old-blob.json'))), 'utf8');
  need(gitHash('blob', oldBody) === OLD, 'decoded old bytes are not the authoritative base blob');
  const newBlob = gitHash('blob', Buffer.from(html));
  let next = newBlob;
  const changes = [];
  for (let i = 3; i >= 0; --i) {
    const old = trees[i];
    const nextEntries = old.tree.map(e => e.path === childNames[i] ? { ...e, sha: next } : { ...e });
    const changed = { ...old, tree: nextEntries };
    const sha = treeHash(changed);
    need(old.tree.filter(e => e.path !== childNames[i]).map(e => JSON.stringify(tuple(e))).join('\n') ===
      nextEntries.filter(e => e.path !== childNames[i]).map(e => JSON.stringify(tuple(e))).join('\n'), 'sibling mutation');
    changes.unshift({ tree_file: names[i], old_tree_SHA: old.sha, new_tree_SHA: sha,
      changed_child: childNames[i], preserved_immediate_sibling_entries: old.tree.length - 1 });
    next = sha;
  }
  return { repository_full_name: 'AlecKriebel/Math', only_path: LEAF,
    parent_commit_SHA: commit.sha, parent_root_tree_SHA: trees[0].sha,
    required_old_blob_SHA: OLD, candidate_blob_SHA: newBlob,
    predicted_new_root_tree_SHA: next, ancestor_tree_changes: changes,
    create_tree_args: { repository_full_name: 'AlecKriebel/Math', base_tree_sha: trees[0].sha,
      tree_elements: [{ path: LEAF, mode: '100644', type: 'blob', content: html }] },
    create_commit_args_after_tree_verified: { repository_full_name: 'AlecKriebel/Math',
      parent_sha: commit.sha, additional_parent_shas: [], tree_sha: next,
      message: 'Redirect strict Dirichlet gap article to verified AlecKriebel.com page' },
    update_ref_args_AFTER_SEPARATE_ROOT_AUTHORIZATION_AND_READBACK: {
      repository_full_name: 'AlecKriebel/Math', branch_name: 'main', expected_sha: commit.sha,
      force: false, sha: '<exact verified direct-child commit SHA; never this placeholder>' },
    Merkle_preservation: 'Every unchanged sibling mode/type/name/object ID is retained at all four path levels; consequently every other remote root descendant is preserved.' };
}

try {
  const argv = process.argv.slice(2);
  const dirAt = argv.indexOf('--snapshot-dir');
  const dir = dirAt < 0 ? path.join(A, 'raw') : path.resolve(argv[dirAt + 1]);
  const html = fs.readFileSync(path.join(A, 'index.html'), 'utf8');
  const cases = redirectContract(html);
  const plan = makePlan(dir, html);
  const bytes = custody();
  if (dirAt < 0 && fs.existsSync(path.join(A, 'PLAN_CAPTURED_PARENT.json')))
    need(JSON.stringify(json(path.join(A, 'PLAN_CAPTURED_PARENT.json'))) === JSON.stringify(plan), 'captured plan changed');
  function rejects(f) { try { f(); } catch { return true; } throw new Error('negative control accepted'); }
  rejects(() => redirectContract(html.replace('target.search = window.location.search;',
    'target.search = window.location.search + window.location.search;')));
  rejects(() => redirectContract(html.replace('target.hash = window.location.hash;', 'target.hash = "";')));
  rejects(() => redirectContract(html.replaceAll(DEST, 'https://evil.example/')));
  const postAt = argv.indexOf('--post-snapshot-dir');
  if (postAt >= 0) {
    const post = path.resolve(argv[postAt + 1]);
    const trees = names.map(n => native(json(path.join(post, n))));
    trees.forEach((t, i) => need(treeHash(t) === t.sha &&
      t.sha === plan.ancestor_tree_changes[i].new_tree_SHA, 'created tree violates exact predicted one-leaf result'));
  }
  if (argv.includes('--plan')) console.log(JSON.stringify(plan, null, 2));
  else console.log(JSON.stringify({ status: 'PASS', read_only: true, network: false, ...bytes,
    redirect_cases: cases, rejected_negative_controls: 3, original_tree_hashes_verified: 4,
    single_leaf: LEAF, base_blob: OLD, candidate_blob: plan.candidate_blob_SHA,
    captured_parent: plan.parent_commit_SHA, predicted_root: plan.predicted_new_root_tree_SHA,
    preserved_sibling_counts_root_to_leaf: plan.ancestor_tree_changes.map(x => x.preserved_immediate_sibling_entries),
    actual_post_tree_checked: postAt >= 0, actual_publication_or_redirect_verified: false }, null, 2));
} catch (e) { console.error(JSON.stringify({ status: 'FAIL', message: e.message })); process.exitCode = 1; }
