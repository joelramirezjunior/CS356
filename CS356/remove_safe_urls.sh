# grabbing all unique lines, filtering for safe domains (e.g. youtube.com)
# then we move it to the unique_no_repeating_domains folder

for FILE in ./found_no_repeating_domain/*.txt; 
do 
    echo $FILE;
    awk '{$1=$1};1' $FILE | sort | uniq > $FILE.cpy; 
    grep -v -f ./safe/safe_urls.txt $FILE.cpy > $FILE.temp;
    mv $FILE.temp ./unique_no_repeating_domain/;
    rm $FILE.cpy; 
 done;

