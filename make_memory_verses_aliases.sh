#!/bin/bash


MEMORY_VERSE_DIR="/mnt/c/Users/New User/Dropbox/Documents/Christ is Life/FTTA Fall 2017 - Term 1 Outlines and Class Notes/Fall 2017 Classes/The Experience of Christ As Life/Memory Verses/"

# The format of the aliases in the bashrc file will be like so:
# ecal_lesson[0-9]+_mv='...'

# Current aliases
current_aliases=$(cat ~/.bashrc | grep -E 'ecal_lesson[0-9]+_mv')

pushd "$MEMORY_VERSE_DIR" > /dev/null
    current_mv_files=$(ls -A)
    #echo "CURRENT ALIASES=${current_aliases}"
    for mv_file in $current_mv_files; do
        # Filename without extension
        filename=$(echo $mv_file | cut -d'.' -f1)
        #echo "CURRENT MV_FILE=${mv_file}"
        if echo $current_aliases | grep $filename > /dev/null; then
            continue
        else
            lesson_number=$(echo $mv_file | cut -d'_' -f2)
            alias_string="alias ecal_${lesson_number}_mv=\"study_it -f '${MEMORY_VERSE_DIR}/${mv_file}'\""
            echo "# ECAL Memory Verse Week ${lesson_number}"
            echo ${alias_string}
        fi
    done
