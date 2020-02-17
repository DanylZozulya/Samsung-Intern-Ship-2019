from Vandermonde_matrix import make_vandermonde,matrix_mult
from Serializer import Packets_Serializer
from Channel_Model import channel_model

class Encoder():
    def __init__(self,packet_len,word_size,data_packet,reduntant_packet):
        self.packet_length = packet_len
        self.word_size = word_size
        self.data = data_packet
        self.reduntant = reduntant_packet
        self.packet_size = packet_len * word_size
        self.filename = ''

    def open_file(self,filename,mode):
        self.filename = filename
        self.file = open(filename,mode)

    def read_file(self):
        tmp = []
        while True:
            reads = self.file.read(self.packet_size)
            if reads == b'':
                self.file.close()
                break
            tmp.append(list(reads))
        self.buffer = tmp

    def encode(self):

        van_matrix = make_vandermonde(self.reduntant, self.data)
        self.buffer += matrix_mult(van_matrix,self.buffer)

    def write_to_file(self):
        self.open_file('encoded' + self.filename[:self.filename.index('.')] + self.filename[self.filename.index('.'):],'wb')
        for i in range(len(self.buffer)):
            self.file.write(bytes(self.buffer[i]))
        self.file.close()

if __name__=='__main__':
    encode = Encoder(1,4,6,3)
    encode.open_file('test.txt','rb')
    encode.read_file()
    encode.encode()
    encode.write_to_file()
    data = Packets_Serializer(1,4,6,3)
    reads = Packets_Serializer(1,4,6,3)
    data.open_file('test.txt','rb')
    data.take_point(reads)
    reads.open_file(reads.filename,'wb')
    channel = channel_model(0.005,0.5)
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
    print(reads.datalist)
    print(reads.redlist)