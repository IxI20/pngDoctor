"""!!File called must be in same directory!!"""
from os.path import dirname, join, realpath
from argparse import ArgumentParser
from zlib import crc32

class PNG_Check:
    def __init__(self, file):
        self.dir_path = dirname(realpath(__file__))  # Get path/directory python file is called in
        self.file_path = join(self.dir_path, file)  # Append provided file name to path
        self.new_file_path = self.file_path.removesuffix(".png") + "-fix.png"  # File path for repaired file
        self.expected_chunks = [b'\x89PNG\r\n\x1a\n',  # File signature
                                b'\x00\x00\x00\x0D',  # IHDR Length
                                b'\x49\x48\x44\x52',  # IHDR signature
                                b'\x00\x00\x00\x00',  # IEND Length
                                b'\x49\x45\x4E\x44',  # IEND Signature
                                b'\x49\x45\x4E\x44']  # IEND crc
        self.chunk_names = ['File signature',
                            'IHDR length',
                            'IHDR signature',
                            'IEND length',
                            'IEND signature',
                            'IEND CRC-32 value']  # Chunk names
        self.file_chunks = []  # List to hold chunks for repair
        self.GREEN, self.RED, self.RESET = "\033[32m", "\033[31m", "\033[0m"  # ANSI codes for message colours

    def get_chunks(self):
        try:
            with open(self.file_path, "rb") as file:
                self.file_chunks.append(file.read(8))  # File signature chunk
                self.file_chunks.append(file.read(4))  # IHDR Length
                self.file_chunks.append(file.read(4))  # IHDR Signature
                self.ihdr_data = file.read(13)  # IHDR data
                self.ihdr_crc = file.read(4)  # IHDR crc-32 value
                self.rest_of_bytes = file.read()[:-12]  # Everything but IEND
                self.file_chunks.append(file.read(4))  # IEND length
                self.file_chunks.append(file.read(4))
                self.file_chunks.append(file.read(4))
        except FileNotFoundError:
            print(f"{self.RED}Error: File not found{self.RESET}")
            exit(1)
        return self  # Return self for function chaining

    def check_chunks(self):
        for i in range(len(self.expected_chunks)):
            if i == 3:
                expected_crc = crc32(self.file_chunks[i-1] + self.ihdr_data)
                if int.from_bytes(self.ihdr_crc, 'big') == expected_crc:
                    print(f"{self.GREEN}IHDR CRC-32 value field is intact{self.RESET}")
                else:
                    self.ihdr_crc = expected_crc.to_bytes(4, 'big')
                    print(f"{self.RED}IHDR CRC-32 value field is damaged, restoring{self.RESET}")

            if self.expected_chunks[i] == self.file_chunks[i]:
                print(f"{self.GREEN}{self.chunk_names[i]} field is intact{self.RESET}")
            else:
                print(f"{self.RED}{self.chunk_names[i]} field is damaged, restoring{self.RESET}")
                self.file_chunks[i] = self.expected_chunks[i]
        return self  # Return self for function chaining

    def write_chunks(self):
        with open(self.new_file_path, "wb") as file:
            file.write(self.file_chunks[0])  # Signature chunk
            file.write(self.file_chunks[1])  # IHDR Length
            file.write(self.file_chunks[2])  # IHDR chunk
            file.write(self.ihdr_data)
            file.write(self.ihdr_crc)
            file.write(self.rest_of_bytes)  # Everything but IEND
            file.write(self.file_chunks[3])  # IEND chunk
            file.write(self.file_chunks[4])
            file.write(self.file_chunks[5])
        print(f"Repaired file written to {self.new_file_path}")
        return self  # Return self for function chaining


parser = ArgumentParser(description="Basic PNG repair tool. Please note PNG being interacted with must be in the same directory")
parser.add_argument("file", metavar='file', help="input file i.e example.png")
args = parser.parse_args()
PNG_Check(args.file).get_chunks().check_chunks().write_chunks()
