"""One passive representation diagnosis; no producer/source/helper imports or runs.
Reads explicit frozen local data and writes two guard files only in this lane.
"""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import html
import json
import os
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P/'verification'
STAGE = V/'hafnian-retract-stage-sol-20261117'
BIND = V/'hafnian-retract-stage-initial-bindings-sol-20261117'
OWN = V/'hafnian-retract-stage-failure-diagnosis-sol-20261117'
M = Path('/Users/alec/Documents/Math')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
EXPECTED = {
    STAGE/'build_private.py':'f5f0a6b84c69996194c8492dd3288a8b16893a7cbc4eac5f8f940452e583b700',
    STAGE/'PLAN.md':'7b3901a53b3aefec1a7e3504a86c062944e9791b1a1aea6ea592962b62128c0d',
    STAGE/'BUILD.stderr.txt':'2dda4324e50bf4997c0c45c49add0c751c404cf61b91d347f67242be6d75de78',
    STAGE/'GUARDS_BEFORE.json':'bec295cc87b3d65f0bbd65c741b8893528db093771d2790a181fa07c84871982',
    STAGE/'GUARDS_AFTER.json':'bec295cc87b3d65f0bbd65c741b8893528db093771d2790a181fa07c84871982',
    BIND/'INPUT_BINDINGS.json':'c7ddeb3e335b317bba3864912807083fe4df423f0392be004de6df376c1b8a40',
}

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(rows):
    result = {}
    for key,value in rows:
        assert key not in result, ('duplicate JSON key',key)
        result[key] = value
    return result

