TEXFILE = mainTemplatePDF
# PNG files are also tracked to ensure Makefile re-runs if they change
# The .gitignore whitelist serves as the list of files to be tracked
IMAGE_PNG_LIST = $(shell sed -n 's/^!//p' .gitignore | grep '\.png$$')
IMAGE_JPG_LIST = $(shell sed -n 's/^!//p' .gitignore | grep '\.jpg$$')

.PHONY: all clean distclean

all: $(TEXFILE).pdf

$(TEXFILE).pdf: $(TEXFILE).tex $(TEXFILE).bib $(IMAGE_PNG_LIST) $(IMAGE_JPG_LIST)
	rm -f $(TEXFILE).aux $(TEXFILE).out $(TEXFILE).log $(TEXFILE).toc $(TEXFILE).bbl $(TEXFILE).blg $(TEXFILE).fls $(TEXFILE).fdb_latexmk
	pdflatex $(TEXFILE).tex
	biber $(TEXFILE)
	pdflatex $(TEXFILE).tex
	pdflatex $(TEXFILE).tex

clean:
	rm -f $(TEXFILE).aux $(TEXFILE).out $(TEXFILE).log $(TEXFILE).toc $(TEXFILE).bbl $(TEXFILE).blg $(TEXFILE).fls $(TEXFILE).fdb_latexmk 

distclean:
	rm -f $(TEXFILE).pdf
