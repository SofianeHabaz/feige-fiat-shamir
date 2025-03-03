import socket
import random
from mod_operations import square_ZnZ
from shared_hash_function import hash_to_bit_vector

class ffs_verifier:
    def __init__(self,n,k,t):
        self.n=n
        self.k=k
        self.t=t
        self.started=False
    
    def listen(self,port):
        self.sersock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sersock.bind(('127.0.0.1',port))
        self.sersock.listen(1)
        conn = self.sersock.accept()[0].makefile(mode="rw")
        
        while True:
            data=conn.readline()
            if data=="PKA\n":
                conn.write("OK PKA\n")
                conn.flush()
                self.handle_advertisment(conn)
            elif data=="START\n":
                conn.write("OK START "+str(self.t)+"\n")
                conn.flush()
                self.started=True
            elif data=="COMMIT\n":
                if (self.pub_key is None) or not (self.started):
                    conn.write("No public key registered for this connection\n")
                    conn.flush()
                    print("No pub key...")
                else:
                    conn.write("OK COMMIT\n")
                    conn.flush()
                    self.handle_challenge(conn)
            elif data=="DIE\n":
                conn.close()
                break
        
    def handle_advertisment(self,sock):
        pub_key_as_string=sock.readline()
        print("Received public key: "+pub_key_as_string)
        self.pub_key = list(map(int,pub_key_as_string.split()))
        
    def handle_challenge(self,sock):
        x=int(sock.readline())
        print("Prover commited to: "+str(x))
        b=hash_to_bit_vector(X=x, bit_length=self.k)
        sock.write("\n")
        sock.flush()
        y=int(sock.readline())
        expected_x=square_ZnZ(y,self.n)
        for i in range(0,self.k):
            if b[i]:
                expected_x*=self.pub_key[i]
        expected_x = expected_x%self.n
        if (expected_x==x):
            print("Challenge correctly completed!\n")
        else:
            print("Failure in challenge")