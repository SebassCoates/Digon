

node root() {
        initialize_data -> filename;
}

node initialize_data(file) {
        a = fileioHERE;

        mean -> a;
        median -> a;
        mode -> a;
}


node mean(a) {

        print_data.0 => val;
}

node median(a) {

        print_data.1 => val;
}

node mode(a) {

        print_data.2 => val;
}

node print_data(m, med, mod) {
        { print m; }
        { print med; }
        { print mod; }
        end;
}
