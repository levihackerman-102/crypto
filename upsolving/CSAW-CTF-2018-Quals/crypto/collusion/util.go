package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/big"
)

func main() {
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	bobRaw, err := ioutil.ReadFile("bobs-key.json")
	if err != nil {
		log.Fatal(err)
	}
	bobsKey := &Decrypter{}
	if err := json.Unmarshal(bobRaw, bobsKey); err != nil {
		log.Fatal(err)
	}
	b, _ := DecrypterId("Bob", bobsKey.N)
	fmt.Println(b)

	carolRaw, err := ioutil.ReadFile("carols-key.json")
	if err != nil {
		log.Fatal(err)
	}
	carolsKey := &Decrypter{}
	if err := json.Unmarshal(carolRaw, carolsKey); err != nil {
		log.Fatal(err)
	}
	c, _ := DecrypterId("Carol", carolsKey.N)
	fmt.Println(c)

	a, _ := DecrypterId("Alice", bobsKey.N)
	fmt.Println(a) 
}

func decrypt(d, N *big.Int, p *Payload) (string, error) {
	K := new(big.Int).Exp(p.V, d, N)
	shared := sha256.Sum256(K.Bytes())

	block, err := aes.NewCipher(shared[:])
	if err != nil {
		return "", err
	}
	ciph, err := cipher.NewGCM(block)
	if err != nil {
		return "", err
	}
	message, err := ciph.Open(nil, p.Nonce, p.Body, nil)
	if err != nil {
		return "", err
	}

	return string(message), nil
}