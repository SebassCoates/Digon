touch output.txt
rm output.txt
touch output.txt

for file in tests/code/*; do
        name=${file#tests/code/}
        python3 digon.py $file > tests/results/$name
        touch output.txt
        diff tests/expected/$name tests/results/$name >> output.txt
        diff tests/expected/$name tests/results/$name > temp
        [ -s temp ] || echo "$name passes test"
        rm temp
done

cat output.txt
