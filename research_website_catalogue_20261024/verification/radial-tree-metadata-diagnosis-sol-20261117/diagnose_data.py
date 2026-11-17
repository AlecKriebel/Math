#!/usr/bin/env python3
"""One aggregate-only forensic reader; raw-index/TREE/commit semantics excluded."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime, timezone
import hashlib, json, os, re, stat, sys, traceback
import xml.etree.ElementTree as ET

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M=P.parent
W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
OLD=P/'verification/radial-tree-post-publication-audit-sol-20261117'
S=P/'verification/radial-tree-stage-sol-20261117'
A=P/'verification/radial-tree-metadata-diagnosis-sol-20261117'
active='initialization';failure=None;before=None
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,value):(A/name).write_text(json.dumps(value,indent=2,ensure_ascii=True)+'\n')
def require(ok,label):
    global active
    active=label
    if not ok:raise AssertionError(label)
def meta(p):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise ValueError('Not regular: '+str(p))
    b=p.read_bytes();return {'bytes':len(b),'SHA256':sha(b),'mode':oct(stat.S_IMODE(st.st_mode))}
def snapshot(root):
    st=root.lstat();files={};dirs={};other={}
    if not stat.S_ISDIR(st.st_mode):raise ValueError('Not directory: '+str(root))
    for p in sorted(root.rglob('*')):
        stp=p.lstat();name=str(p.relative_to(root))
        if stat.S_ISREG(stp.st_mode):files[name]=meta(p)
        elif stat.S_ISDIR(stp.st_mode):dirs[name]=oct(stat.S_IMODE(stp.st_mode))
        else:other[name]={'mode':oct(stat.S_IMODE(stp.st_mode)),'target':os.readlink(p) if p.is_symlink() else None}
    return {'root':str(root),'root_mode':oct(stat.S_IMODE(st.st_mode)),'files':files,'directories':dirs,'other':other}
def native(repo):
    gd=repo/'.git';packed=gd/'packed-refs'
    return {'files':{n:meta(gd/n) for n in ['HEAD','index','config']},'local_heads':snapshot(gd/'refs/heads'),
            'packed_local_head_lines':[x for x in packed.read_text().splitlines() if re.match(r'^[0-9a-f]{40} refs/heads/',x)],
            'packed_refs_mode':oct(stat.S_IMODE(packed.stat().st_mode))}
def guard():
    return {'UTC':now(),'old_frozen_packet':snapshot(OLD),'stage':snapshot(S),'actual_public':snapshot(W/'public'),
            'M_native_local':native(M),'W_native_local':native(W),
            'exclusions':['remote-tracking refs','FETCH_HEAD','nonlocal packed-ref lines','Firebase metadata outside public'],
            'raw_index_read_only_for_whole_file_guard_hash_no_semantic_analysis':True}

class Events(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.stack=[];self.units=[];self.links=[];self.events=[]
    def handle_starttag(self,tag,attrs):
        if tag=='li':self.parts=[];self.links=[];self.events=[];self.stack.append('li')
        if self.stack:
            self.events.append({'start':tag,'attrs':attrs})
            if tag=='a':self.links.append(dict(attrs).get('href'))
    def handle_data(self,data):
        if self.stack:self.parts.append(data);self.events.append({'data':data})
    def handle_endtag(self,tag):
        if self.stack:self.events.append({'end':tag})
        if tag=='li' and self.stack:
            self.units.append({'text':' '.join(' '.join(self.parts).split()),'hrefs':self.links[:],
                               'parts':self.parts[:],'events':self.events[:],
                               'concatenate_then_collapse':' '.join(''.join(self.parts).split()),
                               'strip_then_concatenate':''.join(x.strip() for x in self.parts)})
            self.stack.pop()
def extract(text):
    scripts=re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',text,re.S|re.I)
    lists=[]
    def visit(x):
        if isinstance(x,dict):
            if x.get('@type')=='ItemList':lists.append(x)
            for v in x.values():visit(v)
        elif isinstance(x,list):
            for v in x:visit(v)
    for s in scripts:visit(json.loads(s))
    require(len(lists)==1,'exactly_one_actual_ItemList')
    h=Events();h.feed(text)
    rawhtml=re.findall(r'<li\b[^>]*>.*?</li>',text,re.S|re.I)
    rawjson=[];decoder=json.JSONDecoder();script=next(s for s in scripts if '"ItemList"' in s)
    pos=script.index('[',script.index('"itemListElement"'))+1
    while True:
        while script[pos].isspace() or script[pos]==',':pos+=1
        if script[pos]==']':break
        _,end=decoder.raw_decode(script,pos);rawjson.append(script[pos:end]);pos=end
    return {'old_visible':[{'text':u['text'],'hrefs':u['hrefs']} for u in h.units],
            'old_raw_HTML_units':rawhtml,'old_raw_JSON_units':rawjson,'old_typed':lists[0]['itemListElement'],
            'numberOfItems':lists[0]['numberOfItems'],'event_units':h.units}
def difference(a,b,path=()):
    if type(a)!=type(b):return [{'path':list(path),'kind':'type','extracted':a,'metadata':b}]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out.append({'path':list(path+(k,)),'kind':'key','extracted':a.get(k),'metadata':b.get(k)})
            else:out+=difference(a[k],b[k],path+(k,))
        return out
    if isinstance(a,list):
        out=[]
        if len(a)!=len(b):out.append({'path':list(path),'kind':'length','extracted':len(a),'metadata':len(b)})
        for i,(x,y) in enumerate(zip(a,b)):out+=difference(x,y,path+(i,))
        return out
    if a==b:return []
    row={'path':list(path),'kind':'value','extracted':a,'metadata':b}
    if isinstance(a,str):
        p=0
        while p<min(len(a),len(b)) and a[p]==b[p]:p+=1
        row.update(first_differing_codepoint=p,extracted_context=a[max(0,p-45):p+75],metadata_context=b[max(0,p-45):p+75],
                   extracted_UTF8_SHA256=sha(a.encode()),metadata_UTF8_SHA256=sha(b.encode()))
    return [row]
def xtree(n):return {'tag':n.tag,'attributes':n.attrib,'text':n.text,'tail':n.tail,'children':[xtree(c) for c in n]}

try:
    before=guard();save('GUARDS_BEFORE.json',before)
    require(len(before['old_frozen_packet']['files'])==14 and not before['old_frozen_packet']['directories'],'old_exact_14_file_namespace')
    require(meta(OLD/'data_auditor.py')['SHA256']=='c408cc6be6f732445ee9997d738c21740facb1295300b5c034a4ecb34dc8b362','actual_original_extractor_pin')
    for name in ['AUDIT.stderr','FIRST_FAILURE.json','EXECUTION.json']:(A/('original-'+name)).write_bytes((OLD/name).read_bytes())
    (A/'original-data-auditor.py.txt').write_bytes((OLD/'data_auditor.py').read_bytes())
    actualsource=(OLD/'data_auditor.py').read_text()
    require("'text':' '.join(' '.join(self.parts).split())" in actualsource and 'preservation_data_independently_extracted' in actualsource,'failing_extractor_text_mechanism_read')
    rawmeta=(S/'AGGREGATE_PRESERVATION.json').read_bytes();metadata=json.loads(rawmeta)
    oldbytes=(S/'originals/research-index.html').read_bytes();installedbytes=(W/'public/research/index.html').read_bytes()
    oldxml=(S/'originals/research-sitemap.xml').read_bytes();newxml=(W/'public/research/sitemap.xml').read_bytes()
    old=extract(oldbytes.decode());new=extract(installedbytes.decode())
    fields=['old_visible','old_raw_HTML_units','old_raw_JSON_units','old_typed']; comparisons={}
    for field in fields:
        require(isinstance(metadata['index'][field],list),'metadata_list_'+field)
        differences=difference(old[field],metadata['index'][field])
        comparisons[field]={'extracted_count':len(old[field]),'metadata_count':len(metadata['index'][field]),
                            'exact_equal':old[field]==metadata['index'][field],
                            'mismatching_unit_indexes':sorted({r['path'][0] for r in differences if r['path'] and isinstance(r['path'][0],int)}),
                            'all_component_differences':differences,
                            'actual_installed_prefix_equal_to_actual_original':new[field][:len(old[field])]==old[field]}
    visible=[]
    for i,u in enumerate(old['event_units']):
        m=metadata['index']['old_visible'][i]
        visible.append({'index_zero_based':i,'first_href':u['hrefs'][0] if u['hrefs'] else None,
                        'space_join_text_matches_metadata':u['text']==m['text'],
                        'concatenate_then_collapse_matches_metadata':u['concatenate_then_collapse']==m['text'],
                        'strip_then_concatenate_matches_metadata':u['strip_then_concatenate']==m['text'],
                        'hrefs_exact':u['hrefs']==m['hrefs'],
                        'parts':u['parts'] if u['text']!=m['text'] else None,
                        'events':u['events'] if u['text']!=m['text'] else None})
    save('ALL_FOUR_FIELD_COMPARISONS.json',comparisons);save('VISIBLE_CONVENTION_EVIDENCE.json',visible)
    typed=metadata['index']['old_typed'];serializations={}
    for ascii_flag in [False,True]:
        serializations[str(ascii_flag)]={'matches_metadata_raw':[json.dumps(x,ensure_ascii=ascii_flag)==y for x,y in zip(typed,metadata['index']['old_raw_JSON_units'])],
                                        'matches_actual_raw':[json.dumps(x,ensure_ascii=ascii_flag)==y for x,y in zip(typed,old['old_raw_JSON_units'])]}
    save('RAW_JSON_CONVENTION_EVIDENCE.json',serializations)
    html=installedbytes.decode();restored=html.replace(metadata['index']['appended_HTML'],'',1).replace(metadata['index']['appended_JSON'],'',1).replace('"numberOfItems": 128','"numberOfItems": 126',1)
    ox=ET.fromstring(oldxml);nx=ET.fromstring(newxml)
    oldraw=re.findall(rb'<url>.*?</url>',oldxml,re.S);newraw=re.findall(rb'<url>.*?</url>',newxml,re.S)
    xmlappend=metadata['sitemap']['appended_XML'].encode()
    semantic={'old_numberOfItems':old['numberOfItems'],'installed_numberOfItems':new['numberOfItems'],
              'all_four_actual_prefix_comparisons':{k:v['actual_installed_prefix_equal_to_actual_original'] for k,v in comparisons.items()},
              'full_index_reversal_equals_original_UTF8_bytes':restored.encode()==oldbytes,
              'index_append_HTML_occurrences':html.count(metadata['index']['appended_HTML']),
              'index_append_JSON_occurrences':html.count(metadata['index']['appended_JSON']),
              'original_XML_nodes':len(ox),'installed_XML_nodes':len(nx),
              'all_old_raw_XML_nodes_preserved':newraw[:len(oldraw)]==oldraw,
              'all_old_structured_XML_nodes_preserved':[xtree(x) for x in nx[:len(ox)]]==[xtree(x) for x in ox],
              'XML_append_occurrences':newxml.count(xmlappend),'full_XML_reversal_equals_original_bytes':newxml.replace(xmlappend,b'',1)==oldxml}
    save('ACTUAL_AGGREGATE_PRESERVATION.json',semantic)
    save('DIAGNOSIS.json',{'schema':'bounded-four-field-metadata-diagnosis-v1','UTC':now(),'status':'DIAGNOSIS_COMPLETE',
                         'input_pins':{'metadata':meta(S/'AGGREGATE_PRESERVATION.json'),'original_HTML':meta(S/'originals/research-index.html'),
                                       'installed_HTML':meta(W/'public/research/index.html'),'original_XML':meta(S/'originals/research-sitemap.xml'),'installed_XML':meta(W/'public/research/sitemap.xml')},
                         'field_summary':{k:{n:v[n] for n in ['extracted_count','metadata_count','exact_equal','mismatching_unit_indexes','actual_installed_prefix_equal_to_actual_original']} for k,v in comparisons.items()},
                         'visible_convention_counts':{k:sum(bool(x[k]) for x in visible) for k in ['space_join_text_matches_metadata','concatenate_then_collapse_matches_metadata','strip_then_concatenate_matches_metadata','hrefs_exact']},
                         'actual_aggregate_preservation':semantic,'raw_index_TREE_commit_semantic_checks_executed':False,
                         'old_auditor_modified_or_retried':False,'project_helper_execution_import_AST_compilation_tests':0,'bounded_attempts':1})
except BaseException as ex:
    failure={'UTC':now(),'criterion':active,'exception':repr(ex),'traceback':traceback.format_exc()};save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['traceback'])
finally:
    after=guard();save('GUARDS_AFTER.json',after)
    unchanged=before is not None and {k:v for k,v in before.items() if k!='UTC'}=={k:v for k,v in after.items() if k!='UTC'}
    if not unchanged and failure is None:
        failure={'UTC':now(),'criterion':'protected_before_after_guards','exception':'Observed protected guard drift','traceback':''};save('FIRST_FAILURE.json',failure);sys.stderr.write(failure['exception']+'\n')
    save('ATTEMPT_RESULT.json',{'UTC':now(),'status':'FIRST_FAILURE_STOP' if failure else 'DIAGNOSIS_COMPLETE','first_failure':failure,'protected_guards_unchanged':unchanged,'attempts':1,'no_raw_index_TREE_commit_semantic_execution':True})
    print(json.dumps({'status':'FIRST_FAILURE_STOP' if failure else 'DIAGNOSIS_COMPLETE','guards_unchanged':unchanged,'first_failure':failure['criterion'] if failure else None}))
sys.exit(1 if failure else 0)
