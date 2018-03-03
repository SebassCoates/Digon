node root() {
        [1,2,3,4,5,6,7,8,9,10] => (initialize_data);
}

node initialize_data(data) {
        data => (mean) => (print_data);
        data => (median) => (print_data);
        data => (mode) => (print_data);
}

node mean(data) {
        mean => (child);
}

node median(data) {
        median => (child);
}

node mode(data) {
        mode => (child);
}

node print_data(average, median, mode) {
        average => (print);
        median => (print);
        mode => (print); 
}
