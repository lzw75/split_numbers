# split_numbers

First, we attempt to find m-digit numbers $a$, $b$, $c$ such that $(\overline{abc}) = (a+b+c)^3$, where $(\overline{abc})$ is the concatenation of the 3 numbers (i.e. a $3m$-digit number).

Next, we generalise this to the tasks of finding $(\overline{abcd}) = (a+b+c+d)^4$ and $(\overline{abcde}) = (a+b+c+d+e)^5$.

## Technique for Squares

Here is a brief description of the technique. For concreteness, we'll find 3-digit numbers $a$, $b$ such that $(\overline{ab}) = (a+b)^2$.

The equation becomes $1000a + b = (a+b)^2$; setting $N = a+b$ then gives us

$$999a + N = N^2 \implies N^2 - N \equiv 0 \pmod {999}.$$

Thus $N(N-1)$ is a multiple of $999 = 3^3 \times 37$. Thus we need to solve this congruence relation. One solution involves setting $N \equiv 1 \pmod {3^3}$ and $N \equiv 1 \pmod {37}$, thus giving us $N \equiv 703 \pmod {999}$.

*But why is this sufficient?*

Indeed, suppose conversely we have a 3-digit number $N$ such that $N(N-1)$ is divisible by 999. Let us set $a = \frac{N(N-1)}{999}$. Then we have

$$a = \frac{N(N-1)}{999} \le \frac{N(N-1)}N = N-1$$

so $a \lt N$ and we can define $b=N-a$. Now $a$ and $b$ are 3-digit numbers summing up to $N$ such that $1000a + b = 999a + N = N^2$.

## General Case

The case for cubes and higher powers are similar. To illustrate, let us take 4-digit $a$, $b$, $c$ such that $10^8 a + 10^4 b + c = (a+b+c)^3$. As before, set $N = a+b+c$ so that we get

$$N^3 - N = (10^8 - 1)a + (10^4 - 1)b = 9999(10001a + b).$$

Again we try to solve for $N^3 - N \equiv 0 \pmod {9999}$. Why does this suffice? Well, suppose we have a 4-digit solution for $N$. Set $s = \frac{N^3 - N}{9999}$ as before. We wish to express $s = 10001a + b$. Since $s$ is an 8-digit number, our choices for 4-digit $a$ and $b$ are pretty much forced. The problem now is that we may have $a + b > N$, in which case we cannot set $c = N - (a+b)$. Otherwise, it'd work.

Same reasoning works for 4th and 5th powers.

