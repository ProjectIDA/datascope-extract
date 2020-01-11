#
# I got the inspiration for this project from this snippet of code found at
# https://www.media-division.com/making-a-fixed-width-text-file-to-csv-converter-in-c-java-php-javascript-and-python/


    IN_FILE = "in.txt"
    OUT_FILE = "out.csv"
    RANGES = ((0, 6), (6, 20), (29, 3))
    try:
        rfp = open(IN_FILE, 'r')
    except IOError:
        print ("Could not read from", IN_FILE)
        raise SystemExit
      
    try:
        wfp = open(OUT_FILE, 'w')
    except IOError:  
        print ("Could not write to", OUT_FILE)
        raise SystemExit
    for line in rfp:
        parts = []
        for rng in RANGES:
            parts.append(line[rng[0]:rng[0]+rng[1]].strip())
        wfp.write("\t".join(parts)+"\n")
        
    rfp.close()
    wfp.close()
