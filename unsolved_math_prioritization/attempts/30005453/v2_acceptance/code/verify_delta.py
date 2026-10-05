#!/usr/bin/env python3
"""Independent, bounded-delta verification; standard library only.

Reads but never changes any supplied archive or author directory. The six
approved textual substitutions are transcribed below independently of the
first audit's delta implementation. No source document is embedded.
"""
from pathlib import Path, PurePosixPath
import argparse, copy, difflib, hashlib, io, json, stat, warnings, zipfile

AUTHOR = 'SUBCRITICAL_REINFORCEMENT_30005453_AUTHOR_SAFE_FREEZE.zip'
AUDIT = 'SUBCRITICAL_REINFORCEMENT_30005453_INDEPENDENT_AUDIT_SAFE.zip'
V2 = 'SUBCRITICAL_REINFORCEMENT_30005453_AUTHOR_V2_PROPOSED_SAFE.zip'
ANCHORS = {
    AUTHOR: (19790, '4e2b7cbf89688b04a80bfae946457582f8970cb90d6af260302aa1dad3a33856'),
    AUDIT: (29473, 'e459a35c00246f2cd5db956283e1dced8b0665524919a461dd42e964d20f22cd'),
    V2: (20008, '689cd325db19a449e373441c0c7cb0ede0e103456ec857215a207b7af83d3d8d'),
}
AUTHOR_NAMES = set(('MANIFEST.json PRIOR_ATTEMPT_CHECK.json PROOF.md README.md RESEARCH_LOG.md '
                    'RESULT.json SOURCE_METADATA.json SOURCE_REVIEW.md code/verify_algebra.py '
                    'code/verify_manifest.py results/algebra_checks.json').split())
AUDIT_NAMES = set(('MANIFEST.json AUDIT.md CORRECTIONS.md PRIOR_WORK_CHECK.json PROPOSED_V2.diff '
                   'PROPOSED_V2_BINDING.json PROPOSED_V2_DELTA.json README.md RESULT.json SOURCE_CHECK.json '
                   'code/independent_checks.py code/replay_audit.py code/verify_provenance.py '
                   'results/author_replay.json results/independent_checks.json results/provenance.json').split())
CHANGES = {
 'PROOF.md': [
 ('''among all nonnegative fixed points is false. The intended non-vanishing
homogenization problem is addressed here. Initially zero edges also require a
different statement, because the dynamics never reinforce them.''',
  '''among all nonnegative fixed points is false. The theorem here addresses an
explicitly corrected positive-equilibrium formulation. Interpreting this as the
source's intended non-vanishing homogenization problem is an inference, not an
explicit restriction in the report. Initially zero edges also require a different
statement, because the dynamics never reinforce them.'''),
 ('''  (12) subtract H(N_e(0)), whose contribution after scaling vanishes. No''',
  '''  (9) replace H(N_e(t)) by H(N_e(t))-H(N_e(0)); the initial constant vanishes
  after scaling. No''')],
 'README.md': [
 ('''criticality. This package explicitly distinguishes that literal ambiguity
from the intended positive-equilibrium convergence question.''',
  '''criticality. This package distinguishes the false literal nonnegative-uniqueness
statement from an explicitly corrected positive-equilibrium convergence question.
Calling the latter the source's intended question is an interpretation; the report
does not explicitly state that restriction.''')],
 'SOURCE_REVIEW.md': [
 ('''retrieved primary source was found to establish the complete intended claim.''',
  '''retrieved primary source was found to establish the complete positive-equilibrium
theorem stated here.'''),
 ('''The package claims a complete author-level candidate proof of the intended
positive-equilibrium statement. The outstanding task is independent scrutiny''',
  '''The package claims a complete author-level candidate proof of an explicitly
corrected positive-equilibrium statement. The primary report does not explicitly
restrict uniqueness to positive equilibria; that reading is an interpretation,
not a verified source convention. The outstanding task is independent scrutiny''')],
 'RESULT.json': [
 ('complete_candidate_proof_of_intended_positive_equilibrium_statement',
  'complete_candidate_proof_of_explicitly_corrected_positive_equilibrium_statement')]
}

