"""Single fixed data-only copy/custody comparison. No source/producer code, network or Git execution."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import datetime, hashlib, json, re, stat

R=Path(__file__).resolve().parent; P=R.parents[1]
S=P/'papers/23205181/sources'
W=P/'verification/dyadic-random-cone-editorial-sol-20261116'

def need(test,message):
    if not test: raise RuntimeError(message)

def pin(p,root=None):
    st=p.lstat(); need(stat.S_ISREG(st.st_mode),'not regular: '+str(p)); b=p.read_bytes()
    return dict(path=p.relative_to(root).as_posix() if root else str(p),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=stat.S_IMODE(st.st_mode))

def inventory(root):
    files=[]; dirs=[]
    for p in sorted(root.rglob('*')):
        st=p.lstat()
        if stat.S_ISREG(st.st_mode): files.append(pin(p,root))
        elif stat.S_ISDIR(st.st_mode): dirs.append(dict(path=p.relative_to(root).as_posix(),mode=stat.S_IMODE(st.st_mode)))
        else: raise RuntimeError('unexpected topology: '+str(p))
    return files,dirs

def create(name,value):
    with (R/name).open('x') as f: f.write(value)

def save(name,value): create(name,json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def sha_table(path):
    result={}
    for line in path.read_text().splitlines():
        digest,name=line.split('  ',1)
        if name.startswith('./'): name=name[2:]
        need(name not in result,'duplicate hash path')
        result[name]=digest
    return result

for n in ('CUSTODY_COMPARISON.json','STATIC_COMPARISON.json','REPORT.md','MANIFEST.json','FINAL.json'):
    need(not (R/n).exists(),'already complete: '+n)
need(pin(R/'INITIAL_SEAL.json')['SHA256']=='c3773851f5fcfcd9494dfce149f6b66d2d4493a3bd03363aab26f3556fa715be','own INITIAL seal drift')
need(pin(R/'INITIAL_MANIFEST.sha256')['SHA256']=='8a14ebb2bb900597ed77cc84dd8d274936554a090e7f4827f1e38318bf3c0ea8','own INITIAL manifest drift')
iseal=json.loads((R/'INITIAL_SEAL.json').read_text())
need(pin(R/'INITIAL_SEAL.json')['mode']==int(iseal['extent']['terminal_seal_mode'],8) and pin(R/'INITIAL_SEAL.json')['bytes']==3951,'own INITIAL terminal metadata drift')
ih=sha_table(R/'INITIAL_MANIFEST.sha256'); need(len(ih)==21,'own INITIAL payload count')
for name,digest in ih.items(): need(pin(R/name)['SHA256']==digest,'own INITIAL payload drift: '+name)
for line in (R/'INITIAL_PAYLOAD_MODES_BYTES.txt').read_text().splitlines():
    mode,size,name=line.split(maxsplit=2); name=name[2:] if name.startswith('./') else name
    q=pin(R/name); need(q['mode']==int(mode,8) and q['bytes']==int(size),'own INITIAL mode/size drift')
for key in ('manifest','payload_mode_byte_table','directory_table'):
    q=iseal[key]; actual=pin(R/q['path'],R)
    need(actual['bytes']==q['bytes'] and actual['mode']==int(q['mode'],8) and actual['SHA256']==q['SHA256'],'own INITIAL control metadata drift')
need(stat.S_IMODE(R.lstat().st_mode)==493 and stat.S_IMODE((R/'original-objects').lstat().st_mode)==493,'own INITIAL directory mode drift')
initial=[pin(R/n,R) for n in iseal['extent']['all_paths']]
need(len(initial)==23,'own INITIAL full extent differs')

sh=sha_table(R/'SOURCE_ALL_FILES.sha256'); sf,sd=inventory(S)
need(len(sf)==69 and len(sd)==10 and {q['path']:q['SHA256'] for q in sf}==sh,'source buffers or finite namespace drift')
sm={}
for line in (R/'SOURCE_FILE_MODES_BYTES.txt').read_text().splitlines():
    mode,size,name=line.split(maxsplit=2); name=name[2:] if name.startswith('./') else name
    sm[name]=(int(mode,8),int(size))
need({q['path']:(q['mode'],q['bytes']) for q in sf}==sm,'source file mode/size drift')
dm={}
for line in (R/'SOURCE_DIRECTORY_MODES.txt').read_text().splitlines():
    mode,name=line.split(maxsplit=1); name=name[2:] if name.startswith('./') else name
    dm[name]=int(mode,8)
need(dict([('.',stat.S_IMODE(S.lstat().st_mode))]+[(q['path'],q['mode']) for q in sd])==dm,'source directory modes/namespace drift')
need(pin(W/'FINAL.json')['SHA256']=='bd15c4b344ac07c909b3d7172477e930c359a52b08d45856bad88e86e5c8561c','writer FINAL differs')
need(pin(W/'OWNED_MANIFEST.json')['SHA256']=='204e686e581416204ccd6189c01ca3c8e8c4e54b504320f0762e1631187756ed','writer manifest differs')
need(pin(W/'FINAL.json')['mode']==pin(W/'OWNED_MANIFEST.json')['mode']==420,'writer terminal control mode differs')
wm=json.loads((W/'OWNED_MANIFEST.json').read_text()); wf,wd=inventory(W)
need([q for q in wf if q['path'] not in ('FINAL.json','OWNED_MANIFEST.json')]==wm['files'],'writer payload bytes/modes/namespace differ')
need(wd==wm['directories'] and len(wf)==23 and len(wd)==3 and stat.S_IMODE(W.lstat().st_mode)==wm['root_mode'],'writer finite topology differs')
page=W/'candidate/research/sharp-dyadic-threshold-random-cone/index.html'
need(pin(page)['SHA256']=='3447bd350c42a95ea6421b9685c234cfee1823e3a175435151e9c9dd6e5d97f4','page handoff differs')
need(pin(W/'MODEL.json')['SHA256']=='5df0cfd825c89f35f59b3f9b484b9537f87c83c88fba15b1b2ceafe12e7d5279','model handoff differs')
m=json.loads((W/'MODEL.json').read_text()); a=json.loads((W/'SOURCE_AUTHORITY.json').read_text())
record=json.loads((S/'record.response.body').read_text()); files_api=json.loads((S/'files-23205181.response.body').read_text())
need(a['native_record']==record and a['native_files_API']==files_api and m['native_metadata']==record['metadata'],'whole native metadata/Description/wrappers differ')
for key in ('root_clearance','root_review','record','files_API','controlling_TeX'):
    q=a[key]; actual=pin(Path(q['path'])); need(actual==q,'writer source authority pin differs: '+key)
for q in a['rights_files']: need(pin(Path(q['path']))==q,'rights source pin differs')
need(a['root_clearance']['SHA256']=='0630fbf063143c523587b695fcd35a395358a2ef3a1e5968bb83f1910ec054f5','root authority differs')
need(m['title']==record['metadata']['title'] and m['native_version']==record['metadata']['version'] and m['publication_date']==record['metadata']['publication_date'],'native title/version/date differ')
need(m['native_record_created']==record['created'] and m['native_record_updated']==record['updated'] and m['printed_version'] is None,'record/printed distinction differs')
need(all(m[k] is None for k in ('canonical_url','base_url','production_url','AA','follow_up')) and m['publication_authority'] is False,'private/null/followup gate differs')
need(m['native_files_explicit_order_value']==files_api['order']==[],'literal native ordering wrapper differs')
assets=[]
for q,rf in zip(m['native_files_returned_order'],record['files']):
    need(q['name']==rf['key'],'native entry order differs')
    src=S/'assets'/q['name']; dest=page.parent/q['name']; b=src.read_bytes()
    need(dest.read_bytes()==b and len(b)==q['bytes']==rf['size'],'native whole asset bytes differ')
    need('md5:'+hashlib.md5(b).hexdigest()==q['MD5']==rf['checksum'],'native asset checksum differs')
    need(pin(dest)['mode']==pin(src)['mode']==q['mode'],'native asset mode differs')
    assets.append(dict(source=pin(src,S),candidate=pin(dest,W)))
need(len(assets)==2,'native asset count differs')
css=W/'candidate/research/research.css'
need(pin(css)['bytes']==1170 and pin(css)['SHA256']=='f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a','shared stylesheet differs')
tex=(S/'published-source/container-001/tree/main.tex').read_text()
raw=re.search(r'\\begin\{abstract\}\n(.*?)\\end\{abstract\}',tex,re.S).group(1)
need(raw==m['native_abstract_tex'],'whole raw native TeX abstract differs')
abstract=' '.join(raw.replace('$','').replace('\\ge','≥').split())
need(abstract==m['complete_original_abstract'],'complete rendered abstract differs')

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.ids=[];self.links=[];self.metas={};self.iframe=[];self.bases=[];self.canons=[];self.scripts=[];self.abs=[];self.capture=None;self.script=False;self.schema=[]
    def handle_starttag(self,tag,attrs):
        q=dict(attrs)
        if 'id' in q:self.ids.append(q['id'])
        if q.get('id')=='original-abstract':self.capture=tag
        if tag=='meta':self.metas[q.get('name',q.get('property'))]=q.get('content')
        if tag=='iframe':self.iframe.append(q.get('src'))
        if tag=='base':self.bases.append(q)
        if tag=='link' and q.get('rel')=='canonical':self.canons.append(q)
        if tag=='script':self.scripts.append(q.get('type'));self.script=True
        for key in ('href','src'):
            if key in q:self.links.append(q[key])
    def handle_endtag(self,tag):
        if tag==self.capture:self.capture=None
        if tag=='script':self.script=False
    def handle_data(self,data):
        if self.capture:self.abs.append(data)
        if self.script:self.schema.append(data)

html=page.read_text(); v=Inspect();v.feed(html)
sch=json.loads(''.join(v.schema));need(sch==m['schema'],'actual/model scholarly JSON differ')
need(' '.join(''.join(v.abs).split())==abstract==sch['abstract']==v.metas['DC.description'],'visible/schema/DC complete abstract differ')
need(len(v.ids)==len(set(v.ids)) and v.scripts==['application/ld+json'],'duplicate id or active script')
need(set(v.metas['robots'].split(','))=={'noindex','nofollow'} and not v.bases and not v.canons and 'og:url' not in v.metas,'private wrapper differs')
need(not any(k in sch for k in ('url','@id','mainEntityOfPage')),'active site schema identity')
need(v.metas['citation_title']==record['metadata']['title'] and v.metas['citation_version']=='1.0' and v.metas['citation_doi']==record['doi'],'citation native identity differs')
need(v.metas['citation_publication_date']=='2026/10/06' and sch['datePublished']=='2026-10-06' and sch['dateCreated']==record['created'],'publication/record dates differ')
need(v.metas['citation_pdf_url']==record['files'][0]['links']['self'],'private native PDF citation differs')
head=(W/'HEAD.html').read_text();main=(W/'MAIN.html').read_text()
need(html.count(head)==html.count(main)==1,'standalone head/MAIN not whole exact buffers in page')
need(head.strip()==re.search(r'<head>(.*?)</head>',html,re.S).group(1).strip(),'HEAD omits part of full head')
need(main.strip()==re.search(r'<main\b.*?</main>',html,re.S).group(0).strip(),'MAIN omits part of full MAIN')
local=[];outside_root_navigation=[]
for link in v.links:
    u=urlsplit(link)
    if not u.scheme and not u.netloc:
        if u.path.startswith('/'):
            need(u.path in ('/','/research/'),'unexpected root navigation');outside_root_navigation.append(link);continue
        if u.path:
            p=(page.parent/unquote(u.path)).resolve();need(p.is_relative_to(W/'candidate'),'relative link escapes private candidate')
            need(p.is_file(),'local file missing: '+link);local.append(dict(link=link,pin=pin(p,W)))
        elif u.fragment:need(u.fragment in v.ids,'local fragment missing')
need(len(v.iframe)==1 and urlsplit(v.iframe[0]).path=='paper.pdf','unchanged local PDF embed differs')
need(v.links.index('paper.pdf')<v.links.index('source-and-audit.zip'),'visible native order differs')
need((W/'citation.bib').read_bytes()==(page.parent/'citation.bib').read_bytes(),'Bib copies differ')
bib=(W/'citation.bib').read_text();need(all(s in bib for s in (record['metadata']['title'],record['doi'],'{1.0}','{2026}','{6}')),'Bib native fields differ')
need((W/'assembly.exit').read_text().strip()=='0' and (W/'assembly.stderr').read_bytes()==b'','actual producer stream/exit differs')
need('Original Zenodo description' not in main and 'ROOT_REVIEW' not in main and 'INITIAL_SEAL' not in main,'public duplicate/internal narrative')
for n in ('COMPARISON.stdout.txt','COMPARISON.stderr.txt'):need((R/n).read_bytes()==b'','nonempty own literal stream')
wf2,wd2=inventory(W);sf2,sd2=inventory(S)
need(wf2==wf and wd2==wd and sf2==sf and sd2==sd,'writer/source drift during comparison')
need([pin(R/n,R) for n in iseal['extent']['all_paths']]==initial,'own INITIAL drift during comparison')
need(all(stat.S_IMODE(p.lstat().st_mode)==493 for p in (W,S,R,R/'original-objects')),'root or original INITIAL directory mode drift')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
save('CUSTODY_COMPARISON.json',dict(UTC=now,writer_root=str(W),writer_files=wf,writer_directories=wd,source_root=str(S),source_files=sf,source_directories=sd,
    original_INITIAL_files=initial,original_INITIAL_directories=[dict(path='original-objects',mode=493)],all_writer23_source69_INITIAL23_buffers_modes_namespace_exact_before_after=True,
    root_modes=dict(writer=stat.S_IMODE(W.lstat().st_mode),source=stat.S_IMODE(S.lstat().st_mode),owned=stat.S_IMODE(R.lstat().st_mode))))
save('STATIC_COMPARISON.json',dict(UTC=now,status='PASS_FIXED_PRIVATE_COPY_DATA',ordinary_comparisons=1,all_writer23files3dirs_and_source69files10dirs_and_INITIAL23files1dir_authenticated=True,
    whole_actual_HEAD_MAIN_in_page_exact=True,raw_native_TeX_abstract_and_complete_visible_schema_DC_exact=True,whole_native_record_Description_wrappers_rights_pins_exact=True,
    native_assets=assets,all_native_bytes_modes_MD5_order_exact=True,shared1170CSS_exact=True,local_file_links=local,root_navigation_not_opened=outside_root_navigation,
    private_noindex_inactive_canonical_base_prod_AA_and_followup_null=True,Bib_native_identity_and_two_copies_exact=True,
    iframe=v.iframe[0],FitH_note='Observed presentation convention only; neither a scientific defect nor an explicit user requirement',
    manual_semantic_disposition='PASS full cleared threshold/construction/classical embedding/right-module consequences and boundaries after whole actual page/model/source reading',
    no_new_proof_or_runtime_reader_certificate=True,producer_helpers_or_science_native_old_code_executed=False,network_W_Git_Sheet_CUA_deploy_outreach_actions=False,
    own_stdout_bytes=0,own_stderr_bytes=0))
create('REPORT.md','# Row177 /23205181 private copy-fact review\n\n**PASS for the fixed private copy under the actual full-original clearance.** No factual/scientific correction is required. The source contract was sealed before producer discovery; this is informed editorial fidelity, not another independent scientific proof or publication authority. Prior shared row164 construction exposure and reuse of all7personally viewed clean root source pixels are disclosed.\n\nI read the entire448line original TeX, all7PDFtext pages/pixels, complete native metadata/Description/rights and whole root clearance/review before the candidate. After actual READY I read the complete17685byte HTML, whole9775byte model, separate whole HEAD/MAIN/Bib, complete native objects in SOURCE_AUTHORITY, actual provenance/read/build receipts/streams and full writer report. Producer helper bodies were not used as evidence or executed.\n\nThe copy retains every central cleared claim: least dyadic q≥4 is32 for every allowed pairing in the unchanged seven-extra squared-turn model, exact upper word-sum factor/exponent and positive lower growth at4,8,16; full transported existential construction with at most532generators, finite2D K(G,1), torsion-free finite presentation and scalar ab=1,ac=0,c≠0; classical two-generator HNN realization preserving finite2D classifying space; scalar idempotent e=1−ba and nonzero cyclic projective RIGHT module P=eS, S≅S⊕P and[P]=0 without P=0 or K₀(S)=0, over every characteristic-two field. The finite2D complex also retains finite presentability of H. No global-model optimum, other-characteristic, C*-projection or numerical matching/presentation/product certificate is promised. Turn weights are correctly distinguished from probabilities of words.\n\nSubstantive OpenAI October4input is prominent, September23lineage is credited, HNN/ring/module mechanisms and earlier triage are identified as classical/inherited, and no firstness is asserted. The original existential limitation, lack of full formalization/human refereeing, extensive AI disclosure, passive actual-contribution collaboration and follow-up null remain. No audit-count/date-log replay or duplicate nativeDescription is introduced publicly.\n\nThe sole fully read own data-only comparison passed. Complete writer23files/3dirs, source69files/10dirs and original INITIAL23files/1dir are authenticated with all buffers, modes, exact namespaces and terminal controls, unchanged before/after. Full original abstract is exact in native TeX and complete visible/schema/DC rendering. Both returned-order native assets are byte/mode/checksum exact, raw metadata/Description/wrappers and actual rights pins agree,1170CSS is unchanged, standalone HEAD/MAIN are complete exact page buffers, local assets/fragments and Bib copies/fields agree. Native6October publication/version1.0 versus7October record creation and no printed numeric version are preserved; schema dateCreated uses that explicit native record timestamp. CC BY4authored prose/data and MITnewPython/upstream retained rights agree with actual files.\n\nPrivate metadata is correctly noindex with no active canonical/base/site identity/production/AA; DOI and native citation/encoding URLs refer to the existing Zenodo publication. Those URLs require the separate later production wrapper adaptation already identified by the writer, not a correction to this private packet. The observed paper.pdf#view=FitH is a useful presentation convention, not an explicit user requirement or a scientific gate. No presentation correction is required. External/root navigation was not opened; no link-liveness claim is made.\n\nReader/runtime limits remain: no HTML render, native PDF-reader/iframe display, mobile/download/live or deployment certification; no new primary acquisition, native scientific/old/producer-helper replay, W/Git/Sheet/network/CUA/deploy/source/older-packet mutation or outreach. Own comparison exited0 with literal empty stdout/stderr. This fact PASS is private data/copy evidence for root adoption, not root adoption itself, new science, canonical/AA activation or production authority. No follow-up. Packet frozen and quiescent after FINAL.\n')
with (R/'POST_INITIAL_LOG.md').open('a') as f:f.write('\n- '+now+' — 100%: sole fully read data-only comparison passed; writer23/3, source69/10 and INITIAL23/1 exact. Manual copy fidelity PASS, no correction required. Literal streams empty; no reader/live or publication claim. Finite FINAL next, then quiescent.\n')
files,dirs=inventory(R)
save('MANIFEST.json',dict(UTC=now,schema='whole-copy-fact-final-manifest-v1',files=files,directories=dirs,root_mode=stat.S_IMODE(R.lstat().st_mode),exact_terminal_controls=['MANIFEST.json','FINAL.json'],includes_ignored_empty_bytes_modes=True))
save('FINAL.json',dict(UTC=now,schema='informed-private-copy-fact-final-v1',record=23205181,row=177,status='FROZEN_PASS_PRIVATE_COPY_FACT',required_corrections=[],
    report=pin(R/'REPORT.md',R),manifest=pin(R/'MANIFEST.json',R),static_comparison=pin(R/'STATIC_COMPARISON.json',R),custody_comparison=pin(R/'CUSTODY_COMPARISON.json',R),
    original_INITIAL_seal=pin(R/'INITIAL_SEAL.json',R),writer_FINAL=pin(W/'FINAL.json',W),writer_manifest=pin(W/'OWNED_MANIFEST.json',W),writer_page=pin(page,W),writer_model=pin(W/'MODEL.json',W),
    full_writer23_3_source69_10_INITIAL23_1_authenticated_unchanged=True,own_data_comparison_invocations=1,own_exit=0,literal_stdout=pin(R/'COMPARISON.stdout.txt',R),literal_stderr=pin(R/'COMPARISON.stderr.txt',R),
    informed_not_new_independent_proof=True,prior_exposure_disclosed=True,producer_or_native_science_code_executed=False,follow_up=None,
    publication_Git_W_Sheet_network_CUA_deploy_contact_or_outreach_authority=False,no_new_render_native_reader_live_download_certificate=True,
    completion_percent_copy_fact=100,extent=dict(regular_files=len(files)+2,child_directories=len(dirs),all_paths=sorted([q['path'] for q in files]+['MANIFEST.json','FINAL.json']),directories=dirs),
    all_writes_confined_to_owned_folder=True,quiescent_after_seal=True,terminal_self_hash_excluded=True))
ef,ed=inventory(R);need(len(ef)==len(files)+2 and ed==dirs,'own final extent drift')
for q in files:need(pin(R/q['path'],R)==q,'own payload drift while sealing')
