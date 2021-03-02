# datascope-extract
Code to extract data from datascope format data files to insert to PostgreSQL

This code produces json format files that become the fixtures in
the docker-idastatus Django project.  These fixtures populate the PostgreSQL
database in its container.

The executable, extract_datascope, takes one optional parameter --outdir
which is a target directory for the output files.  If this directory is not
specified, a directory named "output" in the current directory is created 
and the output files are written there.