def sha(b): return hashlib.sha256(b).hexdigest()
def require(value, why):
    if not value: raise ValueError(why)
def strict_object(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'duplicate JSON key')
        out[k] = v
    return out
def decode(b): return json.loads(b, object_pairs_hook=strict_object)
def parse(raw, names):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos = z.infolist()
        require(len(infos) == len(names), 'archive member count')
        require(len({i.filename for i in infos}) == len(infos), 'duplicate archive member')
        require({i.filename for i in infos} == names, 'archive allowlist')
        for i in infos:
            parts = PurePosixPath(i.filename).parts
            require(not i.is_dir() and not i.filename.startswith('/') and '..' not in parts, 'unsafe path')
            require(not stat.S_ISLNK(i.external_attr >> 16), 'symlink')
            require(not i.flag_bits & 1, 'encrypted entry')
        require(z.testzip() is None, 'CRC')
        files = {i.filename: z.read(i) for i in infos}
    m = decode(files['MANIFEST.json'])
    require(len(m['files']) == len(names)-1, 'manifest member count')
    require({e['path'] for e in m['files']} == names-{'MANIFEST.json'}, 'manifest exact coverage')
    for e in m['files']:
        b = files[e['path']]
        require(len(b) == e['bytes'] and sha(b) == e['sha256'], 'manifest hash or size')
    return files

def update_manifest(files):
    m = decode(files['MANIFEST.json'])
    for e in m['files']:
        e['bytes'] = len(files[e['path']]); e['sha256'] = sha(files[e['path']])
    files['MANIFEST.json'] = (json.dumps(m, indent=2)+'\n').encode()

def expected_v2(old):
    expected = dict(old)
    for name, replacements in CHANGES.items():
        text = old[name].decode()
        for before, after in replacements:
            require(text.count(before) == 1, 'approved old wording not unique: '+name)
            text = text.replace(before, after, 1)
        expected[name] = text.encode()
    m = decode(old['MANIFEST.json'])
    m['freeze_label'] = 'subcritical_reinforcement_30005453_author_v2_proposed_unaccepted'
    m['status'] = 'proposed_editorial_delta_pending_separate_review'
    expected['MANIFEST.json'] = (json.dumps(m, indent=2)+'\n').encode()
    update_manifest(expected)
    return expected

def verify_delta(old, new):
    wanted = expected_v2(old)
    require(set(wanted) == set(new), 'delta members')
    for name in wanted:
        require(wanted[name] == new[name], 'unapproved bytes: '+name)
    require({n for n in old if old[n] != new[n]} == set(CHANGES)|{'MANIFEST.json'}, 'changed-file set')
    def core(f):
        p = f['PROOF.md']; start = p.index(b'## 2.'); stop = p.index(b'## 9.')
        return p[start:stop]
    require(core(old) == core(new), 'analytic sections changed')
    require(decode(old['RESULT.json'])['hypotheses'] == decode(new['RESULT.json'])['hypotheses'], 'hypotheses changed')
    return {'status': 'PASS', 'changed_files': sorted(set(CHANGES)|{'MANIFEST.json'}),
            'text_substitution_counts': {k: len(v) for k,v in CHANGES.items()},
            'analytic_sections_2_through_8_bytes': len(core(new)),
            'analytic_sections_2_through_8_sha256': sha(core(new)),
            'code_and_saved_algebra_results_unchanged': True,
            'all_other_bytes_unchanged': True}

