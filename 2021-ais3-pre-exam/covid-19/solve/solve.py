a = [0x41, 0x48, 0x51, 0x30, 0x7f, 0x30, 0x31, 0x33, 0x71, 0x56, 0x62, 0x3b, 0x61, 0x3e, 0x72, 0x78, 0x23, 0x25, 0x60, 0x4c, 0x79, 0x21, 0x23, 0x7c, 0x65]

flag = ''.join(chr(i ^ j) for i, j in enumerate(a))

assert(flag == 'AIS3{574y_h0m3|w34r_m45k}')
