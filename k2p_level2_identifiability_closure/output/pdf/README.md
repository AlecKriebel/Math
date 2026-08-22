# Theorem manuscript PDF

`K2P_SAME_Principal_Domain_Theorem.pdf` is the typeset derivative of the
promotion-locked Markdown manuscript. Build it from the project root with:

```sh
sh output/pdf/render_pdf.sh
```

The renderer requires Pandoc and Tectonic. It uses a fixed
`SOURCE_DATE_EPOCH`, wraps the long certificate hashes, and changes no theorem
content. The final PDF has 14 letter-sized pages and has been rendered to PNG
and visually checked page by page.

