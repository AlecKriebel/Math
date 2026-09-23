# Zenodo upload instructions

This is a manual upload kit for **A note on Γ-supercyclicity of dissipative composition operators**, version 1.0.0. No Zenodo deposition or DOI has been created.

1. Extract `zenodo-upload-kit.zip` and open [New upload](https://zenodo.org/uploads/new).
2. Upload **paper.pdf** and **note-source.zip**. `SHA256SUMS.txt` is an optional third upload. Do not upload the entire outer kit as a substitute for the separately readable paper.
3. Select **Publication / Preprint** and copy the fields in `COPYPASTE.md`. The complete description prominently attributes the result to earlier work. The creator is Alec Kriebel, ORCID 0009-0001-9320-500X. The license is CC BY 4.0.
4. Answer **No** to whether this note already has a DOI. The DOIs in the bibliography and related works identify earlier papers; none is the DOI of this note. Zenodo can reserve a DOI before publication if desired. A reserved DOI may be added to the note before the files are finalized.
5. Save the draft and review its title, author, attribution, version, license, and uploaded files. Publish when ready. Zenodo registers a DOI on publication.

`metadata.json` contains structured fields compatible with Zenodo's deposit metadata format. `metadata-for-api.json` wraps those fields in a `metadata` object for the deposit API; it is provided as data and does not make any API call. These JSON files need not be uploaded as research content. `COPYPASTE.md` is the convenient path for the web form.

The intended scholarly claim is an attributed application answering the report's question. It is not a claim that the scalar criterion or amplification mechanism is new. The note is AI-assisted and unrefereed. Third-party full texts, internal audit transcripts, and numerical verifier scripts are excluded from this compact note-source archive.

Official instructions: [Create an upload](https://help.zenodo.org/docs/deposit/create-new-upload/) and [reserve a DOI](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/). Metadata documentation: [Zenodo developer documentation](https://developers.zenodo.org/).

Do not create a GitHub release merely to upload this kit: this repository's GitHub release integration may create a separate automatic Zenodo deposit.
