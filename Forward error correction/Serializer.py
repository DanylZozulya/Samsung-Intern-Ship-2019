import unittest


class Packets_Serializer():
    def __init__(self, packet_len, word_size, data_packet, reduntant_packet):
        self.packet_length = packet_len
        self.words_size = word_size
        self.data = data_packet
        self.reduntant = reduntant_packet
        self.packet_size = packet_len * word_size
        self.filename = ''
        self.point = None
        self.buffer = b''
        self.position = 0
        self.mode = 's'
        self.datalist = []
        self.redlist = []

    def open_file(self, filename, mode):
        self.filename = filename
        self.file = open(filename, mode)

    def take_point(self, point):
        self.point = point
        point.filename = (self.filename[:self.filename.index('.')] + '1' + self.filename[self.filename.index('.'):])

    def read_file(self):
        data = self.file.read(self.packet_size)
        if len(data) <= self.packet_size:
            if len(data) != self.packet_size:
                for i in range(self.packet_size - len(data)):
                    data += bytes([0])
        if self.mode == 'r' and self.position == (self.reduntant - 1):
            self.file.close()
        self.buffer = data

    def send_to_buffer(self):
        self.point.send_buffer = self.send_buffer
        self.buffer = b''

    def serialize(self):
        if not self.buffer:
            raise Exception('Buffer is empty')
        if self.mode == 's':
            self.send_buffer = bytes([0]) + bytes([self.position]) + self.buffer + bytes([self.packet_size])
        else:
            self.send_buffer = bytes([255]) + bytes([self.position]) + self.buffer + bytes([self.packet_size])
        if self.position == (self.data - 1):
            self.position = 0
            self.mode = 'r'
        else:
            self.position += 1

    def deserialize(self):
        self.buffer = self.send_buffer[2:self.packet_size + 2]
        self.position = self.send_buffer[1]
        if self.send_buffer[0] == 255:
            self.mode = 'r'
            self.redlist.append(self.position)
        else:
            self.datalist.append(self.position)

    def write_to_file(self):
        self.file.write(self.buffer)
        if (self.mode == 'r' and self.position == (self.reduntant - 1)):
            self.file.close()

class TestSerializer(unittest.TestCase):
     def test1(self):
         file = open('test.txt', 'w')
         file1 = open('test1.txt', 'w')
         file.write(5 * 'data' + 4 * 'test')
         file.close()
         file1.close()
         data = Packets_Serializer(1, 4, 5, 4)
         reads = Packets_Serializer(1, 4, 5, 4)
         data.open_file('test.txt', 'rb')
         reads.open_file('test1.txt', 'wb')
         data.take_point(reads)
         for i in range(9):
             data.read_file()
             data.serialize()
             data.send_to_buffer()
             reads.deserialize()
             reads.write_to_file()
         reads.open_file('test1.txt', 'r')
         res = reads.file.read()
         reads.file.close()
         self.assertEqual((reads.datalist,reads.redlist,res),([0,1,2,3,4],[0,1,2,3],5 * 'data' + 4 * 'test'))

if __name__=='__main__':
    unittest.main()