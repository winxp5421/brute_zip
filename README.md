# brute_zip
This script will take a "plaintext" input file and iterate over all zlib compression options and optionally attempt use the compressed data with bkcrack to plaintext attack zip files.  
If you would like the script to automatically call bkcrack on each output file you will need to grab and compile [bkcrack](https://github.com/kimci86/bkcrack)   

Some of the zlib compression code is borrowed from the [bkcrack](https://github.com/kimci86/bkcrack) repository.
