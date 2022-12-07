# sorts and counts all of the lines to show which are repeated the most.

for FILE in ./found_no_repeating_domain/*.txt; 
do 
    echo $FILE;
    awk '{$1=$1};1' $FILE | sort | uniq -c | sort -r > $FILE.count_freq.txt; 
    mv $FILE.count_freq.txt ./analysis/frequency_no_domain/;
 done;

