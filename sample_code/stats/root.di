node root {
        array := [10]int{1,2,3,4,5,6,7,8,9,10}
        array => initialize_data(data);
}

node calculate_stats <= (data []int){
        data => mean() => print_data(average);
        data => median() => print_data(median);
        data => mode() => print_data(mode);
}

node mean <= (data []int) {
        average := 0.0;
        for (i, elem) in data {
                average += elem;
        }

        length := 0;
        data => length() => length;
        average / length => dest();
}

node median <= (data []int) {
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

        length := 0;
        data => length() => length;
        data[length / 2] => dest();
}

node mode <= (data []int) {
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

        mode => dest();
}

node print_data <= (average float, median int, mode int){
        average => println();
        median => println();
        mode => println(); 
}
