(TeX-add-style-hook
 "workbook"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("geometry" "margin=0.8in") ("parskip" "parfill") ("natbib" "sort&compress" "numbers")))
   (add-to-list 'LaTeX-verbatim-environments-local "minted")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "inputenc"
    "fontenc"
    "graphicx"
    "grffile"
    "longtable"
    "wrapfig"
    "rotating"
    "ulem"
    "amsmath"
    "textcomp"
    "amssymb"
    "capt-of"
    "hyperref"
    "minted"
    "geometry"
    "fancyhdr"
    "lastpage"
    "float"
    "tabularx"
    "titlesec"
    "parskip"
    "subfig"
    "natbib"
    "framed"
    "mathtools"
    "cases")
   (LaTeX-add-labels
    "sec:orgcc69334"
    "sec:org410a50a"
    "sec:org220b1be"
    "sec:orgce726bb"
    "sec:orge2aba67"
    "sec:orgf6d54a1"
    "sec:orgd88a24b"
    "distancemap"
    "sec:org274e0c9"
    "distancemappooled"
    "sec:org31c615b"
    "sec:orgcedbe0a"
    "largest"
    "sec:org6a47a65"
    "tfs"
    "sec:orgd8b7154"
    "sec:orgb44efb5"
    "pca"
    "sec:org09358e9"
    "pca_both"))
 :latex)

