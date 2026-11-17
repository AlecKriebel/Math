"""One bounded passive data/custody read; no producer imports or execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import struct
import traceback
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
P=HERE.parents[1]
PREP=P/'verification/hafnian-retract-production-prepare-sol-20261117'
STAGE=P/'verification/hafnian-retract-stage-corrected-sol-20261117'
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'mode':format(stat.S_IMODE(p.lstat().st_mode),'04o')}
def out(name,obj):
    with (HERE/name).open('xb') as f:f.write(enc(obj))
def snapshot(root):
    files={};dirs={}
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();name='.' if p==root else p.relative_to(root).as_posix()
        if stat.S_ISDIR(st.st_mode):dirs[name]={'mode':format(stat.S_IMODE(st.st_mode),'04o'),'empty':not any(p.iterdir())}
        else:
            assert stat.S_ISREG(st.st_mode),(root,name,'nonregular')
            files[name]=pin(p)
    return {'root':str(root),'files':files,'directories':dirs,'regular_files':len(files),'child_directories':len(dirs)-1}
def authentic(root,manifest,actual):
    names=set()
    for r in manifest['payload_files']:
        n=r['path'];assert n not in names;names.add(n)
        assert actual['files'][n]=={k:r[k] for k in ('bytes','SHA256','mode')},n
    assert names|{'FINAL.json','OWNED_MANIFEST.json'}==set(actual['files'])
    assert actual['regular_files']==manifest.get('regular_files',manifest.get('regular_files_after_terminal_creation'))
    assert actual['child_directories']==manifest['child_directories']
    mdirs={r['path']:{'mode':r['mode'],'empty':r['empty']} for r in manifest['directories']}
    if '.' not in mdirs:mdirs['.']={'mode':manifest['root_mode'],'empty':False}
    assert mdirs==actual['directories']
def json_raw_units(raw):
    body=re.findall(r'<script type="application/ld\+json">(.*?)</script>',raw.decode(),re.S)
    assert len(body)==1
    body=body[0];typed=json.loads(body);items=typed['mainEntity']['itemListElement']
    pos=body.index('[',body.index('"itemListElement"'))+1;units=[];decoder=json.JSONDecoder()
    for item in items:
        while body[pos].isspace() or body[pos]==',':pos+=1
        value,end=decoder.raw_decode(body,pos);assert value==item
        units.append(body[pos:end]);pos=end
    return typed,items,units
def xml_value(n):return [n.tag,dict(n.attrib),n.text,n.tail,[xml_value(c) for c in n]]

try:
    assert not (HERE/'BEFORE.json').exists(),'one audit attempt only'
    before={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PREPARATION':snapshot(PREP),'STAGE':snapshot(STAGE)}
    out('BEFORE.json',before)
    expected={PREP/'release_two.py':'6a831b55fbd1d49196619e047e6461d36c9171da94f5ede8d45cdd8148d5b734',
              PREP/'PLAN.json':'682ae4747c3004aef1b74fb8bce7f43b76984c427353419a7e8c770e941fa2a1',
              STAGE/'FINAL.json':'4282c414493774f4d562af7f6b0364a8f3efb90d026b7116936f17f01ef792e5',
              STAGE/'OWNED_MANIFEST.json':'e2a0e565f7849c11af60c774b1cec4903ceae4a7b22f2ac61dcc3ea0002c6318'}
    for path,h in expected.items():assert pin(path)['SHA256']==h,('protected',str(path))
    prep_final=json.loads((PREP/'FINAL.json').read_text());prep_manifest=json.loads((PREP/'OWNED_MANIFEST.json').read_text())
    stage_final=json.loads((STAGE/'FINAL.json').read_text());stage_manifest=json.loads((STAGE/'OWNED_MANIFEST.json').read_text())
    authentic(PREP,prep_manifest,before['PREPARATION']);authentic(STAGE,stage_manifest,before['STAGE'])
    assert pin(PREP/'OWNED_MANIFEST.json')['SHA256']==prep_final['manifest']['SHA256']
    p=json.loads((PREP/'PLAN.json').read_text());targets=json.loads((PREP/'TARGETS.json').read_text())
    assert targets==json.loads((STAGE/'TARGETS.json').read_text())
    control_pins=[]
    for label,r in p['controls'].items():
        actual=pin(Path(r['path']));assert actual=={k:r[k] for k in actual},label
        control_pins.append({'label':label,'path':r['path'],**actual})
    out('INPUT_PINS.json',{'preparation_FINAL':pin(PREP/'FINAL.json'),'preparation_manifest':pin(PREP/'OWNED_MANIFEST.json'),
        'helper':pin(PREP/'release_two.py'),'PLAN':pin(PREP/'PLAN.json'),'controls':control_pins})
    baseline=json.loads((STAGE/'BASELINE_MANIFEST.json').read_text())
    candidate=json.loads((STAGE/'CANDIDATE_MANIFEST.json').read_text())
    changes={n for n in set(baseline['files'])|set(candidate['files']) if baseline['files'].get(n)!=candidate['files'].get(n)}
    adds=set(candidate['files'])-set(baseline['files']);mods={n for n in changes if n in baseline['files']}
    assert adds==set(targets['additions_public_relative']) and mods==set(targets['modifications_public_relative'])
    assert {'public/'+n for n in changes}==set(p['scope_paths']) and len(adds)==9 and len(mods)==2
    dirs=set(candidate['directories'])-set(baseline['directories'])
    assert dirs==set(targets['new_directories_public_relative']) and len(dirs)==4
    assert all(candidate['directories'][n]==v for n,v in baseline['directories'].items())
    agg=json.loads((STAGE/'AGGREGATE_FIDELITY.json').read_text());aggregate=[]
    originals=['ORIGINAL_RESEARCH_INDEX.html','ORIGINAL_RESEARCH_SITEMAP.xml']
    outputs=['research/index.html','research/sitemap.xml']
    pairs=[]
    for original,name,spans in zip(originals,outputs,[agg['index_spans'],agg['XML_spans']]):
        old=(STAGE/original).read_bytes();new=(STAGE/'candidate-public'/name).read_bytes();pairs.append((old,new))
        pos=0;offset=0;parts=[];reverse=[]
        for r in spans:
            a,b=r['start_byte'],r['end_byte'];left=r['old_UTF8'].encode();right=r['new_UTF8'].encode()
            assert pos<=a<=b<=len(old) and old[a:b]==left
            parts.extend([old[pos:a],right]);reverse.append((a+offset,a+offset+len(right),left));offset+=len(right)-len(left);pos=b
        parts.append(old[pos:]);assert b''.join(parts)==new
        restored=new
        for a,b,left in reversed(reverse):restored=restored[:a]+left+restored[b:]
        assert restored==old
        aggregate.append({'original':original,'candidate':name,'whole_forward_reverse':True,'old':{'bytes':len(old),'SHA256':sha(old)},'new':{'bytes':len(new),'SHA256':sha(new)}})
    oi,ni=pairs[0];ot,old_items,old_raw=json_raw_units(oi);nt,new_items,new_raw=json_raw_units(ni)
    old_li=re.findall(r'<li\b[^>]*>.*?</li>',re.search(r'<ul>(.*?)</ul>',oi.decode(),re.S)[1],re.S)
    new_li=re.findall(r'<li\b[^>]*>.*?</li>',re.search(r'<ul>(.*?)</ul>',ni.decode(),re.S)[1],re.S)
    assert len(old_items)==len(old_raw)==len(old_li)==128 and len(new_items)==len(new_raw)==len(new_li)==130
    assert old_raw==new_raw[:128] and old_items==new_items[:128] and old_li==new_li[:128]
    assert new_items[128:]==agg['new_typed_units'] and new_li[128:]==agg['new_visible_units']
    ox,nx=pairs[1];on=re.findall(rb'<url>.*?</url>',ox,re.S);nn=re.findall(rb'<url>.*?</url>',nx,re.S)
    assert len(on)==129 and len(nn)==131 and on==nn[:129]
    assert [xml_value(n) for n in ET.fromstring(ox)]==[xml_value(n) for n in list(ET.fromstring(nx))[:129]]
    out('STATIC_DATA_BINDING.json',{'targets':sorted(changes),'additions':9,'modifications':2,'new_directories':sorted(dirs),
        'untargeted_old_files_exact':len(baseline['files'])-2,'old_directories_exact':len(baseline['directories'])-1,
        'stage_actual_files':before['STAGE']['regular_files'],'stage_actual_childdirs':before['STAGE']['child_directories'],
        'stage_manifest_directory_rows_including_dot':len(stage_manifest['directories']),
        'stage_manifest_payload_files':len(stage_manifest['payload_files']),'exact_terminal_pair_included':True,
        'old128_raw_JSON_typed_HTML_exact':True,'old129_raw_and_full_parsed_XML_exact':True,'aggregate_reversal':aggregate,
        'old_failed_history':stage_final['corrected_continuation_history'],'controls_complete_match':True})
    # Necessary passive native Git-index read only; no Git command/object/helper execution.
    ip=Path(p['website'])/'.git/index';raw=ip.read_bytes();native_before=pin(ip)
    native_match=native_before=={k:p['website_index'][k] for k in native_before}
    assert raw[:4]==b'DIRC' and struct.unpack('>I',raw[4:8])[0]==2 and hashlib.sha1(raw[:-20]).digest()==raw[-20:]
    total=struct.unpack('>I',raw[8:12])[0];pos=12;records={};previous=None
    for _ in range(total):
        start=pos;flags=struct.unpack('>H',raw[start+60:start+62])[0];end=raw.index(b'\0',start+62,len(raw)-20);name=raw[start+62:end]
        pos=start+((end+1-start+7)//8)*8
        assert name and (previous is None or previous<name) and not any(raw[end+1:pos]) and not flags&0x7000
        records[name]=raw[start:pos];previous=name
    ext=raw[pos:-20];assert ext[:4]==b'TREE' and struct.unpack('>I',ext[4:8])[0]==len(ext)-8
    payload=ext[8:];cursor=0;nodes=[]
    def cached(parent,root=False):
        global cursor
        end=payload.index(b'\0',cursor);local=payload[cursor:end];line=payload.index(b'\n',end+1)
        count,children=map(int,payload[end+1:line].split());cursor=line+1
        name=b'' if root else parent+(b'/' if parent else b'')+local
        oid=None
        if count>=0:oid=payload[cursor:cursor+20].hex();cursor+=20
        nodes.append({'path':name.decode(),'entries':count,'children':children,'OID':oid})
        for _ in range(children):cached(name)
    cached(b'',True);assert cursor==len(payload)
    invalid=sorted(n['path'] for n in nodes if n['entries']==-1)
    assert invalid==sorted(p['baseline_invalid_TREE_paths'])
    chosen={s.encode() for s in p['scope_paths']};untargeted=[r for n,r in sorted(records.items()) if n not in chosen]
    out('NATIVE_FORMAT_OBSERVATION.json',{'read_only_native_raw_index':True,'Git_commands':0,'whole_index':native_before,
        'matches_PLAN_current_index':native_match,'records':len(records),'protected_untargeted_records':len(untargeted),
        'protected_whole_raw_concatenation':{'bytes':sum(map(len,untargeted)),'SHA256':sha(b''.join(untargeted))},
        'TREE_extension':{'bytes':len(ext),'SHA256':sha(ext)},'TREE_payload':{'bytes':len(payload),'SHA256':sha(payload)},
        'derived_TREE_nodes':len(nodes),'derived_valid_TREE_nodes':sum(n['entries']>=0 for n in nodes),'invalid_paths_no_OID':invalid,
        'all_TREE_node_records':nodes,'current_index_after_read_exact':pin(ip)==native_before,
        'scope':'Existing data formats only; no helper execution, successor construction, Git tree-object command or runtime semantic certificate.'})
    ignore=(P/'.gitignore').read_text().splitlines();effective=[s for s in ignore if s.strip() and not s.lstrip().startswith('#')]
    out('PREREQUISITES_OBSERVED.json',{'runtime_exists':os.path.lexists(Path(p['runtime_root'])),
        'runtime_ignore_final_literal_present':bool(effective and effective[-1]=='/verification/hafnian-retract-runtime-sol-20261117/'),
        'verification_nested_ignore_exists':os.path.lexists(P/'verification/.gitignore'),
        'no_effective_Git_ignore_engine_check_performed':True,'no_fresh_hosting_observation':True,
        'root_reported_hosting_version':p['root_reported_prior_live_hosting_version'],
        'authority_paths_existing':{k:os.path.lexists(Path(v)) for k,v in p['authority_paths'].items()},
        'future_root_authority_and_stage_helper_adoptions_are_separate':True})
    after={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PREPARATION':snapshot(PREP),'STAGE':snapshot(STAGE)}
    out('AFTER.json',after)
    assert before['PREPARATION']==after['PREPARATION'] and before['STAGE']==after['STAGE']
    out('READER_RECEIPT.json',{'UTC':after['UTC'],'reader':pin(Path(__file__)),'full_helper_and_PLAN_read_before_reader':True,
        'reader_complete_personally_read_before_execution':True,'reader_attempts':1,'helper_or_producer_executions':0,
        'imports_AST_compile_tests_of_producer':0,'Git_commands':0,'network_calls':0,'W_mutations':0,
        'preparation_before_after_exact':True,'stage_before_after_exact':True})
    print(json.dumps({'passive_read_complete':True,'preparation':[before['PREPARATION']['regular_files'],before['PREPARATION']['child_directories']],
        'stage':[before['STAGE']['regular_files'],before['STAGE']['child_directories']],'before_after_exact':True,
        'raw_index_records':len(records),'TREE_nodes':len(nodes),'TREE_valid_nodes':sum(n['entries']>=0 for n in nodes),
        'runtime_ignore_prerequisite_applied':bool(effective and effective[-1]=='/verification/hafnian-retract-runtime-sol-20261117/')}))
except Exception:
    with (HERE/'LITERAL_FAILURE.txt').open('x') as f:f.write(traceback.format_exc())
    raise
