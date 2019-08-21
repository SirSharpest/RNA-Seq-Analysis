(TeX-add-style-hook
 "random_forests"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("geometry" "margin=0.8in") ("parskip" "parfill") ("natbib" "sort&compress" "numbers")))
   (add-to-list 'LaTeX-verbatim-environments-local "minted")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
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
    "sec:orgcd628f4"
    "sec:orga1cf8fc"
    "sec:org7e9ed19"
    "sec:org83696fe"
    "sec:org8a8f50e"
    "sec:org3e8da90"
    "sec:org4c0e844"
    "featbar"
    "sec:org85b15b4"
    "sec:org0a6e6cd"))
 :latex)

