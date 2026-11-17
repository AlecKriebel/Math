"""One passive fixed-artifact stage audit; standard-library data parsing only.
No producer/source/helper imports or runs, subprocess, Git, network or external writes.
Only two exclusive guard JSON destinations in this owned audit lane are written.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import copy
import hashlib
import html
import json
import os
import re
import stat
import struct
import xml.etree.ElementTree as ET
import zlib

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P/'verification'
S = V/'hafnian-retract-stage-corrected-sol-20261117'
A = V/'hafnian-retract-stage-corrected-audit-sol-20261117'
B = V/'hafnian-retract-stage-initial-bindings-sol-20261117'
I = V/'hafnian-retract-stage-initial-sol-20261117'
D = V/'hafnian-retract-stage-failure-diagnosis-sol-20261117'
F = V/'hafnian-retract-stage-sol-20261117'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
M = Path('/Users/alec/Documents/Math')
BASE, CAND = S/'baseline-public', S/'candidate-public'
PINS = {
    S/'FINAL.json':'4282c414493774f4d562af7f6b0364a8f3efb90d026b7116936f17f01ef792e5',
    S/'OWNED_MANIFEST.json':'e2a0e565f7849c11af60c774b1cec4903ceae4a7b22f2ac61dcc3ea0002c6318',
    S/'build_private.py':'bbe547b27bd2c5fa32875d6717078b70c595ed3aba5cd6815a0b6b633d1c306b',
    S/'PRODUCER.diff':'232f3b3cdc5f2160088df38ad9eba8d652f8224663a2290a82c9c13c1f7f6f5b',
    S/'GUARDS_BEFORE.json':'9c883e92611eed08cea271bcb3a3e957ce20bcda3a495b3859434a22ffdad145',
    S/'GUARDS_AFTER.json':'9c883e92611eed08cea271bcb3a3e957ce20bcda3a495b3859434a22ffdad145',
    I/'CONTRACT.json':'f88a8adef0a2960ea6a3a91afa6d64f88dde8ecfe7ed8cabbbadbce562bea49c',
    B/'INPUT_BINDINGS.json':'c7ddeb3e335b317bba3864912807083fe4df423f0392be004de6df376c1b8a40',
}
RULES = [
    (V/'hafnian-editorial-sol-20261117','MANIFEST.json','FINAL.json','finite-private-editorial-manifest-v1','payload_files'),
    (V/'hafnian-fact-sol-20261117','MANIFEST.json','FINAL.json','finite-private-fact-review-manifest-v1','payload_files'),
    (V/'hafnian-legacy-sol-20261117','FINAL_MANIFEST.json','FINAL_SEAL.json','hafnian-legacy-finite-final-manifest-v1','entries'),
    (V/'complex-retract-editorial-sol-20261117','MANIFEST.json','FINAL.json','finite-private-editorial-manifest-v1','payload_files'),
    (V/'complex-retract-fact-sol-20261117','MANIFEST.json','FINAL.json','finite-private-fact-review-manifest-v1','payload_files'),
    (V/'complex-retract-legacy-sol-20261117','OWNED_MANIFEST.json','FINAL.json','finite-complex-retract-legacy-correspondence-manifest-v1','files'),
    (P/'papers/23205294/sources','SOURCE_MANIFEST.json','SOURCE_FINAL.json','finite-source-manifest-v1','files'),
    (P/'papers/23203270/sources','SOURCE_MANIFEST.json','SOURCE_FINAL.json','source-custody-finite-manifest-v1','entries'),
    (I,'OWNED_MANIFEST.json','FINAL.json','finite-hafnian-retract-stage-INITIAL-manifest-v1','payload_files'),
    (B,'OWNED_MANIFEST.json','FINAL.json','finite-hafnian-retract-stage-INITIAL-bindings-manifest-v1','payload_files'),
    (D,'OWNED_MANIFEST.json','FINAL.json','finite-hafnian-retract-stage-failure-diagnostic-manifest-v1','payload_files'),
]

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def pairs(rows):
    d = {}
    for k,v in rows:
        assert k not in d, ('duplicate JSON key',k)
        d[k] = v
    return d

def loads(text):
    return json.loads(text,object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def readj(path):
    return loads(path.read_bytes().decode('utf-8'))

def mode(value):
    if type(value) is str:
        assert re.fullmatch(r'(?:0o)?[0-7]{3,4}',value)
        value = int(value.removeprefix('0o'),8)
    assert type(value) is int and 0 <= value <= 0o7777
    return format(value,'04o')

def pathcheck(value,root=False):
    assert type(value) is str and value and '\\' not in value and '\x00' not in value
    if value == '.' and root:
        return
    assert not value.startswith('/') and all(x not in ('','.','..') for x in value.split('/'))
    assert PurePosixPath(value).as_posix() == value

def pin(path):
    st = path.lstat(); assert stat.S_ISREG(st.st_mode),str(path)
    data = path.read_bytes()
    return {'bytes':len(data),'SHA256':sha(data),'mode':mode(stat.S_IMODE(st.st_mode))}

def validate(s):
    assert type(s) is dict and set(s) == {'root','files','directories','regular_files','child_directories'}
    assert type(s['root']) is str and Path(s['root']).is_absolute()
    fs,ds = s['files'],s['directories']
    assert type(fs) is dict and type(ds) is dict and '.' in ds and not set(fs)&set(ds)
    parents = set()
    for r,x in fs.items():
        pathcheck(r); assert set(x) == {'bytes','SHA256','mode'}
        assert type(x['bytes']) is int and x['bytes'] >= 0
        assert type(x['SHA256']) is str and re.fullmatch('[0-9a-f]{64}',x['SHA256'])
        assert type(x['mode']) is str and re.fullmatch('0[0-7]{3}',x['mode'])
        parents.add(PurePosixPath(r).parent.as_posix())
    for r,x in ds.items():
        pathcheck(r,True); assert set(x) == {'mode','empty'} and type(x['empty']) is bool
        assert type(x['mode']) is str and re.fullmatch('0[0-7]{3}',x['mode'])
        if r != '.': parents.add(PurePosixPath(r).parent.as_posix())
    assert parents <= set(ds)
    assert all(x['empty'] == (r not in parents) for r,x in ds.items())
    assert type(s['regular_files']) is int and s['regular_files'] == len(fs)
    assert type(s['child_directories']) is int and s['child_directories'] == len(ds)-1

def census(root):
    assert stat.S_ISDIR(root.lstat().st_mode)
    fs,ds = {},{}
    for base,dirs,files in os.walk(root,followlinks=False):
        base = Path(base); dirs.sort(); files.sort()
        assert all(not (base/n).is_symlink() for n in dirs+files)
        ds[base.relative_to(root).as_posix()] = {'mode':mode(stat.S_IMODE(base.lstat().st_mode)),
                                               'empty':not dirs and not files}
        for n in files: fs[(base/n).relative_to(root).as_posix()] = pin(base/n)
    s = {'root':str(root),'files':fs,'directories':ds,'regular_files':len(fs),'child_directories':len(ds)-1}
    validate(s); return s

def same_snapshot(x,y,identity=True):
    validate(x); validate(y)
    assert x['files'] == y['files'] and x['directories'] == y['directories']
    assert x['regular_files'] == y['regular_files'] and x['child_directories'] == y['child_directories']
    assert not identity or x['root'] == y['root']

def native(repo):
    g = repo/'.git'; head = (g/'HEAD').read_text()
    assert re.fullmatch(r'ref: refs/heads/[^\n]+\n',head)
    ref = head.removeprefix('ref: ').strip()
    local = [x for x in (g/'packed-refs').read_text().splitlines(keepends=True)
             if re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?',x)]
    assert len({x.split()[1] for x in local}) == len(local)
    vals = [x.split()[0] for x in local if x.split()[1] == ref]
    oid = (g/ref).read_text().strip() if (g/ref).exists() else vals[0]
    assert re.fullmatch('[0-9a-f]{40}',oid)
    return {n:pin(g/n) for n in ('HEAD','index','config')} | {'HEAD_text':head,
        'local_loose_heads':census(g/'refs/heads'),'packed_local_heads':{
            'file_mode':mode(stat.S_IMODE((g/'packed-refs').stat().st_mode)),'raw_lines':local},
        'resolved_native_HEAD':oid}

def capture(t):
    assert set(t) == {'roots','controls','public','native_M','native_W','old_failed_lane',
                      'frozen_diagnostic_lane','binding_lane','stage_control_pins'}
    protected = {'roots':{r:census(Path(r)) for r in t['roots']},
        'controls':{r:pin(Path(r)) for r in t['controls']},'public':census(W/'public'),
        'native_M':native(M),'native_W':native(W),'old_failed_lane':census(F),
        'frozen_diagnostic_lane':census(D),'binding_lane':census(B),
        'stage_control_pins':{r:pin(Path(r)) for r in t['stage_control_pins']}}
    return {'protected':protected,'whole_corrected_stage':census(S)}

def save_guard(name,value):
    assert name in ('GUARDS_BEFORE.json','GUARDS_AFTER.json')
    with (A/name).open('x',encoding='utf-8') as f:
        f.write(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def input_manifest(root,s,manifest,terminal,schema,key,external):
    assert pin(root/manifest) == external['manifest'] and pin(root/terminal) == external['terminal']
    d = readj(root/manifest); assert d['schema'] == schema
    assert [k for k in ('files','payload_files','entries') if k in d] == [key]
    exclusion_keys=[k for k in ('exact_terminal_exclusions','excluded_control_files','exact_already_created_terminal_recursive_hash_exclusions') if k in d]
    assert len(exclusion_keys)==1 and type(d[exclusion_keys[0]]) is list and len(d[exclusion_keys[0]])==2
    want={str(root/manifest),str(root/terminal)} if exclusion_keys[0]=='exact_already_created_terminal_recursive_hash_exclusions' else {manifest,terminal}
    assert set(d[exclusion_keys[0]])==want
    rows = d[key]; assert type(rows) is list
    seen,dirs,controls = set(),set(),set()
    for x in rows:
        assert type(x) is dict; r = x['path']; pathcheck(r,key=='entries')
        assert r not in seen|dirs
        if key == 'entries' and x['kind'] == 'directory':
            assert set(x) == {'path','kind','mode_octal','empty'} and type(x['empty']) is bool
            assert s['directories'][r] == {'mode':mode(x['mode_octal']),'empty':x['empty']}
            dirs.add(r); continue
        assert key != 'entries' or x['kind'] == 'file'
        seen.add(r); actual = s['files'][r]
        assert actual['mode'] == mode(x['mode_octal'] if key=='entries' else x['mode'])
        if x.get('terminal_control') is True:
            assert root == V/'complex-retract-legacy-sol-20261117' and r in (manifest,terminal)
            assert set(x) == {'path','mode','terminal_control'}
            assert actual == external['manifest' if r==manifest else 'terminal']
            controls.add(r); continue
        needed = {'path','kind','mode_octal','bytes','sha256','md5'} if key=='entries' else {'path','bytes','SHA256','mode'}
        assert needed <= set(x) <= needed|({'git_blob_sha1'} if key=='entries' else {'MD5'})
        assert type(x['bytes']) is int and x['bytes'] >= 0
        digest = x['sha256'] if key=='entries' else x['SHA256']
        assert type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest)
        assert (actual['bytes'],actual['SHA256']) == (x['bytes'],digest)
        data = (root/r).read_bytes()
        if 'md5' in x or 'MD5' in x: assert hashlib.md5(data).hexdigest() == x.get('md5',x.get('MD5'))
        if 'git_blob_sha1' in x:
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\x00'+data).hexdigest() == x['git_blob_sha1']
    if key != 'entries':
        assert s['directories']['.']['mode'] == mode(d['root_mode']); dirs.add('.')
        assert type(d['directories']) is list
        for x in d['directories']:
            assert set(x) in ({'path','mode'},{'path','mode','empty'})
            r = x['path']; pathcheck(r); assert r not in seen|dirs
            assert s['directories'][r]['mode'] == mode(x['mode'])
            if 'empty' in x: assert type(x['empty']) is bool and x['empty'] == s['directories'][r]['empty']
            dirs.add(r)
    assert dirs == set(s['directories'])
    assert seen == set(s['files'])-(set() if controls else {manifest,terminal})
    assert not controls or controls == {manifest,terminal}
    if 'counts' in d:
        assert type(d['counts']['payload_regular_files']) is int and d['counts']['payload_regular_files']==len(seen)
        assert type(d['counts']['directories_including_root']) is int and d['counts']['directories_including_root']==len(dirs)
    for k,n in (('file_count',len(seen)),('directory_count',len(dirs)),('regular_files',s['regular_files']),('child_directories',s['child_directories']),('regular_files_after_terminal_creation',s['regular_files'])):
        if k in d: assert type(d[k]) is int and d[k]==n
    return {'root':str(root),'schema':schema,'whole_namespace_exact':True,'terminal_control_rows':sorted(controls)}

def stage_manifest(s):
    d = readj(S/'OWNED_MANIFEST.json')
    assert d['schema'] == 'finite-hafnian-retract-private-stage-manifest-v1'
    assert d['root'] == str(S) and d['root_mode'] == s['directories']['.']['mode'] == '0755'
    assert (d['regular_files'],d['child_directories']) == (1598,760)
    assert set(d['exact_already_created_terminal_recursive_hash_exclusions']) == {str(S/'FINAL.json'),str(S/'OWNED_MANIFEST.json')}
    assert d['other_exclusions'] == [] and d['terminal_modes'] == {'FINAL.json':'0644','OWNED_MANIFEST.json':'0644'}
    seen,dirs = set(),set()
    for x in d['payload_files']:
        assert set(x) == {'path','bytes','SHA256','mode','hidden','empty'}
        assert type(x['bytes']) is int and x['bytes']>=0 and type(x['SHA256']) is str and re.fullmatch('[0-9a-f]{64}',x['SHA256'])
        assert type(x['mode']) is str and re.fullmatch('0[0-7]{3}',x['mode'])
        r=x['path']; pathcheck(r); assert r not in seen; seen.add(r)
        assert {k:x[k] for k in ('bytes','SHA256','mode')} == s['files'][r]
        assert type(x['hidden']) is bool and x['hidden'] == any(p.startswith('.') for p in Path(r).parts)
        assert type(x['empty']) is bool and x['empty'] == (x['bytes']==0)
    for x in d['directories']:
        assert set(x) == {'path','mode','empty','hidden'}
        assert type(x['empty']) is bool and type(x['mode']) is str and re.fullmatch('0[0-7]{3}',x['mode'])
        r=x['path']; pathcheck(r,True); assert r not in dirs; dirs.add(r)
        assert {k:x[k] for k in ('mode','empty')} == s['directories'][r]
        assert type(x['hidden']) is bool and x['hidden'] == any(p.startswith('.') for p in Path(r).parts if p!='.')
    assert len(seen)==1596 and seen == set(s['files'])-{'FINAL.json','OWNED_MANIFEST.json'}
    assert len(dirs)==761 and dirs == set(s['directories'])

class HTML(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True); self.tags=[]; self.data=[]; self.ids=[]
        self.feed(text); self.close(); assert len(self.ids)==len(set(self.ids))
    def handle_starttag(self,tag,attrs):
        assert len(attrs)==len({k for k,v in attrs})
        x=dict(attrs); self.tags.append((tag,x))
        if 'id' in x: self.ids.append(x['id'])
    def handle_data(self,data): self.data.append(data)

def visible(text):
    return ' '.join(''.join(HTML(text).data).split())

def one(pattern,text):
    rows=list(re.finditer(pattern,text,re.S)); assert len(rows)==1; return rows[0]

def xml_full(x):
    return {'tag':x.tag,'attributes':x.attrib,'text':x.text,'tail':x.tail,'children':[xml_full(y) for y in x]}

def aggregate(index,xml):
    text=index.decode(); HTML(text)
    script=one(r'<script type="application/ld\+json">(.*?)</script>',text)
    schema=loads(script[1]); itemlist=schema['mainEntity']
    assert schema['@type']=='CollectionPage' and itemlist['@type']=='ItemList'
    marker=one(r'"itemListElement"\s*:\s*\[',script[1]); pos=marker.end(); raw=[]
    decoder=json.JSONDecoder(object_pairs_hook=pairs)
    while True:
        while script[1][pos].isspace(): pos+=1
        if script[1][pos]==']': break
        start=pos; obj,pos=decoder.raw_decode(script[1],pos); raw.append(script[1][start:pos])
        while script[1][pos].isspace(): pos+=1
        assert script[1][pos] in ',]'
        if script[1][pos]==',': pos+=1; assert script[1][pos:].lstrip()[0]!=']'
    typed=itemlist['itemListElement']; assert [loads(x) for x in raw]==typed
    ul=one(r'<ul(?:\s[^>]*)?>(.*?)</ul>',text)
    units=re.findall(r'<li(?:\s[^>]*)?>.*?</li>',ul[1],re.S)
    assert re.sub(r'<li(?:\s[^>]*)?>.*?</li>','',ul[1],flags=re.S).strip()==''
    assert type(itemlist['numberOfItems']) is int and itemlist['numberOfItems']==len(raw)==len(units)
    for i,(x,r) in enumerate(zip(typed,units),1):
        assert set(x)=={'@type','position','url','name'} and x['@type']=='ListItem' and type(x['position']) is int and x['position']==i
        anchors=[a for t,a in HTML(r).tags if t=='a']; assert anchors
        assert x['url']=='https://aleckriebel.com'+anchors[0]['href']
    assert len({x['url'] for x in typed})==len(typed)
    xmltext=xml.decode(); assert '<!DOCTYPE' not in xmltext and '<!ENTITY' not in xmltext
    tree=ET.fromstring(xml); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
    assert tree.tag==ns+'urlset'; locations=[]
    for x in tree:
        assert x.tag==ns+'url' and len(x)==2 and x[0].tag==ns+'loc' and x[1].tag==ns+'lastmod'
        assert not list(x[0]) and not list(x[1]); locations.append(x[0].text)
    rawxml=re.findall(r'<url(?:\s[^>]*)?>.*?</url>',xmltext,re.S)
    assert len(rawxml)==len(tree)==len(set(locations))
    parsed=[{'tag':x.tag,'attributes':x.attrib,'children':[{'tag':y.tag,'attributes':y.attrib,'text':y.text,'tail':y.tail} for y in x]} for x in tree]
    values={'index_whole_UTF8':text,'sitemap_whole_UTF8':xmltext,'raw_visible_HTML_units':units,
        'visible_text_units':[visible(x) for x in units],'visible_text_rule':'concatenate HTMLParser data events, then whitespace collapse',
        'raw_JSON_units':raw,'typed_ItemList_units':typed,'raw_XML_units':rawxml,'parsed_XML_units':parsed,
        'XML_locations':locations,'counts':{'visible_HTML':len(units),'raw_JSON':len(raw),'typed_JSON':len(typed),'XML':len(tree)}}
    json_end=len(text[:script.start(1)+pos].encode())
    return values,{'schema':schema,'tree':xml_full(tree),'JSON_end_byte':json_end}

def splice_proof(old,new,rows):
    assert type(rows) is list
    previous=0; forward=[]; reverse=[]; delta=0
    for x in rows:
        assert set(x)=={'start_byte','end_byte','old_UTF8','new_UTF8','reason'}
        a,b=x['start_byte'],x['end_byte']; assert type(a) is int and type(b) is int and previous<=a<=b<=len(old)
        ob,nb=x['old_UTF8'].encode(),x['new_UTF8'].encode(); assert old[a:b]==ob
        forward.extend([old[previous:a],nb]); previous=b
        na=a+delta; assert new[na:na+len(nb)]==nb; reverse.append((na,na+len(nb),ob))
        delta+=len(nb)-len(ob)
    forward.append(old[previous:]); assert b''.join(forward)==new
    restored=new
    for a,b,ob in reversed(reverse): restored=restored[:a]+ob+restored[b:]
    assert restored==old
    return {'old_bytes':len(old),'new_bytes':len(new),'old_SHA256':sha(old),'new_SHA256':sha(new),'whole_reverse_SHA256':sha(restored)}

def local_paths(article_path,canonical):
    parsed=HTML(article_path.read_bytes().decode())
    for tag,x in parsed.tags:
        for attr in ('aria-labelledby','aria-describedby','aria-controls'):
            if attr in x: assert all(r in parsed.ids for r in x[attr].split())
        for attr in ('href','src'):
            if attr not in x: continue
            u=urlsplit(x[attr]); target=None
            if u.scheme or u.netloc:
                if u.scheme=='https' and u.netloc=='aleckriebel.com':
                    target=CAND/unquote(u.path).lstrip('/')
                else: continue
            elif u.path.startswith('/'): target=CAND/unquote(u.path).lstrip('/')
            elif u.path: pathcheck(unquote(u.path)); target=article_path.parent/unquote(u.path)
            else: target=article_path
            if target.is_dir(): target=target/'index.html'
            assert target.is_file(),str(target)
            if u.fragment and target==article_path: assert u.fragment in parsed.ids
    return len(parsed.ids)

started=utc()
for p,h in PINS.items(): assert pin(p)['SHA256']==h,str(p)
template=readj(S/'GUARDS_BEFORE.json'); assert template==readj(S/'GUARDS_AFTER.json')
before=capture(template); save_guard('GUARDS_BEFORE.json',before)
try:
    assert before['protected']==template,'Fresh protected state differs'
    stage_manifest(before['whole_corrected_stage'])
    final=readj(S/'FINAL.json'); assert final['schema']=='private-hafnian-retract-stage-final-v1'
    assert final['status']=='PASS_PRIVATE_STAGE_FROZEN_AWAITING_INDEPENDENT_IMPLEMENTATION_AUDIT'
    assert final['manifest']==pin(S/'OWNED_MANIFEST.json')
    for r,x in final['artifacts'].items(): pathcheck(r); assert pin(S/r)==x
    binding=readj(B/'INPUT_BINDINGS.json'); contract=readj(I/'CONTRACT.json')
    assert len(contract['criteria'])==28 and [x['id'] for x in contract['criteria']]==['C'+str(n).zfill(2) for n in range(1,29)]
    auth=readj(S/'INPUT_AUTHENTICATION.json'); receipts={x['root']:x for x in auth['actual_finite_manifests']}
    checked_manifests=[]
    for root,manifest,terminal,schema,key in RULES:
        if root==D:
            external={'manifest':pin(D/'OWNED_MANIFEST.json'),'terminal':pin(D/'FINAL.json')}
            snap=before['protected']['frozen_diagnostic_lane']
        else:
            external=receipts[str(root)]
            snap=before['protected']['binding_lane'] if root==B else before['protected']['roots'][str(root)]
        checked_manifests.append(input_manifest(root,snap,manifest,terminal,schema,key,external))
    for r,snap in binding['guards_before']['roots'].items(): same_snapshot(snap,before['protected']['roots'][r])
    assert binding['guards_before']['controls']==before['protected']['controls']
    for key in ('native_M','native_W'): assert binding['guards_before'][key]==before['protected'][key]
    same_snapshot(readj(D/'GUARDS_BEFORE.json')['producer_whole_packet'],before['protected']['old_failed_lane'])
    assert readj(F/'BUILD_EXECUTION.json')['exit_code']==1 and pin(F/'BUILD.stderr.txt')['bytes']==954
    execution=readj(S/'BUILD_EXECUTION.json'); assert execution==final['execution']
    assert execution['invocations']==1 and execution['exit_code']==0 and execution['error'] is None
    assert execution['stdout']==pin(S/'BUILD.stdout.txt') and execution['stderr']==pin(S/'BUILD.stderr.txt')
    assert pin(S/'BUILD.stdout.txt')['bytes']==pin(S/'BUILD.stderr.txt')['bytes']==0
    base,candidate=census(BASE),census(CAND); same_snapshot(base,template['public'],False)
    same_snapshot(readj(S/'BASELINE_MANIFEST.json'),base); same_snapshot(readj(S/'CANDIDATE_MANIFEST.json'),candidate)
    target=readj(S/'TARGETS.json'); projection=readj(S/'PROJECTION.json')
    adds=sorted(set(candidate['files'])-set(base['files'])); removed=set(base['files'])-set(candidate['files'])
    changed=sorted(r for r in base['files'] if r in candidate['files'] and base['files'][r]!=candidate['files'][r])
    newdirs=sorted(set(candidate['directories'])-set(base['directories']))
    assert len(adds)==9 and len(changed)==2 and len(newdirs)==4 and not removed
    assert adds==sorted(target['additions_public_relative'])==projection['additions_public_relative']
    assert changed==sorted(target['modifications_public_relative'])==projection['modifications_public_relative']
    assert newdirs==sorted(target['new_directories_public_relative'])==projection['new_directories_public_relative']
    assert target['Git_relative_targets']==contract['exact_Git_relative_targets']==binding['exact_Git_relative_targets']==projection['Git_relative_targets']
    assert target['Git_relative_targets']==['public/'+r for r in target['additions_public_relative']+target['modifications_public_relative']]
    assert (base['regular_files'],base['child_directories'],candidate['regular_files'],candidate['child_directories'])==(781,377,790,381)
    assert all(candidate['files'][r]==x for r,x in base['files'].items() if r not in changed)
    assert sum(r not in changed for r in base['files'])==779
    assert all(candidate['directories'][r]==x for r,x in base['directories'].items())
    assert all(candidate['directories'][r]=={'mode':'0755','empty':False} for r in newdirs)
    assert all(candidate['files'][r]['mode']=='0644' for r in adds)
    assert sum(Path(r).name=='.DS_Store' for r in candidate['files'])==17
    pages=[]; heads=readj(S/'HEAD_ACTIVATION.json'); wanted_items=[]; wanted_canon=[]
    for number,accepted in enumerate(binding['pages'],129):
        family=accepted['family']; writer=V/(family+'-editorial-sol-20261117'); model=readj(writer/'page-model.json')
        article=(writer/'article.html').read_bytes(); oldhead=(writer/'head.html').read_bytes()
        newpath=CAND/'research'/accepted['slug']/'index.html'; newarticle=newpath.read_bytes()
        newhead=one(rb'(<head>.*?</head>\n)',newarticle)[1]
        oldhm=one(rb'(<head>.*?</head>\n)',article); newhm=one(rb'(<head>.*?</head>\n)',newarticle)
        assert oldhm[1]==oldhead and article[:oldhm.start(1)]==newarticle[:newhm.start(1)] and article[oldhm.end(1):]==newarticle[newhm.end(1):]
        assert one(rb'(<body>.*?</body>\n)',article)[1]==one(rb'(<body>.*?</body>\n)',newarticle)[1]
        assert one(rb'(<main id="main">.*?</main>\n)',newarticle)[1]==(writer/'main.html').read_bytes()
        body=one(rb'(<body>.*?</body>)',newarticle)[1]; assert (len(body),sha(body))==(accepted['BODY']['bytes'],accepted['BODY']['SHA256'])
        canonical=model['deployment_proposal']['proposed_canonical_url']; wanted_canon.append(canonical)
        oldsch=loads(one(rb'<script type="application/ld\+json">(.*?)</script>',oldhead)[1].decode())
        newsch=loads(one(rb'<script type="application/ld\+json">(.*?)</script>',newhead)[1].decode())
        expected=copy.deepcopy(oldsch); expected.update({k:canonical for k in ('@id','url','mainEntityOfPage')})
        for x in expected['encoding']: x['contentUrl']=canonical+x['contentUrl']
        assert oldsch==accepted['schema_object'] and newsch==expected and newsch['@type']=='ScholarlyArticle' and '@graph' not in newsch
        receipt=next(x for x in heads['pages'] if x['family']==family)
        assert receipt['accepted_head_SHA256']==sha(oldhead) and receipt['candidate_head_SHA256']==sha(newhead)
        allowed=[]
        for name in ('robots','googlebot'):
            old=('<meta name="'+name+'" content="noindex, nofollow">\n').encode(); start=oldhead.index(old); allowed.append((start,start+len(old),old,b''))
        old=b'<meta name="citation_pdf_url" content="assets/paper.pdf">'; start=oldhead.index(old)
        allowed.append((start,start+len(old),old,('<meta name="citation_pdf_url" content="'+canonical+'assets/paper.pdf">').encode()))
        for x in oldsch['encoding']:
            old=('"contentUrl": "'+x['contentUrl']+'"').encode(); start=oldhead.index(old)
            allowed.append((start,start+len(old),old,('"contentUrl": "'+canonical+x['contentUrl']+'"').encode()))
        place=oldhead.index(b'<link rel="stylesheet" href="/research/research.css">\n')
        allowed.append((place,place,b'',('<link rel="canonical" href="'+canonical+'">\n<meta property="og:url" content="'+canonical+'">\n').encode()))
        place=one(rb'<script type="application/ld\+json">(.*?)</script>',oldhead).end(1)-1
        addition=(', "@id": '+json.dumps(canonical)+', "url": '+json.dumps(canonical)+', "mainEntityOfPage": '+json.dumps(canonical)).encode()
        allowed.append((place,place,b'',addition))
        assert [(x['start_byte'],x['end_byte'],x['old_UTF8'].encode(),x['new_UTF8'].encode()) for x in receipt['spans']]==sorted(allowed)
        headproof=splice_proof(oldhead,newhead,receipt['spans'])
        parsed=HTML(newarticle.decode()); metas=[x for t,x in parsed.tags if t=='meta']
        assert not any(x.get('name') in ('robots','googlebot') for x in metas)
        assert [x['href'] for t,x in parsed.tags if t=='link' and x.get('rel')=='canonical']==[canonical]
        assert [x['content'] for x in metas if x.get('property')=='og:url']==[canonical]
        assert [x['href'] for t,x in parsed.tags if t=='link' and x.get('rel')=='stylesheet']==['/research/research.css']
        assert [x['content'] for x in metas if x.get('name')=='DC.description']==[model['abstract']]
        assert [x['content'] for x in metas if x.get('name')=='citation_pdf_url']==[canonical+'assets/paper.pdf']
        assert html.unescape(one(r'<p id="abstract-text">(.*?)</p>',newarticle.decode())[1])==newsch['abstract']==model['abstract']==accepted['abstract']
        assert pin(newpath.parent/'citation.bib')==pin(writer/'citation.bib')==accepted['Bib']
        for asset in accepted['assets']:
            pp=newpath.parent/asset['relative_path']; assert pin(pp)=={k:asset[k] for k in ('bytes','SHA256','mode')}==pin(writer/asset['relative_path'])
            for r in asset['native_source_matches']: assert pin(P/'papers'/model['record_id']/'sources'/r)==pin(pp)
        assert [x['name'] for x in newsch['encoding']]==accepted['native_encoding_names']
        if family=='hafnian': assert model['native_version']==newsch['version']=='1.0.0'
        else: assert model['native_version'] is None and model['native_API_version_field_absent'] is True and 'version' not in newsch
        ids=local_paths(newpath,canonical)
        wanted_items.append({'@type':'ListItem','position':number,'url':canonical,'name':model['title']})
        pages.append({'family':family,'candidate_article':pin(newpath),'BODY':accepted['BODY'],'HEAD_splice_reversal':headproof,'ids':ids,'all_body_MAIN_Bib_assets_abstracts_exact':True})
    oldindex=(BASE/'research/index.html').read_bytes(); oldxml=(BASE/'research/sitemap.xml').read_bytes()
    newindex=(CAND/'research/index.html').read_bytes(); newxml=(CAND/'research/sitemap.xml').read_bytes()
    assert (S/'ORIGINAL_RESEARCH_INDEX.html').read_bytes()==oldindex and (S/'ORIGINAL_RESEARCH_SITEMAP.xml').read_bytes()==oldxml
    old,oldextra=aggregate(oldindex,oldxml); new,newextra=aggregate(newindex,newxml)
    assert old==binding['aggregate_baseline']==readj(S/'BASELINE_AGGREGATE_UNITS.json')
    assert new==readj(S/'CANDIDATE_AGGREGATE_UNITS.json')
    assert old['counts']=={'visible_HTML':128,'raw_JSON':128,'typed_JSON':128,'XML':129}
    assert new['counts']=={'visible_HTML':130,'raw_JSON':130,'typed_JSON':130,'XML':131}
    for k in ('raw_visible_HTML_units','visible_text_units','raw_JSON_units','typed_ItemList_units','raw_XML_units','parsed_XML_units','XML_locations'):
        assert new[k][:len(old[k])]==old[k],k
    assert newextra['tree']['attributes']==oldextra['tree']['attributes'] and newextra['tree']['text']==oldextra['tree']['text']
    assert newextra['tree']['children'][:129]==oldextra['tree']['children']
    assert new['typed_ItemList_units'][128:]==wanted_items and new['XML_locations'][129:]==wanted_canon
    assert all(x['children'][1]['text']=='2026-11-17' for x in newextra['tree']['children'][129:])
    for i,(accepted,canonical) in enumerate(zip(binding['pages'],wanted_canon),128):
        model=readj(V/(accepted['family']+'-editorial-sol-20261117')/'page-model.json')
        unit=new['raw_visible_HTML_units'][i]; parsed=HTML(unit); anchors=[x for t,x in parsed.tags if t=='a']
        assert [x['href'] for x in anchors]==[model['deployment_proposal']['path'],model['deployment_proposal']['path']+'assets/paper.pdf',model['doi_url']]
        assert html.unescape(one(r'<li><a[^>]*>(.*?)</a>',unit)[1])==model['title']
        assert html.unescape(one(r'<p>(.*?)</p>',unit)[1])==model['meta_description']
        metadata=one(r'<span class="entry-meta">(.*?)</span>',unit)[1]
        native_entry=one(r'<p class="entry-meta">(.*?)</p>',(V/(accepted['family']+'-editorial-sol-20261117')/'main.html').read_text())[1].split('</a> · ',1)[1]
        assert metadata==native_entry
        assert visible(unit)==' '.join((model['title']+visible(metadata)+model['meta_description']+'PDF · Zenodo').split())
    fidelity=readj(S/'AGGREGATE_FIDELITY.json')
    count=one(rb'"numberOfItems"\s*:\s*(128)(?=\s*[,}])',oldindex)
    expected_edits=[(count.start(1),count.end(1),'128','130'),
        (oldextra['JSON_end_byte'],oldextra['JSON_end_byte'],'',', '+', '.join(new['raw_JSON_units'][128:])),
        (oldindex.index(b'</ul>'),oldindex.index(b'</ul>'),'','\n'.join(new['raw_visible_HTML_units'][128:])+'\n')]
    assert [(x['start_byte'],x['end_byte'],x['old_UTF8'],x['new_UTF8']) for x in fidelity['index_spans']]==expected_edits
    assert [(x['start_byte'],x['end_byte'],x['old_UTF8'],x['new_UTF8']) for x in fidelity['XML_spans']]==[(oldxml.index(b'</urlset>'),oldxml.index(b'</urlset>'),'','\n'.join(new['raw_XML_units'][129:])+'\n')]
    aggregateproofs={'index':splice_proof(oldindex,newindex,fidelity['index_spans']),
                     'XML':splice_proof(oldxml,newxml,fidelity['XML_spans'])}
    for k,p in (('baseline_index',BASE/'research/index.html'),('candidate_index',CAND/'research/index.html'),('baseline_XML',BASE/'research/sitemap.xml'),('candidate_XML',CAND/'research/sitemap.xml')):
        assert fidelity[k]==pin(p)
    index=(W/'.git/index').read_bytes(); assert len(index)==9059206 and index[:4]==b'DIRC'
    assert struct.unpack('!II',index[4:12])==(2,58721) and hashlib.sha1(index[:-20]).digest()==index[-20:]
    assert sha(index)=='592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365'
    for oid,kind,body in ((binding['guards_before']['native_W']['resolved_native_HEAD'],'commit',binding['native_W_commit_body'].encode()),(binding['native_W_commit_tree'],'tree',bytes.fromhex(binding['native_W_tree_body_hex']))):
        obj=zlib.decompress((W/'.git/objects'/oid[:2]/oid[2:]).read_bytes())
        assert obj==kind.encode()+b' '+str(len(body)).encode()+b'\x00'+body and hashlib.sha1(obj).hexdigest()==oid
    out={'schema':'independent-hafnian-retract-corrected-stage-data-audit-v1','status':'PASS_FIXED_ARTIFACT_DATA_AUDIT',
        'UTC_start':started,'checked_input_manifests':checked_manifests,'pages':pages,
        'aggregate_reversal_proofs':aggregateproofs,'baseline_counts':old['counts'],'candidate_counts':new['counts'],
        'whole128raw_HTML_concat_visible_rawJSON_typed_and129raw_fullparsedXML_prefixes_exact':True,
        'projection':{'additions':adds,'modifications':changed,'new_directories':newdirs,'Git_relative_targets':target['Git_relative_targets']},
        'stage_extent':[1598,760],'baseline_extent':[781,377],'candidate_extent':[790,381],
        'untouched_old_files':779,'old_directory_modes':377,'DSStore':17,
        'all_source_private_initial_bindings_diagnostic_oldfailed_native_public_exact':True,
        'literal_distinct_build_exit_history':[1,0],'whole_raw_W_index_exact_checksum_valid':True,
        'scientific_copy_rendered_live_or_production_certificate':False,'producer_helper_execution':False,
        'Git_network_W_source_otherpacket_mutation':False}
finally:
    after=capture(template); save_guard('GUARDS_AFTER.json',after)
    assert after==before,'Protected state changed during passive audit'
out['UTC_end']=utc(); out['whole_before_after_guards_equal']=True
print(json.dumps(out,indent=2,ensure_ascii=False))
