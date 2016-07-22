#!/usr/bin/python
# -*- coding: utf8 -*-

import argparse
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description='Get a multi-fasta, the trained_dir and the output file as inputs, '
                                                 'to generate GlimmerHMM gene prediction over all contigs')

    parser.add_argument('--multi_fasta', help='Multi fasta file to run GlimmerHMM on', required=True)

    parser.add_argument('--trained_dir', help='Path to the GlimmerHMM trained_dir', required=True)

    parser.add_argument('--output', help='file to output the result into', required=True)

    args = parser.parse_args()

    multi_fasta = args.multi_fasta
    trained_dir = args.trained_dir
    output_file = args.output
    temp_contig = "temp_contig"

    def exec_glimmer(contig_file, first_time=False):
        p = subprocess.Popen(["glimmerhmm", contig_file, trained_dir, "-g"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = p.communicate()

        p.wait()
        # Process the error if != "Done"
        if not errors or (errors.split()[0] != "Done"):
            raise Exception("Error in glimmer: {0}".format(errors))
        else:
            sys.stdout.write(errors)
        # If  not first time, we need to remove the first comments
        if not first_time:
            output = "\n".join(output.split("\n")[1:])

        return output

    with open(output_file, 'w+') as o:
        with open(multi_fasta, 'r') as mf:
            is_first_time = True
            for i, line in enumerate(mf):
                if line[0] == '>':
                    # If it is the first time we finish to read a contig, we let glimmer add the full comments
                    # and write into the output the result
                    if is_first_time is True and i != 0:
                        o.write(exec_glimmer(temp_contig, first_time=is_first_time))
                        is_first_time = False
                    # Else we call glimmer and say this is not the first time (so remove the first comment)
                    # and dump into the output file the result
                    elif i > 0:
                        o.write(exec_glimmer(temp_contig))

                    # Because we are on an indication of a beginning of a sequence, we need to create an empty file
                    # to dump the line into
                    with open(temp_contig, 'w+') as tc:
                        tc.write(line)
                else:
                    # We are in the sequence of a contig, so we append the line in the file
                    with open(temp_contig, 'a+') as tc:
                        tc.write(line)
        # The file is terminate, we did read another contig so we need to save this last one
        o.write(exec_glimmer(temp_contig, first_time=is_first_time))

if __name__ == "__main__":
    main()