def archive_bytes(files, mutation=None):
    out = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        with zipfile.ZipFile(out, 'w') as z:
            for name, b in files.items():
                if mutation == 'missing' and name == 'README.md': continue
                info = zipfile.ZipInfo('../README.md' if mutation == 'traversal' and name == 'README.md' else name)
                if mutation == 'symlink' and name == 'README.md':
                    info.create_system = 3; info.external_attr = (stat.S_IFLNK|0o777)<<16
                z.writestr(info,b)
            if mutation == 'extra_pdf': z.writestr('source.pdf', b'%PDF-')
            if mutation == 'duplicate': z.writestr('README.md', files['README.md'])
    return out.getvalue()

def negative_controls(old, new):
    outcomes = {}
    for kind in ('missing','traversal','symlink','extra_pdf','duplicate'):
        try: parse(archive_bytes(new,kind), AUTHOR_NAMES)
        except ValueError: outcomes[kind] = 'REJECTED'
        else: raise ValueError('negative archive control accepted: '+kind)
    mutations = {
      'analytic_change_with_updated_manifest': ('PROOF.md', b'Every coordinate belongs', b'Almost every coordinate belongs'),
      'code_change_with_updated_manifest': ('code/verify_algebra.py', b'import random', b'import random\n# changed'),
      'false_source_attribution': ('PROOF.md', b'an inference, not an\nexplicit restriction', b'an explicit restriction, not an\ninference'),
      'wrong_initial_offset_reference': ('PROOF.md', b'(9) replace H', b'(12) replace H'),
      'unapproved_research_log_edit': ('RESEARCH_LOG.md', b'\n', b' \n'),
      'false_self_acceptance': ('RESULT.json', b'"independent_check": "PENDING"', b'"independent_check": "PASS"')
    }
    for kind, (name,before,after) in mutations.items():
        mutant = dict(new)
        require(before in mutant[name], 'negative-control target missing')
        mutant[name] = mutant[name].replace(before,after,1)
        update_manifest(mutant)
        checked = parse(archive_bytes(mutant), AUTHOR_NAMES)
        try: verify_delta(old,checked)
        except ValueError: outcomes[kind] = 'REJECTED'
        else: raise ValueError('semantic mutation accepted: '+kind)
    require(len(outcomes)==11, 'negative coverage')
    return outcomes

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input-dir',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    inputs={}; files={}
    for name,(size,digest) in ANCHORS.items():
        raw=(args.input_dir/name).read_bytes()
        require(len(raw)==size and sha(raw)==digest, 'frozen input anchor: '+name)
        files[name]=parse(raw,AUDIT_NAMES if name==AUDIT else AUTHOR_NAMES)
        inputs[name]={'bytes':size,'sha256':digest,'member_count':len(files[name]),
                      'manifest_sha256':sha(files[name]['MANIFEST.json'])}
    old,new,audit=files[AUTHOR],files[V2],files[AUDIT]
    require(sha(new['MANIFEST.json'])=='caa399e49eda33b0365d428f4e5fdf09e9cb04ef59b73e764411da304bb654a3','v2 manifest anchor')
    result=verify_delta(old,new)
    produced=''.join(''.join(difflib.unified_diff(old[n].decode().splitlines(True),new[n].decode().splitlines(True),
                    fromfile='author_v1/'+n,tofile='proposed_author_v2/'+n)) for n in CHANGES)
    require(produced.encode()==audit['PROPOSED_V2.diff'],'first-audit diff does not match independently rebuilt delta')
    for d,arch in [('subcritical_reinforcement_30005453/safe',old),
                   ('subcritical_reinforcement_30005453_author_v2/safe',new),
                   ('subcritical_reinforcement_30005453_independent_audit/safe',audit)]:
        root=args.input_dir/d
        if root.exists():
            require({str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}==set(arch),'directory allowlist')
            for n,b in arch.items(): require((root/n).read_bytes()==b,'preserved directory bytes: '+n)
    out={'status':'PASS','inputs':inputs,'delta':result,
         'first_audit_diff_rebuilt_exactly':True,'original_and_v2_directories_preserved':True,
         'negative_controls':negative_controls(old,new),
         'source_documents_or_private_material_read_by_this_script':False,
         'remote_writes':False}
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
