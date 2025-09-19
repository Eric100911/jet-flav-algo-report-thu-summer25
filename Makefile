TEXFILE = mainTemplatePDF
BIBFILE = refs

.PHONY: all clean distclean

all: $(TEXFILE).pdf

$(TEXFILE).bib: $(TEXFILE).tex $(BIBFILE).bib
	python3 generate_bib.py --bib $(BIBFILE).bib --output $(TEXFILE).bib --tex $(TEXFILE).tex

$(TEXFILE).pdf: $(TEXFILE).tex $(TEXFILE).bib
	rm -f $(TEXFILE).aux $(TEXFILE).out $(TEXFILE).log $(TEXFILE).toc $(TEXFILE).bbl $(TEXFILE).blg $(TEXFILE).fls $(TEXFILE).fdb_latexmk
	pdflatex $(TEXFILE).tex
	bibtex $(TEXFILE)
	pdflatex $(TEXFILE).tex
	pdflatex $(TEXFILE).tex

clean:
	rm -f $(TEXFILE).aux $(TEXFILE).out $(TEXFILE).log $(TEXFILE).toc $(TEXFILE).bbl $(TEXFILE).blg $(TEXFILE).fls $(TEXFILE).fdb_latexmk $(TEXFILE).bib

distclean: clean
	rm -f $(TEXFILE).pdf $(TEXFILE).bib
