# Samsung-Intern-Ship-2019

Implementation of forward error correction based on Galois field arithmetic, Reed-Solomon codes. Testing on audio files.

Forward Error Correction is a technique of error-correcting coding and decoding that allows to correct errors by the proactive method. It is used to correct failures and errors in data transmission by transferring redundant service information, on the basis of which the original content can be restored.

To work with information when encoding and decoding data, all arithmetic operations are performed in Galois fields. Polynomial arithmetic or arithmetic of Galois fields is applied so that the result of any operation is also an element of this field.

The Reed-Solomon code over GF(q^m), which corrects t errors, requires 2t check characters and with it corrects arbitrary bursts of errors of length t or less. Reed-Solomon codes are optimal in terms of packet length and error correction capability - using 2t extra check characters to correct t errors (or less).

![alt text](Samsung-Intern-Ship-2019/Forward error correction/Схема_применения_кода_Рида-Соломона.gif)
