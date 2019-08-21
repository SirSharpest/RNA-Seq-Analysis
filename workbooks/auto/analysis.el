(TeX-add-style-hook
 "analysis"
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
    "sec:orga9cbabb"
    "sec:orgfc96b3e"
    "sec:orgffc340f"
    "sec:orge10bfd4"
    "sec:org894a806"
    "sec:org490c813"
    "sec:org4e1d870"
    "samplecounts"
    "sec:org0f25176"
    "sec:org38f601f"
    "sec:org0933277"
    "sec:org1618a07"
    "sec:orgeedf0bb"
    "pairings_05hr_boxplots"
    "sec:org6ab7a03"
    "sec:org349ce79"
    "sec:org20253f0"
    "pairings_6hr_boxplots"
    "sec:org7d44aa0"
    "sec:org6109b0f"
    "sec:org1965ec5"
    "pairings_05hr_lym_boxplots"
    "sec:org2607aa3"
    "sec:org4eb618e"
    "sec:orgafd91a7"
    "pairings_6hr_lym_boxplots"
    "sec:orgedc71f0"
    "sec:org817d5b8"
    "sec:org874876e"
    "pairings_timings_boxplots"
    "sec:org0c7b177"
    "sec:org5d34bc6"))
 :latex)

