node root {
        x := 5;
        x = 6;
        y := 11;
        y = 5;
        z := 0;
        array := [10]int{1,2,3,4,5,6,7,8,9,10}; 
        array2 := [10]byte;
        str := "hello world";

        x => addTwo(f) => println();
        y => addTwo(g) => println();
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
        q := f + g + 2;
        q => dest();
} 