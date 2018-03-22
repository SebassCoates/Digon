package main

import (
	"fmt"
)

func main() {
	array := [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	calculate_stats(array)
}

func calculate_stats(array [10]int) {
    meanChannel := make(chan float64)
    medChannel := make(chan int)
    modeChannel := make(chan int)
    go mean(array, meanChannel)
    go median(array, medChannel)
    go mode(array, modeChannel)
    print_array(meanChannel, medChannel, modeChannel)
}

func mean(array [10]int, channel chan float64) {
	var average float64 = 0.0
	for _, elem := range array {
		average += float64(elem)
	}
	average /= float64(len(array))

    channel <- average
}

func median(array [10]int, channel chan int) {
    for i := 0; i < len(array); i++ {
            for j := i; j > 1; j-- {
                   if array[j] < array[j - 1] {
                            temp := array[j -1]
                            array[j - 1] = array[j]
                            array[j] = temp
                   } else {
                           break
                   }
            }
    }
    length := len(array)
	channel <- array[length / 2]
}

func mode(array [10]int, channel chan int) {
    m := make(map[int]int)

    for _, elem := range array {
            _, valid := m[elem]
            if !valid {
                    m[elem] = 1
            } else {
                    m[elem] += 1
            }
    }

    highest := 0
    mode := 0
    for key, value := range m {
            if value > highest {
                    mode = key;
                    highest = value;
            }
    }

    channel <- mode
}

func print_array(meanChannel chan float64, medChannel chan int, modeChannel chan int) {
	fmt.Printf("The average is %f\n", <-meanChannel)
	fmt.Printf("The median is %d\n", <-medChannel)
	fmt.Printf("The mode is %d\n", <-modeChannel)
}