def load(path):
    return json.loads(path.read_bytes().decode('utf-8'),object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def pin(path):
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    data = path.read_bytes()
    return {'bytes':len(data),'SHA256':sha(data),'mode':format(stat.S_IMODE(info.st_mode),'04o')}

def census(root):
    assert stat.S_ISDIR(root.lstat().st_mode)
    files,dirs = {},{}
    for base,ds,fs in os.walk(root,followlinks=False):
        base = Path(base); ds.sort(); fs.sort()
        rel = base.relative_to(root).as_posix()
        assert all(not (base/n).is_symlink() for n in ds+fs)
        dirs[rel] = {'mode':format(stat.S_IMODE(base.lstat().st_mode),'04o'),'empty':not ds and not fs}
        for n in fs:
            path = base/n
            files[path.relative_to(root).as_posix()] = pin(path)
    assert '.' in dirs and not set(files)&set(dirs)
    for rel in list(files)+[x for x in dirs if x != '.']:
        assert Path(rel).parent.as_posix() in dirs
    return {'root':str(root),'files':files,'directories':dirs,
            'regular_files':len(files),'child_directories':len(dirs)-1}

def native(repo):
    g = repo/'.git'
    head = (g/'HEAD').read_text()
    assert re.fullmatch(r'ref: refs/heads/[^\n]+\n',head)
    ref = head.removeprefix('ref: ').strip()
    lines = [s for s in (g/'packed-refs').read_text().splitlines(keepends=True)
             if re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?',s)]
    assert len({s.split()[1] for s in lines}) == len(lines)
    packed = [s.split()[0] for s in lines if s.split()[1] == ref]
    resolved = (g/ref).read_text().strip() if (g/ref).exists() else packed[0]
    assert re.fullmatch('[0-9a-f]{40}',resolved)
    return {name:pin(g/name) for name in ('HEAD','index','config')} | {
        'HEAD_text':head,'local_loose_heads':census(g/'refs/heads'),
        'packed_local_heads':{'file_mode':format(stat.S_IMODE((g/'packed-refs').stat().st_mode),'04o'),
                              'raw_lines':lines},'resolved_native_HEAD':resolved}

def capture(template):
    assert set(template) == {'roots','controls','public','native_M','native_W','binding_lane','stage_control_pins'}
    return {'protected':{
        'roots':{r:census(Path(r)) for r in template['roots']},
        'controls':{r:pin(Path(r)) for r in template['controls']},
        'public':census(W/'public'),'native_M':native(M),'native_W':native(W),
        'binding_lane':census(BIND),
        'stage_control_pins':{r:pin(Path(r)) for r in template['stage_control_pins']}},
        'producer_whole_packet':census(STAGE)}

def save_guard(name,value):
    assert name in ('GUARDS_BEFORE.json','GUARDS_AFTER.json')
    with (OWN/name).open('x',encoding='utf-8') as f:
        f.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def one(pattern,data):
    found = list(re.finditer(pattern,data,re.S))
    assert len(found) == 1
    return found[0]

class Metadata(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.dc = []
        self.feed(text); self.close()
    def handle_starttag(self,tag,attrs):
        assert len(attrs) == len({k for k,v in attrs})
        a = dict(attrs)
        if tag == 'meta' and a.get('name') == 'DC.description':
            self.dc.append(a['content'])

started = utc()
for path,digest in EXPECTED.items():
    assert pin(path)['SHA256'] == digest, str(path)
template = load(STAGE/'GUARDS_BEFORE.json')
assert template == load(STAGE/'GUARDS_AFTER.json')
before = capture(template)
save_guard('GUARDS_BEFORE.json',before)
try:
    assert before['protected'] == template, 'Fresh protected data differs from frozen producer guards'
    binding = load(BIND/'INPUT_BINDINGS.json')
    assert binding['schema'] == 'independent-hafnian-retract-stage-INITIAL-binding-continuation-inputs-v1'
    assert binding['status'] == 'PASS_INPUT_BINDINGS_ONLY'
    cases = []
    for accepted in binding['pages']:
        family = accepted['family']
        writer = V/(family+'-editorial-sol-20261117')
        article = (writer/'article.html').read_bytes()
        head = (writer/'head.html').read_bytes(); main = (writer/'main.html').read_bytes()
        model = load(writer/'page-model.json')
        assert pin(writer/'article.html') == accepted['article']
        assert pin(writer/'head.html') == accepted['head']
        assert pin(writer/'main.html') == accepted['MAIN']
        assert pin(writer/'citation.bib') == accepted['Bib']
        assert article.count(b'<body>') == article.count(b'</body>') == 1
        binding_body = one(rb'(<body>.*</body>)',article)
        producer_body = one(rb'(<body>.*?</body>\n)',article)
        a,b = binding_body[1],producer_body[1]
        assert b == a+b'\n', 'Unexpected BODY extent difference'
        assert len(a) == accepted['BODY']['bytes'] and sha(a) == accepted['BODY']['SHA256']
        assert one(rb'(<head>.*?</head>\n)',article)[1] == head
        assert one(rb'(<main id="main">.*?</main>\n)',article)[1] == main
        scholarly = json.loads(one(rb'<script type="application/ld\+json">(.*?)</script>',head)[1].decode(),object_pairs_hook=pairs)
        assert scholarly == accepted['schema_object'] and scholarly['@type'] == 'ScholarlyArticle'
        visible = html.unescape(one(r'<p id="abstract-text">(.*?)</p>',main.decode())[1])
        abstracts_equal = model['abstract'] == accepted['abstract'] == scholarly['abstract'] == visible
        assert abstracts_equal and Metadata(head.decode()).dc == [model['abstract']]
        cases.append({'family':family,'record':model['record_id'],'article':pin(writer/'article.html'),
            'HEAD':pin(writer/'head.html'),'MAIN':pin(writer/'main.html'),'model':pin(writer/'page-model.json'),
            'accepted_BODY_descriptor':accepted['BODY'],
            'binding_span':{'regex':'<body>.*</body>','start':binding_body.start(1),'end':binding_body.end(1),
                'bytes':len(a),'SHA256':sha(a),'tail_hex':a[-32:].hex()},
            'producer_span':{'regex':'(<body>.*?</body>\\n)','start':producer_body.start(1),'end':producer_body.end(1),
                'bytes':len(b),'SHA256':sha(b),'tail_hex':b[-33:].hex()},
            'exact_span_delta':{'bytes':1,'hex':'0a','meaning':'LF after closing BODY tag, outside accepted binding span',
                'producer_equals_binding_plus_one_LF':True},
            'independent_line514_operand_values':{'length_equal':len(b)==accepted['BODY']['bytes'],
                'hash_equal':sha(b)==accepted['BODY']['SHA256'],'model_abstract_equal':model['abstract']==accepted['abstract']},
            'original_runtime_short_circuit':'First length operand false; hash and abstract operands not reached in the original failed producer iteration.',
            'all_abstract_surfaces_equal':True,'whole_HEAD_MAIN_assembly_exact':True,
            'accepted_abstract':accepted['abstract'],'head_shape':'wrapped_single_ScholarlyArticle',
            'native_encoding_order':[x['name'] for x in scholarly['encoding']]})
    baseline,candidate = census(STAGE/'baseline-public'),census(STAGE/'candidate-public')
    for snap in (baseline,candidate):
        assert all(snap[k] == template['public'][k] for k in ('files','directories','regular_files','child_directories'))
    absent = binding['new_public_relative_leaves']+binding['new_public_relative_directories']
    assert len(absent) == 13
    assert all(not (STAGE/'candidate-public'/r).exists() and not (W/'public'/r).exists() for r in absent)
    for name in ('FINAL.json','OWNED_MANIFEST.json','HEAD_ACTIVATION.json','PROJECTION.json'):
        assert not (STAGE/name).exists()
    execution = load(STAGE/'BUILD_EXECUTION.json')
    assert execution['invocations'] == 1 and execution['exit_code'] == 1 and execution['error'] == 'Accepted whole BODY/abstract'
    assert execution['stdout'] == pin(STAGE/'BUILD.stdout.txt') and execution['stderr'] == pin(STAGE/'BUILD.stderr.txt')
    out = {'schema':'independent-hafnian-retract-stage-representation-diagnosis-v1',
        'status':'EXACT_REPRESENTATION_MISMATCH_NO_ACCEPTED_CONTENT_DEFECT_ESTABLISHED',
        'UTC_start':started,'cases':cases,'actual_failed_iteration':'hafnian',
        'second_case':'Independently measured counterfactual under the same comparison, not a second producer execution/failure.',
        'frozen_producer_pins':{str(p):pin(p) for p in EXPECTED},'literal_producer_execution':execution,
        'baseline_and_retained_workbench_extents':[[baseline['regular_files'],baseline['child_directories']],
                                                   [candidate['regular_files'],candidate['child_directories']]],
        'both_complete_clones_exact_to_W_public':True,'all9leaf4dir_absences':True,
        'no_HEAD_activation_or_new_targets_reached':True,'no_terminal_FINAL_manifest_created':True,
        'old_INITIAL14_bindings13_and28contract_unchanged':True,
        'classification':'The preservation requirement is valid. Comparing two distinct BODY extents is an invalid implementation criterion; accepted article/model/HEAD/MAIN/abstract bytes are unchanged.',
        'proposed_code_edits':False,'producer_source_helper_execution_import_AST_compile_test':False,
        'W_Git_network_Sheet_action_otherpacket_mutation':False,'future_producer_GO':False}
finally:
    after = capture(template)
    save_guard('GUARDS_AFTER.json',after)
    assert after == before, 'Whole diagnostic protected state changed'
out['UTC_end'] = utc(); out['whole_guards_before_after_equal'] = True
print(json.dumps(out,indent=2,ensure_ascii=False))
