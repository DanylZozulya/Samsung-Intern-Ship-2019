from Zozulya_GFA import addition,mult,divis
import unittest

def power(x,n):
    if n == 0:
        return 1
    elif n == 1:
        return x
    else:
        for i in range(1,n):
            x = mult(x,x)
        return x


def make_vandermonde(columns,lines):
    matrix = []
    for i in range(lines):
        matrix.append([])
        for j in range(columns):
            matrix[i].append(power(i + 1, j))
    fix_matrix = [[matrix[j][i] for j in range(lines)] for i in range(columns)]
    return fix_matrix

"Функції adj та det реалізовані для пошуку оберненої матриці"

def adj(matrix,a,b):
    return [[matrix[i][j] for i in (list(range(a-1))+list(range(a,len(matrix))))]
            for j in (list(range(b-1))+list(range(b,len(matrix[0]))))]

def det(matrix):
    if (len(matrix) == 2) and (len(matrix[0]) == 2):
        return addition(mult(matrix[0][0], matrix[1][1]), mult(matrix[0][1], matrix[1][0]))
    else:
        res = [matrix[0][j] for j in range(len(matrix[0]))]
        value = 0
        for i in range(len(res)):
            value = addition(value,mult(res[i],det(adj(matrix,1,i+1))))

        return value

def sk_mult(a,b):
    c = 0
    for i in range(len(a)):
        c = addition(c,mult(a[i],b[i]))
    return c
def matrix_mult(m1,m2):
    ml = [[m2[i][j] for i in range(len(m2))] for j in range(len(m2[0]))]
    res = [[0 for i in range(len(m2[0]))] for j in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m1)):
            res[i][j] = sk_mult(m1[i],ml[j])
    return res

def inverse_matrix(matrix):
    "Пошук оберненої матриці ведеться за допомогою алгебраїчних доповнень: inv_matrix = adj(matrix)/det(matrix)"
    det_m = det(matrix)
    res = [[divis(det(adj(matrix,i+1,j+1)),det_m) for i in range(len(matrix))]for j in range(len(matrix))]
    return res

class TestVandermonde(unittest.TestCase):
    def test1(self):
        self.assertEqual(make_vandermonde([0,1,2,3],3,3),[[1,1,1],[1,2,3],[1,4,5]])
class Testinverse(unittest.TestCase):
    def test1(self):
        tmp = make_vandermonde([0,1,2,3],3,3)
        self.assertEqual(inverse_matrix(tmp),[[1,122,122],[1,245,244],[1,143,142]])
if __name__== '__main__':
    unittest.main()



