def addition(a,b):
    return a ^ b

def subtraction(a,b):
    return a ^ b


prim_poly_8 = 0x11d
gf_elements = 1 << 8
gflog = [0] * gf_elements
gfilog = [0] * gf_elements
c = 1
for i in range(0, gf_elements - 1):
    gflog[c] = i
    gfilog[i] = c
    c <<= 1
    if c & gf_elements:
        c = c ^ prim_poly_8


def mult(a,b):

    NW = 2 ** 8
    if a == 0 or b == 0:
        return 0
    sum_log = gflog[a] + gflog[b]
    if sum_log >= NW - 1:
        sum_log -= NW - 1
    return gfilog[sum_log]


def divis(a , b):

    NW = 2 ** 8
    if a == 0:
        return 0
    if b == 0:
        return ZeroDivisionError
    diff_log = gflog[a] - gflog[b]
    if diff_log < 0:
        diff_log += NW - 1
    return gfilog[diff_log]
