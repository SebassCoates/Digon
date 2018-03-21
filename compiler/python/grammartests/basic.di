node root {
        x := 5;
        x = 6;
        y := 11;
        y = 5;
        z := 0; 
}

node takesParams <= (a [10]int, b char, c[][5]byte) {
        a = 5;
        d := 5;

        for i, elem in a {
                for (j) in elem {
                        d = 13;
                }
        }
}

node addTwo <= (f int, g int) {

}