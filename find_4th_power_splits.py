from random import randint

# Program to find m-digit numbers a, b, c, d such that (abcd) = (a+b+c+d)^4,
# where LHS refers to concatenation of a, b, c, d.

m = 15

# Simple probabilistic primality test.

def is_prime(n):
   small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
   if n <= 1: return False
   if n in small_primes: return True
   for p in small_primes:
      if n % p == 0: return False
      
   for p in small_primes:
      a = pow(p, (n-1)//2, n)
      if a != 1 and a != n-1: return False
      
   return True

   
# Take gcd of two positive integers.

def gcd(a, b):
   while b:
      a, b = b, a%b
   return a
   
   
# Factor n into primes, if possible. Otherwise, leave the big factors out.
# Will only run for n = 10^m - 1

def try_pollard_rho(n):
   a1 = a2 = 2
   prod = 1
   
   #print("Running Pollard rho")
   for i in range(10000):
      a1 = (a1 * a1 + 3) % n
      a2 = (a2 * a2 + 3) % n
      a2 = (a2 * a2 + 3) % n
      prod *= (a2 - a1)
      prod %= n
      
      if i % 50 == 0:
         g = gcd(prod, n)
         if g > 1:
            return g
   
   return 1

   
def factor(n):
   ans = []
   for p in range(2,1000):
      power = 0
      while n % p == 0: 
         n //= p
         power += 1
         
      if power: 
         ans += [(p, power)]
         if is_prime(n):
            ans += [(n, 1)]
            n = 1
            break
         
      if n < p*p: 
         if n > 1:
            ans += [(n, 1)]
            n = 1
         break
   
   
   while n > 1:
      ans2 = try_pollard_rho(n)
      if ans2 == 1: break
      ans += [(ans2, 1)]
      n //= ans2
   
   if n > 1:
      ans += [(n, 1)]

   return ans


# Sanity check for prime factors.

def check_factors(n, factors):
   prod = 1
   for (p, pwr) in factors:
      prod *= p ** pwr
   assert n == prod

   
# Inverse modulo (copied from some site).

def mod_inv(a, m):
    m0, x ,y = m, 1, 0
    
    if (m == 1): return 0
 
    while (a > 1):
 
        # q is quotient
        q = a // m
 
        t = m
 
        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y
 
        # Update x and y
        y = x - q * y
        x = t
 
    # Make x positive
    if (x < 0):
        x = x + m0
 
    return x
   
# Chinese remainder theorem: assume moduli all coprime.

def crt(remainders):
   a, n = 0, 1
   for b, m in remainders:
      
      # To solve x = a mod n, x = b mod m.
      
      y = mod_inv(m, n)
      y = ((a-b) * y) % n
      a, n = m*y + b, m*n
   
   return a, n

   
n = 10**m - 1
factors = factor(n)
check_factors(n, factors)
print(factors)


# Shanks-Tonelli algo: shamelessly copied from some site.

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r


def try_find(factors):
   crt_prob = []
   
   for p, pwr in factors:
      check_if_sq = p > 3 and legendre(-3, p) == 1 and pwr == 1
      
      x = randint(0, 1+check_if_sq)
      if x == 0:
         crt_prob.append([1, p**pwr])
      elif x == 1:
         crt_prob.append([0, p**pwr])
      else:
         r = tonelli(-3, p)
         if r % 2 == 1:
            r = (r-1)//2
         else:
            r = (r+p)//2
         crt_prob.append([r, p])
   
   ans, _ = crt(crt_prob)
   print(ans)
   pwr = ans**4
   w = pwr % (10**m)
   x = (pwr // (10**m)) % (10**m)
   y = (pwr // (10**(2*m))) % (10**m)
   z = pwr // (10**(3*m))
   print(pwr)
   print(z, y, x, w)
   outcome = (w >= 10**(m-1) and x >= 10**(m-1) and y >= 10**(m-1) and z >= 10**(m-1) and w+x+y+z == ans)
   print(outcome)
   if outcome:
      print("(%d + %d + %d + %d)**4 == %d" % (z, y, x, w, pwr))
      
   return outcome

   
while True:   
   outcome = try_find(factors)
   if outcome: break