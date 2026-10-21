#!/usr/bin/env python3
"""Additional independent guards; all calls mocked, all writes in review tmp."""
from pathlib import Path
import copy
import importlib.util
import io
import json
import sys
import tempfile
import zipfile
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE / 'tmp/operations_clone'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


p = load('prepare_integration', ROOT / 'prepare_integration.py')
t = load('record_tracker', ROOT / 'record_tracker.py')
DOI = '10.5281/zenodo.99999999'
checks = []


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejects(name, fn, types=(ValueError,)):
    try:
        fn()
    except types:
        checks.append(name)
        return
    raise RuntimeError('unexpected acceptance: ' + name)


meta = {'number':623, 'state':'OPEN', 'baseRefName':'main', 'headRefName':p.BRANCH,
        'headRefOid':p.ORIGINAL, 'isCrossRepository':False, 'headRepositoryOwner':{'login':'AlecKriebel'}}
base_queue = ('| 651 | 30001184 / OWR-3392-012 | title | 0.1067 | 6.0 | 3 | 2009 | claimed_solved | 1/5 |  | finding |  |\n').encode()
for name, altered in [('queued_PR_status',base_queue.replace(b'claimed_solved',b'queued')),
                      ('different_turns',base_queue.replace(b'1/5',b'2/5'))]:
    with patch.object(p,'local_state',return_value={}), patch.object(p,'PUSHED_RECEIPT',HERE/'tmp/nonexistent'), \
            patch.object(p,'pr_metadata',return_value=meta), patch.object(p,'git',return_value=altered), \
            patch.object(p,'load_snapshot',side_effect=RuntimeError('candidate read prohibited')), \
            patch.object(sys,'argv',['prepare_integration.py','--doi',DOI]):
        rejects(name + '_before_candidate_read',p.main)

for label, properties, headers in [
    ('wrong_gid',[{'sheetId':t.GID+1,'title':t.TAB}],[t.HEADERS]),
    ('wrong_title',[{'sheetId':t.GID,'title':'Other'}],[t.HEADERS]),
    ('duplicate_gid',[{'sheetId':t.GID,'title':t.TAB},{'sheetId':t.GID,'title':t.TAB}],[t.HEADERS]),
    ('wrong_headers',[{'sheetId':t.GID,'title':t.TAB}],[['Original Problem','Solution Chat URL','Notes','DOI']]),
    ('extra_header',[{'sheetId':t.GID,'title':t.TAB}],[t.HEADERS+['Extra']]),
]:
    def call(resource, method, params, body=None):
        require(method=='get','read-only fixture')
        if resource=='spreadsheets': return {'sheets':[{'properties':v} for v in properties]}
        if params['range'].endswith('A1:D1'): return {'values':headers}
        return {'values':[]}
    with patch.object(t,'call',side_effect=call):
        rejects('tracker_'+label,t.inspect)

row = t.wanted_row(DOI)
require(t.doi_matches([t.HEADERS,row[:2]+[DOI]+row[3:],row[:2]+[' https://doi.org/'+DOI+'/ ']+row[3:]],DOI)==[2,3], 'DOI normalization')
checks.append('exact_bare_and_URL_DOI_normalization')
require(t.doi_matches([row[:2]+[DOI+'0']+row[3:]],DOI)==[], 'prefix DOI mismatch')
checks.append('DOI_prefix_collision_does_not_match')

valid = {'updates':{'updatedRange':"'Math Puzzles'!A2:D2",'updatedRows':1,'updatedColumns':4,'updatedCells':4}}
for label, response, readback in [
    ('wrong_tab',{'updates':valid['updates']|{'updatedRange':"'Other'!A2:D2"}},[row]),
    ('header_target',{'updates':valid['updates']|{'updatedRange':"'Math Puzzles'!A1:D1"}},[row]),
    ('two_row_range',{'updates':valid['updates']|{'updatedRange':"'Math Puzzles'!A2:D3"}},[row]),
    ('wrong_count',{'updates':valid['updates']|{'updatedCells':3}},[row]),
    ('wrong_readback',valid,[row[:3]+['wrong notes']]),
]:
    with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='edges-') as td:
        pending = Path(td)/'pending.json'
        calls = []
        def call(resource, method, params, body=None):
            calls.append(method)
            if method=='append':
                require(pending.exists(),'pending must precede append')
                return response
            if params['range'].endswith('A2:D2'): return {'values':readback}
            return {'values':[t.HEADERS,row]}
        with patch.object(t,'PENDING',pending),patch.object(t,'inspect',return_value=[t.HEADERS]),patch.object(t,'call',side_effect=call):
            rejects('tracker_'+label,lambda:t.append_once(DOI,row,{}))
            require(p.parse_json(pending.read_bytes())['action_outcome']!='confirmed','failure loses marker')
            rejects('no_blind_retry_after_'+label,lambda:t.append_once(DOI,row,{}))
            require(calls.count('append')==1,'blind append retry')
with tempfile.TemporaryDirectory(dir=HERE/'tmp',prefix='edges-') as td:
    pending = Path(td)/'pending.json'
    def lost_response(*args,**kwargs):
        require(pending.exists(),'pending must precede thrown append')
        raise RuntimeError('simulated lost response')
    with patch.object(t,'PENDING',pending),patch.object(t,'inspect',return_value=[t.HEADERS]),patch.object(t,'call',side_effect=lost_response):
        rejects('ambiguous_network_outcome',lambda:t.append_once(DOI,row,{}),(RuntimeError,))
        rejects('no_blind_retry_after_network_outcome',lambda:t.append_once(DOI,row,{}))

original,_ = p.load_snapshot(ROOT/'native'/p.PREFIX)
extracted = HERE/'tmp/extracted'
members = {x.relative_to(extracted).as_posix():x.read_bytes() for x in extracted.rglob('*') if x.is_file()}
paper = {n:members[n] for n in ('gns_generation_counterexample.pdf','gns_generation_counterexample.tex')}
source = members['CURRENT_PRIORITY_AND_STATUS.md']
def archive(modified, special=None):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w') as z:
        for name,data in modified.items():
            if special and name==special:
                info=zipfile.ZipInfo(name)
                info.create_system=3
                info.external_attr=0o120777<<16
                z.writestr(info,data)
            else:z.writestr(name,data)
    return buf.getvalue()
rejects('archive_symlink_member',lambda:p.archive_binding(archive(members,'README.md'),original,paper,source))
bad=copy.copy(members)
del bad['CURRENT_PRIORITY_AND_STATUS.md']
rejects('archive_missing_notice',lambda:p.archive_binding(archive(bad),original,paper,source))
bad=copy.copy(members)
bad['candidate/packet/PROOF.md']+=b'!'
manifest=p.parse_json(bad['PACKAGE_MANIFEST.json'])
for e in manifest['files']:
    if e['path']=='candidate/packet/PROOF.md':e.update(bytes=len(bad[e['path']]),sha256=p.sha(bad[e['path']]))
bad['PACKAGE_MANIFEST.json']=p.json_bytes(manifest)
rejects('archive_rehashed_frozen_proof',lambda:p.archive_binding(archive(bad),original,paper,source))
out={'result':'PASS','independent_edge_checks':len(checks),'checks':checks,'all_service_calls_mocked':True,
     'service_mutations':0,'writes_confined_to_review_folder':True}
(HERE/'OPERATION_EDGE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
