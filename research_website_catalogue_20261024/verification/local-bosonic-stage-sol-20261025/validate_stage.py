"""Validate only owned private stages, including altered copies and custody."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape, unescape
import ast, copy, datetime, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, unicodedata
import xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent
R=O.parents[1]
S=O/'public'
Q=R/'verification/local-quadratic-stage-sol-20261025'
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PYTHON='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(O)+os.pathsep+str(R/'scripts'))
IDS=['23306332','23203100','22089807']
CONFIG={rid:json.loads((R/'papers'/rid/'publication.json').read_text()) for rid in IDS}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):
    path=O/name;path.parent.mkdir(parents=True,exist_ok=True)
    assert not path.exists(),path
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n' if not isinstance(data,str) else data)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run_check(site,rids,out,stem):
    proc=subprocess.run([PYTHON,'-B',str(O/'final-content-check.stage.py'),*rids,'--site',str(site),'--output-dir',str(out),'--output-stem',stem],env=ENV,capture_output=True,text=True)
    (out/(stem+'.stdout.json')).write_text(proc.stdout);(out/(stem+'.stderr.txt')).write_text(proc.stderr)
    report=json.loads((out/(stem+'.json')).read_text()) if (out/(stem+'.json')).exists() else None
    return proc,report
class Visible(HTMLParser):
    def __init__(self,h):
        super().__init__();self.body=False;self.parts=[];self.feed(h)
    def handle_starttag(self,t,a):
        if t=='body':self.body=True
        if self.body and t in ['p','h1','h2','li','br','section','header','footer']:self.parts.append('\n')
    def handle_endtag(self,t):
        if t=='body':self.body=False
        if self.body and t in ['p','h1','h2','li','section']:self.parts.append('\n')
    def handle_data(self,d):
        if self.body:self.parts.append(d)

positive,report=run_check(S,IDS,O,'target-stage-check-final')
assert positive.returncode==0 and not positive.stderr and report['status']=='PASS'
for rid in IDS:
    c=CONFIG[rid];h=(S/'research'/c['slug']/'index.html').read_text();v=Visible(h)
    text='\n\n'.join(' '.join(x.split()) for x in ''.join(v.parts).split('\n') if x.strip())+'\n'
    save('public-copy-'+rid+'.txt',text)
    sections={sid:[unescape(x) for x in re.findall('<p>(.*?)</p>',segment,re.S)] for sid,segment in re.findall('<section id="([^"]+)">(.*?)</section>',h,re.S)}
    save('public-sections-'+rid+'.json',sections)
    if rid=='23203100':
        expected=json.loads((R/'papers'/rid/'reviews/editorial/public-sections.json').read_text())
        assert all(sections[k]==s['paragraphs'] for k,s in expected.items() if 'paragraphs' in s)
    if rid=='23306332':
        assert sha(S/'research'/c['slug']/'index.html')==sha(Q/'public/research'/c['slug']/'index.html')
        assert text==(Q/'public-copy-23306332.txt').read_text()

def item_list(text):return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S).group(1))['mainEntity']
old_index=(LIVE/'research/index.html').read_text();index=(S/'research/index.html').read_text()
old_items=item_list(old_index);items=item_list(index)
assert old_items['numberOfItems']==47 and items['numberOfItems']==50
assert items['itemListElement'][:47]==old_items['itemListElement']
assert len({x['url'] for x in items['itemListElement']})==50
old_lis=re.findall(r'<li>.*?</li>',old_index,re.S);new_lis=re.findall(r'<li>.*?</li>',index,re.S)
assert new_lis[:47]==old_lis and len(old_lis)==47 and len(new_lis)==50
urls=lambda path:[x.text for x in ET.fromstring(path.read_text()).iter() if x.tag.endswith('loc')]
old_urls=urls(LIVE/'research/sitemap.xml');new_urls=urls(S/'research/sitemap.xml')
assert len(old_urls)==48 and len(new_urls)==len(set(new_urls))==51
assert new_urls[:48]==old_urls and set(new_urls)-set(old_urls)=={CONFIG[x]['canonical_url'] for x in IDS}
assert sha(S/'research/research.css')==sha(LIVE/'research/research.css') and sha(S/'robots.txt')==sha(LIVE/'robots.txt')
save('index-sitemap-checks.json',{'utc':now(),'status':'PASS','original_entries':47,'new_entries':50,'sitemap_urls':51,'old_47_visible_list_items_byte_identical':True,'old_47_structured_items_exact':True,'old_48_sitemap_urls_same_order':True,'only_three_new_urls':[CONFIG[x]['canonical_url'] for x in IDS],'quadratic_html_and_actual_public_copy_unchanged':True})

# Pure helper output equality over every original mapping, plus exact reversal
# in build_stage_tools, establishes preservation of every legacy dispatch.
def helpers(path):
    tree=ast.parse(path.read_text());env={'re':re,'unicodedata':unicodedata,'Path':Path};nodes=[]
    for n in tree.body:
        if isinstance(n,ast.FunctionDef):nodes.append(n)
        elif isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id.isupper() for t in n.targets):
            try:ast.literal_eval(n.value)
            except (ValueError,TypeError):continue
            nodes.append(n)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<pure helpers>','exec'),env);return env
before=helpers(O/'inputs/final-content-check.py');after=helpers(O/'final-content-check.proposed.py');legacy={}
for rid,path in before['TEX_PATHS'].items():
    assert after['TEX_PATHS'][rid]==path
    source=(R/'papers'/rid/'sources'/path).read_text()
    if rid=='22089551':source=re.search(r'\\ifdefined\\japsubmission(.*?)\\else(.*?)\\fi',source,re.S).group(2)
    a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',source,re.S).group(1)
    legacy[rid]=before['abstract_tokens'](a,rid)==after['abstract_tokens'](a,rid)
assert len(legacy)==46 and all(legacy.values())
save('legacy-dispatch-comparison.json',{'utc':now(),'status':'PASS','original_mappings_and_abstract_dispatches':legacy,'combined_mappings':len(after['TEX_PATHS'])})

# Actual complete original/proposed rendering comparison for three materially
# distinct versioned cases: default edition, custom edition, standard tar.gz.
comparison={}
for rid in ['23539283','23306332','22089807']:
    root=O/'versioned-comparison'/rid;root.mkdir(parents=True)
    c=json.loads((R/'papers'/rid/'publication.json').read_text());outputs={}
    for label,source in [('original',O/'inputs/render_page.py'),('proposed',O/'render_page.proposed.py')]:
        target=root/label/'public';(target/'research').mkdir(parents=True)
        for rel in ['research/index.html','research/research.css','research/sitemap.xml','robots.txt']:shutil.copyfile(LIVE/rel,target/rel)
        code=source.read_text().replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path('+repr(str(R))+')').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",'SITE = Path('+repr(str(target/'research'))+')')
        script=root/(label+'.py');script.write_text(code)
        proc=subprocess.run([PYTHON,'-B',str(script),rid],env=ENV,capture_output=True,text=True)
        assert proc.returncode==0 and not proc.stderr,(rid,label,proc.stderr)
        outputs[label]={str(p.relative_to(target)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(target.rglob('*')) if p.is_file()}
    assert outputs['original']==outputs['proposed'],rid
    comparison[rid]={'all_files_byte_identical':True,'files':outputs['original']}
save('versioned-render-comparison.json',{'utc':now(),'status':'PASS','cases':comparison,'scope':'Private outputs only; no actual-site rendering.'})

negative=[]
def alter_case(name,rid,mutator,expected):
    root=O/'negative'/name;root.mkdir(parents=True);stage=root/'public';shutil.copytree(S,stage)
    c=CONFIG[rid];page=stage/'research'/c['slug']/'index.html';mutator(stage,page,c)
    proc,r=run_check(stage,[rid],root,'check')
    assert proc.returncode!=0,name
    issues=r['issues'] if r else []
    assert expected in issues or (not r and proc.stderr), (name,expected,issues,proc.stderr)
    negative.append({'case':name,'record_id':rid,'rejected':True,'exit_code':proc.returncode,'expected_issue':expected,'issues':issues,'stderr':proc.stderr})
def page_replace(old,new):
    def mutate(stage,page,c):
        h=page.read_text();assert old in h;page.write_text(h.replace(old,new,1))
    return mutate
for rid in IDS:
    c=CONFIG[rid]
    for which in ['first','middle','final']:
        abstract=c['abstract'].split('\n\n');part_index=-1 if which=='final' else 0
        sentences=re.split(r'(?<=\.)\s+',abstract[part_index]);ix=0 if which=='first' else len(sentences)//2 if which=='middle' else -1
        omitted=sentences.pop(ix);altered=' '.join(sentences)
        alter_case(rid+'-abstract-'+which,rid,page_replace('<p>'+escape(abstract[part_index])+'</p>','<p>'+escape(altered)+'</p>'),rid+': abstract')
    alter_case(rid+'-wrong-citation-doi',rid,page_replace('name="citation_doi" content="'+c['doi']+'"','name="citation_doi" content="10.5281/zenodo.0"'),rid+': citation_doi')
    # Generic JSON-LD comparison must reject altered public edition metadata.
    if c['version'] is None:old='"creativeWorkStatus": "Unrefereed preprint"';new='"version": "1.0", '+old
    else:old='"version": "'+c['version']+'"';new='"version": "v0"'
    alter_case(rid+'-invented-version',rid,page_replace(old,new),rid+': jsonld')
    alter_case(rid+'-canonical-omission',rid,page_replace('<link rel="canonical" href="'+c['canonical_url']+'">',''),rid+': canonical')
    def drop_index(stage,page,c):
        index=stage/'research/index.html';index.write_text(index.read_text().replace('href="/research/'+c['slug']+'/"','href="/research/omitted/"'))
    alter_case(rid+'-index-omission',rid,drop_index,rid+': index_entry')
    def drop_sitemap(stage,page,c):
        sitemap=stage/'research/sitemap.xml';sitemap.write_text(sitemap.read_text().replace('<loc>'+c['canonical_url']+'</loc>','<loc>https://aleckriebel.com/research/omitted/</loc>'))
    alter_case(rid+'-sitemap-omission',rid,drop_sitemap,rid+': sitemap')
    for key in ['pdf_filename','supplement_filename']:
        def damage(stage,page,c,key=key):
            asset=page.parent/c[key];asset.write_bytes(asset.read_bytes()+b'\nprivate negative control\n')
        alter_case(rid+'-corrupt-'+key,rid,damage,rid+': '+key)
for rid,old,new in [('23203100','>6 October 2026</time>','>7 October 2026</time>'),('22089807','>25 August 2026</time>','>8 August 2026</time>')]:
    alter_case(rid+'-wrong-visible-date',rid,page_replace(old,new),rid+': rendered_date_label')
alter_case('bosonic-secrecy-convention-mixing','23203100',page_replace('Consumed private communication and key V=(J,S_B) are traced out','Consumed private communication and key V=(J,S_B) are protected jointly'), '23203100: literal_and_generated_secrecy_distinguished')
alter_case('bosonic-independent-lambda','23203100',page_replace('Choose one common λ','Choose separate parameters'), '23203100: six_exact_inequalities_common_lambda')
alter_case('amplifier-unrestricted-optimum','22089807',page_replace('optimal among fixed positive σ and λ','optimal over all graph families'),'22089807: lower_bound_and_restricted_response_optimum')
alter_case('amplifier-reversed-quantifiers','22089807',page_replace('All weights are fixed before r is quantified','Weights may depend on the fitness'),'22089807: fixed_fitness_eventual_quantifier')
save('negative-controls.json',{'utc':now(),'status':'PASS','controls_rejected':len(negative),'cases':negative})

# Authority mutations use copied bytes and an intercepted read-only path
# resolver. No original config/source/receipt/report/clearance is ever modified.
spec=importlib.util.spec_from_file_location('owned_bosonic_adapter',O/'bosonic_source.proposed.py');adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
p=R/'papers/23203100';c=CONFIG['23203100'];g=json.loads((p/'promotion.json').read_text());original=adapter.contained_file
authority=[]
def reject_authority(name,relative=None,transform=None,config_transform=None,gate_transform=None):
    cc=copy.deepcopy(c);gg=copy.deepcopy(g);redirect={}
    if relative:
        source=(R/relative) if relative.startswith('verification/') else p/relative
        data=source.read_bytes();changed=transform(data);target=O/'authority-negative'/name/source.name;target.parent.mkdir(parents=True);target.write_bytes(changed);redirect[source.resolve()]=target
    if config_transform:config_transform(cc)
    if gate_transform:gate_transform(gg)
    def read(root,relative):
        actual=original(root,relative);return redirect.get(actual,actual)
    adapter.contained_file=read
    try:
        adapter.bosonic_source_view(p,cc,gg)
    except (AssertionError,ValueError,KeyError,TypeError) as error:
        authority.append({'case':name,'rejected':True,'error_type':type(error).__name__,'source_mutated':False})
    else:raise AssertionError('Authority mutation accepted: '+name)
    finally:adapter.contained_file=original
reject_authority('raw-list-schema','sources/record/transport_receipts.json',lambda b:json.dumps({'files':json.loads(b)}).encode())
reject_authority('raw-transport-status','sources/record/transport_receipts.json',lambda b:b.replace(b'"status": 200',b'"status": 404',1))
reject_authority('api-record-bytes','sources/record/zenodo_record.json',lambda b:b+b' ')
reject_authority('source-pdf-bytes','sources/assets/paper.pdf',lambda b:b+b' ')
reject_authority('source-zip-bytes','sources/assets/zenodo-upload-kit.zip',lambda b:b+b' ')
reject_authority('root-authority-bytes','verification/root-clearance-23203100-20261025.json',lambda b:b+b' ')
for role,v in g['reviews'].items():
    reject_authority('report-'+role,v['report'],lambda b:b+b' ')
    reject_authority('verdict-'+role,v['verdict_file'],lambda b:b+b' ')
reject_authority('invented-version',config_transform=lambda cc:cc.update(version='1.0'))
reject_authority('receipt-binding',config_transform=lambda cc:cc['source_binding'].update(receipt_sha256='0'*64))
reject_authority('promoted-root-rewrite',gate_transform=lambda gg:gg['root_clearance_record'].update(approved_scope='rewritten'))
reject_authority('scope-custom-verdict-rewrite',gate_transform=lambda gg:gg['reviews']['scope']['verdict'].update(status='PASS'))
save('authority-negative-controls.json',{'utc':now(),'status':'PASS','controls_rejected':len(authority),'cases':authority,'raw_source_paths_preserved':True})

bindings={}
for name in ['inputs-before.json','amplifier-inputs-before.json']:bindings.update(json.loads((O/name).read_text())['files'])
changed=[path for path,b in bindings.items() if not Path(path).is_file() or sha(Path(path))!=b['sha256'] or Path(path).stat().st_size!=b['bytes']]
assert not changed,changed
prior=json.loads((Q/'stage-readiness-manifest.json').read_text())
assert len(prior['input_bindings'])==5654 and all(sha(Path(p))==b['sha256'] for p,b in prior['input_bindings'].items())
assert all(sha(Q/p)==b['sha256'] for p,b in prior['artifacts'].items())
readiness=R/'verification/local-braid-wave-cantor-20261025/readiness-manifest.json';live=json.loads(readiness.read_text())
assert sha(readiness)=='78473ab6ccd0564084f753f716d2f0af095c5af31366f94f4acad5466a2cd0e4'
assert len(live['files'])==51 and all(sha(Path(x['path']))==x['sha256'] for x in live['files'])
save('stage-validation.json',{'utc':now(),'completion_percent':95,'status':'PASS','input_bindings_checked':len(bindings),'all_inputs_unchanged':True,'prior_quadratic_5654_inputs_and_186_outputs_unchanged':True,'live47_readiness51_unchanged':True,'target_checks':{rid:len(report['papers'][rid]['checks']) for rid in IDS},'negative_stage_controls_rejected':len(negative),'authority_controls_rejected':len(authority),'all_46_legacy_dispatches_equal':True,'three_actual_versioned_render_comparisons_byte_identical':True,'index_count':50,'sitemap_count':51,'production_mutation':False,'live_http_or_browser_or_native_publication_pass':False})
print(json.dumps({'status':'PASS','checks':{rid:len(report['papers'][rid]['checks']) for rid in IDS},'stage_negatives':len(negative),'authority_negatives':len(authority),'unchanged_inputs':len(bindings)}))
