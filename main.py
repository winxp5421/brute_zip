import os
import zlib
import argparse
import subprocess

# Create an ArgumentParser object
parser = argparse.ArgumentParser()

# Define the command-line arguments
parser.add_argument("--plaintext", "-p", help="Plaintext file that needs to be compressed", required=True)
parser.add_argument("--output_dir", "-o", default='./',
                    help="Set the location the output files should be placed Default: './'")
parser.add_argument("--bkcrack", help="Run bkcrack on the generated files", action="store_true")
parser.add_argument("--keep", "-k", default=False, action="store_true",
                    help="Keep all zip files generated by script. Only applies when --bkcrack option is used "
                         "Default: Only keep files that result in successful bkcrack keys")
parser.add_argument("--cipher_file", "-c",
                    help="Zip entry (filename inside) or file on disk containing ciphertext (required with --bkcrack)",
                    required=False)
parser.add_argument("--cipher_zip", "-C",
                    help="Zip archive containing the ciphertext entry (required with --bkcrack)", required=False)
parser.add_argument("--bkcrack_loc", default='./bkcrack',
                    help="Set the location of the bkcrack binary Default: './bkcrack'")


args = parser.parse_args()
bkcrack_enable = args.bkcrack
cipher_file = args.cipher_file
cipher_zip = args.cipher_zip
keep_files = args.keep
plaintext_file = args.plaintext
output_dir = args.output_dir
bkcrack_loc = args.bkcrack_loc

if bkcrack_enable:
    if cipher_file is None or cipher_zip is None:
        parser.error("If using --bkcrack, both --cipher_file and --cipher_zip are required.")

if bkcrack_enable and not os.path.isfile(bkcrack_loc):
    parser.error(bkcrack_loc + " not found.")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def deflate(raw_data, level=-1, wbits=-zlib.MAX_WBITS, strategy=zlib.Z_DEFAULT_STRATEGY):
    """Returns compressed data."""
    compressor = zlib.compressobj(level, zlib.DEFLATED, wbits, zlib.DEF_MEM_LEVEL, strategy)
    return compressor.compress(raw_data) + compressor.flush()


# Compression level settings
compressions = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
# Word size settings
word_sizes = ["9", "10", "11", "12", "13", "14", "15"]
# Strategy settings
strategies = ["default", "filtered", "huffman_only", "rle", "fixed"]

# Strategies are described in the documentation of the deflateInit2 function in zlib's manual.
# See: https://www.zlib.net/manual.html#Advanced
zlib_strategies = {
    'default': zlib.Z_DEFAULT_STRATEGY,
    'filtered': zlib.Z_FILTERED,
    'huffman_only': zlib.Z_HUFFMAN_ONLY,
    'rle': zlib.Z_RLE,
    'fixed': zlib.Z_FIXED
}

with open(plaintext_file, 'rb') as f_in:
    data = f_in.read()

for c in compressions:
    for w in word_sizes:
        for s in strategies:
            output_file_name = f"output-c{c}-w{w}-s{s}.zip"
            output_location = output_dir + output_file_name
            comp_level = int(c)
            wsize = int(w)
            comp_strategy = zlib_strategies[s]
            with open(output_location, 'wb') as f_out:
                f_out.write(deflate(data, comp_level, -wsize, comp_strategy))
            if bkcrack_enable:
                command = [bkcrack_loc, '-p', output_location, '-C', cipher_zip, '-c', cipher_file]
                process = subprocess.run(command, capture_output=True)
                if process.returncode == 0:
                    print(process.stdout.decode('utf-8'))
                    print(f"{output_location}: Was successful")
                    if not keep_files:
                        break
                else:
                    if not keep_files:
                        try:
                            os.remove(output_location)
                        except OSError as error:
                            print(f"Error deleting file: {error}")
