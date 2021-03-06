'''
mmff.
The program reads one or more input FASTA files, and
modifies them according to metamorphic relationships (MRs)
passed in as parameters.'''

from argparse import ArgumentParser
from math import floor
import sys
from Bio import SeqIO
import skbio
import pkg_resources
from mmff.morphs.morphs_singles import mmff_reverse,mmff_passthrough


EXIT_FILE_IO_ERROR = 1
EXIT_COMMAND_LINE_ERROR = 2
EXIT_FASTA_FILE_ERROR = 3
DEFAULT_VERBOSE = False
PROGRAM_NAME = "mmff"


try:
    PROGRAM_VERSION = pkg_resources.require(PROGRAM_NAME)[0].version
except pkg_resources.DistributionNotFound:
    PROGRAM_VERSION = "undefined_version"


def exit_with_error(message, exit_status):
    '''Print an error message to stderr, prefixed by the program name and 'ERROR'.
    Then exit program with supplied exit status.
    Arguments:
        message: an error message as a string.
        exit_status: a positive integer representing the exit status of the
            program.
    '''
    print("{} ERROR: {}, exiting".format(PROGRAM_NAME, message), file=sys.stderr)
    sys.exit(exit_status)


def parse_args():
    '''Parse command line arguments.
    Returns Options object with command line argument values as attributes.
    Will exit the program on a command line error.
    '''
    parser = ArgumentParser(description='Create metamorphic tests of FASTA files')

    parser.add_argument('--morphs',
                        nargs='+',
                        type=str,
                        help='Metamorphic tests to create.'
)
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + PROGRAM_VERSION)
    parser.add_argument('--verbose',
                        action='store_true',
                        default=DEFAULT_VERBOSE,
                        help="Print more stuff about what's happening")
    parser.add_argument('fasta_files',
                        nargs='*',
                        metavar='FASTA_FILE',
                        type=str,
                        help='Input FASTA files')
    return parser.parse_args()




def mmff_from_file(fasta_file, morphs):
    '''Compute a FastaStats object from an input FASTA file.
    Arguments:
       fasta_file: an open file object for the FASTA file
       morphs: list of morph functions to apply
    Result:
       tbc
    '''

    morphs_dict={
    'reverse':mmff_reverse,
    "passthrough": mmff_passthrough
    }
    morphed_sequences= []

    for seq in SeqIO.parse(fasta_file, "fasta"):
        for morph in morphs:
            print("morph "+str(morphs_dict[morph])+" on "+seq.id)
            morphed_sequences.append(morphs_dict[morph](seq))
    return morphed_sequences

def process_files(options):
    '''Compute and save MR for each input FASTA file specified on the
    command line. If no FASTA files are specified on the command line then
    read from the standard input (stdin).
    Arguments:
       options: the command line options of the program
    Result:
       None
    '''

    morph_list = ["passthrough"] + options.morphs
    print(morph_list)
    if options.fasta_files:
        for fasta_filename in options.fasta_files:
            try:
                fasta_file = open(fasta_filename)
            except IOError as exception:
                exit_with_error(str(exception), EXIT_FILE_IO_ERROR)
            else:
                with fasta_file:
                    new_seqs = mmff_from_file(fasta_file, morph_list)
                    print(new_seqs)
    else:
        #stats = mmff_from_file(sys.stdin, options.morphs)
        #print(stats.pretty("stdin"))
        print("STDIN not supported yet")


def main():
    "Mighty Morphin FASTA files - go go!"
    options = parse_args()
    print(options)
    process_files(options)


# If this script is run from the command line then call the main function.
if __name__ == '__main__':
    main()
