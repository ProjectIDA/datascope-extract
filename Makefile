# Make different targets for this project

all:

ls:			## Show list of make targets 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

pages:			## make document pages from markdown
	cat docs/pandoc_header.txt README.md > docs/pandoc_page.1.md
	pandoc docs/pandoc_page.1.md -s -t man -o docs/extract_datascope.1

viewpage:		## view the manpage
	nroff -man docs/extract_datascope.1 | less
