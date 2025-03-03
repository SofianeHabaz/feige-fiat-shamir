import random

# Calculates the inverse of p in Z/nZ using Bézout's algorithm
def inverse(p, n):
    (r, u, v, r1, u1, v1) = (p, 1, 0, n, 0, 1)
    
    while r1 != 0:
        q = r // r1  # Integer division
        (r, u, v, r1, u1, v1) = (r1, u1, v1, r - q * r1, u - q * u1, v - q * v1)
    
    # Check if the inverse exists (it exists if gcd(p, n) = 1)
    if r != 1:
        raise ValueError(f"No inverse for {p} modulo {n}")
    
    return u % n



def coin_flip():
    if random.randint(0,1) == 1:
        return 1
    else:
        return -1

#Returns m^2 mod n
def square_ZnZ(m,n):
    return (m*m)%n