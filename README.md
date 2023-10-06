# brute_zip
This script will take a "plaintext" input file and iterate over all zlib compression options and optionally attempt use the compressed data with bkcrack to plaintext attack zip files.  
If you would like the script to automatically call bkcrack on each output file you will need to grab and compile [bkcrack](https://github.com/kimci86/bkcrack)   

# Why?
This can be very helpful if you have a "plaintext" (unecrypted, not compressed) file that you suspect the encrypted zip file contains the same file within it but, are unsure of the compression methods used to create the encrypted zip file.  

This essentially tries (almost) all compression settings in zlib to "brute force" or generate deflated versions of the file/string to be used in an attempt plaintext attack the encrypted archive. 
#
Some of the zlib compression code is borrowed from the [bkcrack](https://github.com/kimci86/bkcrack) repository.
