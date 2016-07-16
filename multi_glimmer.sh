#!/bin/bash
set -e

reference_fasta=$1
trained_dir=$2
output=$3

# Generate the index
function samtools_faidx {
    samtools faidx $1
}

# Read, in the file passed in parameter $1, the contig passed in parameter $2
function samtools_faidx_show_contig {
    samtools faidx $1 $2
}

# Write the glimmerhmm, with the comments
function glimmerHMM_first {
    glimmerhmm $1 ${trained_dir} -o ${output} -g
}

# Write the glimmerhmm output without the comments
function glimmerHMM_without_comments {
    glimmerhmm $1 ${trained_dir} -g | tail -n +3 >> ${output}
}

# We create the index
samtools_faidx ${reference_fasta}

count=1
# Loop through the contigs to run glimmer on each
while read contig others_fields 
do
    # Get the content of actual contig
    samtools_faidx_show_contig ${reference_fasta} ${contig} > contig_content
    if [ ${count} -eq 1 ]
    then
		glimmerHMM_first contig_content;
		(( count++ ))
	else
	    glimmerHMM_without_comments contig_content;
	fi
done < "${reference_fasta}.fai"

# Delete the index
rm ${reference_fasta}.fai

exit 0