package main

import (
	"fmt"
	"net"
)

func main() {
	coon, err := net.Dial("tcp", "144.76.43.242:7782")
	fmt.Println(err)
	defer coon.Close()
	fmt.Println(coon)
	respBuff := make([]byte, 1024)
	n, err := coon.Read(respBuff)
	fmt.Println(err)
	fmt.Print(string(respBuff[:n]))
	for {
		for n != 0 {
			fmt.Print(string(respBuff[:n]))
			n, _ = coon.Read(respBuff)
		}
		n, _ = coon.Read(respBuff)
	}
}
