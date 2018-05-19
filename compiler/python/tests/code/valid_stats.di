node root {
        array := [10]int{1,2,3,4,5,6,7,8,9,10};
        array => calculate_stats(data);
}

node calculate_stats <= (data []int){
        data => mean() => print_data(average);
        data => median() => print_data(median);
        data => mode() => print_data(mode);
}

node mean <= (data1 []int) {
        average := 0.0;
        for i, elem in data1 {
                average += elem;
        }

        length := 0;
        data1 => length() => length;
        average / length => dest();
}

node median <= (data2 []int) {
        for i, elem in data2 {
                for j, _ in data2[i:1:-1] {
                        if data2[j] < data2[j - 1] {
                                temp := data2[j - 1];
                                data2[j - 1] = data2[j];
                                data2[j] = temp;
                        } else {
                                break;
                        }
                }
        }

        length := 0;
        data2 => length() => length;
        data2[length / 2] => dest();
}

node mode <= (data3 []int) {
        m := map<int, int>;

        for index, elem in data3 {
                (value, valid) = m[elem];
                if !valid {
                        m[elem] = 1;
                } else {
                        m[elem] += 1;
                }
        }

        highest := 0;
        mode := 0;
        for key, value in m {
                if value > highest {
                        mode = key;
                        highest = value;
                }
        }

        mode => dest();
}

node print_data <= (average1 float, median1 int, mode1 int){
        average1 => println();
        median1 => println();
        mode1 => println(); 
}
