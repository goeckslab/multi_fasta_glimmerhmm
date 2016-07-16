#!/bin/sh
set -e

reference_fasta=$1
trained_dir=$2
output=$3
temp="temp_contig_file"

# Write the glimmerhmm, with the comments
glimmerHMM_first () {
    glimmerhmm $1 ${trained_dir} -o ${output} -g
}

# Write the glimmerhmm output without the comments
glimmerHMM_without_comments () {
    glimmerhmm $1 ${trained_dir} -g | tail -n +2 >> ${output}
}

count=1
# Loop through the contigs to run glimmer on each
while read line
do
    # Get the content of actual contig
    #samtools_faidx_show_contig ${reference_fasta} ${contig} > contig_content
    first_char=$(echo ${line} | cut -c1-1)

    if [ ${first_char} = '>' ]
    then
        # If true, it means we have finished reading at least the first contig
        if [ -f ${temp} ]
        then
            if [ ${count} -eq 1 ]
            then
                glimmerHMM_first ${temp};
                count=$((count+1))
            else
                glimmerHMM_without_comments ${temp};
            fi
        fi
        echo ${line} > ${temp}
    else
        echo ${line} >> ${temp}
    fi
done < "${reference_fasta}"

# Still last contig to process
glimmerHMM_without_comments ${temp};

# Delete the temp_contig_file
rm ${temp}
