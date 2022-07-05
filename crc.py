class CRCalc:
    def __init__(self) -> None:
         pass

    def calc_crc(self, payload):
            '''
            Calculates 16-bit CRC-CCITT
            '''
            crc = 0x1D0F
            for bytedata in payload:
                crc = crc ^ (bytedata << 8)
                i = 0
                while i < 8:
                    if crc & 0x8000:
                        crc = (crc << 1) ^ 0x1021
                    else:
                        crc = crc << 1
                    i += 1

            crc = crc & 0xffff
            crc_msb = (crc & 0xFF00) >> 8
            crc_lsb = (crc & 0x00FF)
            return [hex(crc_msb), hex(crc_lsb)]

    def run(self):
        payload = b''
        payload_bytes = input('input payload:')
        payload_str = f'{payload_bytes}'
        payload_str = payload_str.split(' ')
        for i in payload_str:
            byte_data = bytes.fromhex(i)
            payload += byte_data
        crc_lst = self.calc_crc(payload)
        fst_crc = crc_lst[0][2:4]
        sec_crc = crc_lst[0][2:4]
        print(f'CRC: {fst_crc} {sec_crc}')

if __name__ == '__main__':
    crc = CRCalc()
    crc.run()