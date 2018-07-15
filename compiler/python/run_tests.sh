touch output.txt
rm output.txt
touch output.txt

test_file() 
{
        file=$1
        name=${file#$2}
        name=$(echo $name | cut -f 1 -d '.') #remove extension
        python3 digon.py $file > tests/results/$name
        touch output.txt
        diff tests/expected/$name tests/results/$name >> output.txt
        diff tests/expected/$name tests/results/$name > temp
        [ -s temp ] || echo "$name passes test"
        rm temp
}

test_files_in_dir()
{
        for file in tests/$1/*; do
                test_file $file "tests/$1/"
                echo $file
        done   
}

if [ "$1" == "" ]; then
        echo "Please specify which tests to run"
        echo "To see list of available tests, run with --tests"

elif [ "$1" == "--help" -o "$1" == "-help" -o "$1" == "help" -o \
      "$1" == "--usage" -o "$1" == "-usage" -o "$1" == "usage" ]; then
        echo "--tests: list available testing options"
        echo "Nothing else for now!"

elif [ "$1" == "--tests" ]; then #list test options
        echo "all: - run all tests available"
        echo "lexer: - run lexer tests (not yet ready)"
        echo "parser: - run parser tests (not yet ready)"
        echo "concurrent: - run tests for concurrency (not yet ready)"

elif [ "$1" == "all" ]; then #run full tests
        test_files_in_dir "lexer"
        test_files_in_dir "parser"
        test_files_in_dir "concurrent"
        test_files_in_dir "full"

elif [ "$1" == "lexer" ]; then #run full tests
        test_files_in_dir "lexer"
elif [ "$1" == "parser" ]; then #run full tests
        test_files_in_dir "parser"
elif [ "$1" == "concurrent" ]; then #run full tests
        test_files_in_dir "concurrent"
elif [ "$1" == "full" ]; then #run full tests
        test_files_in_dir "full"

else #run specified tests by filename
        for file in "$@"; do
                name=${file#tests/code/}
                name=$(echo $name | cut -f 1 -d '.') #remove extension
                echo $name
                python3 digon.py tests/code/$file > tests/results/$name
                touch output.txt
                diff tests/expected/$name tests/results/$name >> output.txt
                diff tests/expected/$name tests/results/$name > temp
                [ -s temp ] || echo "$name passes test"
                rm temp
        done
fi

cat output.txt