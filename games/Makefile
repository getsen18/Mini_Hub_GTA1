# Variables
LATEX_COMPILER = pdflatex
BIB_COMPILER   = bibtex
FILENAME       = report
SOURCE_FILE    = $(FILENAME).tex
PDF_FILE       = $(FILENAME).pdf
all: $(PDF_FILE)

$(PDF_FILE): $(SOURCE_FILE)
	$(LATEX_COMPILER) $(SOURCE_FILE)
	-$(BIB_COMPILER) $(FILENAME)
	$(LATEX_COMPILER) $(SOURCE_FILE)
	$(LATEX_COMPILER) $(SOURCE_FILE)

clean:
	rm -f *.aux *.log *.out *.toc *.blg *.bbl *.snm *.nav
