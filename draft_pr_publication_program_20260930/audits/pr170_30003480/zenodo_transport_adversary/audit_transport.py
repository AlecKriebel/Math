"""Offline bounded controls for one exact Zenodo HTML transport allowance.

Run with the pinned Python 3.14.6 stdlib, ordinary and -O. No assertions are
used. Candidate, original kit, and all external inputs are read only.
"""
from pathlib import Path
import argparse
import contextlib
import copy
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import importlib.util
import io
import json
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
ROOT = Path('/Users/alec/Documents/Math')
KIT = ROOT / 'zenodo_deposit_tool/zenodo.py'
GUARD = BASE / 'zenodo_exact_description_guard.py'
FROZEN = BASE / 'publication_package_v2/metadata.json'
DIAGNOSTIC = BASE / 'ZENODO_HTML_REPRESENTATION_DIAGNOSTIC.json'
MANIFEST = BASE / 'zenodo-deposit.v2.json'
GATE = BASE / 'ROOT_PUBLICATION_GATE.json'
TG = BASE / 'ROOT_PUBLICATION_TRANSPORT_GATE.json'
ID = 23318851
ROWS = []
NETWORK_EVENTS = []
STATE_SECRET_EVENTS = []

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def audit_hook(event, args):
    if event.startswith('socket.'):
        NETWORK_EVENTS.append(event)
        raise RuntimeError('Network forbidden by offline audit hook')
    if event == 'open' and isinstance(args[0], (str, bytes)):
        p = str(args[0])
        if '/.secrets/' in p or '/.zenodo-state/' in p:
            STATE_SECRET_EVENTS.append('forbidden_private_open')
            raise RuntimeError('Private credentials/state forbidden by audit hook')

sys.addaudithook(audit_hook)

