from bottle import run, get, put
import json
import hashlib

# BUGLIST
# - insercao da mesma chave 2 vezes, possibilita inserir o mesmo par de chave/valer em posicoes diferentes da DHT
# - necessario cria uma maneira para inicializar a DHT, a partir de uma chave inicial
# - necessario implementar comunicacao em grupo, e propagar os inserts e lookups

def subkeys(k):
    for i in range(len(k), 0, -1):
        yield k[:i]
    yield ""


class DHT:
    def __init__(self, k):
        self.k = k
        self.h = {}

        for sk in subkeys(self.k):
            self.h[sk] = None

    def insert(self, k, v):
        for sk in subkeys(k):
            if sk in self.h:
                if not self.h[sk]:
                    self.h[sk] = (k, v)
                    return sk
                else:
                    return None #se o primeio match que eu achar na DHT estiver ocupado, já retorna null. Assim não é possível inserir dois iguais 
        return None

    def lookup(self, k):
        print(list(subkeys(k)))
        for sk in subkeys(k):
            print(sk)
            print(self.h)
            if sk in self.h:
                if self.h[sk]:
                    (ki, vi) = self.h[sk]
                    if ki == k:
                        return vi
        return None

    def __repr__(self):
        return "<<DHT:"+ repr(self.h) +">>"


prt = 8080

def ValorHash(value):
	InitKey = hashlib.md5()
	InitKey.update(str(value).encode('utf-8'))
	txtCru = InitKey.hexdigest()
	txt = ""
	for i in txtCru:
		txt = txt + str(ord(i) % 4)
	return txt

#print (ValorHash(prt))
dht = DHT(ValorHash(prt)) # criar uma maneira de que para todo nó da rede seja diferente.


@get('/dht/<key>')
def dht_lookup(key):
    global dht
    return json.dumps(dht.lookup(ValorHash(key)))

@put('/dht/<key>/<value>')
def dht_insert(key, value):
    global dht
    return json.dumps(dht.insert(ValorHash(key), value))


run(host='localhost', port=prt)
