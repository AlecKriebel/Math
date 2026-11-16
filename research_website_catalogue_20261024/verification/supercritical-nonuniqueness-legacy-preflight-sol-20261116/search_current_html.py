#!/usr/bin/env python3
"""One offline data-only current-HTML lookup; print receipt, write nothing."""
from pathlib import Path
import hashlib, html, json, re, stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
N = P/'verification/supercritical-nonuniqueness-legacy-preflight-sol-20261116'
PRIOR = P/'verification/annular-martin-legacy-preflight-sol-20261116/HTML_IDENTITY_LOOKUP.json'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def read(path):
    need(path.is_absolute() and '..' not in path.parts, 'absolute input')
    need(all(not p.is_symlink() for p in (path, *path.parents)), 'no symlink input')
    s = path.stat()
    need(stat.S_ISREG(s.st_mode), 'ordinary input')
    b = path.read_bytes()
    need((s.st_ino, s.st_size, s.st_mtime_ns) == (path.stat().st_ino, len(b), path.stat().st_mtime_ns), 'stable input')
    return b

def pin(b):
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}

def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def connector(name):
    packet = json.loads(read(N/name))
    need(packet.get('isError') is not True, 'successful GitHub read')
    return json.loads(packet['structuredContent']['content'])

def tree_oid(rows):
    parts = []
    for row in sorted(rows, key=lambda r: (r['path']+('/' if r['type']=='tree' else '')).encode()):
        need('/' not in row['path'] and row['type'] in ('blob','tree'), 'one-level tree entry')
        parts.append(row['mode'].lstrip('0').encode()+b' '+row['path'].encode()+b'\0'+bytes.fromhex(row['sha']))
    body = b''.join(parts)
    return hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()

ref = connector('OPEN_REF.connector.json')
commit = connector('OPEN_COMMIT.connector.json')
root = connector('OPEN_ROOT.connector.json')
docs = connector('OPEN_DOCS_RECURSIVE.connector.json')
need(ref['ref']=='refs/heads/main' and ref['object']['sha']==commit['sha'], 'current main commit')
need(root['sha']==commit['tree']['sha'] and root['truncated'] is False and tree_oid(root['tree'])==root['sha'], 'complete root tree identity')
need(next(r['sha'] for r in root['tree'] if r['path']=='docs' and r['type']=='tree')==docs['sha'], 'current docs membership')
need(docs['truncated'] is False and len(docs['tree'])==304, 'finite complete recursive docs tree')
need(len({r['path'] for r in docs['tree']})==304, 'unique recursive tree entries')
objects = {'': docs['sha'], **{r['path']:r['sha'] for r in docs['tree'] if r['type']=='tree'}}
for directory, oid in objects.items():
    children = []
    for row in docs['tree']:
        parent, _, name = row['path'].rpartition('/')
        if parent==directory:
            children.append({**row, 'path':name})
    need(tree_oid(children)==oid, 'whole docs tree object: '+directory)
current = sorted((r for r in docs['tree'] if r['type']=='blob' and r['path'].lower().endswith('.html')), key=lambda r:r['path'])
need(len(current)==47, 'exact47 current HTML bodies')
prior_raw = read(PRIOR)
need(pin(prior_raw)=={'bytes':52875,'SHA256':'0d055d0e7d0fed6517d27881365a6e75170f91c0537dedbcced6c37c5c286c00'}, 'frozen prior lookup')
prior = {r['path']:r for r in json.loads(prior_raw)['HTML_identity_rows']}
changed_packet = json.loads(read(N/'CHANGED_KNUDSON_BLOB.connector.json'))
changed = changed_packet['structuredContent']['content'].encode()
need(changed_packet.get('isError') is not True, 'fresh changed HTML GitHub read')

native_path = P/'papers/23573603/sources/record.response.body'
adoption_path = P/'verification/root-editorial-23573603-20261116.json'
model_path = P/'papers/23573603/reviews/editorial/PAGE_MODEL.json'
main_path = P/'papers/23573603/reviews/editorial/MAIN.html'
source_expected = [
    (native_path,10517,'f02f53780e411a3a4487d758619fecd9ccabab5de39694cf824682205845211c'),
    (adoption_path,3509,'9c8a2c7f3bc1e5cd1f914b0e3e6eb939711f73d7b2c85533f9f937e21e7c4bc4'),
    (model_path,6312,'85bfdafbe96c906c485689bc69e84a8b6c3afbc1d1f5bdcfa86ceb1ea2ed7780'),
    (main_path,13364,'02baf93b27cefe58761ce0daa06149d4352b73a748b3bcab14245b68ff2a3402')]
