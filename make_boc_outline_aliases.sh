#-----------------------------------------------------------------------------
#
# Name: make_boc_outline_aliases.sh
# Description:
# This small bash script outputs alias commands, usually directed to .bashrc,
# that make aliaes to apply the 'study_it.py' program to the Body of Christ
# outlines.
# The location directory for the Body of Christ outlines is hardcoded.
# The name of the alias command is in the format below:
# boc_<#>
# The Boc Ouline filename format is like so:
# "Lesson_<#>"
# This script compares the lesson number in the filename to the lesson number
# in the boc alias command name. If it's already in .bashrc, then the command
# will not be printed out.
# Author: Alex Cantu
# Date: 10/21/2017
#
#
#-----------------------------------------------------------------------------


# VARS -----------------------------------------------------------------------
## String variable
SOME_VARIABLE='HELLO WORLD'
BOC_OUTLINE_DIRECTORY="/mnt/c/Users/New User/Dropbox/Documents/Christ is Life/FTTA Fall 2017 - Term 1 Outlines and Class Notes/Fall 2017 Classes/The Body of Christ/Text Outlines (Typed Out)"
CURRENT_BOC_ALIASES=$(cat ~/.bashrc | grep -E 'boc_[0-9]+')

# MAIN -----------------------------------------------------------------------

pushd "$BOC_OUTLINE_DIRECTORY" > /dev/null
    current_files=$(ls -A)
    for outline_file in $current_files; do
        #Filename without extension
        lesson_number=$(echo $outline_file | cut -d'_' -f2 | cut -d'.' -f1)
        # If the alias is already in place, do not print it.
        if echo $CURRENT_BOC_ALIASES | grep "boc_${lesson_number}" > /dev/null; then
            continue
        else
            alias_string="alias boc_${lesson_number}=\"study_it -f '${BOC_OUTLINE_DIRECTORY}/${outline_file}' -o\""
            echo "# BOC Outline Lesson ${lesson_number}"
            echo ${alias_string}
        fi
    done
