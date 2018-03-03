package main

import (
	"fmt"
)

func main() {
	array := [10]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	calculate_stats(array)
}

func calculate_stats(array [10]int) {
        channel := make(chan int)
	mean(array, channel)
}

func mean(array [10]int, channel chan int) {
        medChannel := make(chan int)
        modeChannel := make(chan int)
	go median(array, medChannel)
	go mode(array, modeChannel)

	var average float64 = 0.0
	for _, elem := range array {
		average += float64(elem)
	}
	average /= float64(len(array))

	print_array(average, <-medChannel, <-modeChannel)
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

func print_array(average float64, median int, mode int) {
	fmt.Printf("The average is %f\n", average)
	fmt.Printf("The median is %d\n", median)
	fmt.Printf("The mode is %d\n", mode)
}
