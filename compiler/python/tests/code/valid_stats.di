node root {
        array := [10]int{1,2,3,4,5,6,7,8,9,10};
        array => calculate_stats(data);
}

node calculate_stats <= (data [10]int){
        data => mean() => print_data(average);
        data => median() => print_data(median);
        data => mode() => print_data(mode);
}

node mean <= (data1 [10]int) {
        average := 0.0;
        for _, elem in data1 {
                average += float64(elem);
        }

        length := 0;
        data1 => length() => length;
        average / float64(length) => dest();
}

node median <= (data2 [10]int) {
        length := 0;
        data2 => length() => length;

        for i, _ in data2 {
                for j := i; j > 1; j-- {
                        if data2[j] < data2[j - 1] {
                                temp := data2[j - 1];
                                data2[j - 1] = data2[j];
                                data2[j] = temp;
                        } else {
                                break;
                        }
                }
        }

        data2[length / 2] => dest();
}

node mode <= (data3 [10]int) {
        m := map<int, int>;

        for _, elem in data3 {
                _, valid := m[elem];
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
