#png being interacted with must be in same folder/directory
import os,argparse
dir_path = os.path.dirname(os.path.realpath(__file__))

def buildFilePath(dir_path,file):
        name = dir_path+'\\'+file
        return name

def checkSignature(signature):
    if signature == b'\x89PNG\r\n\x1a\n':
        print("PNG signature is intact")
        return signature
    else:
        print("PNG signature is damaged, restoring signature")
        signature = b'\x89PNG\r\n\x1a\n'
        return signature

def checkIHDR(ihdrBlock):
    if ihdrBlock == b'\x49\x48\x44\x52':
        print("IHDR block is intact")
        return ihdrBlock
    else:
        print("IHDR block is damaged, restoring IHDR block")
        ihdrBlock = b'\x49\x48\x44\x52'
        return ihdrBlock
    
def checkIEND(iendBlock):
    if iendBlock == b'\x49\x45\x4E\x44':
        print("IEND block is intact")
        return iendBlock
    else:
        print("IEND block is damaged, restoring IEND block")
        iendBlock = b'\x49\x45\x4E\x44'
        return iendBlock
    
parser = argparse.ArgumentParser(description="Basic png repair tool, Please note PNG being interacted with must be in the same directory")
parser.add_argument("inFile",metavar ='inFile', help="input file i.e example.png")
args = parser.parse_args()
inputFile = args.inFile

with open(buildFilePath(dir_path,inputFile), "rb") as in_file:
    sig = in_file.read(8)                            
    new_sig=checkSignature(sig)
    header = in_file.read(4)                         
    ihdr = in_file.read(4)                           
    new_ihdr = checkIHDR(ihdr)                       
    rest_of_bytes = in_file.read()[:-8]
    iend_block = in_file.read(4)
    new_iend = checkIEND(iend_block)
    end = in_file.read()                   

with open(buildFilePath(dir_path,inputFile.strip(".png")+"-fix.png"), "wb") as out_file:
    out_file.write(new_sig)
    out_file.write(header)
    out_file.write(new_ihdr)
    out_file.write(rest_of_bytes)
    out_file.write(new_iend)
    out_file.write(end)
    print("Repaired PNG has been written to :   "+buildFilePath(dir_path,inputFile.strip(".png")+"-fix.png"))
