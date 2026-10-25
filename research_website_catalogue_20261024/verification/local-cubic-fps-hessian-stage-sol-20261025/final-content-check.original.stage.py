"""Verify rendered research content. Supported source layouts are listed in TEX_PATHS.
Uses Python standard library plus an existing pdftotext executable; installs nothing.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
import json,hashlib,re,datetime,subprocess,zipfile,gzip,tarfile,zlib,unicodedata,argparse,sys
from html import unescape
sys.path.insert(0, '/Users/alec/Documents/Math/research_website_catalogue_20261024/scripts')
from published_assets import PublishedAssets, asset_name, normalized_receipt_view
from bosonic_source import bosonic_source_view
from dipole_source import dipole_source_view
parser=argparse.ArgumentParser(description='Read-only generated research-page checks; only QA reports are written.')
parser.add_argument('record_ids',nargs='*',default=['23539283','23577484'])
parser.add_argument('--site',type=Path,default=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public'))
parser.add_argument('--output-stem',default='final-content-check')
parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
args=parser.parse_args()
if not re.fullmatch(r'[a-zA-Z0-9_-]+',args.output_stem):parser.error('output-stem must be a simple filename stem')
R=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
if not args.output_dir.resolve().is_relative_to(R/'verification'):parser.error('output-dir must be inside verification')
S=args.site
TEX_PATHS={
 '23431676':'published-source/pr1097_support_v1_0/paper.tex',
 '23387442':'published-source/satoh_filtration_verification/satoh_filtration_counterexamples.tex',
 '23328912':'published-source/aim_5_2_source/preprint.tex',
 '23524971':'published-source/dfc_stability_verification/dfc_stability_verification/main.tex',
 '23572690':'published-source/bv-generators-source-and-verification/main.tex',
 '23539283':'published-source/free-product-tensor-core-verification/manuscript/main.tex',
 '23577484':'published-source/main.tex',
 '23310484':'published-source/manuscript.tex',
 '23331395':'published-source/paper.tex',
 '22770864':'published-source/kourovka_16_63/report/kourovka_16_63.tex',
 '22729537':'published-source/NMSC_Paper_A_Source/manuscript/main.tex',
 '21699161':'related-records/21699181/published-source/main.tex',
 '22089551':'published-source/bimolecular_positive_recurrence_submission_v1_2_4/manuscript/paper_content.tex',
 '22729545':'published-source/NMSC_Paper_B_Source/manuscript/main.tex',
 '23441523':'published-source/main.tex',
 '23356680':'published-source/note.tex',
 '23445342':'published-source/main.tex',
 '23387753':'published-source/note.tex',
 '23352246':'published-source/rational_mixed_integer_bipartite_covers_v1/research_note.tex',
 '23414025':'published-source/note.tex',
 '23390181':'published-source/note.tex',
 '23410944':'published-source/paper.tex',
 '23422055':'published-source/paper/note.tex',
 '23203334':'published-source/source-and-verification/main.tex',
 '22929486':'published-source/kourovka_16_45/proof.tex',
 '23088066':'published-source/paper.tex',
 '23353160':'published-source/grassmann_calibrations_v1/research_note.tex',
 '23147866':'w4_locc_dense_coding.tex',
 '23157237':'published-source/spectral-tensor-consistency/spectral_tensor_consistency.tex',
 '22729355':'published-source/Exact_Diffusion_Design_Source_v1.0.11/main.tex',
 '22136869':'published-source/k2p-k3p-theta-collision-19cf11f65ed4/combined-paper-clarified.tex',
 '23180194':'published-source/mass_stationarity_verification/paper.tex',
 '23127646':'published-source/biconstrained-asymmetry-verification/biconstrained-asymmetry-verification/biconstrained_asymmetry.tex',
 '23191301':'published-source/odd_power_sos_verification/paper.tex',
 '23127955':'published-source/paper.tex',
 '23430642':'published-source/rank_one_uniqueness_v1_0/paper.tex',
 '23387814':'published-source/seshadri_counterexample_verification/seshadri_counterexample.tex',
 '23431716':'published-source/paper.tex',
 '22089373':'published-source/Strong_Tree_Childness_Sharp_Level2_JC_source/paper/main.tex',
 '23444839':'published-source/main.tex',
 '23592692':'published-source/main.tex',
 '23441906':'published-source/simple-brace-counterexample-source-and-verification/main.tex',
 '23431313':'published-source/paper.tex',
 '23393596':'published-source/deep-derived-pure-braids-source-verification-v1.0/note.tex',
 '23358014':'published-source/critical_wave_verification/manuscript/critical_wave_growth.tex',
 '23356964':'published-source/generic-wreath-hyperfiniteness-verification/note.tex',
 '23203100':'extracted/zenodo-upload-kit/manuscript/main.tex',
 '22089807':'published-source/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/main.tex',
 '23390551':'cache/extracted/dipole_spectrum.tex',
 '23430326':'support/paper.tex',
 '23444606':'published-source/initial-omnific-models-source-and-verification/main.tex',
 '23440119':'support/main.tex',
 '23224103':'support/brownian_first_visit.tex',
 '23383961':'published-source/verification_package/support_slit_verification/support_slit.tex',
 '23430906':'support/paper.tex',
 '23306332':'published-source/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics_verification/nonunique_nearest_stable_complex_quadratics.tex',
}
DIPOLE_LANGLANDS_IDS={'23390551','23430326'}
def normalized_dipole_langlands_abstract(rid,body):
 if rid=='23390551':
  replacements=[("Costabel's",'Costabel’s'),('Costabel--Dauge--Nedaiasl','Costabel–Dauge–Nedaiasl'),('Hilbert--Schmidt','Hilbert–Schmidt'),(r'$10^{-4}$','10⁻⁴'),(r'$n^{-1}\Z^3$','n⁻¹ℤ³'),(r'$3\times3$','3 × 3')]
 else:
  replacements=[(r'$F=\Q_3$','F=ℚ₃'),('$E/F$','E/F'),('$[4,6],[2,5],[3,3],[1,4],[0,2]$','[4,6],[2,5],[3,3],[1,4],[0,2]'),(r'$\GL_{15}(E)$','GL₁₅(E)'),('Feigon--Lapid--Offen','Feigon–Lapid–Offen'),(r"Lapid--M\'inguez",'Lapid–Mínguez'),('$k=1$','k=1'),('Luo--Zha','Luo–Zha'),(r'\href{https://doi.org/10.1007/s11464-025-0256-0}{10.1007/s11464-025-0256-0}','10.1007/s11464-025-0256-0'),(r'\textbf{UNKNOWN}','UNKNOWN')]
 for old,new in replacements:body=body.replace(old,new)
 if '\\' in body or '$' in body:raise ValueError('Unrecognized dipole/Langlands abstract command')
 return ' '.join(body.split())

def dipole_archive_inventory(archive_path,source_root):
 from io import BytesIO
 rows=[];nested=[];readers=[];layers=[];safe=True
 def visit(data,base,depth,prefix=''):
  nonlocal safe
  layers.append(depth)
  with zipfile.ZipFile(BytesIO(data)) as archive:
   names=set()
   for item in archive.infolist():
    if item.is_dir():continue
    relative=Path(item.filename)
    if relative.is_absolute() or '..' in relative.parts or item.filename in names:raise ValueError('Unsafe recursive archive member')
    names.add(item.filename);payload=archive.read(item);target=base/relative
    if target.is_symlink() or not target.resolve().is_relative_to(source_root.resolve()):raise ValueError('Unsafe extracted recursive member')
    safe=safe and target.read_bytes()==payload
    row={'member':prefix+item.filename,'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload),'source':str(target)};rows.append(row)
    if item.filename.lower().endswith('.pdf'):readers.append(row)
    if item.filename.lower().endswith('.zip'):
     nested.append(row);visit(payload,Path(str(target)+'.expanded'),depth+1,prefix+item.filename+'!/')
 visit(archive_path.read_bytes(),source_root,1)
 return {'rows':rows,'nested':nested,'readers':readers,'layers':max(layers),'all_member_bytes_match':safe,'unique_hashes':len({x['sha256'] for x in rows}),'hidden':sum(any(part.startswith('.') for part in x['member'].replace('!/', '/').split('/')) for x in rows)}

DL_PINS={'23390551': {'publication': '1d7df178ea6f314425bcb1a6a0bc5373ebdb120dcf6b9c21ff4c6198bed4c10c', 'promotion': 'fe19f1d535b20f4dc2bbeb71a4d91593a168194c4d7b6ce4fb9e8dfbdf67857d', 'root': '4c727e1b34afddf6804c9b0954f6706868f45b697bdad9697471d8205eedd16a', 'editorial': '48d1e4cc76a09d099aa614b37c9dec8c4d64bbd89668e8fffe94f176465de6e3', 'seal': 'fc5b275e2e172d11fa11f594be569b562a504291bc36f9f7156fcc50cce2dcaf', 'tex': '5d1145a052135d34997614be42142f9b63ef76730ca9992e045d52548747dd7e', 'receipt': 'a2ee05395c76c0478ba4b06671cc7fbdd466604a12446e92495597106880a81f', 'metadata': '006d05e2d9db6331bf5ea07716fd79b59a2f998cdaaf9951ba38ca079e15e532', 'created': '2026-10-15T09:25:22.728191+00:00', 'pages': 11, 'display_date': '15 October 2026'}, '23430326': {'publication': '46dd56b81011798e0034fb434af5d5c45b26c718a120d5de94afc38b585e2d05', 'promotion': 'bceb30a3f9febeaa9809c5abf65192eeed51273e96c595ccd621a3abd7186908', 'root': 'ca0ea2a7b0ecf7243d8e23b2ed1aa7e18e9890ff28c786e468237e052c118dbf', 'editorial': 'b02dd9a24c58f6e99d33ba5887695c3164d87b76759af62ba3ea861146ed45bd', 'seal': '8cb4bba5816f303ee01722f03b73da33e2d21c73860ceb8580619a9d49a98869', 'tex': '34af8011ff03036283dae6ae51b9a4ddee9410026b29e6988b00ccda2576fbf6', 'receipt': 'b3ff10e63b0062748ca9f1c633df4aa1873daeedd9cd91f7a9ff7712ccb36b02', 'metadata': '3f1cefb024d648c866e61a9e67289398dc263b7dfd2895eba56a1514a748280e', 'created': '2026-10-17T04:42:23.636225+00:00', 'pages': 9, 'display_date': '16 October 2026'}}
SURREAL_CONE_BROWNIAN_IDS={'23444606','23440119','23224103'}
SCB_PINS={'23444606': {'publication': '5d51c3f2a89a9ebde5a3bc4213fe5502f7cd9e80bd739206aa3399407369edb8', 'promotion': 'c5f5ea046d6b387b42775aaf1d9199719315f42794206604f3bab45e363118b4', 'root': '8f9acb77adf26af8699a42bfdc1f706e2c77978ae722083f8be50d63f8e89aa1', 'editorial': '04b1718d780eadd55fc39ec3dd2c4f4d410c6470b49d8773df3c0099f42f8bc2', 'seal': '039a360667deef3b79979163307455514c9e66af2c6493ecb9f8cbf28385d276', 'pages': 7, 'members': 145, 'display_date': '17 October 2026'}, '23440119': {'publication': '5038dc4356a3827926e33db5fc8d09a2989be475a3090f0c6a6049e8b689250d', 'promotion': '39ec28de766a2463f78d01476a254c9d6bbce130619904fedad4ec96c074a43d', 'root': '8b51684b5e6cd6b36d8dd3302e2bbc5f29f261eb29affa753636812fb15cba56', 'editorial': '07681369ba08e412bf71e5fb858fb2ad42d72cb570d53aa973e02c3a6387b979', 'seal': '46340cef94deccd49fd095854cecd466b0df2a05834f5618681fe92589093fb6', 'pages': 5, 'members': 26, 'display_date': '17 October 2026'}, '23224103': {'publication': '779d861cdb61eb3586f366cd2431d436470083175c57b4a6839a7c98818c7763', 'promotion': '0707bd558a2635493d2dae7d4e31242a496a97d677735aad02443c663a8ddf3c', 'root': '9968ef5b5eec175ae7fcf2ffba58b143d56f5aa3221bbc29d92507573ae8c569', 'editorial': '3c03f413da3fc960400c2d54d2b2432509c0ea61edd85e80d924751d37e62851', 'seal': '169cbdd3e43de4bd848342e3935342e0ea8390e84d58827cb5b81d428764eaa1', 'pages': 6, 'members': 52, 'display_date': '7 October 2026'}}
def normalized_surreal_cone_brownian_abstract(rid,body):
 if rid=='23440119':
  for old,new in [(r"Tun\c{c}el's",'Tunçel’s'),(r'$K=\{(x,y,z)\geq0:xy^2\geq z^3\}$','K = {(x,y,z) ≥ 0: xy² ≥ z³}'),(r'$F=-25\log\bigl(z(xy^2-z^3)\bigr)$','F = −25 log(z(xy² − z³))'),('$100$','100'),(r'$D^3F(a)[h,u,u]\leq0$','D³F(a)[h,u,u] ≤ 0'),(r'$a\in\inter K$','a ∈ int K'),(r'$h\in K$','h ∈ K'),(r'$u\in\R^3$','u ∈ ℝ³'),('$K$','K'),(r'$\R^3$','ℝ³'),("Hildebrand's",'Hildebrand’s')]:body=body.replace(old,new)
 elif rid=='23224103':body=body.replace("Georgakopoulos's",'Georgakopoulos’s')
 if '\\' in body or '$' in body:raise ValueError('Unrecognized surreal/cone/Brownian abstract command')
 return ' '.join(body.split())
SLIT_GAUSSIAN_IDS={'23383961','23430906'}
def normalized_slit_gaussian_abstract(rid,body):
 replacements=[('P.~L.~Duren','P. L. Duren'),('Problem~6.72','Problem 6.72'),('Hayman--Lingham','Hayman–Lingham'),(r'\(a_2+i10^{-24}(a_4-3a_3)\)','a₂+i10⁻²⁴(a₄−3a₃)')] if rid=='23383961' else [(r'$H\in(1/4,1)$','H ∈ (1/4,1)'),(r'$X_T=\int_0^T B^1_s\,dB^2_s$','X_T = ∫₀ᵀ B¹_s dB²_s'),('$n$','n'),('$[0,T]$','[0,T]'),('$c_HT^{2H}n^{1/2-2H}$','c_H T^(2H)n^(1/2−2H)'),('$H$','H'),('$T>0$','T > 0'),(r'$n\ge1$','n ≥ 1'),('$L^2$','L²')]
 for old,new in replacements:body=body.replace(old,new)
 if '\\' in body or '$' in body:raise ValueError('Unrecognized slit/Gaussian abstract command')
 return ' '.join(body.split())
def normalized_quadratic_abstract(body):
 return ' '.join(body.replace('$z^2$','z²').split())
def normalized_bosonic_abstract(body):
 return ' '.join(body.replace('--','–').split())
def normalized_amplifier_abstract(body):
 body=body.replace('\n\\[\n',' ').replace('\n\\]\n',' ')
 for old,new in [('R^6-8R^5+22R^4-30R^3+21R^2-6R+1.','R⁶ − 8R⁵ + 22R⁴ − 30R³ + 21R² − 6R + 1.'),(r'r\in(1,R)','r ∈ (1,R)'),(r'1<r<\Rhyb','1 < r < R_hyb'),(r'\Rsim\geq\Rhyb=1.5028569127905696\ldots>3/2','R_sim ≥ R_hyb = 1.5028569127905696… > 3/2'),(r'\Rsim','R_sim'),(r'\Rhyb','R_hyb'),(r'(\sigma,\lambda)','(σ,λ)'),('$',''),('--','–')]:body=body.replace(old,new)
 if '\\' in body:raise ValueError('Unrecognized amplifier abstract command')
 return '\n\n'.join(' '.join(p.split()) for p in re.split(r'\n\s*\n',body.strip()))
BRAID_WAVE_WREATH_IDS={'23393596','23358014','23356964'}
def normalized_braid_abstract(body):
 for old,new in [('$',''),(r'\geq','≥'),(r'\not\subset','⊄'),(r'\F','F'),('--','–')]:body=body.replace(old,new)
 return ' '.join(body.split())
def normalized_wave_abstract(body):
 return ' '.join(body.split()).replace('$L^2$','L²').replace(r'$L^\infty$','L∞').replace('$L^1$','L¹').replace(r'$\{0\}$','{0}').replace(r'$o(\norm{u}_{L^2}^2)$','o(‖u‖²L²)')
def normalized_wreath_abstract(body):
 for old,new in [('$',''),(r'G_\delta','Gδ'),(r'\Z\wr\Z','ℤ ≀ ℤ'),('--','–')]:body=body.replace(old,new)
 return ' '.join(body.split())
REACH_SATOH_IDS={'23431676','23387442'}
def normalized_reach_satoh_abstract(rid,body):
 if rid=='23431676':body=body.replace(r'T\'othm\'er\'esz','Tóthmérész')
 else:
  body=body.replace('$','').replace(r'\SL','SL').replace(r'\C','ℂ')
  body=body.replace(r'\setminus',' '+chr(92)+' ').replace(r'\geq','≥').replace("Satoh's",'Satoh’s')
 return ' '.join(body.split())
BRACE_NIJENHUIS_IDS={'23441906','23431313'}
def normalized_brace_nijenhuis_abstract(rid,body):
 if rid=='23441906':body=body.replace("Ced\\'o",'Cedó').replace('~',' ').replace('\\,',' ').replace('$','').replace('\\ne','≠').replace('^3','³')
 else:body=body.replace('$','').replace('\\R^n','ℝⁿ').replace('\\lambda','λ')
 return ' '.join(body.split())
NEVO_WARM_IDS={'23444839','23592692'}
def normalized_nevo_warm_abstract(rid,body):
 if rid=='23444839':body=body.replace('Cohen--Macaulay','Cohen–Macaulay')
 else:
  for old,new in {r'$\alpha>1$':'α>1',r'$\alpha$':'α',r'$\alpha>4/3$':'α>4/3','$4/3$':'4/3',r'$\alpha\ge17/4$':'α≥17/4','$m$':'m',r'$\alpha>\sec^2(\pi/(2m))$':'α>sec²(π/(2m))'}.items():body=body.replace(old,new)
 return ' '.join(body.split())
def normalized_jc_abstract(body):
 body=body.replace('Jukes--Cantor','Jukes–Cantor').replace('$n\\ge4$','n ≥ 4').replace('$2n+1$','2n + 1')
 return '\n\n'.join(' '.join(x.split()) for x in re.split(r'\n\s*\n',body.strip()))
GAME_SESHADRI_IDS={'23430642','23387814'}
def normalized_game_seshadri_abstract(rid,body):
 if rid=='23430642':
  body=body.replace(r'\rank(A+B)=1','rank(A + B) = 1').replace('\\PART\\','Partition').replace('$','')
 elif rid=='23387814':
  replacements={r'$\eps(S,L;x)\ge (2+|K_S^2|^{1/4})^{-1}$':'ε(S,L;x) ≥ (2+|K_S²|^(1/4))⁻¹',r'$d\ge7$':'d ≥ 7',r'$K_S^2=6(d-1)(d-3)$':'K_S² = 6(d−1)(d−3)','$L$':'L','$L^2=6$':'L² = 6',r'$\eps(S,L;x)\le1/(d-1)$':'ε(S,L;x) ≤ 1/(d−1)','$d=7$':'d = 7'}
  for old,new in replacements.items():body=body.replace(old,new)
 return ' '.join(body.split())
def tar_gz_integrity(path):
 """Read the complete gzip stream and tar members without extracting files."""
 try:
  with gzip.open(path,'rb') as stream:
   while stream.read(1024*1024):pass
  with tarfile.open(path,'r:gz') as archive:
   for member in archive:
    if member.isfile():
     with archive.extractfile(member) as stream:
      while stream.read(1024*1024):pass
  return True
 except (OSError,EOFError,tarfile.TarError,zlib.error):return False
OCTOBER_EDITOR_IDS={'23127646','23191301'}
def normalized_october_abstract(rid,body):
 body=body.replace('$','')
 if rid=='23127646':
  for old,new in [(r'\psi','ψ'),(r'\theta','θ'),(r'\geq','≥')]:body=body.replace(old,new)
  body=body.replace('ψ(x,y)','ψ(x, y)').replace('|ψ(13/27,14/27)-ψ(14/27,13/27)|≥','|ψ(13/27, 14/27) − ψ(14/27, 13/27)| ≥').replace('ψ(1-θ,θ)=1-θ/d(θ)','ψ(1 − θ, θ) = 1 − θ/d(θ)')
 elif rid=='23191301':
  body=body.replace('q=3','q = 3').replace(r'3\cdot10^{62}','3 · 10^62').replace(r'q\ge3','q ≥ 3').replace(r'220\times220','220 × 220')
 return ' '.join(body.split())
ADDED_IDS={'23203334','22929486','23088066','23353160','23147866','23157237','22729355'}
def decode_added_abstract(tex):
 tex=tex.replace(r'Rei\ss{}','Reiß').replace('$L^2$','L²')
 for old,new in {r'\ge':'≥',r'\sum':'∑',r'\chi':'χ',r'\Theta':'Θ',r'\sqrt n':'√n','n-1':'n−1','n-2':'n−2','n-3':'n−3'}.items():tex=tex.replace(old,new)
 for old,new in {r'\mup':'μ′',r'\Sep':'Sep',r'\mathbb R^{12}':'R¹²',r'K\"ahler':'Kähler','Bru\\ss\\':'Bruß',r'\hbin':'h₂',r'\ldots':'…','C_{4,12}':'C₄,₁₂',r'C_b^\infty\cap L^2':'C_b^∞ ∩ L²',r'e_a e_b/m_a':'eₐe_b/mₐ'}.items():tex=tex.replace(old,new)
 return tex.replace(r'\[','').replace(r'\]','').replace('$','').replace('--','–').replace("'",'’')
LATEX_WORDS={r'\omega':'ω',r'\delta':'δ',r'\log':'log',r'\geq':'≥',r'\simeq':'≃',r'\PP':'P',r'\dim':'dim',r'\Aut':'Aut',r'\qquad':' ',r'\emph':'',r'\CCR':'CCR',r"V\'ertesi":'Vértesi',r'\times':'×'}
def normalized_cubulation_abstract(body):
 body=body.replace(r'\CAT','CAT').replace(r'\mapsto','→').replace('$','').replace('~',' ')
 return ' '.join(body.split())
def normalized_dfc_abstract(body):
 body=body.replace('birth--death','birth–death')
 return ' '.join(body.split())
def normalized_bv_abstract(body):
 body=' '.join(body.split())
 replacements={r'\(0\ne h\in k[x]\)':'0≠h∈k[x]',r'\(A_h=k\langle x,Y\rangle/(Yx-xY-h(x))\)':'A_h=k⟨x,Y⟩/(Yx−xY−h(x))',r'\(k\)':'k',r'\(h\)':'h','Batalin--Vilkovisky':'Batalin–Vilkovisky','~':' '}
 for old,new in replacements.items():body=body.replace(old,new)
 return body
def abstract_tokens(tex,record_id=None):
 if record_id in DIPOLE_LANGLANDS_IDS:return wt(normalized_dipole_langlands_abstract(record_id,tex))
 if record_id in SURREAL_CONE_BROWNIAN_IDS:return wt(normalized_surreal_cone_brownian_abstract(record_id,tex))
 if record_id in SLIT_GAUSSIAN_IDS:return wt(normalized_slit_gaussian_abstract(record_id,tex))
 if record_id=='23203100':return wt(normalized_bosonic_abstract(tex))
 if record_id=='22089807':return wt(normalized_amplifier_abstract(tex))
 if record_id=='23306332':return wt(normalized_quadratic_abstract(tex))
 if record_id in BRAID_WAVE_WREATH_IDS:return wt({'23393596':normalized_braid_abstract,'23358014':normalized_wave_abstract,'23356964':normalized_wreath_abstract}[record_id](tex))
 if record_id in REACH_SATOH_IDS:return wt(normalized_reach_satoh_abstract(record_id,tex))
 if record_id=='23328912':return wt(normalized_cubulation_abstract(tex))
 if record_id=='23524971':return wt(normalized_dfc_abstract(tex))
 if record_id=='23572690':return wt(normalized_bv_abstract(tex))
 if record_id in BRACE_NIJENHUIS_IDS:return wt(normalized_brace_nijenhuis_abstract(record_id,tex))
 if record_id in NEVO_WARM_IDS:return wt(normalized_nevo_warm_abstract(record_id,tex))
 if record_id=='22089373':return wt(normalized_jc_abstract(tex))
 if record_id in GAME_SESHADRI_IDS:return wt(normalized_game_seshadri_abstract(record_id,tex))
 if record_id in ADDED_IDS:tex=decode_added_abstract(tex)
 if record_id in OCTOBER_EDITOR_IDS:tex=normalized_october_abstract(record_id,tex)
 if record_id=='23180194':tex=tex.replace(r'\xi','ξ').replace('$','').replace('--','–')
 if record_id=='23127955':tex=tex.replace(r'\R^3','ℝ³').replace('$','').replace('~',' ')
 tex=tex.replace(r"Krej\v{c}\'i\v{r}\'ik",'Krejčířík')
 tex=tex.replace('K_4','K₄').replace(r'\sqrt','√')
 tex=tex.replace(r'\Z^d','Zᵈ').replace(r'\ZZ','Z').replace(r'\Z','Z').replace(r'\textbf','').replace(r'H\"aggstr\"om','Häggström')
 tex=re.sub(r'\\ge(?![A-Za-z])','≥',tex)
 tex=re.sub(r'\\(g|n|to)(?![A-Za-z])',lambda m:{'g':'g','n':'n','to':'→'}[m.group(1)],tex).replace('j_1','j₁').replace('j_2','j₂')
 for old,new in LATEX_WORDS.items():tex=tex.replace(old,new)
 commands=re.findall(r'\\[A-Za-z]+',tex)
 if commands:raise ValueError('Unrecognized abstract TeX commands: '+repr(commands))
 return wt(tex)
def normalized_kimura_abstract(tex):
 return '\n\n'.join(' '.join(p.split()) for p in re.split(r'\n\s*\n',tex.replace('$','').replace('~',' ').replace('--','–').strip()))
class Doc(HTMLParser):
 def __init__(self,p):
  super().__init__();self.a=[];self.text=[];self.feed(p.read_text())
 def handle_starttag(self,t,a):self.a.append((t,dict(a)))
 def handle_data(self,t):self.text.append(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wt(t):return re.findall('[A-Za-z0-9]+|[\u0370-\u03ff]',unicodedata.normalize('NFKC',t))
result={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'papers':{},'issues':[]}
index=(S/'research/index.html').read_text(); sitemap=(S/'research/sitemap.xml').read_text()
for rid in args.record_ids:
 p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());f=S/'research'/c['slug']/'index.html';h=f.read_text();d=Doc(f);base='https://aleckriebel.com/research/'+c['slug']+'/';checks={}
 def test(k,v):
  checks[k]=bool(v)
  if not v:result['issues'].append(rid+': '+k)
 meta={a.get('name',a.get('property')):a.get('content') for t,a in d.a if t=='meta'}
 test('title',unescape(re.search('<title>(.*?)</title>',h).group(1))==c['title']+' | Alec Kriebel')
 for k,v in {'description':c['description'],'citation_title':c['title'],'citation_author':c['author'],'citation_publication_date':c['publication_date'].replace('-','/'),'citation_doi':c['doi'],'citation_pdf_url':base+c['pdf_filename'],'citation_author_orcid':'0009-0001-9320-500X','og:title':c['title'],'og:description':c['description'],'og:url':base,'article:published_time':c['publication_date']}.items():test(k,meta[k]==v)
 test('canonical',[a['href'] for t,a in d.a if t=='link' and a.get('rel')=='canonical']==[base])
 schemas=[json.loads(x) for x in re.findall('<script type="application/ld\\+json">(.*?)</script>',h,re.S)]
 art=next(x for x in schemas[0]['@graph'] if x['@type']=='ScholarlyArticle')
 test('jsonld',all(art[k]==c[k] for k in ['description','abstract']) and (('version' not in art) if rid=='23203100' else art['version']==c['version']) and art['name']==c['title'] and art['datePublished']==c['publication_date'] and art['sameAs']=='https://doi.org/'+c['doi'] and art['encoding']['contentUrl']==base+c['pdf_filename'] and art['author'][0]['name']==c['author'] and art['identifier']['value']==c['doi'])
 for sec,key in [('abstract','abstract'),('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations')]:
  segment=re.search('<section id="'+sec+'">(.*?)</section>',h,re.S).group(1)
  paras=[unescape(x) for x in re.findall('<p>(.*?)</p>',segment,re.S)]
  expected=c[key] if isinstance(c[key],list) else c[key].split('\n\n')
  test(sec,paras==expected)
 textpath=p/'sources'/TEX_PATHS[rid]
 source=textpath.read_text()
 abstract_source=source
 if rid=='22089551':
  branch=re.search(r'\\ifdefined\\japsubmission(.*?)\\else(.*?)\\fi',source,re.S)
  main_source=(textpath.parent/'main_arxiv.tex').read_text()
  test('non_jap_abstract_source_selected',branch is not None and r'\input{paper_content}' in main_source and 'japsubmission' not in main_source)
  abstract_source=branch.group(2)
 a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',abstract_source,re.S).group(1)
 test('abstract_full_source_words',abstract_tokens(a,rid)==wt(c['abstract']))
 if rid in GAME_SESHADRI_IDS:
  test('abstract_full_source_text',normalized_game_seshadri_abstract(rid,a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())=={'23430642':140,'23387814':97}[rid])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='22136869':
  test('abstract_full_source_text',normalized_kimura_abstract(a)==c['abstract'])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='23180194':
  normalized_abstract=' '.join(a.replace(r'\xi','ξ').replace('$','').replace('--','–').split())
  test('abstract_full_source_text',normalized_abstract==c['abstract'])
  test('abstract_full_113_words',len(c['abstract'].split())==113)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in OCTOBER_EDITOR_IDS:
  test('abstract_full_source_text',normalized_october_abstract(rid,a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())=={'23127646':109,'23191301':123}[rid])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='23127955':
  normalized_abstract=' '.join(a.replace(r'\R^3','ℝ³').replace('$','').replace('~',' ').split())
  test('abstract_full_source_text',normalized_abstract==c['abstract'])
  test('abstract_full_122_words',len(c['abstract'].split())==122)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ADDED_IDS:
  compact=lambda text: re.sub(r'\s+','',unicodedata.normalize('NFKC',text))
  test('abstract_full_source_text',compact(decode_added_abstract(a))==compact(c['abstract']))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ('23441523','23356680'):
  normalized_abstract=a.replace('$K_4$','K₄').replace('$3$','3').replace(r'$4+\sqrt{17}$','4 + √17').replace('--','–').replace('~',' ')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ('23445342','23387753','23352246'):
  normalized_abstract=a.replace(r'$\ZZ$','Z').replace(r'$\Z^d$','Zᵈ').replace(r'$d\ge2$','d ≥ 2').replace('$p<1$','p < 1').replace(r'\textbf{Priority qualification:}','Priority qualification:').replace(r'H\"aggstr\"om','Häggström').replace(r'\ ',' ').replace('$','').replace('~',' ').replace('--','–').replace("'",'’')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid=='23414025':
  normalized_abstract=a.replace(r'\(\g\)','g').replace(r'\(\n\)','n').replace(r'\(j_1,j_2:\g\to\n\)','j₁, j₂ : g → n')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
 if rid in ('23390181','23410944','23422055'):
  normalized_abstract=a.replace('$1/3<d<1$','1/3 < d < 1').replace("Kazhdan's","Kazhdan’s").replace(r"Krej\v{c}\'i\v{r}\'ik",'Krejčířík').replace('--','–')
  test('abstract_full_source_text',' '.join(normalized_abstract.split())==' '.join(c['abstract'].split()))
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
  printed_date=re.search(r'\\date\{([^}]+)\}',source).group(1)
  expected_dates={'23390181':r'October 15, 2026\quad (version 1.0.0)','23410944':r'15 October 2026\\ \small Research note, version 1.0','23422055':r'October 16, 2026 \quad Version 1.0'}
  test('printed_version_date',printed_date==expected_dates[rid] and c['source_binding']['manuscript_version']==c['version']==c['source_binding']['zenodo_version'])
 test('no_noindex','noindex' not in meta.get('robots',''))
 visible_text=''.join(d.text).lower()
 novelty_checked_text=visible_text.replace('does not certify worldwide first priority','').replace('does not establish worldwide first priority','')
 test('no_audit_replay',not any(x in novelty_checked_text for x in ['24 october 2026','october 24','audit completed','checks passed','worldwide first','first-ever']))
 test('no_followup',c['follow_up'] is None and 'id="further-research"' not in h)
 test('authorship_once',h.count('Authorship and responsibilities would be discussed in relation to the substantive contributions made.')==1)
 test('ai_disclosure',c.get('ai_disclosure','') in unescape(h))
 test('collaboration',c['collaboration'] in unescape(h))
 ids=[a['id'] for t,a in d.a if 'id' in a];test('unique_ids',len(ids)==len(set(ids)))
 local=[]
 for tag,attrs in d.a:
  for key in ['href','src']:
   if key not in attrs:continue
   u=urlsplit(urljoin(base,attrs[key]))
   if u.netloc!='aleckriebel.com':continue
   q=S/unquote(u.path).lstrip('/')
   if q.is_dir():q=q/'index.html'
   good=q.is_file()
   if good and q.suffix=='.html' and u.fragment:good=unquote(u.fragment) in [b['id'] for _,b in Doc(q).a if 'id' in b]
   local.append(good)
 test('local_links_anchors',all(local))
 receipt_file=p/'sources/receipt.json';asset_root=p/'sources'
 if rid=='23390551':
  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=dipole_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']
 elif rid=='23203100':
  gate=json.loads((p/'promotion.json').read_text());raw_receipt,receipt,asset_root=bosonic_source_view(p,c,gate);receipt_file=p/c['source_binding']['receipt_path']
 else:raw_receipt=json.loads(receipt_file.read_bytes());receipt=normalized_receipt_view(raw_receipt)
 hashes={'html':sha(f),'publication':sha(p/'publication.json')}
 resolver=PublishedAssets(asset_root,receipt,c.get('source_binding',{}).get('embedded_assets',[]))
 for asset in c.get('additional_assets',[]):resolver.additional_asset_kind(asset)
 assets=[(key,c[key]) for key in ['pdf_filename','supplement_filename'] if c.get(key)]
 assets += [('additional_asset_'+asset['filename'],asset['filename']) for asset in c.get('additional_assets',[])]
 for key,name in assets:
  original=resolver.resolve(name)
  actual=sha(f.parent/name);hashes[name]=actual
  test(key,actual==original.sha256 and name in [a.get('href') for t,a in d.a if t=='a'])
  if name.endswith('.zip'):
   with zipfile.ZipFile(f.parent/name) as z:test('zip_integrity_'+name,z.testzip() is None)
  if name.endswith('.tar.gz'):
   test('tar_gz_integrity_'+name,tar_gz_integrity(f.parent/name))
  if key.startswith('additional_asset_') and name.endswith('.pdf'):
   extra_text=subprocess.check_output(['/opt/homebrew/bin/pdftotext',str(f.parent/name),'-'],text=True).split('\f')
   if not extra_text[-1].strip():extra_text.pop()
   test('supplement_pdf_searchable_'+name,all(len(t.strip())>100 for t in extra_text))
   test('supplement_pdf_page_label_'+name,f'PDF, {len(extra_text)} pages' in h)
   if original.pages is not None:
    test('embedded_pdf_page_count_'+name,len(extra_text)==original.pages)
    label=next(x['label'] for x in c['additional_assets'] if x['filename']==name)
    test('embedded_pdf_individual_page_label_'+name,f'PDF, {len(extra_text)} pages' in label)
 texts=subprocess.check_output(['/opt/homebrew/bin/pdftotext',str(f.parent/c['pdf_filename']),'-'],text=True).split('\f')
 if not texts[-1].strip():texts.pop()
 test('pdf_searchable',all(len(t.strip())>100 for t in texts));test('page_count',f'PDF, {len(texts)} pages' in h)
 frames=[a for t,a in d.a if t=='iframe'];test('iframe',len(frames)==1 and frames[0]['src']==c['pdf_filename']+'#view=FitH' and bool(frames[0].get('title')))
 test('index_entry',f'href="/research/{c["slug"]}/"' in index and c['description'] in unescape(index))
 ix=json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',index,re.S).group(1));items=ix['mainEntity']['itemListElement'];test('index_jsonld',len([x for x in items if x['url']==base and x['name']==c['title']])==1 and ix['mainEntity']['numberOfItems']==len(items))
 test('sitemap',sitemap.count('<loc>'+base+'</loc>')==1)
 bib=(f.parent/'citation.bib').read_text();test('bibtex',all(x in bib for x in [c['title'],('Kriebel, Alec' if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS else c['author']),c['doi'],(c['bibtex_note'] if 'bibtex_note' in c else ('Unrefereed preprint, version '+c['version'] if c['version'] is not None else 'Unrefereed preprint; no version number supplied'))]))
 test('background_links',all(x['url'] in (unescape(h) if rid in SURREAL_CONE_BROWNIAN_IDS or rid in DIPOLE_LANGLANDS_IDS else h) and x['title'] in unescape(h) and x['note'] in unescape(h) for x in c['background']))
 record_file=p/'sources'/('zenodo_record.json' if rid=='23390551' else 'metadata.json' if rid=='23306332' else 'record/zenodo_record.json' if rid=='23203100' else 'record.json')
 record=json.loads(record_file.read_text())['metadata'];test('record_metadata',all(c[k]==record[k] for k in ['title','doi','publication_date']) and (c['version']==record['version'] if 'version' in record else rid in ('21699161','23203334','23203100') and c['source_binding']['zenodo_version'] is None))
 if c.get('edition_label'):test('edition_label',c['edition_label'] in unescape(h) and c['citation_edition_label'] in unescape(h) and c['edition_note'] in unescape(h))
 if c.get('related_resources') and rid not in SLIT_GAUSSIAN_IDS and rid not in SURREAL_CONE_BROWNIAN_IDS and rid not in DIPOLE_LANGLANDS_IDS:
  materials=re.search('<section id="materials">(.*?)</section>',h,re.S).group(1)
  test('supporting_materials_links',all(x['url'] in materials and x['label'] in unescape(materials) and x.get('doi','') in unescape(materials) for x in c['related_resources']))
  related_bound=True
  for related in c['source_binding'].get('related_records',[]):
   related_receipt=p/related.get('receipt','sources/related-records/'+related['record_id']+'/receipt.json')
   if not related_receipt.resolve().is_relative_to(p.resolve()):raise ValueError('Related receipt must remain within its paper folder')
   rp=related_receipt.parent;rr=normalized_receipt_view(json.loads(related_receipt.read_bytes()))
   related_bound=related_bound and rr['record_id']==related['record_id'] and rr['files']==related['files']
   related_bound=related_bound and all(sha(rp/asset_name(x))==x['sha256'] for x in rr['files'])
  test('related_resource_source_bindings',related_bound)
 if (p/'promotion.json').exists():
  gate=json.loads((p/'promotion.json').read_text())
  test('promotion_pdf_binding',gate['status']=='PASS' and gate['pdf_sha256']==sha(asset_root/c['pdf_filename']))
  if gate.get('publication_sha256'):test('promotion_publication_binding',gate['publication_sha256']==sha(p/'publication.json'))
  if rid in ('23441523','23356680','23445342','23387753','23352246','23414025','23390181','23410944','23422055','23180194','23127955') or rid in ADDED_IDS or rid in OCTOBER_EDITOR_IDS:
   test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
   test('promotion_review_bindings',all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()) and set(gate['reviews'])=={'analytic','adversarial','scope'})
  if rid in ADDED_IDS or rid in ('23180194','23127955') or rid in OCTOBER_EDITOR_IDS:
   test('all_published_source_assets_bound',gate['source_files']==receipt['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
 if rid=='23577484':test('commuting_fixed','elements that commute with the starting involution' in h and 'produces commuting elements' not in h);test('scope_complete',all(x in unescape(h) for x in ['[d/3, 2d/3]','independent, exactly uniform','sufficiently large','separately','0 < δ < 1']))
 if rid=='23310484':test('scope_complete',all(x in unescape(h) for x in ['finite simplicial complex','actual vertex set','Nevo and Wagner’s result for PL spheres already excludes arbitrary topological embeddings','d = 0']))
 if rid=='23331395':test('scope_complete',all(x in unescape(h) for x in ['smooth integral projective variety','arbitrary characteristic','one closed point','mult_x(ρ_*Γ)','inseparable degree']))
 if rid=='22770864':test('scope_complete',all(x in unescape(h) for x in ['full automorphism group','1009^52359','i ≥ 7','Lie-ring automorphism','awaiting confirmation by mathematicians','Omirov and Ruan','does not claim that G and Aut(G) are isomorphic']))
 if rid=='22729537':test('scope_complete',all(x in unescape(h) for x in ['population alignment laws indexed by locus length','stationary reversible','not a canonical species graph','incidence-separated','scalar-separator faithfulness','compact semianalytic','no practical numerical bound','L + 1']))
 if rid=='21699161':
  printed_date=re.search(r'\\date\{([^}]+)\}',source).group(1)
  test('printed_edition_archive_distinction',printed_date==c['version']==c['source_binding']['manuscript_date']=='July 2026' and c['archive_version_label']=='1.1.0' and 'version' not in record and 'Version July 2026' not in h and c['supplement_filename'] is None and len(c['related_resources'])==4)
  test('scope_complete',all(x in unescape(h) for x in ['shared-randomness convex hulls','dimension at most two','finite, input-dependent output alphabets','zero projectors','same-state simulation','Neither is claimed to be the exact global optimum','Vértesi and Bene established that phenomenon in 2010']))
 if rid=='22089551':test('scope_complete',all(x in unescape(h) for x in ['strictly positive rate constants','one linkage class','at most two molecules','unique on each reachable class','no closed-form or product-form formula','pure-species condition','supplementary-note-v1.2.4.pdf']))
 if rid=='22729545':
  test('scope_complete',all(x in unescape(h) for x in ['tree-child under every admissible rooting','surjective onto the terminal taxa','inheritance weights lie strictly between zero and one','distinct internal biological events have distinct ages','does not limit the entire network to two reticulations','Q1–Q8','not unique recovery of every raw event and parameter','one triple, three nucleotide sites or three observed genealogies','no effective practical sequence-length bound','compact semianalytic normalized finite-presentation charts','relies on the companion preprint']))
  test('abstract_verbatim_source',' '.join(a.split())==' '.join(c['abstract'].split()))
  companion=R/'papers/22729537/promotion.json'
  test('companion_gate_binding',gate['companion_import']['status']=='PASS' and gate['companion_import']['promotion_sha256']==sha(companion) and json.loads(companion.read_text())['status']=='PASS')
  test('all_four_published_materials',all(name in [x.get('href') for t,x in d.a if t=='a'] for name in ['NMSC_Paper_B_Main.pdf','NMSC_Paper_B_Supplement.pdf','NMSC_Paper_B_Source.zip','NMSC_Paper_B_Reproducibility.zip']))
 if rid=='23441523':
  test('scope_complete',all(x in unescape(h) for x in ['every nonempty input size','sequence of positive rational ε','total sample-plus-adjacency cost','complete positive rational weight vector','unordered changed vertex pairs','not a sample-only bound','does not imply polynomial running time','established two-sided triangle-testing lower bound of Alon and Shapira']))
  test('heavy_apex_distance_direction','new graph’s distance from P is exactly one quarter of the tail’s triangle-free distance' in unescape(h))
 if rid=='23356680':
  test('scope_complete',all(x in unescape(h) for x in ['every Lipschitz domain Ω compactly contained in U','Competitors need not be continuous','positive area','not Korevaar–Schoen harmonic','not a global minimizer','complete metric target','4 + √17','2√2 + √6','revised journal body was not available','neither unchanged final wording nor continued open status','First priority and optimal constants are not claimed']))
  test('pinned_question_history',any(x['url']=='https://arxiv.org/abs/2503.08553v1' for x in c['background']))
 if rid=='23445342':
  test('scope_complete',all(x in unescape(h) for x in ['fixed iid space-time environment law','every deterministic real sequence M_N','uniformly in each deterministic alignment','twice the usual total variation distance','may diverge nonmonotonically and arbitrarily slowly','not a simultaneous assertion for partitions selected after observing the environment','Novelty and historical priority remain unresolved','four relevant older original full texts could not be accessed']))
  test('credited_methods',all(x in unescape(h) for x in ['Dunlap–Gu','Barraquand–Rychnovsky','auxiliary polynomial rate']))
 if rid=='23387753':
  test('scope_complete',all(x in unescape(h) for x in ['ordinary finite energy','every integer d ≥ 2','Finite components are allowed','quenched: X is fixed','internal site thresholds','maximum finite-side size','connected one-ended spanning tree','not the induced bond graph','factor-of-iid','No first-priority claim']))
  test('credited_planar_antecedent',all(x in unescape(h) for x in ['planar perturbation mechanism is due to Häggström and Mester','additional bounded-cutset deduction']))
 if rid=='23352246':
  test('scope_complete',all(x in unescape(h) for x in ['Variables have unrestricted signs','total binary encoding','Dimension, integer-coordinate count and denominators may all vary','integral improving recession direction','actual convex hull conv(S) is a closed rational polyhedron','including boundary points','width at most 2n','at most 2n|I| nodes','two integer coordinates','separate subtree-hull Conjecture 2 remains unaddressed','not claim an algorithm for arbitrary unencoded real data','not implement the full polynomial-time']))
  test('credited_classical_methods',all(x in unescape(h) for x in ['Classical mixed proximity','hybrid partial minimization','ring-family submodular minimization','exact optimization–separation']))
 if rid=='23414025':
  test('scope_complete',all(x in unescape(h) for x in ['same finite dimension','tr(ad_g x) = 0','n is semisimple','invertible linear difference','zero-dimensional case is included','Remark 4 supplies','merely reductive target is not covered','not asserted to be a group homomorphism','nilpotent targets are outside','original body of Onishchik’s 1969 decomposition paper was not accessible']))
  test('credited_classical_methods',all(x in unescape(h) for x in ['predecessor in Baues’s work','established pair j₁ = R + I and j₂ = R','holomorphic identity theorem','stabilizer is closed and discrete']))
 if rid=='23390181':
  test('scope_complete',all(x in unescape(h) for x in ['n ≥ 3','nonempty finite inverse-closed generating sets','Words are not identified under rotation or inversion','independent uniform elements of Sℓ with replacement','through all integers','factors, alphabets and density remain fixed','at most two','distinct sampling law','d = 1/3','not infinitude or factor embeddings','earlier collapse theorem already covers d > one-half']))
  test('credited_established_program',all(x in unescape(h) for x in ['Montee and Steenbock','almost-equal blocks','common-suffix finite-index','triangular-link criterion','Tropp','independent whole-relator Laplacians']))
 if rid=='23410944':
  test('scope_complete',all(x in unescape(h) for x in ['every integer d ≥ 2','connected open quasi-conical set','H₀¹(Ω)','closure of the point spectrum','Both cube widths and window widths are chosen inductively','zero-thickness interface screens','without explicit numerical bounds','not asserted to equal the whole half-line','It does not mean an isolated sequence of eigenvalues or compact resolvent']))
  test('credited_spectral_antecedents',all(x in unescape(h) for x in ['Krejčířík and Lotoreichik','Hempel, Seco and Simon','not a new general principle','does not certify historical first priority']))
 if rid=='23422055':
  test('scope_complete',all(x in unescape(h) for x in ['at least three independent','one fixed coordinate ball','Three fixed, linearly independent classes','h⁻_Jε ≥ 3','not an exact dimension','unrestricted compact-four-manifold integrability conjecture','real dimension two','no common positive compatible metric','not closed']))
  test('credited_geometry_antecedents',all(x in unescape(h) for x in ['prior work of Tan–Wang–Zhang–Zhu','pluricanonical sections','different invariant','bounded comparison does not certify exhaustive novelty']))
 if rid=='23203334':
  test('scope_complete',all(x in unescape(h) for x in ['Fix a finite number of species in three space dimensions','positive mass and a real charge, including zero charge','compact support in position and momentum','every spatial derivative is bounded','Maxwell divergence constraints','smooth on every finite time interval','No smallness, symmetry or neutrality condition','No uniform infinite-species or zero-mass limit','pinned OpenAI family 362','no independently reproduced proof-assistant certificate'.capitalize()]))
  test('no_invented_numbered_version','version' not in record and c['source_binding']['manuscript_version'] is None and 'Version 6 October' not in h and c['edition_label']=='Manuscript dated 6 October 2026')
  extra=gate['additional_reviews']['primary_adversarial'];gap=gate['gap_resolution'];old=gate['reviews']['adversarial']['verdict']
  test('additional_primary_review_binding',extra['sha256']==sha(p/extra['report']) and extra['verdict_sha256']==sha(p/extra['verdict_file']) and extra['verdict']==json.loads((p/extra['verdict_file']).read_text()) and extra['verdict']['status']=='PASS')
  test('conditional_review_preserved',old['status']=='conditional_multispecies_transfer_supported_upstream_global_verification_incomplete' and old['disposition']=='verification_coverage_dependency_hold' and old['unconditional_global_theorem_independently_verified'] is False)
  test('root_gap_resolution_binding',gate['disposition_by']=='root' and gap['additional_review_key']=='additional_reviews.primary_adversarial' and gap['additional_report_sha256']==extra['sha256'] and gap['additional_verdict_sha256']==extra['verdict_sha256'] and gap['upstream_pdf_sha256']==extra['verdict']['upstream']['pdf_sha256'] and gap['upstream_commit']==extra['verdict']['upstream']['commit'])
 if rid=='22929486':
  test('scope_complete',all(x in unescape(h) for x in ['G = F₂₉² ⋊ H','100920','b_f(G) = b(G) = 3 and μ′(G) = 4','inclusion-minimal','faithful and nonfaithful','not claimed to have the smallest','characteristic-11','not a journal acceptance']))
  test('notebook_confirmation_scoped',all(x in unescape(h) for x in ['reports confirmation by P. J. Cameron','distinct from journal publication']) and c['external_status']['doi_cited']==c['doi'] and c['external_status']['url'] in h)
 if rid=='23088066':
  test('scope_complete',all(x in unescape(h) for x in ['e_PL(K) = 3','e_lin(K) = 5','first barycentric subdivision','need not be arithmetic barycenters','including nongeneric placements','n = 2²⁵⁶','not a displayed small model','no explicit list of facets','need not be a surface or manifold']))
  test('credited_embedding_antecedents',all(x in unescape(h) for x in ['Brehm–Sarkaria','Newman','Lee–Nevo','withdrawn odd-dimensional claim']))
 if rid=='23353160':
  test('scope_complete',all(x in unescape(h) for x in ['C₄,₁₂','including both orientations','normalized complex Sep(3,3)','arbitrary auxiliary variables and affine equalities','affine-linear polynomials modulo the full real vanishing ideal','coefficients of the unnormalized ℓ can be rational','No coefficient list, exact comass','No claim is made that this is the least dimension']))
  test('credited_nonrepresentability_antecedents',all(x in unescape(h) for x in ['Fawzi’s established result','prior tensor-to-wedge lemma','Question 6.5','not the failing form']))
 if rid=='23147866':
  test('scope_complete',all(x in unescape(h) for x in ['independent uniformly distributed messages','R₁ < 3/2, R₂ < 3/2','vanishing uniform average decoding error','A₁B₁ : A₂B₂','R₁ = R₂ = 9/8','lower bound on the optimal LOCC capacity','not a one-copy advantage','Zero-error and maximal-error coding are not established','no extra shared entanglement']))
  test('eight_files_no_invented_zip',len(receipt['files'])==8 and all(not asset_name(x).endswith('.zip') for x in receipt['files']) and c['supplement_filename'] is None and 'Source and verification (ZIP)' not in h)
  links=[a['href'] for t,a in d.a if t=='a' and 'href' in a]
  test('all_eight_original_files_linked',all(any(link==asset_name(x) or '/files/'+asset_name(x) in link for link in links) for x in receipt['files']))
 if rid=='23157237':
  test('scope_complete',all(x in unescape(h) for x in ['known bounded connected C∞ domain','d ≥ 2','L = μ⁻¹ div(S∇)','conormal reflection n·S∇u = 0','stationary exact positions','every positive empirical eigenpair','Fourth powers of the transition eigenvalues','Any strictly positive deterministic ridge sequence tending to zero','separately fitted vector','density estimate converges in C² on the closure','globally in L²(D)','not a claim about differentiating the estimated tensor']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['Ordinary normal reflection is not an interchangeable','No convergence rate, finite-sample guarantee','different estimator obtained from classical variational regularization','does not prove consistency of the main spectral fit']))
  test('metadata_printed_version_distinction',record['version']==c['version']=='1.0' and c['source_binding']['manuscript_version'] is None and r'\date{October 5, 2026}' in source and c['edition_label']=='Zenodo version 1.0')
 if rid=='22729355':
  test('scope_complete',all(x in unescape(h) for x in ['For every n ≥ 4','every positive-equilibrium realization','d_Z > 8h_Z ∑_{j=2}^{n−2} d_j/h_j','strictly positive diffusion coefficients','not attained','χ_Dχ_H > 8(n−3)','one-dimensional Neumann interval','locally exponentially stable in H¹','fixed-integrated-mass class defined by the semipositive conservation law','Both contrasts are Θ(√n)']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['networks are synthetic','stationary zero-eigenvalue crossings','conserved quantity has zero weight on X₁','do not give global attraction','exponent-optimal only within this topology','does not claim intrinsic finite wavelength selection']))
  test('printed_month_edition_date_distinction',record['version']==c['version']=='1.0.11' and record['publication_date']=='2026-09-12' and c['source_binding']['manuscript_date']=='August 2026' and r'\date{August 2026}' in source and c['edition_label']=='Zenodo version 1.0.11')
  test('both_reader_pdfs_labelled',len(texts)==19 and 'Mathematical supplement (PDF, 19 pages)' in unescape(h))
  links=[a['href'] for t,a in d.a if t=='a' and 'href' in a]
  test('all_eight_published_assets_linked',len(receipt['files'])==8 and all(any(link==asset_name(x) or '/files/'+asset_name(x) in link for link in links) for x in receipt['files']))
  test('companion_software_doi_distinct','https://doi.org/10.5281/zenodo.22625980' in links and c['doi']=='10.5281/zenodo.22729355')
 if rid=='22136869':
  test('scope_complete',all(x in unescape(h) for x in ['proper lower-dimensional subset','generic choice of parameters on the network is not tree-equivalent','theta admits no tree-child rooting','network multispecies coalescent','Jukes–Cantor tree–network theorem','no clock or global timing','one chosen vertex','fixed theta maps have ambient ranks 9 under K2P and 15 under K3P']))
  test('record_manuscript_edition_distinction',record['version']==c['version']=='1.2.6' and record['publication_date']==c['publication_date']=='2026-08-28' and c['source_binding']['manuscript_version']=='1.2.7' and c['source_binding']['manuscript_date']=='August 2026' and r'\date{August 2026}' in source and 'v1.2.7' in source and '1.2.6' in c.get('edition_note','') and '1.2.7' in c.get('edition_note',''))
  test('reader_pdf_provenance',len(c['source_binding']['embedded_assets'])==2 and all(x['archive_filename']==c['supplement_filename'] and x['pages']==2 for x in c['source_binding']['embedded_assets']))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  gap=gate['gap_resolution']
  test('root_gap_resolution_file_binding',gate['disposition_by']=='root' and gap['disposition_by']=='root' and gap['status']=='RESOLVED_WITH_CONTEXTUAL_SCOPE' and gate['gap_resolution_sha256']==sha(p/gate['gap_resolution_file']) and gap==json.loads((p/gate['gap_resolution_file']).read_text()))
  test('frozen_scope_hold_preserved',gate['reviews']['scope']['verdict']['publication_hold'] is True and all(x['sha256']==sha(p/x['path']) for x in [gap['frozen_scope_content'],gap['frozen_scope_report'],gap['frozen_scope_verdict']]) and json.loads((p/gap['frozen_scope_content']['path']).read_text())['publication_hold']==gap['original_scope_hold'] and gap['original_scope_hold']['active'] is True and not c.get('publication_hold',{}).get('active',False))
  test('gap_independent_evidence_bindings',all(x['sha256']==sha(p/x['path']) for x in gap['analytic_evidence']+gap['adversarial_evidence']) and any(x['path']=='reviews/analytic/INTERPRETIVE_NOTE.md' for x in gap['analytic_evidence']) and any(x['path']=='reviews/analytic/counterexample_ratio_results.json' for x in gap['analytic_evidence']) and any(x['path']=='reviews/adversarial/structural_control_results.json' for x in gap['adversarial_evidence']) and any(x['path']=='reviews/adversarial/counterexample_results.json' for x in gap['adversarial_evidence']))
  test('gap_original_context_binding',gap['source']['sha256']==sha(textpath) and gap['main_pdf_sha256']==sha(p/'sources'/c['pdf_filename']) and gap['equation_17_source'] in source and gap['construction_paragraph_source'] in source and gap['public_scope_note'] in unescape(h) and gap['broad_reading_counterexample_preserved'] is True and gap['no_source_repair'] is True)
  test('main_mathematical_disposition_scoped',gate['reviews']['analytic']['verdict']['status']=='PASS' and gate['reviews']['adversarial']['verdict']['main_claims_supported_at_stated_hypotheses'] is True and gate['reviews']['adversarial']['verdict']['substantive_main_theorem_defect_identified'] is False)
  links=[attrs['href'] for tag,attrs in d.a if tag=='a' and 'href' in attrs]
  test('all_original_materials_linked',all(asset_name(x) in links for x in receipt['files']) and all(x['filename'] in links for x in c['source_binding']['embedded_assets']))
  test('no_false_top_level_zenodo_reader_links',all(not any('/files/'+x['filename'] in link for link in links) for x in c['source_binding']['embedded_assets']))
 if rid=='23180194':
  test('scope_complete',all(x in unescape(h) for x in ['locally compact second countable Hausdorff Abelian group','acting jointly measurably on an arbitrary measurable space Ω','sigma-finite measure on Ω','covariant, locally finite Radon random measure','nonzero Q-almost everywhere','every invariant, pointwise ξ-preserving, ξ-measurable Markov transport kernel','each row has mass one','every nonnegative measurable function f on Ω','every nonnegative measurable g on Ω × G','joint Mecke identity, or Campbell reversal']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['no assumption that the marginal law of ξ is sigma-finite','Invariance of the law of ξ alone is not a substitute','deterministic transports','Cox allocations','does not cover non-Abelian groups or the zero random measure','Standard Borel structure is used for the space of Radon measures; it is not imposed on Ω']))
  test('credited_classical_imports',all(x in unescape(h) for x in ['classical Mecke/Palm and Palm/mass-stationarity equivalences','known converse transport invariance','Problem 7.3 from 2009','complete final journal body was unavailable','complete final journal body was not checked']))
  test('printed_edition_date_binding',record['version']==c['version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-06' and c['source_binding']['manuscript_version'] is None and r'\date{6 October 2026\quad---\quad Unrefereed research note}' in source)
  test('two_original_assets_only',len(receipt['files'])==2 and len(texts)==7 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==113)
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/candidate-content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/c['source_binding']['frozen_scope_content_path']))
  test('root_disposition_at_stated_scope',gate['disposition_by']=='root' and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['reviews']['analytic']['verdict']['status']=='SUPPORTED_AT_STATED_SCOPE' and gate['reviews']['adversarial']['verdict']['status']=='PASS' and gate['reviews']['scope']['verdict']['verdict']=='PASS_SCOPE_ONLY')
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['verdict']['mathematical_clearance'] is False and bool(gate['scope_gate_resolution']))
 if rid in OCTOBER_EDITOR_IDS:
  expected_date={'23127646':'2026-10-03','23191301':'2026-10-06'}[rid]
  printed_date={'23127646':r'\date{October 3, 2026}','23191301':r'\date{6 October 2026}'}[rid]
  candidate_path={'23127646':'reviews/scope/candidate-content.json','23191301':'reviews/scope/content.json'}[rid]
  test('printed_edition_date_binding',record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and record['publication_date']==c['publication_date']==expected_date and c['source_binding']['manuscript_version'] is None and printed_date in source)
  test('two_original_assets_only',len(receipt['files'])==2 and len(texts)=={'23127646':4,'23191301':6}[rid] and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']==candidate_path and c['source_binding']['frozen_scope_content_sha256']==sha(p/candidate_path))
  av=gate['reviews']['adversarial']['verdict'];sv=gate['reviews']['scope']['verdict']
  test('root_disposition_at_stated_scope',gate['disposition_by']=='root' and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['reviews']['analytic']['verdict']['status']=='PASS' and av.get('status',av.get('verdict'))=='PASS')
  test('frozen_scope_chronology_preserved',(sv['mathematical_clearance'] is False if rid=='23127646' else sv['mathematical_gate'] is False) and bool(gate['scope_gate_resolution']))
 if rid=='23127646':
  test('scope_complete',all(x in unescape(h) for x in ['finite and simple','nonempty stable parts A, B and C','no A–C edges','all four conditions','x|B| neighbors in B','x|A| neighbors in A and y|C| neighbors in C','y|B| neighbors in B','Each reached A vertex is counted once','infimum of this maximum over all eligible finite graphs','every rational θ with 0 < θ < 1','ψ(1−θ,θ) = 1−θ/d(θ)','attained by a finite ordinary graph','minimum unweighted maximum row degree','distinct columns and strictly positive rational probability vectors b and q','Mq = θ1 and Mᵀb = θ1']))
  test('quantitative_gap_and_limits',all(x in unescape(h) for x in ['|ψ(13/27,14/27) − ψ(14/27,13/27)| ≥ 1/108','Neither exact value nor their ordering is asserted','two integer minima','upper bounds only','not claimed to attain the infima','not claimed to be the exact gap','no claim about irrational boundary parameters','The inherited seven-type example is credited prior work']))
  test('universal_proof_not_examples_only',all(x in unescape(h) for x in ['lower bound valid for every finite graph','minimum connection requirement in both directions','finite ordinary graph','d(13/27) ≤ 4 and d(14/27) ≤ 4','known symmetry of the related one-direction function φ is a different result']))
 if rid=='23191301':
  test('scope_complete',all(x in unescape(h) for x in ['real homogeneous forms','squares of real polynomials','Here n counts variables','N = 10^62','C(3 · 10^62,6,3) is nonconvex','every fixed odd q ≥ 3','finite n(q)','different separating functional','coefficient-1 modified Motzkin sextic','220 monomials','eight parity blocks']))
  test('quantifiers_and_limits',all(x in unescape(h) for x in ['not prove nonconvexity for three variables','one common dimension that works for all odd exponents','not a classification','no claim of optimality','no stubbornness claim','It is not integration against a positive measure','not materialized numerically']))
  test('credited_classical_ingredients',all(x in unescape(h) for x in ['The classical polynomial and its sum-of-squares cube come from earlier work','separation, product positivity and distinct-index counting have earlier sources','application to a fixed-exponent obstruction','larger odd power after the polynomials are added']))
 if rid=='23127955':
  test('scope_complete',all(x in unescape(h) for x in ['every three pairwise disjoint convex subsets','union of all complete affine lines','three-dimensional Lebesgue outer measure zero','Tangency requires actual intersection with the set and containment of the line in a supporting plane','contact may be an entire segment','their closures may intersect','If any set is empty','sets need not be closed, bounded, full dimensional, strictly convex or smooth']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['does not prove containment in countably many 2-manifolds','Hausdorff-dimension bound of two','union of tangent lines need not itself be closed','Contact with a closure alone is not enough','not an algorithm for enumerating tangents','not a certification of first priority']))
  test('proof_and_credited_inputs',all(x in unescape(h) for x in ['countably many disjoint compact caps','At almost every parameter','three distinct contacts give it three distinct roots','Separate cases handle points, segments and planar sets','Conjecture 4 in Oberwolfach Report 44/2008','standard density theorem, Rademacher’s theorem and area formula']))
  test('printed_edition_date_binding',record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-03' and c['source_binding']['manuscript_version'] is None and r'\date{3 October 2026\\\small Unrefereed preprint}' in source)
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==8 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']} and sha(p/'sources/published-source/common_tangent_nullness.pdf')==sha(p/'sources'/c['pdf_filename']))
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==122)
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/content.json'))
  test('root_disposition_at_stated_scope',gate['disposition_by']=='root' and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['reviews']['analytic']['verdict']['status']=='PASS' and gate['reviews']['adversarial']['verdict']['status']=='PASS' and gate['reviews']['scope']['verdict']['status']=='PASS_SCOPE_ONLY' and gate['reviews']['scope']['verdict']['completion_percent']==100 and bool(gate['scope_gate_resolution']))
  test('proof_wording_precision_preserved',bool(gate['nonblocking_proof_wording']) and 'globally smooth' not in unescape(h))
 if rid in GAME_SESHADRI_IDS:
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  decision=next(x for x in clearance['papers'] if x['record_id']==rid)
  test('root_clearance_binding',clearance['status']==decision['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==decision and gate['approved_scope']==decision['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False)
  test('root_clearance_source_review_identity',decision['pdf_sha256']==gate['pdf_sha256'] and decision['supplement_sha256']==gate['supplement_sha256'] and decision['source_receipt_sha256']==gate['source_receipt_sha256'] and all(decision['reviews'][k]['report_sha256']==v['sha256'] and decision['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)=={'23430642':9,'23387814':5}[rid] and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
 if rid=='23430642':
  test('scope_complete',all(x in unescape(h) for x in ['one equilibrium to be found in polynomial time','deciding uniqueness is coNP-complete','exact rank(A + B) = 1','variable positive dimensions','entire mixed-strategy equilibrium pair','known strict pure equilibrium','Arbitrary degeneracy','positive-dimensional equilibrium sets','(8n + 9) rows and (16n + 22) columns','rank-invalid inputs belong to neither']))
  test('complexity_limits_and_credit',all(x in unescape(h) for x in ['Unless P = NP','does not establish strong hardness','fixed dimensions','nondegeneracy promise','uniqueness of equilibrium payoffs','does not run the potentially exponential sequence','Disser and Skutella','Adsul and coauthors','worldwide priority']))
  test('tar_gz_label_and_identity',c['supplement_filename']=='supportkit-v1.0.tar.gz' and 'Source and verification (tar.gz)' in h and 'Source and verification (ZIP)' not in h and all(not asset_name(x).endswith('.zip') for x in receipt['files']))
  test('printed_edition_date_binding',r'\date{13 October 2026\quad Version 1.0}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-13')
  test('archive_main_pdf_identity',sha(p/'sources/published-source/rank_one_uniqueness_v1_0/output/pdf/paper.pdf')==sha(p/'sources/paper.pdf'))
 if rid=='23387814':
  test('scope_complete',all(x in unescape(h) for x in ['For every integer d ≥ 7','smooth integral complex projective surface','ample canonical bundle','ample integral line bundle','K_S² = 6(d−1)(d−3)','L² = 6','ε(S,L;x) ≤ 1/(d−1) < 1/(2+(K_S²)^(1/4))','The additive 2 is outside the fourth root','The surfaces vary with d and x is a special point']))
  test('scope_limits_and_credit',all(x in unescape(h) for x in ['does not determine its exact value','very-general-point','Picard-rank-one','canonical or adjoint polarization bounds','Miranda’s classical pencil construction','does not list explicit coefficients','Historical priority']))
  test('printed_edition_date_binding',r'\date{October 14, 2026}' in source and c['source_binding']['manuscript_version'] is None and record['version']==c['version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-14' and c['edition_label']=='Zenodo version 1.0')
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/candidate-content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/candidate-content.json'))
 if rid=='23431716':
  normalized_abstract=' '.join(a.replace('--','–').split())
  test('abstract_full_source_text',normalized_abstract==c['abstract'])
  test('abstract_full_142_words',len(c['abstract'].split())==142)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n')))
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==142)
  test('scope_complete',all(x in unescape(h) for x in ['finite loopless simple strongly connected digraph with at least two vertices','arbitrary nonnegative integer chip configuration encoded in binary','actual outdegree','There is no dissipative sink','deterministic polynomial-time many-one reductions','oriented subclass','forbids antiparallel arcs','acyclic graph with no directed path of two arcs','polynomial numerical total initial chips','written in unary','without a fairness assumption']))
  test('complexity_limits_and_credit',all(x in unescape(h) for x in ['Unless P = NP','does not give a polynomial-time simulation','does not claim bounded-degree or Eulerian hardness','Holroyd–Levine–Winkler','Stockmeyer–Meyer','Gramlich','NP-membership method of Farrell–Levine','Exact full-result and realization priority remain unknown']))
  test('printed_edition_date_binding',r'\date{Version 1.0, 16 October 2026}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0' and record['publication_date']==c['publication_date']=='2026-10-16')
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==7 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['supplement_sha256']==gate['supplement_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/CONTENT_CANDIDATE.md' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/CONTENT_CANDIDATE.md'))
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['verdict']['mathematical_verdict'] is None and bool(gate['scope_gate_resolution']))
 if rid=='22089373':
  test('abstract_full_source_text',normalized_jc_abstract(a)==c['abstract'])
  test('abstract_full_223_words',len(c['abstract'].split())==223)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==2)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==223)
  test('scope_complete',all(x in unescape(h) for x in ['binary, LSA-rootable, already-simple','level at most two','every admissible rooting must be tree-child','uniform root distribution','displayed-tree mixture','strictly between zero and one','source model’s full dimension','labelled reduced bridge trees','ordinary triangle redirection','proper algebraic exceptional set','dimension 2n + 1','dimension 2n']))
  test('scope_limits_preserved',all(x in unescape(h) for x in ['not equality of entire stochastic model images','within this class','do not show that every weakly tree-child network is ambiguous','physical bridge multipliers remain unidentifiable','exact full distribution with 4^n entries','does not establish worldwide priority']))
  test('zenodo_date_and_printed_month_distinct',r'\date{August 2026}' in source and c['publication_date_label']=='Zenodo date' and c['edition_label']=='Zenodo version 1.1.7' and record['publication_date']==c['publication_date']=='2026-08-23' and record['version']==c['version']=='1.1.7' and c['source_binding']['manuscript_date']=='August 2026' and c['source_binding']['manuscript_version'] is None and '<br>Zenodo date <time datetime="2026-08-23">23 August 2026</time>' in h and c['edition_note'] in unescape(h))
  test('two_original_reader_pdfs',len(texts)==33 and 'Reader supplement (PDF, 7 pages)' in unescape(h) and c['source_binding'].get('embedded_assets',[])==[])
  links=[attrs['href'] for tag,attrs in d.a if tag=='a' and 'href' in attrs]
  test('all_four_selected_assets_linked',len(receipt['files'])==4 and all(asset_name(x) in links for x in receipt['files']))
  related=c['source_binding']['related_records'][0];rp=p/related['receipt'];rr=json.loads(rp.read_text());archive='stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz'
  test('separate_companion_archive_identity',related['record_id']=='22064121' and len(rr['files'])==10 and related['source_receipt_sha256']==sha(rp) and related['record_sha256']==sha(rp.parent/'record.json') and 'https://zenodo.org/records/22064121/files/'+archive+'?download=1' in links and archive not in [asset_name(x) for x in receipt['files']] and not (f.parent/archive).exists())
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['supplement_pdf_sha256']==c['source_binding']['reader_pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()) and all(sha(p/name)==v['sha256'] for name,v in clearance['source_receipts'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/content.json'))
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['verdict']['mathematical_gate']=='NOT_PERFORMED_BY_SCOPE_REVIEWER' and bool(gate['scope_gate_resolution']))
 if rid in NEVO_WARM_IDS:
  test('abstract_full_source_text',normalized_nevo_warm_abstract(rid,a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())=={'23444839':116,'23592692':162}[rid])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)=={'23444839':5,'23592692':7}[rid] and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('archive_main_pdf_identity',sha(p/'sources/published-source/output/pdf'/c['pdf_filename'])==sha(p/'sources'/c['pdf_filename']))
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/CONTENT_CANDIDATE.md' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/CONTENT_CANDIDATE.md'))
  test('frozen_scope_chronology_preserved',bool(gate['scope_gate_resolution']))
 if rid=='23444839':
  test('scope_complete',all(x in unescape(h) for x in ['finite pure two-dimensional abstract simplicial complex','every field of characteristic zero','over any field','both globally and in every face link','need not be induced','after every vertex deletion','not a claim over every field of positive characteristic','without subdivision or an enlarged ambient complex','each of its edges belongs to twelve triangles']))
  test('credited_methods_and_limits',all(x in unescape(h) for x in ['Nevo’s earlier decomposition into minimal cycle complexes','Lubotzky, Samuels and Vishne','modulo t⁹','weighted-cocycle','Euler characteristic two','not a certificate of worldwide priority']))
  test('printed_version_date',r'\date{17 October 2026 \quad (version 1.0.0)}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0.0' and record['publication_date']==c['publication_date']=='2026-10-17')
 if rid=='23592692':
  test('scope_complete',all(x in unescape(h) for x in ['finite simple undirected loopless graph','fixed positive finite rate','fixed positive integer count','α > 4/3','α ≥ 17/4','rates are equal','tree of diameter at most three','1 < α < 4/3','positive probability','unit counts','no assertion at α = 4/3']))
  test('limits_and_prior_credit',all(x in unescape(h) for x in ['uniform bare-cycle spectrum','even-cycle method','least-weight and champion methods','unequal-rate whisker conclusions are false','noninteger initial offsets','not establish the suggested sharp equal-rate whisker conclusion','α > 24','without claiming the first possible numerical improvement of 25','does not certify worldwide priority']))
  test('original_abstract_disclosure_retained',c['abstract'].endswith('AI tools were extensively involved. This is an unrefereed preprint.'))
  test('printed_version_date',r'\date{21 October 2026 \quad Version 1.0.0 \quad Preprint}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0.0' and record['publication_date']==c['publication_date']=='2026-10-21')
 if rid in BRACE_NIJENHUIS_IDS:
  test('abstract_full_source_text',normalized_brace_nijenhuis_abstract(rid,a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())=={'23441906':105,'23431313':141}[rid])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==5 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  duplicate=p/'sources'/({'23441906':'published-source/simple-brace-counterexample-source-and-verification/output/pdf/simple-brace-counterexample.pdf','23431313':'published-source/paper.pdf'}[rid])
  test('archive_main_pdf_identity',sha(duplicate)==sha(p/'sources'/c['pdf_filename']))
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  candidate={'23441906':'reviews/scope/content.json','23431313':'reviews/scope/CONTENT_CANDIDATE.md'}[rid]
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']==candidate and c['source_binding']['frozen_scope_content_sha256']==sha(p/candidate))
  test('frozen_scope_chronology_preserved',bool(gate['scope_gate_resolution']))
 if rid=='23441906':
  test('scope_complete',all(x in unescape(h) for x in ['20,000-element counterexample','additive group C₅⁴ × C₂⁵','(C₅³ ⋊ C₂) × (C₂⁴ ⋊ C₅)','metabelian with all Sylow subgroups abelian','two trivial braces','full admissible symmetric-cocycle definition','(x∗x)∗x = x³ ≠ 0','left-associated product','same additive primary part']))
  test('limits_and_prior_credit',all(x in unescape(h) for x in ['no smallest-order claim','does not classify all finite simple braces','does not exclude asymmetric products with nontrivial factors','general matched-product descriptions','does not assert that every mixed-primary triple product vanishes','does not claim a new general construction formalism','Problem 9, printed page 3228']))
  test('printed_version_date',r'\date{17 October 2026 \quad Version 1.0.0}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0.0' and record['publication_date']==c['publication_date']=='2026-10-17')
 if rid=='23431313':
  test('scope_complete',all(x in unescape(h) for x in ['For every integer n ≥ 1','every prescribed numerical real Jordan matrix J','globally C∞, compactly supported real Nijenhuis operator on ℝⁿ','smooth commuting local frame','nonempty open domain','every eigenvalue at every point','multiple blocks belonging to the same eigenvalue','negative or zero eigenvalues and the zero matrix','In dimension one','same dimension']))
  test('limits_and_prior_credit',all(x in unescape(h) for x in ['does not give a nonzero real-analytic','arbitrarily preassigned realization domain are not prescribed','Global algebraic regularity and a single global Jordan type are not guaranteed','does not forbid local models with nonreal eigenvalues','Earlier work supplies the nonreal obstruction','Historical priority of the full result or this construction is not established','Problem 5.11']))
  policy=clearance['publication_date_policy']
  test('declared_date_not_record_creation',r'\date{15 October 2026, version 1.0}' in source and record['publication_date']==c['publication_date']==policy['publication_date']=='2026-10-15' and c['publication_date_label']==policy['publication_date_label']=='Manuscript dated' and c['source_binding']['record_created_utc']==policy['record_created_utc']=='2026-10-17T05:41:33.490188+00:00' and '<br>Manuscript dated <time datetime="2026-10-15">15 October 2026</time>' in h and all(x in c['edition_note'] for x in ['created on 17 October 2026','not verified public availability','Neither date establishes first priority']))
  test('printed_version_binding',record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0')
  test('original_abstract_limits_and_disclosure_retained',c['abstract'].endswith('This preprint is unrefereed and has no external human peer review or formal proof-assistant certification.'))
 if rid=='23328912':
  test('abstract_full_source_text',normalized_cubulation_abstract(a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())==97)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['formal_machine_verification'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/CONTENT_CANDIDATE.md' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/CONTENT_CANDIDATE.md'))
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['verdict'].get('mathematical_verdict') is None and gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and bool(gate['scope_gate_resolution']))
  test('no_unjustified_follow_up',c['follow_up'] is None and gate['follow_up'] is None)
  test('metadata_version_not_printed_version',record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and c['source_binding']['manuscript_version'] is None and c['edition_label']=='Zenodo version 1.0')
  test('record_creation_exact',json.loads((p/'sources/record.json').read_text())['created']==c['source_binding']['record_created_utc']=='2026-10-13T00:50:56.980394+00:00')
  test('date_qualification_visible',c['publication_date_label']=='Manuscript dated' and all(x in unescape(h) for x in [c['edition_note'],'Manuscript dated','not verified public availability','Neither date establishes first priority']))
  test('scope_complete',all(x in unescape(h) for x in ['φ(a)=a, φ(b)=ab and φ(c)=bcb','the final b in bcb is positive','cell counts (1,7,8,2)','full group F⋊φZ','free, proper and cocompact','general cube-complex convention','before subdivision']))
  test('limits_and_credit',all(x in unescape(h) for x in ['b↦aba','distinct from the b↦ab target','No minimum dimension, minimum cell count, virtual specialness','no historical-firstness or absolute-novelty claim','does not establish current worldwide openness','WPD, Morse and cubical-completion theorems','Leary','Minasyan and Osin','Hagen and Wise']))
  test('printed_manuscript_date',r'\date{October 12, 2026}' in source and record['publication_date']==c['publication_date']=='2026-10-12')
  test('all_three_original_assets_one_reader',len(receipt['files'])==3 and len(texts)==6 and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={'aim_5_2_two_cube_cubulation.pdf','aim_5_2_source.zip','aim_5_2_verification.zip'})
  test('separate_source_verification_links',c['supplement_filename'] is None and len(c['additional_assets'])==2 and {x['filename'] for x in c['additional_assets']}=={'aim_5_2_source.zip','aim_5_2_verification.zip'} and all(x['kind']=='zip' for x in c['additional_assets']) and all(name in [x.get('href') for t,x in d.a if t=='a'] for name in ['aim_5_2_source.zip','aim_5_2_verification.zip']))
  test('no_single_primary_supplement',gate['supplement_sha256'] is None and c['source_binding']['supplement_sha256'] is None)
 if rid=='23524971':
  test('abstract_full_source_text',normalized_dfc_abstract(a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())==124)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==len(c['abstract'].split()))
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['formal_machine_verification'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/content.json'))
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['verdict'].get('mathematical_verdict') is None and gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and bool(gate['scope_gate_resolution']))
  test('no_unjustified_follow_up',c['follow_up'] is None and gate['follow_up'] is None)
  test('metadata_version_not_printed_version',record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and c['source_binding']['manuscript_version'] is None and c['edition_label']=='Zenodo version 1.0')
  test('record_creation_exact',json.loads((p/'sources/record.json').read_text())['created']==c['source_binding']['record_created_utc']=='2026-10-21T04:47:15.316269+00:00')
  test('date_qualification_visible',c['publication_date_label']=='Manuscript dated' and all(x in unescape(h) for x in [c['edition_note'],'Manuscript dated','not verified public availability','Neither date establishes first priority']))
  test('scope_complete',all(x in unescape(h) for x in ['For every fixed real λ>0','N₀⁴','nonexplosive, irreducible and positive recurrent','unique stationary probability distribution','every finite initial state','D=x+y+1','rate λ/2','a(x+1)/D and b(y+1)/D','x(y+1)/D and y(x+1)/D','decrementing a zero coordinate has rate zero','unbounded aggregate seed upload']))
  test('limits_and_credit',all(x in unescape(h) for x in ['empty waiting rooms excluded from the contact denominator','not a solution for a capped-seed','No bound uniform in λ, stationary population moment, completion-time estimate, convergence rate or geometric ergodicity','At λ=0 the zero state is absorbing','2009 preprint conjectured high-load instability','2010 Oberwolfach stability conjecture','retained 2011 author-proof model','does not certify worldwide priority or continued openness','Foster–Lyapunov method','Meyn and Tweedie']))
  test('printed_manuscript_date',r'\date{20 October 2026\\\small Unrefereed preprint draft}' in source and record['publication_date']==c['publication_date']=='2026-10-20')
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==6 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={'dfc_stability.pdf','dfc_stability_verification.zip'})
  test('primary_source_verification_zip',c['supplement_filename']=='dfc_stability_verification.zip' and gate['supplement_sha256']==c['source_binding']['supplement_sha256']==sha(p/'sources'/c['supplement_filename']) and c['supplement_filename'] in [x.get('href') for t,x in d.a if t=='a'])
  test('distinct_original_verdict_schema_preserved',gate['reviews']['analytic']['verdict']['verdict']=='PASS' and gate['reviews']['adversarial']['verdict']['verdict']=='PASS' and gate['reviews']['adversarial']['verdict']['status']=='complete')
 if rid=='23572690':
  test('abstract_full_source_text',normalized_bv_abstract(a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())==114)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath) and c['source_binding']['abstract_word_count']==114)
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path) and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['formal_machine_verification'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] for k,v in gate['reviews'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/content.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/content.json'))
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and bool(gate['scope_gate_resolution']))
  test('no_unjustified_follow_up',c['follow_up'] is None and gate['follow_up'] is None)
  test('printed_edition_date',r'\date{22 October 2026\\\small Preprint, version 1.0.0}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0.0' and record['publication_date']==c['publication_date']=='2026-10-22')
  test('record_creation_exact',json.loads((p/'sources/record.json').read_text())['created']==c['source_binding']['record_created_utc']=='2026-10-22T17:40:39.241356+00:00')
  test('date_qualification_visible',c['publication_date_label']=='Manuscript dated' and c['edition_note'] in unescape(h) and 'do not establish first priority' in unescape(h))
  test('exact_nonzero_characteristic_zero_domain',all(x in unescape(h) for x in ['For any characteristic-zero field k and nonzero h∈k[x]','ordinary HH•(A_h,A_h)','canonical Gerstenhaber bracket','Nonzero constant polynomials','original field','does not require the polynomial to split']))
  test('all_generator_obstruction_and_zero_positive_case',all(x in unescape(h) for x in ['no bracket generator exists','zero operator is a BV generator','every degree-minus-one bracket generator','even if its square is not required to vanish','central degree-one class annihilates every other degree-one class']))
  test('embedded_zero_boundary',all(x in unescape(h) for x in ['literal embedded h=0 case instead gives k[x]','Δ(f∂x)=−f′','abstract two-generator presentation gives a different algebra, k[x,Y]']))
  test('scope_limits_and_predecessors',all(x in unescape(h) for x in ['does not classify arbitrary Weyl subalgebras, positive-characteristic cases, twisted-coefficient variants, or Poisson analogues','It makes no first-discovery claim','Lopes and Solotar','Benkart, Lopes and Ondrus','Herscovich and Li','Proposition 4.15','Theorem 1.7 assumes a semisimple modular automorphism']))
  test('two_original_assets_one_reader',len(receipt['files'])==2 and len(texts)==6 and c.get('additional_assets',[])==[] and c['source_binding'].get('embedded_assets',[])==[] and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']})
  test('primary_source_verification_zip',c['supplement_filename']=='bv-generators-source-and-verification.zip' and gate['supplement_sha256']==c['source_binding']['supplement_sha256']==sha(p/'sources'/c['supplement_filename']) and c['supplement_filename'] in [x.get('href') for t,x in d.a if t=='a'])
 if rid in REACH_SATOH_IDS:
  source_hash={'23431676':'daaacbeb3b198a8c13208663a6e49fc417a5b7ec2e7a0bfa62a9a87e42ce7f5f','23387442':'6860fe1479f4fb0737489311e0b6c6ec4fda616e98e245feede72b4bde593af8'}[rid]
  clearance_hash={'23431676':'8e97b60c0ef40677bb217806a59269949bfae6cc25fbfd02dbc29b58cabf733c','23387442':'1a100a1722debd437303b74a81585a97cce3defca16923179af9fc5b912ede1f'}[rid]
  test('abstract_full_source_text',normalized_reach_satoh_abstract(rid,a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())==c['source_binding']['abstract_word_count']=={'23431676':125,'23387442':104}[rid])
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',c['source_binding']['abstract_source']=='sources/'+TEX_PATHS[rid] and c['source_binding']['abstract_source_sha256']==sha(textpath)==source_hash and c['source_binding']['source_tex_path']==c['source_binding']['abstract_source'] and c['source_binding']['source_tex_sha256']==source_hash)
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==sha(p/'sources/receipt.json')==c['source_binding']['receipt_sha256']==c['source_binding']['source_receipt_sha256'])
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_bytes()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==c['source_binding']['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] and (p/'sources'/asset_name(x)).stat().st_size==x['bytes'] for x in receipt['files']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_bytes())
  test('root_clearance_binding',clearance['record_id']==rid and clearance['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['root_clearance_sha256']==sha(clearance_path)==clearance_hash and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['source_repair'] is False and gate['human_peer_review'] is False and gate['formal_machine_verification'] is False)
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] and clearance['reviews'][k]['report']==('papers/'+rid+'/'+v['report']) and clearance['reviews'][k]['verdict']==('papers/'+rid+'/'+v['verdict_file']) for k,v in gate['reviews'].items()))
  test('frozen_scope_candidate_binding',c['source_binding']['frozen_scope_content_path']=='reviews/scope/candidate.json' and c['source_binding']['frozen_scope_content_sha256']==sha(p/'reviews/scope/candidate.json'))
  scope_verdict=gate['reviews']['scope']['verdict']
  test('frozen_scope_chronology_preserved',scope_verdict['status']=='SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING' and scope_verdict['mathematical_verdict'] is None and scope_verdict['publication_authorized'] is False and gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and gate['scope_gate_resolution']==clearance['scope_gate_resolution'])
  test('no_unjustified_follow_up',c['follow_up'] is None and gate['follow_up'] is None and clearance['follow_up'] is None)
  test('metadata_author_orcid',c['author']=='Alec Kriebel' and art['author'][0]['sameAs']=='https://orcid.org/0009-0001-9320-500X' and c['doi']=='10.5281/zenodo.'+rid)
  test('record_metadata_binding',sha(p/'sources/record.json')==c['source_binding'].get('metadata_sha256',c['source_binding'].get('record_sha256')))
  test('record_creation_exact',json.loads((p/'sources/record.json').read_bytes())['created']==c['source_binding']['record_created_utc']=={'23431676':'2026-10-17T05:45:36.045033+00:00','23387442':'2026-10-15T07:50:10.998117+00:00'}[rid])
  test('manuscript_date_distinguished',c['publication_date_label']=='Manuscript dated' and c['publication_date']==record['publication_date']=='2026-10-15' and c['source_binding']['manuscript_date']=='2026-10-15' and c['edition_note'] in unescape(h) and '<br>Manuscript dated <time datetime="2026-10-15">15 October 2026</time>' in h)
  test('unrefereed_ai_and_authorship',all(x in unescape(h) for x in ['Unrefereed preprint','AI tools were used extensively','human peer review','actual research contributions']) and art['creativeWorkStatus']=='Unrefereed preprint')
  test('two_original_assets_one_reader',len(receipt['files'])==2 and {asset_name(x) for x in receipt['files']}=={name for _,name in assets} and c['source_binding']['embedded_assets']==[] and len(frames)==1 and len(texts)=={'23431676':6,'23387442':4}[rid])
  if rid=='23431676':
   test('raw_assets_schema_preserved','files' not in raw_receipt and receipt['files']==raw_receipt['assets'] and gate['source_receipt_asset_field']==c['source_binding']['receipt_asset_field']=='assets' and sha(p/'sources/receipt.json')=='c4ecaf95a88e3cf418f6587396cdb1ad05f191cbe96c6546c990e523f29cb548')
   test('scope_complete',all(x in unescape(h) for x in ['finite nonempty loopless strongly connected directed multigraphs','finite sequential legal firing word','nonnegative initial configuration','specified nonnegative target','deterministic polynomial-time many-one reductions','number of vertices varies with the input','both configurations are encoded in binary','empty firing word is allowed','may stop even when another move remains available','Malformed inputs are rejected','one-vertex loopless case, reachability is exactly equality','every target-reaching word','polynomially many bits']))
   test('limits_and_prior_credit',all(x in unescape(h) for x in ['No corresponding classification is established for simple graphs, unary encodings, bounded degrees or bounded total chip counts','Both input configurations are nonnegative','does not establish coNP membership for every signed formulation','not the running time of a reachability algorithm','Prior work by Hujter, Kiss and Tóthmérész supplies coNP membership','Farrell and Levine','Björner and Lovász','Priority of the complete result or gate/marker mechanism, independent discovery and present worldwide openness remain unestablished']))
   test('printed_version_date',r'\date{15 October 2026, version 1.0}' in source and record['version']==c['version']==c['source_binding']['manuscript_version']=='1.0' and c['source_binding']['publication_date_policy']['record_created_utc']==clearance['publication_date_policy']['record_created_utc'] and 'not verified public availability' in unescape(h))
   test('authenticated_missing_kind_zip',c['supplement_filename'] is None and gate['supplement_sha256'] is None and c['additional_assets']==[{'filename':'pr1097_support_v1_0.zip','label':'Source and verification package (ZIP)'}] and resolver.additional_asset_kind(c['additional_assets'][0])=='zip')
  else:
   test('abstract_five_complete_sentences',len(re.findall(r'\.(?:\s|$)',c['abstract']))==5 and hashlib.sha256(a.strip().encode()).hexdigest()==c['source_binding']['abstract_tex_sha256'])
   test('scope_complete',all(x in unescape(h) for x in ['integral lower central series','entire J/J^{k+1}','rational algebra of SL(2,ℂ) matrix-entry functions','[g,h]=ghg⁻¹h⁻¹','w=[[[x₁,x₂],[x₁,x₃]],x₁]','For every n≥4, the automorphism x₄↦x₄w fixing the other generators lies in D_n(5) but not A_n(5)','v=[[[x₁,x₂],[x₁,[x₁,x₂]]],x₁]','For every n≥3, the automorphism x₃↦x₃v fixing the other generators lies in D_n(6) but not A_n(6)','actual powers J⁶ and J⁷','Integral Magnus expansions']))
   test('limits_and_prior_credit',all(x in unescape(h) for x in ['does not establish a degree-five counterexample at rank three, failure in every degree, or an extension to larger matrix sizes','not a theorem about a trace algebra, a character algebra or a Grothendieck representation ring','distinct from the comparison of the Andreadakis filtration with the lower central series of IA_n','no new polynomial identity, historical firstness, exhaustive novelty clearance or continuing worldwide openness','2018 Oberwolfach report, pp.87–90','8 December 2017','2021 Pacific Journal of Mathematics publication','final journal text was not inspected','27 February 2015','Razmyslov','through Burde']))
   test('metadata_version_not_printed_version',r'\date{15 October 2026}' in source and record['version']==c['version']==c['source_binding']['zenodo_version']=='1.0' and c['source_binding']['manuscript_version'] is None and c['edition_label']==c['citation_edition_label']=='Zenodo version 1.0' and 'manuscript does not print a version number' in unescape(h))
   test('primary_source_verification_zip',c['supplement_filename']=='satoh_filtration_verification.zip' and c['additional_assets']==[] and gate['supplement_sha256']==c['source_binding']['supplement_sha256']==sha(p/'sources'/c['supplement_filename']))
 if rid in BRAID_WAVE_WREATH_IDS:
  binding=c['source_binding'];scope_verdict=gate['reviews']['scope']['verdict']
  normalizer={'23393596':normalized_braid_abstract,'23358014':normalized_wave_abstract,'23356964':normalized_wreath_abstract}[rid]
  expected_words={'23393596':81,'23358014':116,'23356964':93}[rid]
  expected_sentences={'23393596':5,'23358014':6,'23356964':6}[rid]
  expected_tex_sha={'23393596':'0f469c9c6c70475bdefac2ea261e7a8cbf2fe5c9e6714447a2a25cd2db0da897','23358014':'bf4e13509ee738d1c5f73555e322ce77b9f2041b2306e4f80dfc588c98289584','23356964':'d636a7b3502bfa2e5bd79e01d5b332fd3b796c9ada60b67bbce30e54eac5aa02'}[rid]
  expected_clearance_sha={'23393596':'36b0ccc972b713e507c5ea5a60f86f332fc0668fb9805e8e523d755c6643a871','23358014':'7ecd074783bbf82d6a7a6f31074cd6c6e0bf22fa9180400cc96949c259a5b8cf','23356964':'e845d4a8a6c1db3c442a3d67889bbb5cfe027b5b87897243dc1782935818ca6b'}[rid]
  expected_date={'23393596':'2026-10-15','23358014':'2026-10-14','23356964':'2026-10-13'}[rid]
  expected_created={'23393596':'2026-10-15T11:19:16.531335+00:00','23358014':'2026-10-14T05:39:12.680683+00:00','23356964':'2026-10-14T04:32:49.677542+00:00'}[rid]
  expected_version='1.0.0' if rid=='23356964' else '1.0'
  candidate_path='reviews/scope/content.json' if rid=='23358014' else 'reviews/scope/candidate.json'
  candidate=json.loads((p/candidate_path).read_text())
  test('abstract_full_source_text',normalizer(a)==c['abstract'])
  test('abstract_full_source_word_count',len(c['abstract'].split())==expected_words)
  test('abstract_full_source_sentence_count',len(re.findall(r'\.(?:\s|$)',c['abstract']))==expected_sentences)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',binding['abstract_source']==binding['source_tex_path']=='sources/'+TEX_PATHS[rid] and binding['abstract_source_sha256']==binding['source_tex_sha256']==sha(textpath)==expected_tex_sha and binding['abstract_tex_sha256']==hashlib.sha256(a.strip().encode()).hexdigest() and binding['abstract_word_count']==expected_words)
  test('frozen_scope_candidate_binding',binding['frozen_scope_content_path']==candidate_path and binding['frozen_scope_content_sha256']==sha(p/candidate_path) and candidate['abstract']==c['abstract'])
  test('promotion_source_receipt_binding',gate['source_receipt_sha256']==binding['source_receipt_sha256']==binding['receipt_sha256']==sha(p/'sources/receipt.json'))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  test('all_published_source_assets_bound',gate['source_files']==receipt['files']==binding['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  test('source_pdf_supplement_bindings',gate['pdf_sha256']==binding['pdf_sha256']==sha(p/'sources'/c['pdf_filename']) and gate['supplement_sha256']==binding['supplement_sha256']==sha(p/'sources'/c['supplement_filename']))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',gate['root_clearance_file']==c['review_metadata']['root_clearance_file']=='verification/root-clearance-'+rid+'-20261025.json' and gate['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']==sha(clearance_path)==expected_clearance_sha and gate['root_clearance_record']==clearance and clearance['record_id']==rid and clearance['status']==gate['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and gate['approved_scope']==clearance['approved_scope'])
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and set(clearance['reviews'])==set(gate['reviews']) and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] and clearance['reviews'][k]['report']=='papers/'+rid+'/'+v['report'] and clearance['reviews'][k]['verdict']=='papers/'+rid+'/'+v['verdict_file'] for k,v in gate['reviews'].items()) and all(sha(p/name)==v['sha256'] for name,v in clearance['source_receipts'].items()))
  test('root_disposition_at_stated_scope',gate['source_repair'] is False and clearance['source_repair'] is False and gate['human_peer_review'] is False and gate['formal_machine_verification'] is False and all(gate['reviews'][k]['verdict']['status']=='PASS' and gate['reviews'][k]['root_disposition']=='PASS' for k in ['analytic','adversarial']))
  test('frozen_scope_chronology_preserved',gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and gate['scope_gate_resolution']==clearance['scope_gate_resolution'] and (scope_verdict['status']=='SCOPE_COMPLETE_PENDING_MATHEMATICAL_REVIEW' and scope_verdict['mathematical_pass'] is False and scope_verdict['promotion_authorized'] is False if rid=='23358014' else scope_verdict['status']=='SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING' and scope_verdict['mathematical_verdict'] is None and scope_verdict['publication_authorized'] is False))
  test('record_metadata_binding',sha(p/'sources/record.json')==binding['record_sha256']==raw_receipt['record_sha256'])
  test('record_creation_exact',json.loads((p/'sources/record.json').read_text())['created']==binding['record_created_utc']==expected_created)
  printed_date={'23393596':r'\date{October 15, 2026\quad (version 1.0)}','23358014':r'\date{October 14, 2026 \quad (version 1.0)}','23356964':r'\date{October 13, 2026\quad (version 1.0.0)}'}[rid]
  test('printed_version_date',printed_date in source and record['version']==c['version']==binding['manuscript_version']==binding['zenodo_version']==expected_version and record['publication_date']==c['publication_date']==binding['manuscript_date']==binding['zenodo_publication_date']==expected_date)
  test('manuscript_date_distinguished',c['publication_date_label']=='Manuscript dated' and c['edition_label']==c['citation_edition_label']=='Version '+expected_version and '<br>Manuscript dated <time datetime="'+expected_date+'">' in h and c['edition_note'] in unescape(h) and 'do not establish first priority' in c['edition_note'])
  test('metadata_author_orcid',c['author']=='Alec Kriebel' and c['orcid']==art['author'][0]['sameAs']=='https://orcid.org/0009-0001-9320-500X' and c['doi']=='10.5281/zenodo.'+rid and c['canonical_url']==base)
  test('two_original_assets_one_reader',len(receipt['files'])==2 and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']} and c['supplement_filename'].endswith('.zip') and c['additional_assets']==[] and binding['embedded_assets']==[] and len(frames)==1 and len(texts)==c['pdf_pages']=={'23393596':4,'23358014':6,'23356964':5}[rid])
  with zipfile.ZipFile(p/'sources'/c['supplement_filename']) as original_archive:
   embedded_pdf_members=[x for x in original_archive.infolist() if not x.is_dir() and x.filename.lower().endswith('.pdf')]
   test('archive_only_duplicate_or_no_reader',len(embedded_pdf_members)==(0 if rid=='23358014' else 1) and all(hashlib.sha256(original_archive.read(x)).hexdigest()==binding['pdf_sha256'] for x in embedded_pdf_members))
  if rid=='23358014':
   test('raw_assets_receipt_preserved','files' not in raw_receipt and receipt['files']==raw_receipt['assets'] and sha(p/'sources/receipt.json')=='8f0fb5b950d0b62c8bf31c5d7d7a6bc754e742ef8c08aa775b58fcb8d487cc8f')
  else:
   test('archive_main_pdf_identity',sha(textpath.parent/'note.pdf')==binding['pdf_sha256'])
  test('unrefereed_ai_and_authorship',art['creativeWorkStatus']=='Unrefereed preprint' and all(x in unescape(h) for x in ['Unrefereed preprint',c['ai_disclosure'],c['collaboration'],'used extensively','actual research contributions']) and any(x in unescape(h) for x in ['human peer review','human or journal peer review']))
  test('no_unjustified_follow_up',c['follow_up'] is None and gate['follow_up'] is None and clearance['follow_up'] is None)
  test('no_private_custody_or_replay',not any(x in visible_text for x in ['25 october 2026','october 25','2026-10-25','sha256','sha-256','root-clearance','replay counts','checks passed','audit completed',expected_clearance_sha]))
 if rid=='23393596':
  test('scope_complete',all(x in unescape(h) for x in ['classical disk pure braid group','For every m≥3 and every finite integer k≥1','standard oriented closure','integrally smoothly 1-solvable','Otto Definition 2.3','string-link concordance classes','P_m^(n+2)⊄F_n^m for every m≥3 and integer n≥1']))
  test('derived_depth_and_category_limits',all(x in unescape(h) for x in ['witness may depend on the finite depth k','No single braid in the intersection of all derived subgroups','For m=1 and m=2, the positive derived subgroups are trivial','integers n≥1','prior n=0 containment','power subgroups, lower central series, rational derived series, surface braid groups, rational solvability or a merely topological solvability category']))
  test('finite_example_exact_scope',all(x in unescape(h) for x in ['a=σ₁², b=σ₂², c=[a,b], d=a⁻¹ca, e=b⁻¹cb, u=[c,d], v=[d,e] and β=[u,v]','[x,y]=xyx⁻¹y⁻¹','104-letter freely reduced Artin word','closure signature −2','explicit 104-crossing word is supplied only for k=3','No minimal crossing number or effective word-length bound at arbitrary depth','arbitrary-depth existence proof is independent of that calculation']))
  test('power_amplification_mechanism',all(x in unescape(h) for x in ['ordinary signature and its homogenization are distinct','q restricted to the pure braid group P₃ is not a homomorphism','solvable, hence amenable, quotient','suitable positive power is essential','nonzero q on a braid does not by itself give nonzero ordinary signature on that same braid','zero pairwise linking numbers','adding split trivial strands reaches every m≥3']))
  test('credited_tools_history_and_limits',all(x in unescape(h) for x in ['Harvey, with Park and Ray','Question 3 on page 3021','2017/50 and was published in 2018','Gambaudo and Ghys','Calegari','Kawasaki, Kimura, Maruyama, Matsushita and Mimura','Toffoli','printed index discrepancy in Erle’s matrix formula','crossing geometry','separate Burau–Meyer calculation','No historical firstness, exhaustive novelty clearance or continued worldwide openness']))
 if rid=='23358014':
  test('scope_complete',all(x in unescape(h) for x in ['real defocusing quintic wave equation yₜₜ − Δy + y⁵ = u','three-dimensional unit ball B','zero position and velocity initially','homogeneous Dirichlet boundary conditions and final time 1','H=L²(B)','L²(0,1;H)','‖u(t)‖H ≤ ρ almost everywhere in time','every fixed 0<ρ≤ρ* and every fixed finite ν≥0']))
  test('only_quadratic_control_cost_removed',all(x in unescape(h) for x in ['L⁴(0,1;L¹²(B)) state norm','L¹(0,1;H) sparse-control penalty: γ=β₁=1','Only the quadratic control penalty is removed, β₂=0','ν‖yₜ(1)‖²H⁻¹(B)/2','not a pointwise bound on |u(t,x)|','No assertion concerns ν = ∞']))
  test('nonlinear_global_growth_counterexample',all(x in unescape(h) for x in ['zero is the unique global optimizer over all admissible controls','Δ(u)≥A³/(12ρ²)','ordinary critical cone is {0}','strict substitute second-variation condition is vacuous','uₕ=he·1{|t−1/2|<h}','‖uₕ‖²L²(0,1;H)=2h³','Δ(uₕ)=(π²/3+2/π²)h⁴+O(h⁶)','fails in both L² and L∞ neighborhoods of zero','does not assume that the nonlinear solution stays in one eigenmode']))
  test('every_optimizer_and_uniformity_scope',all(x in unescape(h) for x in ['Global optimizers exist for every terminal target d∈H','every choice of global optimizers satisfies ‖uε‖L²/ε→∞','Δ(u)≥‖u‖²L¹/(4π²)','arbitrary nearby target πe+w, put ε=‖w‖H','‖u‖L¹=O(ε) and ‖u‖L²=O(√ε)','constants and this upper-bound neighborhood can be chosen uniformly over all finite ν≥0','‖uε‖L¹=Θ(ε) and cε³ᐟ⁴≤‖uε‖L²≤C√ε','lower-comparison neighborhood may depend on the fixed ν','do not assert a sharp L² response exponent']))
  test('response_limits_and_positive_countercase',all(x in unescape(h) for x in ['does not rule out adapted sufficient conditions, enlarged cones, nondegeneracy assumptions or growth in weaker norms','do not prove perturbed-optimizer uniqueness, a pairwise Lipschitz selection, L∞ convergence of perturbed optimizers','does not assert the same failure for every domain, every target, arbitrary large caps, Neumann conditions or boundary control','For target d=0 in the same model','J0,ν(u)≥‖u‖L¹≥‖u‖²L²/ρ','strong quadratic growth does hold']))
  test('classical_credit_and_source_editions',all(x in unescape(h) for x in ['established concentration and noncoercivity mechanism','Dunn’s earlier counterexample','Prior group-sparsity and subgradient calculus','arXiv:1907.02744v1 (5 July 2019)','2020 journal publication, whose final body was not inspected','Printed pp.438–440','addresses the unchanged implication, not every possible unregularized theory','without a worldwide-firstness or present-day-openness claim']))
 if rid=='23356964':
  test('scope_complete',all(x in unescape(h) for x in ['countable discrete restricted wreath product','dense Gδ subset of the full Polish space Act(W,2^ℕ)','subspace topology from Homeo(2^ℕ)^W','hyperfinite orbit equivalence relation on the entire Cantor space 2^ℕ','actual Borel map p:X→Ẑ satisfying p(gx)=p(x)+χ(g)','permits stabilizers and does not require freeness, minimality, an invariant probability measure or surjectivity of p']))
  test('genericity_and_height_limits',all(x in unescape(h) for x in ['not identify the entire set of hyperfinite actions as Gδ','Stabilizers and nonsurjective maps are allowed','onto height obtained for generic continuous Cantor actions is a consequence of that compact setting','does not treat all Borel W-actions without a height factor','No comeager conjugacy class, uniform Borel choice of heights or exhaustions across actions, or clopen finite exhaustion']))
  test('compatible_metrics_and_exceptional_height',all(x in unescape(h) for x in ['dimension may grow with the width, and slab components may be infinite','Divisible widths give nested slab graphs with decreasing distances','exact compatible-metric hypothesis of their Theorem 7.3','full preimage of the embedded integers, which may be uncountable','height cutoff is essential to keep the pulled-back classes finite','rather than a general theorem about increasing unions of hyperfinite relations']))
  test('credited_inputs_and_historical_scope',all(x in unescape(h) for x in ['Question 3 in Iyer’s contribution, joint with Shinko','established Cantor-action lifting principles','Corollary 5.5','Theorem 7.3','Corollary 7.5','The prior generic hyperfiniteness theorem assumes locally finite asymptotic dimension','linked 2006 author preprint','later 2008 journal paper','Finite diagnostics','do not prove the Baire-category or infinite Borel assertions','No historical firstness, continued worldwide openness']))
 if rid=='23306332':
  binding=c['source_binding'];metadata_file=p/'sources/metadata.json'
  quadratic_public_text=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<body>(.*?)</body>',h,re.S).group(1))).split()).lower()
  test('abstract_full_source_text',normalized_quadratic_abstract(a)==c['abstract'])
  test('abstract_full_124_words_seven_sentences',len(c['abstract'].split())==binding['abstract_word_count']==124 and len(re.findall(r'\.(?:\s|$)',c['abstract']))==7)
  test('abstract_source_paragraphs',len(re.split(r'\n\s*\n',a.strip()))==len(c['abstract'].split('\n\n'))==1)
  test('abstract_source_binding',binding['source_tex_path']==binding['abstract_source']=='sources/'+TEX_PATHS[rid] and binding['source_tex_sha256']==binding['abstract_source_sha256']==sha(textpath)=='caf327484a7068244ab98494eab835f50b84521a6d7ba364007bda31f7478677' and binding['abstract_tex_sha256']==hashlib.sha256(a.strip().encode()).hexdigest()=='e923d5b23fa4b00127bb3c3b1a9ec5382d45ebb2d366aadab0ce6f3e959c8aff')
  candidate_path=p/'reviews/scope/public-candidate.json';candidate=json.loads(candidate_path.read_text())
  test('frozen_scope_candidate_binding',binding['frozen_scope_content_path']=='reviews/scope/public-candidate.json' and binding['frozen_scope_content_sha256']==sha(candidate_path) and binding['frozen_scope_abstract_field']=='full_original_abstract' and candidate['full_original_abstract']==c['abstract'])
  test('original_metadata_path_binding',record_file==metadata_file and binding['metadata_path']==binding['record_path']==gate['metadata_path']=='sources/metadata.json' and sha(metadata_file)==binding['metadata_sha256']==binding['record_sha256']==gate['metadata_sha256']==raw_receipt['metadata_sha256']=='82e624db015b8f612e7d1eb56463b6c035130e88d4579887c3b5306ef3dd9bdd')
  test('original_receipt_schema_binding',raw_receipt['record_id']==23306332 and all('filename' in x and 'name' not in x for x in raw_receipt['files']) and gate['source_receipt_sha256']==binding['receipt_sha256']==binding['source_receipt_sha256']==sha(p/'sources/receipt.json')=='1267dcd347b53c295116bac15151fa92dff359469da3c0c7e16c1e6a8de3d53a')
  test('all_published_source_assets_bound',gate['source_files']==binding['files']==receipt['files'] and all(sha(p/'sources'/asset_name(x))==x['sha256'] for x in receipt['files']))
  test('pdf_zip_source_bindings',gate['pdf_sha256']==binding['pdf_sha256']==sha(p/'sources'/c['pdf_filename']) and gate['supplement_sha256']==binding['supplement_sha256']==sha(p/'sources'/c['supplement_filename']))
  test('two_original_assets_one_reader',len(receipt['files'])==2 and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']} and c['additional_assets']==binding['embedded_assets']==[] and len(frames)==1 and len(texts)==c['pdf_pages']==6 and c['supplement_filename']=='nonunique_nearest_stable_complex_quadratics_verification.zip')
  with zipfile.ZipFile(p/'sources'/c['supplement_filename']) as original_archive:
   members=[x for x in original_archive.infolist() if not x.is_dir()]
   test('twelve_double_nested_source_members',len(members)==12 and all((p/'sources/published-source/nonunique_nearest_stable_complex_quadratics_verification'/x.filename).read_bytes()==original_archive.read(x) for x in members))
   test('no_embedded_reader_or_nested_archive',not any(x.filename.lower().endswith(('.pdf','.zip','.tar','.gz')) for x in members))
  test('promotion_review_bindings',set(gate['reviews'])=={'analytic','adversarial','scope'} and all(v['sha256']==sha(p/v['report']) and v['verdict_sha256']==sha(p/v['verdict_file']) and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for v in gate['reviews'].values()))
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('root_clearance_binding',gate['root_clearance_file']==c['review_metadata']['root_clearance_file']=='verification/root-clearance-23306332-20261025.json' and gate['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']==sha(clearance_path)=='9faabde229535455e707dfae14639727c129953be08b08b2984299a83da0b436' and clearance==gate['root_clearance_record'] and clearance['record_id']==rid and clearance['status']==gate['status']=='PASS' and clearance['disposition_by']==gate['disposition_by']=='root' and clearance['approved_scope']==gate['approved_scope'])
  test('root_clearance_source_review_identity',clearance['pdf_sha256']==gate['pdf_sha256'] and clearance['source_receipt_sha256']==gate['source_receipt_sha256'] and set(clearance['reviews'])==set(gate['reviews']) and all(clearance['reviews'][k]['report_sha256']==v['sha256'] and clearance['reviews'][k]['verdict_sha256']==v['verdict_sha256'] and clearance['reviews'][k]['report']=='papers/'+rid+'/'+v['report'] and clearance['reviews'][k]['verdict']=='papers/'+rid+'/'+v['verdict_file'] for k,v in gate['reviews'].items()) and all(sha(p/name)==x['sha256'] for name,x in clearance['source_receipts'].items()))
  test('original_review_seals_bound',all(sha(R/x['path'])==x['sha256'] for x in clearance['root_review_seals_rehashed']))
  av=gate['reviews']['analytic']['verdict'];dv=gate['reviews']['adversarial']['verdict'];sv=gate['reviews']['scope']['verdict']
  test('custom_scientific_verdicts_preserved',av['verdict']=='PASS_WITH_BOUNDED_BIBLIOGRAPHIC_LIMITS' and av['publication_clearance'] is False and dv['result']=='no_substantive_mathematical_defect_found' and dv['promotion_clearance'] is False and gate['reviews']['analytic']['root_disposition']==gate['reviews']['adversarial']['root_disposition']=='PASS')
  test('frozen_scope_chronology_preserved',sv['scope_status']=='COMPLETE — conditional scope candidate ready' and sv['mathematical_pass'] is False and sv['mathematical_verdict'] is None and sv['promotion_authorized'] is False and gate['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and gate['scope_gate_resolution']==clearance['scope_gate_resolution'])
  test('no_source_repair_or_review_overclaim',gate['source_repair'] is clearance['source_repair'] is False and gate['human_peer_review'] is gate['formal_machine_verification'] is False)
  test('record_creation_exact',json.loads(metadata_file.read_text())['created']==binding['record_created_utc']=='2026-10-11T23:14:10.664861+00:00')
  test('printed_date_and_metadata_version_distinguished',r'\date{11 October 2026\quad\textnormal{(research note; unrefereed preprint)}}' in source and 'version 1.0' not in source.lower() and binding['manuscript_version'] is None and record['version']==c['version']==binding['zenodo_version']=='1.0' and record['publication_date']==c['publication_date']==binding['manuscript_date']=='2026-10-11' and c['edition_label']==c['citation_edition_label']=='Zenodo version 1.0' and c['publication_date_label']=='Manuscript dated' and '<br>Manuscript dated <time datetime="2026-10-11">11 October 2026</time>' in h and c['edition_note'] in unescape(h) and 'without printing a version number' in c['edition_note'] and 'do not establish first priority' in c['edition_note'])
  test('metadata_author_orcid',c['title']=='Nonunique nearest stable complex quadratics' and c['author']=='Alec Kriebel' and c['orcid']==art['author'][0]['sameAs']=='https://orcid.org/0009-0001-9320-500X' and c['doi']=='10.5281/zenodo.23306332' and c['canonical_url']==base)
  test('scope_complete',all(x in unescape(h) for x in ['complex monic quadratic p(z)=z²+az+b','α(p)≤0','(Re a, Im a, Re b, Im b)','For each fixed real symmetric positive-definite coefficient matrix G','every neighborhood of that point contains some unstable quadratic','at least two distinct attained global nearest points','all complex stable quadratics, including repeated and imaginary-axis roots']))
  test('full_degree_attainment_scope',all(x in unescape(h) for x in ['ℓ≠0','at (1,0,0)','coefficient metric on ℝ⁶','Both real leading-coefficient directions are included','original exact-degree set','not globally closed','clipped set is compact','less than R/3','more than 2R/3','clipped and original global minimizers coincide']))
  test('mixed_epigraph_covector_scope',all(x in unescape(h) for x in ['entire abscissa epigraph','height zero over the monic and full-degree base points','metric may mix height and coefficient coordinates','limiting support covector is horizontal','representing normal vector can tilt in a mixed metric']))
  test('separate_finite_subgradient_function_scope',all(x in unescape(h) for x in ['Separately, the monic complex quadratic abscissa','each fixed finite limiting subgradient v₀','real Euclidean coefficient metric','local constants may depend on the chosen v₀','epigraph normal is (v₀,−1)','does not give constants uniform over all finite subgradients','full-degree function theorem','function theorem for every mixed coefficient/height metric']))
  test('actual_normals_and_classical_projection',all(x in unescape(h) for x in ['x≥0, U=u+y²/4≥0 and V²≤x²U','Both nonnegativity conditions are needed','n₀·cₜ=t³','2t⁴+t⁶','actual proximal normals','classical Poliquin–Rockafellar–Thibault projection characterization','bounded minimizing-sequence argument','Theorem 1.3(a),(k)','local weak-closedness condition is automatic in finite dimensions']))
  test('function_proof_and_composition_caveat',all(x in unescape(h) for x in ['invertible discriminant-coordinate map (a,b)↦(a,a²−4b)','transports lower supports in both directions','Fixing a finite subgradient','Theorem 3.1 is a prox-regularity composition result under hypotheses','does not itself state unconditional exact subdifferential equality','explicit two-sided diffeomorphism and lower-support argument independently supplies the equality']))
  test('historical_conventions_and_prior_credit',all(x in unescape(h) for x in ['Section 8, printed pp.166–168','Question 1 on p.106','leaves field, normalization and metric unspecified','Burke and Overton','Kirillov and Overton','Orban de Xivry','Moses and Liu','original Cross, Moses–Liu and Bottema bodies were not inspected','exact example and nonuniqueness comparisons are not asserted here']))
  test('limits_and_positive_real_boundary',all(x in unescape(h) for x in ['no all-degree or real-only classification','convex orthant a≥0,b≥0','unique projection in every fixed positive-definite inner product','arbitrary norms, singular or varying metrics','nonlinear parameter-dependent metrics','does not apply to every nearby unstable target','No explicit unstable input together with its two minimizing stable polynomials','Decimal controls are not interval-certified bounds','No historical firstness, exhaustive novelty clearance or continued worldwide openness']))
  test('unrefereed_ai_and_authorship',art['creativeWorkStatus']=='Unrefereed preprint' and all(x in unescape(h) for x in ['Unrefereed preprint',c['ai_disclosure'],c['collaboration'],'used extensively','not independent human or journal peer review','without formal proof-assistant certification','actual research contributions']))
  test('no_unjustified_follow_up',c['follow_up'] is gate['follow_up'] is clearance['follow_up'] is None)
  test('no_private_audit_narrative',not any(x in quadratic_public_text for x in ['root-clearance','sha256','sha-256','replay','31,233','31233','4,305','4305','2,005','2005 rational','25 october 2026','2026-10-25']))
 if rid=='23203100':
  binding=c['source_binding'];body=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<body>(.*?)</body>',h,re.S).group(1))).split())
  clearance=gate['root_clearance_record']
  test('authenticated_original_source_layout',type(raw_receipt) is list and asset_root==p/'sources/assets' and record_file==p/'sources/record/zenodo_record.json' and gate['source_receipt_sha256']==binding['receipt_sha256']==sha(receipt_file)=='8170b3100a1e00bb4f1c5cb0477079b48dd162cf3d8fcb4b063c87473ba28025')
  test('full_original_abstract',normalized_bosonic_abstract(a)==c['abstract']==(p/'reviews/editorial/ABSTRACT.txt').read_text().strip()==(p/'reviews/scope/ORIGINAL_ABSTRACT.txt').read_text().strip())
  test('abstract_146_words_eight_sentences_one_paragraph',len(c['abstract'].split())==binding['abstract_word_count']==146 and len(re.findall(r'\.(?:\s|$)',c['abstract']))==8 and len(re.split(r'\n\s*\n',a.strip()))==1)
  test('tex_and_abstract_hashes',binding['source_tex_path']==binding['abstract_source']=='sources/'+TEX_PATHS[rid] and sha(textpath)==binding['source_tex_sha256']==binding['abstract_source_sha256']=='eda0b20fb843fda3b7b70203b63628e36ebf5d4a1b6c817624d3a5810f9beaab' and hashlib.sha256(a.strip().encode()).hexdigest()==binding['abstract_tex_sha256'] and hashlib.sha256(c['abstract'].encode()).hexdigest()==binding['abstract_sha256'])
  candidate_path=p/binding['frozen_scope_content_path'];candidate=json.loads(candidate_path.read_text())
  test('frozen_scope_abstract',sha(candidate_path)==binding['frozen_scope_content_sha256'] and candidate[binding['frozen_scope_abstract_field']]==c['abstract'])
  expected=json.loads((p/'reviews/editorial/public-sections.json').read_text())
  for section_id,section in expected.items():
   segment=re.search('<section id="'+section_id+'">(.*?)</section>',h,re.S).group(1)
   test('approved_section_'+section_id,unescape(re.search('<h2>(.*?)</h2>',segment,re.S).group(1))==section['heading'] and ([unescape(x) for x in re.findall('<p>(.*?)</p>',segment,re.S)]==section['paragraphs'] if 'paragraphs' in section else all(x['title'] in unescape(segment) and x['url'] in segment and x['note'] in unescape(segment) for x in section['items'])))
  test('honest_absent_version_and_exact_dates','version' not in art and c['version'] is binding['zenodo_version'] is binding['manuscript_version'] is clearance['metadata_version'] is clearance['manuscript_version'] is None and c['publication_date']==clearance['publication_date']=='2026-10-06' and r'\date{October 6, 2026}' in source and c['edition_label']==c['citation_edition_label']=='No version number supplied' and '7 October 2026 UTC' in body and all(x not in body for x in ['Version None','Version null','Version 1.0','Version v1']))
  test('rendered_date_label',re.findall(r'<time datetime="([^"]+)">(.*?)</time>',h)==[('2026-10-06','6 October 2026')] and 'Manuscript dated <time' in h)
  test('all_five_original_custom_reviews',len(gate['reviews'])==5 and gate['reviews']['scope']['verdict']['status']=='scope_intake_complete_no_scientific_verdict' and gate['reviews']['analytic']['verdict']['publication_clearance'] is False and gate['reviews']['adversarial']['verdict']['unconditional_global_capacity_clearance'] is False and gate['reviews']['upstream_analytic']['verdict']['verdict']=='PASS' and gate['reviews']['upstream_adversarial']['verdict']['verdict']=='PASS_UPSTREAM_REQUIRED_VE')
  test('root_dependency_resolution',gate['scope_gate_resolution']==clearance['scope_gate_resolution'] and gate['root_clearance_sha256']=='e186543476c3a507b7ba5fc59df50432963efce03d6791015eb8f48becb61ca6' and gate['dependency_resolution']['current_mathematical_disposition'].startswith('Exact general CQE and explicit GEN private regions'))
  test('six_exact_inequalities_common_lambda',all(x in body for x in ['C+2Q ≤ g(λN)+g(ηN)−g((1−η)λN)','Q+E ≤ g(ηλN)−g((1−η)λN)','C+Q+E ≤ g(ηN)−g((1−η)λN)','R+P ≤ g(ηN)','P+S ≤ g(ηλN)−g((1−η)λN)','R+P+S ≤ g(ηN)−g((1−η)λN)','one common λ','using that same λ']) and body.count('closed union over λ ∈ [0,1]')==2)
  test('literal_and_generated_secrecy_distinguished',all(x in body for x in ['W=(M,T_A)','V=(J,S_B) are traced out','Eve does not additionally receive the consumed key','U=(M,T_A,J,S_B)','1 ≤ 1/(d_M d_T_A)+(ε_sec+ε_rel)/2','d_M d_T_A=1 eventually','(−1,1,−1)','2(1−1/d)','even after optimizing the comparison public marginal','This obstruction does not depend on EPnI']))
  test('operational_scope_and_boundary',all(x in body for x in ['1/2 ≤ η ≤ 1','0 ≤ N < ∞','Arbitrary entanglement','maximally mixed logical source','averaged over classical messages, shared key and encoder randomness','finite gross generation and consumption rates','logarithmic dimensions O(n)','Required finite seeds are charged','no semantic-security guarantee','no secrecy guarantee after revealing consumed key','At N=0 and at η=1 both complete regions','At η=1/2 the complete corrected-private region','No peak, per-codeword','No free two-way assistance, superlinear catalysts']))
  test('credited_external_epni_and_existing_formulas',all(x in body for x in ['Wilde, Hayden and Guha already gave the formulas','OpenAI proof','De Palma','not an independent proof of EPnI','external unrefereed EPnI proof','No firstness, exhaustive novelty clearance']))
  test('explicit_pdf_download',len([x for t,x in d.a if t=='a' and x.get('href')==c['pdf_filename'] and 'download' in x])==2)
  test('one_reader_two_unchanged_deposits',len(receipt['files'])==2 and c['additional_assets']==binding['embedded_assets']==[] and len(frames)==1 and len(texts)==c['pdf_pages']==7)
  with zipfile.ZipFile(asset_root/c['supplement_filename']) as archive:
   members=[x for x in archive.infolist() if not x.is_dir()]
   test('forty_original_zip_members',len(members)==40 and all((p/'sources/extracted/zenodo-upload-kit'/x.filename).read_bytes()==archive.read(x) for x in members) and not any(x.filename.lower().endswith(('.pdf','.zip','.tar','.gz')) for x in members))
  test('ai_unrefereed_no_formal_claim',all(x in body for x in ['used extensively','not independent human or journal peer review','external EPnI dependency is also unrefereed','No reproduced Lean build or proof-assistant certification','actual research contributions']))
  test('no_followup_or_private_audit',c['follow_up'] is gate['follow_up'] is clearance['follow_up'] is None and not any(x in body.lower() for x in ['root-clearance','sha256','sha-256','axiom closure','comparator','intentional sorry','2026-10-25','25 october 2026','/users/','checks passed']))
 if rid=='22089807':
  binding=c['source_binding'];body=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<body>(.*?)</body>',h,re.S).group(1))).split())
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  test('full_original_two_paragraph_abstract',normalized_amplifier_abstract(a)==c['abstract']==(p/'reviews/editorial/ABSTRACT.txt').read_text().strip() and len(c['abstract'].split())==binding['abstract_word_count']==214 and len(c['abstract'].split('\n\n'))==binding['abstract_paragraphs']==2)
  test('tex_and_abstract_hashes',binding['source_tex_path']==binding['abstract_source']=='sources/'+TEX_PATHS[rid] and sha(textpath)==binding['source_tex_sha256']==binding['abstract_source_sha256']=='bcc2a0e5f502105ac3d5539a1d2dd752e732463d89c2106f7e67ce4da27d7aac' and hashlib.sha256(a.strip().encode()).hexdigest()==binding['abstract_tex_sha256'])
  candidate_path=p/binding['frozen_scope_content_path'];candidate=json.loads(candidate_path.read_text())
  test('frozen_scope_abstract',sha(candidate_path)==binding['frozen_scope_content_sha256'] and ' '.join(candidate[binding['frozen_scope_abstract_field']].split())==' '.join(c['abstract'].split()))
  test('root_authority_and_scope',gate['root_clearance_file']==c['review_metadata']['root_clearance_file']=='verification/root-clearance-22089807-20261025.json' and sha(clearance_path)==gate['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']=='547296ed820667dfb47b36f796631c23f5eae67be7fb5c2ad898fb5d0bb72125' and clearance==gate['root_clearance_record'] and clearance['approved_scope']==gate['approved_scope'] and clearance['scope_gate_resolution']==gate['scope_gate_resolution'])
  test('original_custom_review_bindings',set(gate['reviews'])=={'scope','analytic','adversarial'} and all(v['sha256']==sha(p/v['report'])==clearance['reviews'][k]['report_sha256'] and v['verdict_sha256']==sha(p/v['verdict_file'])==clearance['reviews'][k]['verdict_sha256'] and v['verdict']==json.loads((p/v['verdict_file']).read_text()) for k,v in gate['reviews'].items()))
  test('historical_scope_hold_preserved',gate['reviews']['scope']['verdict']['mathematical_gate']=='not_decided_by_this_scope_verdict' and gate['reviews']['scope']['verdict']['promotion_authorized'] is False and gate['reviews']['analytic']['verdict']['verdict']=='PASS_STATED_CLAIMS' and gate['reviews']['adversarial']['verdict']['verdict']=='supported_as_stated_no_substantive_fault_found')
  test('standard_original_receipt_metadata_assets',type(raw_receipt) is dict and raw_receipt['record_id']==rid and sha(receipt_file)==binding['receipt_sha256']==binding['source_receipt_sha256']==gate['source_receipt_sha256']==clearance['source_receipt_sha256']=='6cfdd2ec0be534ac37db9572f6d215e9ed1add81b85e428cb5ec75fb6bfa0f13' and sha(record_file)==binding['metadata_sha256']==binding['record_sha256']=='4cddc3b454e3e5a7c653fa3711b209cd9c8b41b834ead10a57984ce0ed79fd88' and sha(p/binding['raw_record_path'])==binding['raw_record_sha256'] and gate['source_files']==binding['files']==receipt['files'] and all(sha(asset_root/asset_name(x))==x['sha256'] for x in receipt['files']))
  test('edition_chronology',c['version']==binding['zenodo_version']==clearance['reviewed_zenodo_version']=='2.0.4' and c['publication_date']==clearance['reviewed_edition_publication_date']=='2026-08-25' and binding['original_named_release']['date']==clearance['earlier_same_work_release_date']=='2026-08-08' and str(binding['original_named_release']['record_id'])==clearance['earlier_same_work_record_id']=='21852072' and '25 August 2026' in body and '8 August 2026' in body and 'earlier date is not the publication date of version 2.0.4' in body)
  test('rendered_date_label',re.findall(r'<time datetime="([^"]+)">(.*?)</time>',h)==[('2026-08-25','25 August 2026')] and 'Reviewed edition published <time' in h)
  test('fixed_fitness_eventual_quantifier',all(x in body for x in ['one fitness-independent sequence','for every fixed 1 < r < R_hyb','there exists t₀(r)','every t ≥ t₀(r)','Each comparison uses the complete graph on the same n_t vertices','All weights are fixed before r is quantified','one family, then every fixed fitness, then a fitness-dependent size threshold']))
  test('distinct_pure_process_finite_baselines',all(x in body for x in ['finite connected loopless undirected weighted graphs','uniformly initialized single-mutant fixation','ρ_Bd(K_n,r) = (1−r⁻¹)/(1−r⁻ⁿ)','ρ_dB(K_n,r) = ((n−1)/n)(1−r⁻¹)/(1−r⁻⁽ⁿ⁻¹⁾)','Bd chooses a fitness-weighted parent','dB first chooses a uniformly random death site']))
  test('lower_bound_and_restricted_response_optimum',all(x in body for x in ['R_sim ≥ R_hyb = 1.5028569127905696… > 3/2','optimal among fixed positive σ and λ','displayed first-order dilute response model','σ = 19/137 and λ = 20/27','1.50176815223369… > 3/2','does not establish optimality over all growing graph families','singular or size-dependent parameter choices','supplies no universal upper bound']))
  test('gain_and_endpoint_practical_limits',all(x in body for x in ['Θ(t⁻³) = Θ(n_t⁻³/⁴) and tends to zero','Neutrality r = 1 and the upper endpoint r = R_hyb are excluded','no size bound uniform near either endpoint','no guarantee for fitness varying with population size','need not contain a graph of every integer order','No useful finite-size onset, fixation-time bound, bounded weight ratio','no empirical prediction','randomly mixes the update rules']))
  test('prior_credit_ai_and_no_formal_claim',all(x in body for x in ['Svoboda','Tkadlec','1 < r < 1.2','different quantifier order','Generative AI was used extensively','not independent human or journal peer review','without formal proof-assistant certification','actual research and writing contributions']))
  test('standalone_reader_never_substituted',sha(f.parent/c['pdf_filename'])==gate['pdf_sha256']==binding['pdf_sha256']==clearance['pdf_sha256']=='1d6d1d31a782776b07b9240467f02d624b47dcde5c83f4740a192136c2dfb8e3' and binding['embedded_pdf_sha256']==clearance['embedded_pdf_sha256']=='1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9' and c['additional_assets']==binding['embedded_assets']==[] and len(frames)==1 and len(texts)==21 and len(receipt['files'])==2)
  with tarfile.open(asset_root/c['supplement_filename'],'r:gz') as archive:
   members=[x for x in archive if x.isfile()]
   test('complete_23_member_tar_preserved',len(members)==23 and all((p/'sources/published-source'/x.name).read_bytes()==archive.extractfile(x).read() for x in members))
   wheels=[x for x in members if x.name.endswith('.whl')]
   test('two_nested_wheels_preserved',len(wheels)==2)
  test('no_followup_or_private_audit',c['follow_up'] is gate['follow_up'] is clearance['follow_up'] is None and not any(x in body.lower() for x in ['root-clearance','sha256','sha-256','2026-10-25','25 october 2026','/users/','checks passed']))
 if rid in SLIT_GAUSSIAN_IDS:
  binding=c['source_binding'];body=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<body>(.*?)</body>',h,re.S).group(1))).split())
  pinned={
   '23383961':{'publication':'612ffcb71b262816975cc36e7bac77c7f3c98abc223a03935fa79597c21f5f0e','promotion':'13a75c4cb020e329d4e30eda1ee62998bf00a81ff591388c4f6779cc974c57cb','root':'2a9214e52b408d2a67a4aef4d6887b8cf86f8eb46f99423ad977c4a8cf847122','editorial':'0745312d4c077b83e356bc8e7c8285b2a8ab64f9bf63f2700fc050ec3b65c42e','tex':'c4e557a58999b938578eb105c03d7224f087c04f273dbbd86e09ab45b855a4b3','metadata':'9109f682be5c735d8e49a50aa1b332a1745308433ee50a887fd9e30e23dbc1e4','receipt':'694bd1f9f680612d3080557f91eb59e59ecd8e67f5383a13764a39a454656401','created':'2026-10-15T04:00:29.066300+00:00','pages':5,'members':255},
   '23430906':{'publication':'48aa3177f3105e68f61dda74b7d4b06ed414b8ec9e86a8184bc431d4e0c888dd','promotion':'b045ca98a16472c8021fb51f64afe9da36b1ee3427e2df9dda6de7d690c6759e','root':'86a8ceed51423cf9c79c71b41389c644361d9b75b54b6bce9093ff9fa0307e8d','editorial':'cd4c8200a36401c7d64874220eee40697a406cc2fa99f76213e5983ac6f9a01d','tex':'4ffbe0d65609213fd91aecf675661ff278e4e1bd5037db8836f1291f5bdc1d78','metadata':'5821cbcb2052b6e3445d13683470a0e48c827b2f6e678397f26ba825ec9e9cbd','receipt':'814617d4e7941126dd052a918a66e12e9460d58e55ba6c9edb58da82c1f22443','created':'2026-10-17T05:14:35.437960+00:00','pages':7,'members':225}
  }[rid]
  clearance_path=R/('verification/root-clearance-'+rid+'-20261025.json');clearance=json.loads(clearance_path.read_text())
  editorial_path=R/('verification/root-editorial-'+rid+'-20261025.json');editorial=json.loads(editorial_path.read_text())
  test('exact_approved_config_bytes',sha(p/'publication.json')==gate['publication_sha256']==pinned['publication'] and sha(p/'promotion.json')==pinned['promotion'])
  test('exact_tex_path_and_bytes',binding['source_tex_path']==binding['abstract_source']=='sources/'+TEX_PATHS[rid] and sha(textpath)==binding['source_tex_sha256']==binding['abstract_source_sha256']==pinned['tex'])
  test('complete_original_abstract',normalized_slit_gaussian_abstract(rid,a)==c['abstract'] and a.strip()==binding['abstract_tex'].strip() and hashlib.sha256(binding['abstract_tex'].encode()).hexdigest()==binding['abstract_tex_sha256'] and len(c['abstract'].split('\n\n'))==1)
  test('original_abstract_heading',c['abstract_heading']==binding['abstract_display_heading']=='Original abstract' and c['abstract_is_original'] is True and re.search(r'<section id="abstract"><h2>(.*?)</h2>',h).group(1)=='Original abstract')
  candidate_path=p/binding['frozen_scope_content_path'];candidate=json.loads(candidate_path.read_text())
  test('frozen_original_abstract',sha(candidate_path)==binding['frozen_scope_content_sha256'] and candidate[binding['frozen_scope_abstract_field']]==c['abstract'])
  test('exact_root_authority',gate['root_clearance_file']==c['review_metadata']['root_clearance_file']==str(clearance_path.relative_to(R)) and sha(clearance_path)==gate['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']==pinned['root'] and gate['root_clearance_record']==clearance and clearance['status']=='PASS' and clearance['disposition_by']=='root' and gate['approved_scope']==clearance['approved_scope'] and gate['scope_gate_resolution']==clearance['scope_gate_resolution'])
  editorial_gate='rendered_live_browser_native_gates_passed' if rid=='23430906' else 'rendered_live_browser_native_publication_pass'
  test('exact_editorial_authority',sha(editorial_path)==pinned['editorial'] and editorial['publication_sha256']==pinned['publication'] and editorial['promotion_sha256']==pinned['promotion'] and editorial[editorial_gate] is False)
  test('complete_custom_verdict_objects',set(gate['reviews'])=={'scope','analytic','adversarial'} and all(v['sha256']==sha(p/v['report'])==clearance['reviews'][role]['report_sha256'] and v['verdict_sha256']==sha(p/v['verdict_file'])==clearance['reviews'][role]['verdict_sha256'] and v['verdict']==json.loads((p/v['verdict_file']).read_text()) and 'papers/'+rid+'/'+v['report']==clearance['reviews'][role]['report'] and 'papers/'+rid+'/'+v['verdict_file']==clearance['reviews'][role]['verdict'] and v['root_disposition']==('SCOPE_COMPLETE' if role=='scope' else 'PASS') for role,v in gate['reviews'].items()))
  test('receipt_metadata_and_assets',type(raw_receipt) is dict and raw_receipt['record_id']==rid and sha(receipt_file)==binding['receipt_sha256']==binding['source_receipt_sha256']==gate['source_receipt_sha256']==clearance['source_receipt_sha256']==pinned['receipt'] and sha(record_file)==binding['metadata_sha256']==binding['record_sha256']==gate['metadata_sha256']==pinned['metadata'] and gate['source_files']==binding['files'] and len(receipt['files'])==2 and all(any(all(entry.get(k)==v for k,v in bound.items()) for entry in raw_receipt['files']) for bound in binding['files']) and all(sha(asset_root/asset_name(x))==x['sha256'] and (asset_root/asset_name(x)).stat().st_size==x['bytes'] and hashlib.md5((asset_root/asset_name(x)).read_bytes()).hexdigest()==x['md5'] and x['zenodo_checksum']=='md5:'+x['md5'] for x in raw_receipt['files']))
  full_record=json.loads(record_file.read_text())
  test('metadata_asset_receipt_comparison',str(full_record['id'])==rid and full_record['status']=='published' and full_record['created']==binding['record_created_utc']==pinned['created'] and len(full_record['files'])==2 and all(any(api['key']==asset_name(entry) and api['size']==entry['bytes'] and api['checksum']==entry['zenodo_checksum'] and api['links']['self']==entry['url'] for api in full_record['files']) for entry in raw_receipt['files']))
  test('edition_chronology',c['version']==binding['zenodo_version']==clearance['reviewed_zenodo_version']=='1.0' and c['publication_date']==clearance['publication_date']=='2026-10-14' and re.findall(r'<time datetime="([^"]+)">(.*?)</time>',h)==[('2026-10-14','14 October 2026')] and 'Manuscript and declared publication date <time' in h)
  test('source_custody_receipt',gate['root_custody_receipt']==clearance['root_custody_receipt'] and sha(R/gate['root_custody_receipt'])==gate['root_custody_receipt_sha256']==clearance['root_custody_receipt_sha256'])
  test('original_pdf_download_and_open',len([x for t,x in d.a if t=='a' and x.get('href')==c['pdf_filename'] and 'download' in x])==2 and any(t=='a' and x.get('href')==c['pdf_filename'] and 'download' not in x for t,x in d.a) and any(t=='a' and x.get('href')=='https://zenodo.org/records/'+rid+'/files/'+c['pdf_filename'] for t,x in d.a))
  materials=re.search(r'<section id="materials">(.*?)</section>',h,re.S)
  test('complete_supporting_material_links',materials is not None and '<h2>Supporting materials</h2>' in materials.group(1) and '<a href="'+c['supplement_filename']+'" download>' in materials.group(1) and c['supplement_label'] in unescape(materials.group(1)) and 'https://zenodo.org/records/'+rid+'/files/'+c['supplement_filename'] in materials.group(1))
  test('one_unchanged_reader',len(frames)==1 and len(texts)==c['pdf_pages']==pinned['pages'] and c['additional_assets']==binding['embedded_assets']==[] and sha(f.parent/c['pdf_filename'])==gate['pdf_sha256']==binding['pdf_sha256']==clearance['pdf_sha256'] and sha(f.parent/c['supplement_filename'])==gate['supplement_sha256']==binding['supplement_sha256']==clearance['supplement_sha256'])
  with zipfile.ZipFile(asset_root/c['supplement_filename']) as archive:
   members=[x for x in archive.infolist() if not x.is_dir()];source_root=p/'sources'/('published-source/verification_package' if rid=='23383961' else 'support')
   test('all_original_archive_members',len(members)==pinned['members'] and all((source_root/x.filename).read_bytes()==archive.read(x) for x in members) and not any(x.filename.lower().endswith(('.zip','.tar','.gz')) for x in members))
   readers=[x for x in members if x.filename.lower().endswith('.pdf')]
   test('archive_reader_identity',not readers if rid=='23383961' else len(readers)==1 and archive.read(readers[0])==(asset_root/c['pdf_filename']).read_bytes())
  test('ai_authorship_and_private_state',all(x in body for x in ['used extensively','not independent human or journal peer review','without formal proof-assistant certification','mutual agreement','actual research and writing contributions']) and c['follow_up'] is gate['follow_up'] is clearance['follow_up'] is None and gate['native_sheet_aa_url'] is None and gate['rendered_copy_verified'] is gate['live_verified'] is False and not any(x in body.lower() for x in ['root-clearance','sha256','sha-256','2026-10-25','25 october 2026','/users/','checks passed']))
  if rid=='23383961':
   test('historical_scope_hold_preserved',gate['reviews']['scope']['verdict']['status']=='SCOPE_COMPLETE_PENDING_INDEPENDENT_MATHEMATICAL_REVIEW' and gate['reviews']['scope']['verdict']['mathematical_pass'] is False and gate['reviews']['scope']['verdict']['scientific_verdict'] is None and gate['reviews']['scope']['verdict']['ready_to_publish'] is False and gate['reviews']['analytic']['verdict']['status']=='analytic_pass_no_substantive_defect_found' and gate['reviews']['analytic']['verdict']['publication_clearance'] is False and gate['reviews']['adversarial']['verdict']['verdict']=='PASS_SCIENTIFIC_SCOPE')
   test('slit_every_maximizer_fixed_parameters',all(x in body for x in ['Set ε = 10⁻²⁴ and L(f)','η = 10⁻¹²','Every such maximizer','actual analytic slit Γ','Both nondecreasing and nonincreasing','signed outward radial angle','ordinary unsigned outward radial angle','no claim for arbitrary larger perturbations','No explicit maximizing map or uniqueness theorem is required']))
   test('slit_actual_geometry_and_angle_mechanisms',all(x in body for x in ['actual omitted slit tip inside radius 3/10','modulus greater than 25/81','agrees with the actual omitted slit near infinity','local trajectory uniqueness','Increasing t points inward','outward tangent is −W′','tends to zero at infinity','interior zero','ordinary angle |β|']))
   test('slit_bounded_historical_credit',all(x in body for x in ['Hayman','Pfluger','Duren','Brown','de Branges','Friedland','No historical firstness','uninspected','Finite rational checks']))
  else:
   test('historical_scope_hold_preserved',gate['reviews']['scope']['verdict']['verdict']=='SCOPE_COMPLETE_ATTRIBUTION_QUALIFIED_MATHEMATICAL_GATE_PENDING' and gate['reviews']['scope']['verdict']['mathematical_verdict'] is None and gate['reviews']['scope']['verdict']['substantive_defect_found'] is None and gate['reviews']['scope']['verdict']['promotion_authorized'] is False and gate['reviews']['analytic']['verdict']['status']=='COMPLETE' and gate['reviews']['analytic']['verdict']['verdict']=='PASS' and gate['reviews']['analytic']['verdict']['publication_clearance_claimed'] is False and gate['reviews']['analytic']['verdict']['review_self_correction'] and gate['reviews']['adversarial']['verdict']['verdict']=='NO_SUBSTANTIVE_DEFECT_OR_UNRESOLVED_CENTRAL_GAP_FOUND' and 'status' not in gate['reviews']['adversarial']['verdict'])
   test('original_receipt_shape_preserved',raw_receipt==gate['source_receipt_record'] and 'record_sha256' not in raw_receipt and sha(p/binding['record_raw_path'])==raw_receipt['record_raw_sha256']==binding['record_raw_sha256'] and all(x['http_status']==200 for x in raw_receipt['files']))
   test('gaussian_fixed_all_parameter_quantifiers',all(x in body for x in ['Fix H ∈ (1/4,1)','independent centered standard fractional Brownian motions','same Hurst parameter','both complete deterministic uniform grids','including T, with n observations per component','For T > 0 and an integer n ≥ 1','Every F ∈ L²(G_(T,n))','every nonlinear square-integrable estimator','canonical iterated integral']))
   test('gaussian_exact_constant_and_mechanism',all(x in body for x in ['c_H = 2πa/(D_H√(P̄_fP̄_g))','a = 4/45045','P̄_r = π^α L_r² + 2N_r²π^(α−6)(1 + 1/[2(5−α)])','allows dependence between cells','fixed observation grid','n a(T/n)^(2H)','established external inputs']))
   test('gaussian_convention_and_scope_limits',all(x in body for x in ['A_T = (I₁₂−I₂₁)/2','X_T−B¹_TB²_T/2','unhalved antisymmetric difference has twice','No sharp constant','constant uniform in H','does not cover unequal Hurst parameters','nonuniform or adaptive sampling','Historical theorem and method priority, full novelty, and worldwide current-open status remain unverified','Broader implications of the Dickinson and Jackowski methods remain unverified','no publisher-byte identity or current journal-error claim']))
 if rid in SURREAL_CONE_BROWNIAN_IDS:
  pinned=SCB_PINS[rid];binding=c['source_binding'];body=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<body>(.*?)</body>',h,re.S).group(1))).split())
  section_text={sid:' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<section id="'+sid+r'">(.*?)</section>',h,re.S).group(1))).split()) for sid in ['result','proof','limits']}
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  editorial_path=R/('verification/root-editorial-'+rid+'-20261025.json');editorial=json.loads(editorial_path.read_text());seal_path=p/'reviews/editorial/SEAL.json';seal=json.loads(seal_path.read_text())
  test('exact_approved_config_bytes',sha(p/'publication.json')==gate['publication_sha256']==pinned['publication'] and sha(p/'promotion.json')==pinned['promotion'])
  test('exact_source_tex_path_and_bytes',binding['source_tex_path']==binding['abstract_source']=='sources/'+TEX_PATHS[rid] and sha(textpath)==binding['source_tex_sha256']==binding['abstract_source_sha256']==clearance['source_tex_sha256'])
  test('complete_original_abstract',normalized_surreal_cone_brownian_abstract(rid,a)==c['abstract'] and a.strip()==binding['abstract_tex'] and hashlib.sha256(a.strip().encode()).hexdigest()==binding['abstract_tex_sha256'] and c['abstract_is_original'] is True and len(c['abstract'].split('\n\n'))==1)
  test('original_abstract_heading',c['abstract_heading']==binding['abstract_display_heading']=='Original abstract' and re.search(r'<section id="abstract"><h2>(.*?)</h2>',h).group(1)=='Original abstract')
  candidate_path=p/binding['frozen_scope_content_path'];candidate=json.loads(candidate_path.read_text())
  test('frozen_original_scope_candidate',sha(candidate_path)==binding['frozen_scope_content_sha256'] and candidate[binding['frozen_scope_abstract_field']]==c['abstract'])
  test('exact_separate_root_authority',gate['root_clearance_file']==c['review_metadata']['root_clearance_file']=='verification/root-clearance-'+rid+'-20261025.json' and sha(clearance_path)==gate['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']==pinned['root'] and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['scope_gate_resolution']==clearance['scope_gate_resolution'] and gate['status']==clearance['status']=='PASS' and gate['disposition_by']==clearance['disposition_by']=='root')
  test('exact_separate_root_editorial_authority',sha(editorial_path)==pinned['editorial'] and editorial['status']=='ROOT_ACCEPTED_EDITORIAL_BOUND_COPY' and editorial['publication_sha256']==pinned['publication'] and editorial['promotion_sha256']==pinned['promotion'] and editorial['scientific_authority']==gate['root_clearance_file'] and editorial['scientific_authority_sha256']==pinned['root'] and editorial['staging_authorized'] is True and editorial['rendered_live_browser_native_gates_passed'] is False)
  test('complete_editorial_seal',sha(seal_path)==editorial['seal_sha256']==pinned['seal'] and seal['original_review_objects_and_receipt_preserved'] is True and seal['full_original_abstract_preserved'] is True and all((R/x['path']).stat().st_size==x['bytes'] and sha(R/x['path'])==x['sha256'] for x in seal['files']))
  test('complete_original_custom_verdicts',set(gate['reviews'])=={'scope','analytic','adversarial'} and all(v['sha256']==sha(p/v['report'])==clearance['reviews'][role]['report_sha256'] and v['verdict_sha256']==sha(p/v['verdict_file'])==clearance['reviews'][role]['verdict_sha256'] and v['verdict']==json.loads((p/v['verdict_file']).read_text()) and 'papers/'+rid+'/'+v['report']==clearance['reviews'][role]['report'] and 'papers/'+rid+'/'+v['verdict_file']==clearance['reviews'][role]['verdict'] and v['root_disposition']==('SCOPE_COMPLETE' if role=='scope' else 'PASS') for role,v in gate['reviews'].items()))
  test('complete_original_receipt_and_source_assets',raw_receipt==gate['source_receipt_record'] and type(raw_receipt) is dict and raw_receipt['record_id']==rid and sha(receipt_file)==binding['receipt_sha256']==binding['source_receipt_sha256']==gate['source_receipt_sha256']==clearance['source_receipt_sha256'] and gate['source_files']==binding['files']==raw_receipt['files'] and len(raw_receipt['files'])==2 and all(sha(asset_root/asset_name(x))==x['sha256'] and (asset_root/asset_name(x)).stat().st_size==x['bytes'] and hashlib.md5((asset_root/asset_name(x)).read_bytes()).hexdigest()==x['md5'] and x['zenodo_checksum']=='md5:'+x['md5'] for x in raw_receipt['files']))
  full_record=json.loads(record_file.read_text())
  test('readable_metadata_and_api_asset_comparison',sha(record_file)==binding['metadata_sha256']==binding['record_sha256']==gate['metadata_sha256'] and str(full_record['id'])==rid and full_record['status']=='published' and full_record['created']==binding['record_created_utc']==clearance['record_created_utc'] and full_record['updated']==binding['record_updated_utc'] and len(full_record['files'])==2 and all(any(api['key']==asset_name(x) and api['size']==x['bytes'] and api['checksum']==x['zenodo_checksum'] and api['links']['self']==x['url'] for api in full_record['files']) for x in raw_receipt['files']))
  if rid=='23444606':test('original_receipt_record_shape',raw_receipt['record_sha256']==sha(record_file) and 'record_raw_sha256' not in raw_receipt)
  else:test('original_receipt_record_shape','record_sha256' not in raw_receipt and sha(p/binding['record_raw_path'])==binding['record_raw_sha256']==raw_receipt['record_raw_sha256'] and all(x['http_status']==200 for x in raw_receipt['files']))
  test('edition_chronology',c['version']==binding['zenodo_version']==clearance['reviewed_zenodo_version'] and c['publication_date']==binding['zenodo_publication_date']==clearance['publication_date'] and re.findall(r'<time datetime="([^"]+)">(.*?)</time>',h)==[(c['publication_date'],pinned['display_date'])] and 'Manuscript and declared publication date <time' in h and binding['manuscript_version']==(c['version'] if rid=='23440119' else None) and c['edition_note'] in body)
  test('root_custody_receipt',gate['root_custody_receipt']==clearance['root_custody_receipt'] and sha(R/gate['root_custody_receipt'])==gate['root_custody_receipt_sha256']==clearance['root_custody_receipt_sha256'])
  test('explicit_pdf_download_open_original',len([x for t,x in d.a if t=='a' and x.get('href')==c['pdf_filename'] and 'download' in x])==2 and any(t=='a' and x.get('href')==c['pdf_filename'] and 'download' not in x for t,x in d.a) and any(t=='a' and x.get('href')=='https://zenodo.org/records/'+rid+'/files/'+c['pdf_filename'] for t,x in d.a))
  materials=re.search(r'<section id="materials">(.*?)</section>',h,re.S)
  test('complete_local_original_supporting_links',materials is not None and '<a href="'+c['supplement_filename']+'" download>' in materials.group(1) and c['supplement_label'] in unescape(materials.group(1)) and 'https://zenodo.org/records/'+rid+'/files/'+c['supplement_filename'] in materials.group(1))
  test('one_unchanged_standalone_reader',len(frames)==1 and len(texts)==c['pdf_pages']==pinned['pages'] and c['additional_assets']==binding['embedded_assets']==[] and sha(f.parent/c['pdf_filename'])==binding['pdf_sha256']==gate['pdf_sha256']==clearance['pdf_sha256'] and sha(f.parent/c['supplement_filename'])==binding['supplement_sha256']==gate['supplement_sha256']==clearance['supplement_sha256'])
  with zipfile.ZipFile(asset_root/c['supplement_filename']) as archive:
   members=[x for x in archive.infolist() if not x.is_dir()];source_root=p/'sources'/('published-source/initial-omnific-models-source-and-verification' if rid=='23444606' else 'support');readers=[x for x in members if x.filename.lower().endswith('.pdf')]
   test('all_complete_original_zip_members',len(members)==binding['archive_regular_file_count']==pinned['members'] and all((source_root/x.filename).read_bytes()==archive.read(x) for x in members) and not any(x.filename.lower().endswith(('.zip','.tar','.gz')) for x in members))
   test('original_archive_reader_identity',not readers if rid=='23224103' else len(readers)==1 and archive.read(readers[0])==(asset_root/c['pdf_filename']).read_bytes())
  proposed_sections=json.loads((p/'reviews/editorial/public-sections.json').read_text());prepared_bib=(p/'reviews/editorial/citation.bib').read_text()
  test('exact_prepared_bibtex_and_license',bib==prepared_bib==proposed_sections['bibtex'] and art['license']=='https://creativecommons.org/licenses/by/4.0/' and c['license']=='CC BY 4.0' and any(t=='a' and x.get('href')==art['license'] for t,x in d.a))
  test('all_approved_public_section_paragraphs',all(re.search(r'<section id="'+x['id']+r'"><h2>(.*?)</h2>',h).group(1)==x['heading'] and all(paragraph in body for paragraph in x.get('paragraphs',[]) if x['id']!='cite') for x in proposed_sections['sections']))
  test('ai_authorship_no_private_narrative_or_followup',all(x in body for x in ['used extensively','does not constitute independent human or journal peer review','no formal proof-assistant certification','mutual agreement','actual research and writing contributions']) and c['follow_up'] is gate['follow_up'] is clearance['follow_up'] is None and gate['rendered_copy_verified'] is gate['live_verified'] is gate['browser_verified'] is False and gate['native_sheet_aa_url'] is None and not any(x in body.lower() for x in ['root-clearance','sha256','sha-256','2026-10-25','25 october 2026','/users/','checks passed','custody receipt']))
  scope=gate['reviews']['scope']['verdict'];analytic=gate['reviews']['analytic']['verdict'];adverse=gate['reviews']['adversarial']['verdict']
  if rid=='23444606':
   test('original_custom_scope_history',scope['status']=='SCOPE_COMPLETE_PENDING_MATHEMATICAL_REVIEW' and scope['mathematical_pass'] is None and scope['root_publication_clearance'] is False and scope['candidate_only'] is True and analytic['status']=='PASS' and adverse['status']=='PASS' and adverse['publication_authorized_by_this_agent'] is False)
   test('surreal_actual_ambient_initial_image_and_class_scope',all(x in section_text['result'] for x in ['NBG set theory with global choice','actual initial ordered additive subgroup of No','addition and order inherited from No','actual subgroup H⊆Oz that is initial in No','set and proper-class groups; the zero group uses the identity','all proper ordinal-length sign-sequence prefixes in the ambient No','H=T[G]']))
   test('surreal_actual_supports_bottom_and_limits',all(x in section_text['proof'] for x in ['including limit ordinal lengths and empty tails','right-simplicity-predecessor obligations','normalizing the bottom coefficient group to ℤ','precisely the actual set-sized supports in G','published appendix','legal integer-perturbation cuts']) and all(x in section_text['limits'] for x in ['no full Hahn completion is adjoined','every individual normal-form support is a set','No ring, field, multiplicative or simplicity-preserving isomorphism','Historical priority, full novelty and worldwide current-open status remain unverified']))
  else:
   test('original_custom_scope_history',scope['mathematical_verdict'] is None and scope['page_promotion_permission'] is False and analytic['status']=='COMPLETE' and analytic['mathematical_verdict']=='SUPPORTED_AT_LITERAL_SCOPE' and analytic['publication_clearance'] is False and adverse['status']=='COMPLETE' and adverse['exact_remaining_mathematical_gap_found'] is None and adverse['promotion_clearance' if rid=='23440119' else 'publication_clearance'] is False)
   if rid=='23440119':
    test('cone_exact_barrier_parameter_and_all_directions',all(x in section_text['result'] for x in ['F(x,y,z)=−25 log(z(xy²−z³))','normal barrier with parameter 100','squared dual Hessian gradient norm is exactly 100','For every a∈int K, every h∈K and every u∈ℝ³','including zero and its boundary','no homogeneous real polynomial H of any degree in the same ℝ³']))
    test('cone_prior_three_no_parameter_improvement_and_degeneracy',all(x in section_text['limits'] for x in ['Roy–Xiao give a parameter-3','Parameter 100 is an explicit sufficient certificate','no parameter improvement or optimality claim','does not assert nonpositive sectional curvature','does not exclude projections or higher-dimensional lifts']) and all(x in section_text['proof'] for x in ['separate lower-block certificate at t=1','Gram certificate for the x-axis','includes t=0, h=0 and directions with h_y=0']))
   else:
    test('brownian_joint_law_cumulative_clocks_and_quantifiers',all(x in section_text['result'] for x in ['Let k≥1 be a finite integer','distinct fixed labeled points','independent standard Brownian motions with generator ½d²/dx²','continue through every encounter and prior visit','For real θ_i≥0','finite permutation and label sums','explicit strict linear inequalities in cumulative clocks','retaining dependence among one walker’s query visits','all mixed moments and hence the full joint Borel probability measure']))
    test('brownian_exact_outer_bound_and_inner_limits',all(x in section_text['result'] for x in ['For every integer N≥0','|ℒ_p(θ)−∑_{m=0}^N(−1)^m M_m(θ;p)/m!|≤θ_*^(N+1)/(N+1)!','uniform over all admissible seed vectors','Sorting the seeds before assigning labels']) and all(x in section_text['limits'] for x in ['controls only the outer series for real nonnegative θ','no inner Fourier-tail, numerical quadrature or coefficient-evaluation certificate','does not say that ties are absent simultaneously at every point','No extension to deterministically coincident seeds','Equally spaced labeled starts have cyclic and dihedral symmetry']))
 if rid in DIPOLE_LANGLANDS_IDS:
  pinned=DL_PINS[rid];binding=c['source_binding'];body=' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<body>(.*?)</body>',h,re.S).group(1))).split())
  section_text={sid:' '.join(unescape(re.sub(r'<[^>]+>',' ',re.search(r'<section id="'+sid+r'">(.*?)</section>',h,re.S).group(1))).split()) for sid in ['result','proof','limits']}
  clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
  editorial_path=R/('verification/root-editorial-'+rid+'-20261025.json');editorial=json.loads(editorial_path.read_text());seal_path=p/'reviews/editorial/SEAL.json';seal=json.loads(seal_path.read_text())
  test('exact_approved_config_bytes',sha(p/'publication.json')==gate['publication_sha256']==pinned['publication'] and sha(p/'promotion.json')==pinned['promotion'])
  test('exact_source_tex_path_and_bytes',binding['source_tex_path']==binding['abstract_source']=='sources/'+TEX_PATHS[rid] and sha(textpath)==binding['source_tex_sha256']==binding['abstract_source_sha256']==pinned['tex'])
  test('complete_original_abstract',normalized_dipole_langlands_abstract(rid,a)==c['abstract'] and a.strip()==binding['abstract_tex'] and hashlib.sha256(a.strip().encode()).hexdigest()==binding['abstract_tex_sha256'] and c['abstract_is_original'] is True and len(c['abstract'].split('\n\n'))==1)
  test('original_abstract_heading',c['abstract_heading']==binding['abstract_display_heading']=='Original abstract' and re.search(r'<section id="abstract"><h2>(.*?)</h2>',h).group(1)=='Original abstract')
  candidate_path=p/binding['frozen_scope_content_path'];candidate=json.loads(candidate_path.read_text())
  test('frozen_original_scope_candidate',sha(candidate_path)==binding['frozen_scope_content_sha256'] and ((p/binding['frozen_scope_abstract_path']).read_text().strip()==c['abstract'] and sha(p/binding['frozen_scope_abstract_path'])==binding['frozen_scope_abstract_sha256'] if rid=='23390551' else candidate[binding['frozen_scope_abstract_field']]==c['abstract']))
  test('exact_separate_root_authority',gate['root_clearance_file']==c['review_metadata']['root_clearance_file']=='verification/root-clearance-'+rid+'-20261025.json' and sha(clearance_path)==gate['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']==pinned['root'] and gate['root_clearance_record']==clearance and gate['approved_scope']==clearance['approved_scope'] and gate['scope_gate_resolution']==clearance['scope_gate_resolution'] and gate['status']==clearance['status']=='PASS' and gate['disposition_by']==clearance['disposition_by']=='root')
  test('exact_separate_root_editorial_authority',sha(editorial_path)==pinned['editorial'] and editorial['status']=='ROOT_ACCEPTED_EDITORIAL_BOUND_COPY' and editorial['publication_sha256']==pinned['publication'] and editorial['promotion_sha256']==pinned['promotion'] and editorial['scientific_authority']==gate['root_clearance_file'] and editorial['scientific_authority_sha256']==pinned['root'] and editorial['staging_authorized'] is True and editorial['rendered_live_browser_native_gates_passed'] is False)
  test('complete_editorial_seal',sha(seal_path)==editorial['seal_sha256']==pinned['seal'] and seal['original_review_objects_and_receipt_preserved'] is True and seal['full_original_abstract_preserved'] is True and all((R/x['path']).stat().st_size==x['bytes'] and sha(R/x['path'])==x['sha256'] for x in seal['files']))
  test('complete_original_custom_verdicts',set(gate['reviews'])=={'scope','analytic','adversarial'} and all(v['sha256']==sha(p/v['report'])==clearance['reviews'][role]['report_sha256'] and v['verdict_sha256']==sha(p/v['verdict_file'])==clearance['reviews'][role]['verdict_sha256'] and v['verdict']==json.loads((p/v['verdict_file']).read_text()) and 'papers/'+rid+'/'+v['report']==clearance['reviews'][role]['report'] and 'papers/'+rid+'/'+v['verdict_file']==clearance['reviews'][role]['verdict'] and v['root_disposition']==('SCOPE_COMPLETE' if role=='scope' else 'PASS') for role,v in gate['reviews'].items()))
  test('complete_original_receipt_and_source_assets',raw_receipt==gate['source_receipt_record'] and type(raw_receipt) is dict and sha(receipt_file)==binding['receipt_sha256']==binding['source_receipt_sha256']==gate['source_receipt_sha256']==clearance['source_receipt_sha256']==pinned['receipt'] and gate['source_files']==binding['files']==raw_receipt['files']==receipt['files'] and len(raw_receipt['files'])==2 and all(sha(asset_root/asset_name(x))==x['sha256'] and (asset_root/asset_name(x)).stat().st_size==x['bytes'] and hashlib.md5((asset_root/asset_name(x)).read_bytes()).hexdigest()==x['md5'] for x in raw_receipt['files']))
  full_record=json.loads(record_file.read_text())
  test('readable_metadata_and_api_asset_comparison',sha(record_file)==binding['metadata_sha256']==binding['record_sha256']==gate['metadata_sha256']==pinned['metadata'] and str(full_record['id'])==rid and str(full_record['conceptrecid'])==binding['concept_record_id'] and full_record['status']=='published' and full_record['created']==binding['record_created_utc']==pinned['created'] and full_record['updated']==binding['record_updated_utc'] and len(full_record['files'])==2 and full_record['metadata']['license']['id']=='cc-by-4.0' and all(any(api['key']==asset_name(x) and api['size']==x['bytes'] and api['checksum']=='md5:'+x['md5'] for api in full_record['files']) for x in raw_receipt['files']))
  if rid=='23390551':
   test('original_custom_receipt_no_alias_or_invented_http','record_id' not in raw_receipt and 'record_sha256' not in raw_receipt and 'http_status' not in raw_receipt and not (p/'sources/receipt.json').exists() and not (p/'sources/record.json').exists() and raw_receipt['sha256']==sha(record_file) and raw_receipt['bytes']==record_file.stat().st_size and all('http_status' not in x and 'name' not in x and x['fetch_error'] is None and x['record_file_metadata'] in full_record['files'] and x['request_url']==x['final_url']==x['record_file_metadata']['links']['self'] for x in raw_receipt['files']))
  else:
   test('original_standard_receipt_raw_record_preserved',raw_receipt['record_id']==rid and 'record_sha256' not in raw_receipt and sha(p/binding['record_raw_path'])==binding['record_raw_sha256']==raw_receipt['record_raw_sha256'] and json.loads((p/binding['record_raw_path']).read_text())==full_record and all(x['http_status']==200 and x['zenodo_checksum']=='md5:'+x['md5'] and x['url']==x['final_url'] for x in raw_receipt['files']))
  test('edition_chronology',c['version']==binding['zenodo_version']==binding['manuscript_version']==clearance['reviewed_zenodo_version'] and c['publication_date']==binding['zenodo_publication_date']==clearance['publication_date'] and re.findall(r'<time datetime="([^"]+)">(.*?)</time>',h)==[(c['publication_date'],pinned['display_date'])] and 'Manuscript and declared publication date <time' in h and c['edition_note'] in body)
  test('root_custody_receipt',gate['root_custody_receipt']==clearance['root_custody_receipt'] and sha(R/gate['root_custody_receipt'])==gate['root_custody_receipt_sha256']==clearance['root_custody_receipt_sha256'])
  test('explicit_pdf_download_open_original',len([x for t,x in d.a if t=='a' and x.get('href')==c['pdf_filename'] and 'download' in x])==2 and any(t=='a' and x.get('href')==c['pdf_filename'] and 'download' not in x for t,x in d.a) and any(t=='a' and x.get('href')=='https://zenodo.org/records/'+rid+'/files/'+c['pdf_filename'] for t,x in d.a))
  materials=re.search(r'<section id="materials">(.*?)</section>',h,re.S)
  test('complete_local_original_supporting_links',materials is not None and '<a href="'+c['supplement_filename']+'" download>' in materials.group(1) and c['supplement_label'] in unescape(materials.group(1)) and 'https://zenodo.org/records/'+rid+'/files/'+c['supplement_filename'] in materials.group(1))
  test('one_selected_unchanged_public_reader',len(frames)==1 and len(texts)==c['pdf_pages']==pinned['pages'] and c['additional_assets']==binding['embedded_assets']==binding['additional_reader_pdfs']==[] and sha(f.parent/c['pdf_filename'])==binding['pdf_sha256']==gate['pdf_sha256']==clearance['pdf_sha256'] and sha(f.parent/c['supplement_filename'])==binding['supplement_sha256']==gate['supplement_sha256']==clearance['supplement_sha256'] and {x.name for x in f.parent.iterdir() if x.is_file()}=={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']})
  if rid=='23390551':
   inventory=dipole_archive_inventory(asset_root/c['supplement_filename'],p/'sources/cache/extracted')
   test('all_recursive_original_archive_occurrences',inventory['all_member_bytes_match'] and len(inventory['rows'])==binding['archive_recursive_regular_member_occurrences']==323 and inventory['unique_hashes']==binding['archive_unique_member_sha256_count']==170 and inventory['hidden']==binding['archive_hidden_member_occurrences']==16 and len(inventory['nested'])==binding['nested_archive_count']==1 and inventory['layers']==binding['archive_layers']==2 and sum('!/' not in x['member'] for x in inventory['rows'])==binding['archive_regular_file_count']==187)
   test('historical_distinct_reader_preserved_only_in_complete_zip',len(inventory['readers'])==binding['archive_embedded_pdf_count']==1 and inventory['readers'][0]['sha256']==binding['archive_historical_reader_pdfs'][0]['sha256']=='5368254f4192d7a617bb27b6bbc6454c89e5ddd62ed2fa9c5d617f95442507af' and inventory['readers'][0]['bytes']==112956 and len({x['sha256'] for x in inventory['readers']}|{gate['pdf_sha256']})==binding['total_distinct_reader_pdf_count']==2 and inventory['nested'][0]['sha256']==binding['nested_archives'][0]['sha256']=='dfc0a9c0775af5b205494e56e561cbd27c1519af734b3cb387ad7e06a4b7760d')
   historical=subprocess.check_output(['/opt/homebrew/bin/pdftotext',inventory['readers'][0]['source'],'-'],text=True).split('\f')
   if not historical[-1].strip():historical.pop()
   test('historical_reader_eleven_searchable_pages',len(historical)==11 and all(len(x.strip())>100 for x in historical))
  else:
   with zipfile.ZipFile(asset_root/c['supplement_filename']) as archive:
    members=[x for x in archive.infolist() if not x.is_dir()];readers=[x for x in members if x.filename.lower().endswith('.pdf')]
    test('all_complete_original_zip_members',len(members)==binding['archive_regular_file_count']==binding['archive_recursive_regular_member_occurrences']==37 and all((p/'sources/support'/x.filename).read_bytes()==archive.read(x) for x in members) and not any(x.filename.lower().endswith(('.zip','.tar','.gz')) for x in members) and binding['nested_archive_count']==0)
    test('sole_embedded_reader_equals_selected',len(readers)==binding['archive_embedded_pdf_count']==binding['total_distinct_reader_pdf_count']==1 and archive.read(readers[0])==(asset_root/c['pdf_filename']).read_bytes())
  proposed_sections=json.loads((p/'reviews/editorial/public-sections.json').read_text());prepared_bib=(p/'reviews/editorial/citation.bib').read_text()
  test('exact_prepared_bibtex_and_license',bib==prepared_bib==proposed_sections['bibtex'] and art['license']=='https://creativecommons.org/licenses/by/4.0/' and c['license']=='CC BY 4.0' and any(t=='a' and x.get('href')==art['license'] for t,x in d.a))
  test('all_approved_public_section_paragraphs',all(re.search(r'<section id="'+x['id']+r'"><h2>(.*?)</h2>',h).group(1)==x['heading'] and all(paragraph in body for paragraph in x.get('paragraphs',[]) if x['id']!='cite') for x in proposed_sections['sections']))
  test('ai_authorship_no_private_narrative_or_followup',all(x in body for x in ['used extensively','human or journal peer review','formal proof-assistant certification','mutual agreement','actual research and writing contributions']) and c['follow_up'] is gate['follow_up'] is clearance['follow_up'] is None and gate['rendered_copy_verified'] is gate['live_verified'] is gate['browser_verified'] is False and gate['native_sheet_aa_url'] is None and not any(x in body.lower() for x in ['root-clearance','sha256','sha-256','2026-10-25','25 october 2026','/users/','checks passed','custody receipt']))
  scope=gate['reviews']['scope']['verdict'];analytic=gate['reviews']['analytic']['verdict'];adverse=gate['reviews']['adversarial']['verdict']
  if rid=='23390551':
   test('original_custom_scope_history',scope['status']=='STATIC_SCOPE_INTAKE_COMPLETE' and scope['mathematical_verdict'] is None and scope['publication_recommendation'] is None and analytic['status']=='pass_as_stated_with_explicit_scope_limits' and analytic['publication_clearance'] is False and adverse['publication_authorization_granted'] is False)
   test('dipole_actual_zero_diagonal_volume_geometry_and_interval',all(x in section_text['result'] for x in ['chosen representative for deciding center membership','Fix κ∈ℂ throughout the mesh limit','arbitrary translations a_h','|Ω_h△Ω|→0','every 3×3 diagonal block zero','S_κ=A_κ−I/3','exact closed numerical range','Both gap directions','h³∑_m|u_m|²']))
   test('dipole_full_spectral_scope_and_fixed_irregular_obstruction',all(x in section_text['result'] for x in ['uniformly bounded discrete inverses','total algebraic multiplicity','operator norm','one fixed compact positive-volume support','κ=1/10000','3×3 zero matrix','existential finite index']) and all(x in section_text['limits'] for x in ['No spectral correctness inside J_lat','mesh-dependent-frequency limit','Individual Jordan block sizes','full announced 2022/2023','Rahola’s full article','no firstness']))
  else:
   test('original_custom_scope_history',scope['mathematical_verdict'] is None and scope['mathematical_clearance'] is False and scope['publication_clearance'] is False and scope['candidate_held'] is True and analytic['publication_authority_granted'] is False and adverse['root_promotion'].startswith('PENDING:') and adverse['source_edits'] is False)
   test('langlands_actual_quotient_entire_induction_and_fixed_orbits',all(x in section_text['result'] for x in ['F=ℚ₃','unramified quadratic extension','smooth admissible complex','irreducible-quotient segment convention','not itself an entire normalized induction','every nonsingular 15-dimensional Hermitian space']) and all(x in section_text['proof'] for x in ['each fixed Hermitian orbit','strict-containment swaps','Entire independent open-orbit restrictions','Only containment of proper rank-one images','No general equality generating that kernel','partition of the five segment occurrences']))
   test('langlands_unknown_Luo_Zha_and_limits',all(x in section_text['limits'] for x in ['do not assume π is unitarizable','do not assert that π is spherical','No separate kernel-generation disproof','Luo–Zha','remain UNKNOWN','may overlap, be contained in, or be superseded','No exhaustive literature absence']) and 'remain UNKNOWN' in c['abstract'] and any(x['title'].startswith('Luo and Zha') and 'UNKNOWN' in x['note'] for x in c['background']))
 result['papers'][rid]={'checks':checks,'hashes':hashes,'local_links_checked':len(local),'pdf_pages':len(texts),'pdf_chars_per_page':[len(t) for t in texts]}
result['shared']={'index_sha256':sha(S/'research/index.html'),'sitemap_sha256':sha(S/'research/sitemap.xml'),'robots_sitemap':'Sitemap: https://aleckriebel.com/research/sitemap.xml' in (S/'robots.txt').read_text()}
result['status']='PASS' if not result['issues'] and result['shared']['robots_sitemap'] else 'ISSUES_FOUND'
try:
 target=args.output_dir/args.output_stem
 target.with_suffix('.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 lines=['# Final content QA','',result['time'],'','Status: '+result['status'],'','Completion: 100% of requested checks executed.','',
 'Read-only checks of generated content against approved publication data and published source. Browser rendering and external HTTP checks are separate.','']
 for rid,item in result['papers'].items():
  lines += [rid+': '+str(sum(item['checks'].values()))+'/'+str(len(item['checks']))+' checks passed; '+str(item['local_links_checked'])+' local links/anchors; '+str(item['pdf_pages'])+' searchable PDF pages.','']
 lines += ['Issues: '+('; '.join(result['issues']) or 'None.'),'','SHA-256 bindings and individual checks are recorded in the accompanying JSON.']
 target.with_suffix('.md').write_text('\n'.join(lines)+'\n')
 result['saved']=True
except OSError as error:result['saved']=False;result['save_error']=str(error)
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result['status']=='PASS' and result['saved'] else 1)
