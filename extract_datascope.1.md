---
title: EXTRACT_DATASCOPE
section: 1
header: User Manual
footer: extract_datascope 1.0.0
date: March 18, 2021
---

# NAME
extract_datascope - tool to extract data from datascope database files and save to JSON format

# SYNOPSIS
**extract_datascope** [*OPTION*]...

# DESCRIPTION
**extract_datascope** is a simple Python script to extract data from our datascope database
files and to output that data to JSON fixture files that are loadable by our PostgreSQL 
idastatus database

# OPTIONS
**-h**, **\-\-help**
: display the usage message

**\-\-outdir OUTPUT_DIRECTORY_NAME**
: name of the directory in which to save the output.  If this is not specified, the default is used, a directory in the curren directory name "output"

# ENVIRONMENT
This script requires the **IDA_DATASCOPEDB_DIR** environment variable for the location of the datascope database files