for path, size, digest in source_expected:
    need(pin(read(path))=={'bytes':size,'SHA256':digest}, 'whole source identity')
native=json.loads(read(native_path)); adoption=json.loads(read(adoption_path)); model=json.loads(read(model_path)); main=read(main_path)
need(native['id']==adoption['record_id']==model['record_id']==23573603, 'same native paper')
need(adoption['private_proposed_slug']==model['proposed_slug']=='supercritical-nonuniqueness-square-lattice', 'approved private slug')
need(adoption['AA'] is None and adoption['canonical_url'] is None and adoption['production_install_Git_deploy_or_tracker_authority'] is False, 'private adoption only')
need(pin(main)=={k:adoption['MAIN_file_includes_one_final_newline'][k] for k in ('bytes','SHA256')}, 'whole approved MAIN')
need(main.endswith(b'\n') and pin(main[:-1])==adoption['approved_exact_MAIN_fragment'], 'exact adopted MAIN fragment')
patterns = [
    ('complete native title',re.escape(native['metadata']['title'])),
    ('native record ID','23573603'),('concept ID','23573602'),
    ('native DOI',re.escape(native['doi'])),('concept DOI',re.escape(native['conceptdoi'])),
    ('supercritical','supercritical'),('nonuniqueness',r'non[\s\-‐‑–—]*uniqueness'),
    ('rough isometry',r'rough(?:ly)?[\s\-‐‑–—]*isometr'),
    ('Problem9.6',r'problem\s*9\s*\.\s*6'),
    ('PR1348',r'(?:pr\s*#?\s*1348|/pull/1348)'),
    ('10000037','10000037'),('AMR-099-0037',r'AMR[\s_\-]*099[\s_\-]*0037'),
    ('native asset/source alias',r'supercritical[\-_]nonuniqueness')]
rows=[]; hits=[]; reused=0; fetched=0
for row in current:
    path='docs/'+row['path']; previous=prior[path]
    if row['sha']==previous['Git_blob']:
        reference=previous['whole_body_authenticated_reference']; b=read(Path(reference['path']))
        need(pin(b)=={k:reference[k] for k in ('bytes','SHA256')}, 'exact cached whole HTML')
        reused+=1
    else:
        need(path=='docs/papers/knudson-gradient-path/index.html' and row['sha']=='7d981818a556c58b1fafae3310a57d2982a94cc1', 'only known changed HTML')
        b=changed; reference={'path':str(N/'CHANGED_KNUDSON_BLOB.connector.json'),'container':'structuredContent.content UTF-8'}; fetched+=1
    need(len(b)==row['size'] and blob(b)==row['sha'], 'current-tree whole HTML identity: '+path)
    raw=b.decode('utf-8'); text=' '.join(html.unescape(re.sub(r'<[^>]*>',' ',raw)).split())
    matches=[]
    for label, expression in patterns:
        found=[]
        for representation, value in [('whole raw HTML',raw),('entity-decoded tag-stripped whitespace-normalized text',text)]:
            all_matches=list(re.finditer(expression,value,re.I))
            if all_matches:
                found.append({'representation':representation,'total_matches':len(all_matches),'first_context':value[max(0,all_matches[0].start()-100):all_matches[0].end()+160]})
        if found:
            matches.append({'term':label,'evidence':found})
    result={'path':path,'Git_blob':row['sha'],**pin(b),'body_reference':reference,'matched_terms':matches}
    rows.append(result)
    if matches: hits.append(result)
need(reused==46 and fetched==1, '46 exact reused plus one fresh changed HTML')
print(json.dumps({'scope':'one full-body query over exact47 current docs HTML; no history/assets/PDF/ZIP search','main':commit['sha'],'root_tree':root['sha'],'docs_tree':docs['sha'],'tree_entries':304,'tree_objects_authenticated':len(objects),'HTML_count':47,'reused_unchanged_HTML':reused,'fresh_changed_HTML':fetched,'terms':[label for label,unused in patterns],'native_identity':{'title':native['metadata']['title'],'DOI':native['doi'],'concept_DOI':native['conceptdoi'],'version':native['metadata']['version'],'publication_date':native['metadata']['publication_date'],'created':native['created'],'related_identifiers':native['metadata']['related_identifiers']},'approved_private_MAIN_ids':re.findall(r'\bid="([^"]+)"',main.decode()),'rows':rows,'hits':hits,'private_target_slug':model['proposed_slug'],'target_public_live_AA_authority':False,'source_pins':[{'path':str(path),'bytes':size,'SHA256':digest} for path,size,digest in source_expected]},indent=2))
