from random import randrange

def channel_model(p, q):
    state = True
    while True:
        x = randrange(0,1)
        if state and x < p:
            state = False
        elif not state and x < q:
            state = True
        yield state



def noise(filename, points):

    file_1 = open(filename, 'rb')
    pos = filename.rfind('.')
    file_2 = open(filename[:pos] + '_noised' + filename[pos:], 'wb')

    for i in channel_model(*points):
        info = file_1.read(2)
        if info:
            if not i:
                file_2.write(bytes([randrange(0, 256) for j in range(2)]))
            else:
                file_2.write(info)
        else:
            break

    file_1.close()
    file_2.close()

lost_1 = (0.005, 0.4993)
lost_l5 = (0.034, 0.6555)
lost_10 = (0.08452, 0.7625)
lost_20 = (0.1866, 0.7455)

if __name__ == '__main__':
    noise('rain.mp3', lost_20)

