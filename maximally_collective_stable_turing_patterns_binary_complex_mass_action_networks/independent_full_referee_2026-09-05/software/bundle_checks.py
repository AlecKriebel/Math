import hashlib, json, pathlib, zipfile
import audit_driver as a

bundles=[('data','public/data_archive/final_release_data.zip'),('submission/biorxiv/source','submission/biorxiv/source_package.zip'),('submission/arxiv/source','submission/arxiv/arxiv_source.zip'),('submission/journal/source','submission/journal/source_package.zip')]+[(f'external_audit/packets/{kind}',f'external_audit/packets/{kind}_audit_packet.zip') for kind in ('reaction_network','pde','symbolic')]
for number,(origin,stored) in enumerate(bundles):
    base=a.SOURCE/origin
    expected={str(p.relative_to(base)):p.read_bytes() for p in base.rglob('*') if p.is_file()}
    with zipfile.ZipFile(a.SOURCE/stored) as z:
        assert len(z.namelist())==len(set(z.namelist()))
        actual={i.filename:z.read(i) for i in z.infolist()}
        assert actual==expected
        assert list(actual)==sorted(actual)
    target=a.SCRATCH/('rebuilt_bundle_'+str(number)+'.zip')
    assert a.run('bundle_regenerate_'+str(number),['python',str(a.SOURCE/'release/deterministic_zip.py'),str(base),str(target)],a.HERE)==0
    assert target.read_bytes()==(a.SOURCE/stored).read_bytes()
    target.unlink()
    print('BUNDLE_CONTENT_METADATA_AND_BYTE_IDENTITY_PASS',stored,len(expected))
for kind in ('biorxiv','arxiv','journal'):
    source=a.SOURCE/f'submission/{kind}/source'
    for name in ('main.tex','supplement.tex'):
        canonical=(a.SOURCE/'manuscript'/name).read_text().replace('../figures/','figures/').replace('../data/','data/')
        assert (source/name).read_text()==canonical
    assert (source/'journal_review_mode.tex').exists()==(kind=='journal')
    assert (source/'main.bbl').exists()==(kind!='arxiv')
    print('DETACHED_SOURCE_CONTENT_EQUALS_CANONICAL_WITH_DOCUMENTED_PATH_AND_MODE_CHANGES',kind)
frozen=pathlib.Path('/mnt/data')
names=['qbio_mass_action_turing_final_flagship.zip','qbio_mass_action_turing_all_spectrum_paper.zip','qbio_mass_action_turing_all_spectrum_stable.zip','qbio_mass_action_turing_diffusion_design.zip','qbio_mass_action_turing_nonlinear_frontier.zip']
for name in names: print('DEFAULT_LINEAGE_PREREQUISITE',name,'PRESENT' if (frozen/name).is_file() else 'MISSING')
print('BUNDLE_AND_SOURCE_STATIC_AUDIT_PASS; DETACHED_BUILDS_NOT_EXECUTED')
