from Vandermonde_matrix import make_vandermonde,matrix_mult,inverse_matrix
from Serializer import Packets_Serializer
from Channel_Model import channel_model
from Encoder import Encoder
import unittest

class Decoder():
    def __init__(self,filename):
        self._filename = filename
        self.file = open(filename,'wb')

    def open_recievedfile(self,reciever):
        self.reciever = reciever
        self.reciever.file = open(self.reciever.filename,'rb')

    def decode(self):
        vandermonde_matrix = make_vandermonde(self.reciever.data,self.reciever.reduntant)
        datasize = self.reciever.data
        matrix_e = [[0] * i + [1] + [0] * (datasize - i - 1) for i in range(datasize)]
        dec_matrix = []
        for i in self.reciever.datalist:
            dec_matrix.append(matrix_e[i])
        for i in self.reciever.redlist:
            if len(dec_matrix) < self.reciever.data:
                dec_matrix.append(vandermonde_matrix[i])

        if len(dec_matrix) < self.reciever.data:
            print('Not enough received packets')
        else:
            inv_dec_matrix = inverse_matrix(dec_matrix)
            S = []
            recsize = 0
            while True:
                tmp = self.reciever.file.read(self.reciever.word_size)
                S.append(list(tmp))
                recsize += 1
                if recsize == datasize:
                    break
            print(S)
            res_matrix = matrix_mult(inv_dec_matrix,S)
            for i in range(len(res_matrix)):
                self.file.write(bytes(res_matrix[i]))
            self.file.close()




class TestAll(unittest.TestCase):
    def test1(self):
        tmp = open('data.txt', 'w')
        file = open('dataencoded.txt', 'w')
        file1 = open('dataencoded1.txt', 'w')
        tmp.write(5 * 'data' + 4 * 'test')
        tmp.close()
        file.close()
        file1.close()
        encode = Encoder(1,4,6,4)
        encode.open_file('data.txt','rb')
        encode.read_file()
        encode.encode()
        encode.write_to_file()
        data = Packets_Serializer(1,4,6,4)
        reads = Packets_Serializer(1,4,6,4)
        data.open_file('dataencoded.txt','rb')
        data.take_point(reads)
        reads.open_file(reads.filename,'wb')
        channel = channel_model(0.004,0.6)
        value = data.data + data.reduntant
        tmp = 1
        for i in channel:
            data.read_file()
            data.serialize()
            if i:
                data.send_to_buffer()
                reads.deserialize()
                reads.write_to_file()
            if tmp == value:
                channel.close()
                data.file.close()
                reads.file.close()
            tmp += 1
        decode = Decoder('tempdecoded.txt')
        decode.open_recievedfile(reads)
        decode.decode()
if __name__=='__main__':
    unittest.main()
