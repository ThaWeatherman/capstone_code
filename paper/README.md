# Create the PDF

```
chmod 744 clean.sh
chmod 744 compile.sh
./clean.sh
./compilesh
```

Voila, you now have `paper.pdf`.

# Dependencies

This is written in TeX, so you need to install tex.
On Arch, I installed `texlive-bin` and `texlive-core`.
You can determine dependencies on your own for your system.
`compile.sh` runs `pdflatex` and `bibtex`, so make sure you have those.
