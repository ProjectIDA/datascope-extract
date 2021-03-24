# Make different targets for this project

all:

ls:			## Show list of make targets 
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

manpage:		## make manpage from markdown
	pandoc extract_datascope.1.md -s -t man -o extract_datascope.1

viewmanpage:		## view the manpage
	nroff -man extract_datascope.1 | less
