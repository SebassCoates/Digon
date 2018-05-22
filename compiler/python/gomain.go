package main

import "fmt"

func main() {
array:=[10]int{1,2,3,4,5,6,7,8,9,1}
;
calculate_stats(array);
}

func calculate_stats(data [ 10 ] int) {
meanChannel := make(chan float64)
go mean(data, meanChannel);
medianChannel := make(chan int)
go median(data, medianChannel);
modeChannel := make(chan int)
go mode(data, modeChannel);

print_data(meanChannel, medianChannel, modeChannel);

}

func mean(data1 [ 10 ] int, channel chan float64) {
average:=0.0;
for _,elem := range data1{
average+=float64(elem);
}
length:=0;
length = len(data1);
channel<-average/float64(length);
}

func median(data2 [ 10 ] int, channel chan int) {
length:=0;
length = len(data2);
for i,_ := range data2{
for j:=i;
j>1;
j--{
if data2[j]<data2[j-1]{
temp:=data2[j-1];
data2[j-1]=data2[j];
data2[j]=temp;
}else{
break;
}
}
}
channel<-data2[length/2];
}

func mode(data3 [ 10 ] int, channel chan int) {
m:=make(map[int]int);
for _,elem := range data3{
_,valid:=m[elem];
if !valid{
m[elem]=1;
}else{
m[elem]+=1;
}
}
highest:=0;
mode:=0;
for key,value := range m{
if value>highest{
mode=key;
highest=value;
}
}
channel<-mode;
}

func print_data(average1chan chan float64 , median1chan chan int , mode1chan chan int ) {
average1 := <- average1chan;
median1 := <- median1chan;
mode1 := <- mode1chan;
fmt.Println(average1);
fmt.Println(median1);
fmt.Println(mode1);
}