def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def load(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m

INPUTS = [GUARD, FROZEN, DIAGNOSTIC, KIT, GATE, MANIFEST,
          BASE / 'publication_package_v2/gram_locus_note.pdf',
          BASE / 'publication_package_v2/gram_locus_support.zip',
          ROOT / 'zenodo_deposit_tool/metadata_updates.py', Path(sys.executable)]
PINS = {str(p): pin(p) for p in INPUTS}
INITIAL = {'UTC': datetime.now(timezone.utc).isoformat(), 'inputs': PINS,
           'candidate_transport_gate_present_at_start': TG.exists(),
           'runtime': {'version': sys.version, 'executable': sys.executable,
                       'flags': str(sys.flags)}}
if not (OUT / 'PINNED_INPUTS.json').exists():
    (OUT / 'PINNED_INPUTS.json').write_text(json.dumps(INITIAL, indent=2)+'\n')
else:
    saved = json.loads((OUT / 'PINNED_INPUTS.json').read_text())
    need(saved['inputs'] == PINS, 'Inputs changed from first pinned audit run')

kit = load('independent_original_zenodo', KIT)
guard = load('independent_transport_guard', GUARD)
expected = json.loads(FROZEN.read_text())
remote = json.loads(DIAGNOSTIC.read_text())
gate = json.loads(GATE.read_text())
metadata, files = kit.load_manifest(MANIFEST)
need(metadata == expected, 'Manifest metadata differs from frozen metadata')
need(pin(FROZEN) == gate['files']['metadata.json'], 'Frozen metadata differs from root gate pin')
need(pin(MANIFEST)['sha256'] == gate['deposit_manifest_sha256'], 'Manifest differs from root gate pin')
for n, ident in gate['kit_files'].items():
    need(pin(ROOT/n) == ident, 'Original kit pin mismatch: '+n)
for n in gate['upload_files']:
    need(pin(BASE/'publication_package_v2'/n) == gate['files'][n], 'Upload pin mismatch: '+n)

raw = expected['description']
canonical = raw.replace('n>=3', 'n&gt;=3').replace('n>=4', 'n&gt;=4')
need(raw.count('n>=3') == raw.count('n>=4') == 1, 'Wrong frozen occurrence count')
need(remote['metadata']['description'] == canonical, 'Diagnostic differs from exact canonical transport')
need(remote['id'] == ID and remote['submitted'] is False, 'Diagnostic fixture identity/state mismatch')
need({k: v for k,v in remote['metadata'].items() if k != 'description'} ==
     {k: v for k,v in expected.items() if k != 'description'}, 'Other diagnostic metadata differs')

class Semantics(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.structure = []
        self.text = []
    def handle_starttag(self, tag, attrs):
        self.structure.append(['start',tag,attrs])
    def handle_endtag(self, tag):
        self.structure.append(['end',tag])
    def handle_data(self, data):
        self.text.append(data)
    def handle_comment(self, data):
        self.structure.append(['comment',data])
    def semantic(self, value):
        self.feed(value)
        self.close()
        return {'structure': self.structure, 'text': ''.join(self.text)}

raw_sem = Semantics().semantic(raw)
canon_sem = Semantics().semantic(canonical)
need(raw_sem == canon_sem, 'Exact serialization changed HTML text/structure')
need(raw_sem['structure'] == [['start','p',[]],['end','p']]*3, 'Comparators may occur in unexpected markup')
SEMANTIC = {
    'raw_description_utf8_sha256': hashlib.sha256(raw.encode()).hexdigest(),
    'canonical_description_utf8_sha256': hashlib.sha256(canonical.encode()).hexdigest(),
    'raw_characters':len(raw), 'canonical_characters':len(canonical),
    'net_added_characters':len(canonical)-len(raw),
    'target_occurrences':{'n>=3':raw.count('n>=3'),'n>=4':raw.count('n>=4')},
    'canonical_entities':canonical.count('&gt;'),
    'HTML_structure_and_decoded_text_equal':raw_sem == canon_sem,
    'paragraph_count':3, 'all_paragraph_attributes_empty':True,
    'decoded_text_sha256':hashlib.sha256(raw_sem['text'].encode()).hexdigest(),
}

def evaluate(name, action, should_accept):
    try:
        result = action()
        accepted = True
        error = None
    except Exception as exc:
        accepted = False
        result = None
        error = {'type':type(exc).__name__, 'message':str(exc)}
    row = {'name':name,'expected_accept':should_accept,'accepted':accepted,
           'passed':accepted == should_accept}
    if error:
        row['error'] = error
    if isinstance(result,list):
        row['normalizations'] = result
    ROWS.append(row)
    need(row['passed'], 'Unexpected outcome for '+name)
    return result

def gv(deposit, submitted=expected, wanted_files=files):
    return guard.guarded_verify(kit.verify,deposit,submitted,wanted_files)

exact_raw = copy.deepcopy(remote)
exact_raw['metadata']['description'] = raw
evaluate('original_rejects_observed_two_entity_representation',lambda:kit.verify(remote,expected,files),False)
evaluate('original_accepts_exact_raw_description',lambda:kit.verify(exact_raw,expected,files),True)
evaluate('guard_accepts_exact_raw_description',lambda:gv(exact_raw),True)
allowances = evaluate('guard_accepts_only_exact_known_two_entity_representation',lambda:gv(remote),True)
need(len(allowances)==1 and allowances[0]['field']=='description', 'New path has unexpected allowances')

descriptions = {
    'only_n3_escaped': raw.replace('n>=3','n&gt;=3'),
    'only_n4_escaped': raw.replace('n>=4','n&gt;=4'),
    'n3_double_escaped': canonical.replace('n&gt;=3','n&amp;gt;=3'),
    'both_double_escaped': canonical.replace('&gt;','&amp;gt;'),
    'n3_decimal_entity': canonical.replace('n&gt;=3','n&#62;=3'),
    'both_hexadecimal_entities': canonical.replace('&gt;','&#x3e;'),
    'uppercase_entity': canonical.replace('&gt;','&GT;'),
    'missing_entity_semicolon': canonical.replace('&gt;','&gt'),
    'entire_HTML_escaped': canonical.replace('<','&lt;').replace('>','&gt;'),
    'replace_paragraph_tags': canonical.replace('<p>','<div>').replace('</p>','</div>'),
    'paragraph_class_attribute': canonical.replace('<p>','<p class="x">',1),
    'paragraph_title_attribute': canonical.replace('<p>','<p title="n>=3">',1),
    'insert_comment': canonical.replace('</p>','<!-- extra --></p>',1),
    'insert_script': canonical+'<script>alert(1)</script>',
    'new_inline_markup': canonical.replace('real tensor','<em>real tensor</em>',1),
    'trailing_space':canonical+' ',
    'paragraph_separator_space':canonical.replace('</p><p>','</p> <p>',1),
    'text_edit':canonical.replace('no single','one single',1),
    'n3_changed_to_n2':canonical.replace('n&gt;=3','n&gt;=2'),
    'inequality_reversed':canonical.replace('n&gt;=3','n&lt;=3'),
    'raw_extra_n3':raw+'n>=3',
    'missing_description':None,
    'description_nonstring':{'value':canonical},
}
for name, desc in descriptions.items():
    altered = copy.deepcopy(remote)
    altered['metadata']['description'] = desc
    evaluate('reject_description_'+name,lambda d=altered:gv(d),False)

def remote_metadata_case(name, mutate):
    d = copy.deepcopy(remote)
    mutate(d['metadata'])
    evaluate('reject_remote_metadata_'+name,lambda:gv(d),False)

remote_metadata_case('author_name',lambda m:m['creators'][0].update(name='Different, Author'))
remote_metadata_case('author_orcid',lambda m:m['creators'][0].update(orcid='0000-0000-0000-0000'))
remote_metadata_case('author_affiliation',lambda m:m['creators'][0].update(affiliation=None))
remote_metadata_case('extra_author',lambda m:m['creators'].append({'name':'Extra, Author'}))
remote_metadata_case('extra_author_field',lambda m:m['creators'][0].update(role='editor'))
remote_metadata_case('keyword_edit',lambda m:m['keywords'].__setitem__(0,'edited'))
remote_metadata_case('keyword_reorder',lambda m:m['keywords'].reverse())
remote_metadata_case('extra_keyword',lambda m:m['keywords'].append('extra'))
remote_metadata_case('related_identifier_edit',lambda m:m['related_identifiers'][0].update(identifier='10.0/changed'))
remote_metadata_case('related_relation_edit',lambda m:m['related_identifiers'][0].update(relation='isIdenticalTo'))
remote_metadata_case('related_scheme_edit',lambda m:m['related_identifiers'][0].update(scheme='url'))
remote_metadata_case('related_identifier_reorder',lambda m:m['related_identifiers'].reverse())
remote_metadata_case('extra_related_identifier',lambda m:m['related_identifiers'].append({'identifier':'x','scheme':'url','relation':'references'}))
remote_metadata_case('title_edit',lambda m:m.update(title='Changed title'))
remote_metadata_case('license_edit',lambda m:m.update(license='cc0-1.0'))
remote_metadata_case('missing_version',lambda m:m.pop('version'))
invalid = copy.deepcopy(remote)
invalid['metadata'] = []
evaluate('reject_remote_metadata_nonobject',lambda:gv(invalid),False)

for name, change in [
    ('description',lambda m:m.update(description=canonical)),
    ('title',lambda m:m.update(title='Changed title')),
    ('author',lambda m:m['creators'][0].update(name='Changed')),
    ('keyword',lambda m:m['keywords'].append('extra')),
    ('related_identifier',lambda m:m['related_identifiers'].pop()),
    ('extra_field',lambda m:m.update(extra='new')),
]:
    m = copy.deepcopy(expected)
    change(m)
    evaluate('reject_nonfrozen_submitted_'+name,lambda m=m:gv(remote,m),False)

file_cases = {
    'extra_file': lambda f:f.append({'filename':'extra.txt','filesize':1,'checksum':'0'*32}),
    'missing_file': lambda f:f.pop(),
    'duplicate_filename': lambda f:f.append(copy.deepcopy(f[0])),
    'renamed_pdf': lambda f:f[0].update(filename='other.pdf'),
    'pdf_wrong_checksum':lambda f:f[0].update(checksum='0'*32),
    'zip_wrong_checksum':lambda f:f[1].update(checksum='f'*32),
    'pdf_wrong_size':lambda f:f[0].update(filesize=f[0]['filesize']+1),
    'zip_wrong_size':lambda f:f[1].update(filesize=f[1]['filesize']-1),
    'missing_checksum':lambda f:f[0].pop('checksum'),
    'missing_size':lambda f:f[0].pop('filesize'),
    'nondict_file':lambda f:f.append(None),
}
for name, change in file_cases.items():
    d = copy.deepcopy(remote)
    change(d['files'])
    evaluate('reject_remote_file_'+name,lambda d=d:gv(d),False)
for invalid in (None,{},'files'):
    d = copy.deepcopy(remote)
    d['files'] = invalid
    evaluate('reject_invalid_remote_file_list_'+type(invalid).__name__,lambda d=d:gv(d),False)

# Changed local bytes in owned fixtures, still compared by the original loader.
fixture = OUT/'fixture'
fixture.mkdir(exist_ok=True)
for i, original_file in enumerate(files):
    altered_path = fixture/('altered-'+original_file['name'])
    data = bytearray(original_file['path'].read_bytes())
    data[len(data)//2] ^= 1
    altered_path.write_bytes(data)
    fixture_manifest = fixture/('altered-manifest-'+str(i)+'.json')
    items = [{'path':str(altered_path if j==i else f['path']), 'name':f['name']} for j,f in enumerate(files)]
    fixture_manifest.write_text(json.dumps({'metadata':expected,'files':items}))
    loaded_m, loaded_f = kit.load_manifest(fixture_manifest)
    evaluate('reject_corrupt_local_bytes_'+original_file['name'],lambda m=loaded_m,f=loaded_f:gv(remote,m,f),False)
    altered_path.unlink()
    fixture_manifest.unlink()

# Original validation uses exact builtin ID and submitted-state types.
for name, value in [('other',ID+1),('string',str(ID)),('float',float(ID)),('boolean',True),('none',None)]:
    d = copy.deepcopy(remote)
    d['id'] = value
    evaluate('original_reject_record_id_'+name,lambda d=d:kit.validate_record(d,ID),False)
for name, value in [('string','false'),('int',0),('none',None)]:
    d = copy.deepcopy(remote)
    d['submitted'] = value
    evaluate('original_reject_record_state_'+name,lambda d=d:kit.validate_record(d,ID),False)

# Existing original API representation allowances are preserved, not expanded.
same = copy.deepcopy(remote)
same['metadata']['server_generated_field'] = 'existing original comparator behavior'
evaluate('inherited_allowance_remote_extra_server_field_original',lambda:kit.verify(same,{**expected,'description':canonical},files),True)
evaluate('inherited_allowance_remote_extra_server_field_guard',lambda:gv(same),True)
same = copy.deepcopy(remote)
same['files'].reverse()
same['files'][0]['checksum']='md5:'+same['files'][0]['checksum'].upper()
same['files'][0]['filesize']=str(same['files'][0]['filesize'])
evaluate('inherited_file_order_md5_prefix_case_string_size_original',lambda:kit.verify(same,{**expected,'description':canonical},files),True)
evaluate('inherited_file_order_md5_prefix_case_string_size_guard',lambda:gv(same),True)

class FakeClient:
    def __init__(self, context):
        self.context = context
        self.deposit = copy.deepcopy(context['deposit'])
    def get(self, ident):
        self.context['events'].append({'method':'get','id':ident})
        return copy.deepcopy(self.deposit)
    def publish(self, ident):
        self.context['events'].append({'method':'publish_sentinel','id':ident})
        need(ident==ID,'Synthetic publish target differs')
        self.deposit['submitted'] = True
        return copy.deepcopy(self.deposit)

orig_spec = importlib.util.spec_from_file_location
orig_read_text = Path.read_text
orig_read_bytes = Path.read_bytes

def main_control(name, changes=None, should_accept=False, expect_publish=False):
    c = {'command':'publish','confirm_id':ID, 'manifest':str(MANIFEST),
         'gate':copy.deepcopy(gate),
         'transport_gate':{'status':'EXACT_HTML_DESCRIPTION_TRANSPORT_GUARD_INDEPENDENTLY_VERIFIED','guard_identity':pin(GUARD)},
         'state':{'manifest':str(MANIFEST.resolve()),'environment':'production','id':ID},
         'deposit':copy.deepcopy(remote),'events':[], 'kit_modules':[],
         'manifest_bytes_override':None}
    if changes:
        changes(c)
    synthetic_state = fixture/'synthetic-state.json'
    if c['state'] is not None:
        synthetic_state.write_text(json.dumps(c['state']))
    elif synthetic_state.exists():
        synthetic_state.unlink()
    def fake_read_text(path, *args, **kwargs):
        if path == TG:
            if c['transport_gate'] is None:
                raise FileNotFoundError('Synthetic absent transport gate')
            return json.dumps(c['transport_gate'])
        if path == GATE:
            return json.dumps(c['gate'])
        return orig_read_text(path,*args,**kwargs)
    def fake_read_bytes(path, *args, **kwargs):
        if path == MANIFEST and c['manifest_bytes_override'] is not None:
            return c['manifest_bytes_override']
        return orig_read_bytes(path,*args,**kwargs)
    class OfflineLoader:
        def __init__(self, real):
            self.real = real
        def create_module(self, spec):
            return self.real.create_module(spec)
        def exec_module(self, module):
            self.real.exec_module(module)
            # Original run/local_state/verify code remains untouched. Redirect
            # private state path and replace only external side effects.
            c['kit_modules'].append(module)
            module.state_path=lambda path,environment:synthetic_state
            module.token_for=lambda environment:'OFFLINE_NONCREDENTIAL_SENTINEL'
            module.ZenodoClient=lambda environment,token:FakeClient(c)
            module.save_state=lambda path,value:c['events'].append({'method':'save_state_sentinel'})
            module.doi_status=lambda doi:{'status':'offline_sentinel'}
    def fake_spec(name,path,*args,**kwargs):
        sp = orig_spec(name,path,*args,**kwargs)
        if Path(path)==KIT:
            sp.loader = OfflineLoader(sp.loader)
        return sp
    argv=['guard',c['command'],c['manifest']]
    if c['confirm_id'] is not None:
        argv += ['--confirm-id',str(c['confirm_id'])]
    old_argv = sys.argv
    Path.read_text = fake_read_text
    Path.read_bytes = fake_read_bytes
    importlib.util.spec_from_file_location = fake_spec
    sys.argv = argv
    try:
        output = io.StringIO()
        def invoke():
            with contextlib.redirect_stdout(output):
                guard.main()
            return json.loads(output.getvalue())
        result = evaluate('main_'+name,invoke,should_accept)
        row = ROWS[-1]
        row['side_effect_sentinels']=copy.deepcopy(c['events'])
        sentinels = [e for e in c['events'] if e['method']=='publish_sentinel']
        need(bool(sentinels)==expect_publish,'Unexpected synthetic publication call: '+name)
        need(len(sentinels)<=1,'Repeated publication sentinel: '+name)
        if result:
            row['result_state']=result['state']
            row['result_id']=result['id']
        for m in c['kit_modules']:
            need(m.run.__code__.co_code == kit.run.__code__.co_code, 'Original run code changed in harness')
            need(m.local_state.__code__.co_code == kit.local_state.__code__.co_code, 'Original local_state code changed in harness')
    finally:
        Path.read_text=orig_read_text
        Path.read_bytes=orig_read_bytes
        importlib.util.spec_from_file_location=orig_spec
        sys.argv=old_argv
        if synthetic_state.exists():
            synthetic_state.unlink()

main_control('valid_exact_transport_inspect',lambda c:c.update(command='inspect',confirm_id=None),True,False)
main_control('valid_exact_transport_single_publish_sentinel',should_accept=True,expect_publish=True)
main_control('valid_raw_single_publish_sentinel',lambda c:c['deposit']['metadata'].update(description=raw),True,True)
main_control('missing_transport_gate',lambda c:c.update(transport_gate=None))
main_control('uncleared_transport_gate',lambda c:c['transport_gate'].update(status='PENDING'))
main_control('wrong_guard_identity',lambda c:c['transport_gate']['guard_identity'].update(sha256='0'*64))
main_control('wrong_manifest_path',lambda c:c.update(manifest=str(fixture/'wrong-manifest.json')))
main_control('wrong_manifest_content',lambda c:c.update(manifest_bytes_override=orig_read_bytes(MANIFEST)+b' '))
main_control('wrong_gate_manifest_hash',lambda c:c['gate'].update(deposit_manifest_sha256='0'*64))
main_control('wrong_original_kit_pin',lambda c:c['gate']['kit_files']['zenodo_deposit_tool/zenodo.py'].update(sha256='0'*64))
main_control('absent_state',lambda c:c.update(state=None))
main_control('empty_state',lambda c:c.update(state={}))
main_control('other_state_id',lambda c:c['state'].update(id=ID+1))
main_control('state_string_id',lambda c:c['state'].update(id=str(ID)))
main_control('state_boolean_id',lambda c:c['state'].update(id=True))
main_control('state_wrong_manifest',lambda c:c['state'].update(manifest='different'))
main_control('state_wrong_environment',lambda c:c['state'].update(environment='sandbox'))
main_control('missing_confirm_id',lambda c:c.update(confirm_id=None))
main_control('other_confirm_id',lambda c:c.update(confirm_id=ID+1))
main_control('wrong_remote_id',lambda c:c['deposit'].update(id=ID+1))
main_control('remote_float_id',lambda c:c['deposit'].update(id=float(ID)))
main_control('remote_invalid_state',lambda c:c['deposit'].update(submitted=0))
main_control('partial_escape_prevents_publish',lambda c:c['deposit']['metadata'].update(description=descriptions['only_n3_escaped']))
main_control('description_edit_prevents_publish',lambda c:c['deposit']['metadata'].update(description=descriptions['text_edit']))
main_control('author_edit_prevents_publish',lambda c:c['deposit']['metadata']['creators'][0].update(name='Different'))
main_control('extra_file_prevents_publish',lambda c:c['deposit']['files'].append({'filename':'extra.txt','filesize':1,'checksum':'0'*32}))
main_control('checksum_edit_prevents_publish',lambda c:c['deposit']['files'][0].update(checksum='0'*32))
main_control('valid_already_submitted_no_publish_sentinel',lambda c:c['deposit'].update(submitted=True),True,False)

need(not NETWORK_EVENTS,'Network was attempted')
need(not STATE_SECRET_EVENTS,'Private credentials/state read was attempted')
need({str(p):pin(p) for p in INPUTS} == PINS,'Consumed inputs changed during audit')
need(all(r['passed'] for r in ROWS),'A control failed')
result = {
    'UTC':datetime.now(timezone.utc).isoformat(),
    'scope':'Exact frozen two paragraph-text greater-than serialization allowance; no publication approval',
    'runtime':{'version':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,
               'ignore_environment':sys.flags.ignore_environment,'no_site':sys.flags.no_site,
               'dont_write_bytecode':sys.flags.dont_write_bytecode,'safe_path':sys.flags.safe_path},
    'semantic_HTML_check':SEMANTIC,
    'controls':ROWS,'controls_count':len(ROWS),'all_controls_pass':True,
    'network_attempts':NETWORK_EVENTS,'private_credential_or_state_read_attempts':STATE_SECRET_EVENTS,
    'all_pinned_inputs_unchanged':True,
    'verdict':'PASS_FOR_PRECISELY_THIS_FROZEN_TRANSPORT_ALLOWANCE',
    'completion_percent':100,
}
arg = argparse.ArgumentParser()
arg.add_argument('--output',required=True)
args = arg.parse_args()
out_path=OUT/args.output
need(out_path.parent==OUT,'Output must be a direct owned artifact')
out_path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'controls':len(ROWS),'all_pass':True,'optimize':sys.flags.optimize,'output':str(out_path)}))
