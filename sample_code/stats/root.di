node root() {
        [1,2,3,4,5,6,7,8,9,10] => (initialize_data);
}

node (data []int) => initialize_data => (float){
        data => (mean) => (print_data);
        data => (median) => (print_data);
        data => (mode) => (print_data);
}

node (data []int) => mean => (int){
        average := 0.0;
        for (i, elem) in data {
                average += elem;
        }

        data => (length) => length;
        average / length => (child);
}

node (data []int) => median {
        for (i, elem) in data {
                for j in range data[i:1:-1] {
                        if data[j] < data[j - 1] {
                                temp := data[j - 1];
                                data[j - 1] = data[j];
                                data[j] = temp;
                        } else {
                                break;
                        }
                }
        }

        data => (length) => length;
        data[length / 2] => (child);
}

node (data []int) => mode => (int) {
        m := map<int, int>;

        for (index, elem) in data {
                (value, valid) = map[elem];
                if !valid {
                        map[elem] = 1;
                } else {
                        map[elem] += 1;
                }
        }

        highest := 0;
        mode := 0;
        for (key, value) in map {
                if value > highest {
                        mode = key;
                        highest = value;
                }
        }

        mode => (child);
}

node (average float, median int, mode int) => print_data {
        average => (print);
        median => (print);
        mode => (print); 
}
