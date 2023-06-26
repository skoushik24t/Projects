import argparse
from time import gmtime, strftime
import os.path
import hashlib
import getpass


def stamp(mode=0):
    # 0 = info
    # 1 = warn
    # 2 = error
    msg = "INFO"
    if mode == 0:
        msg = "INFO"
    elif mode == 1:
        msg = "WARN"
    elif mode == 2:
        msg = "ERRO"
    return strftime("[" + msg + " %H:%M:%S" + "]")


def getpasswordhash():
    m = hashlib.md5()
    print(stamp(), "Prompting user for password")
    pwd = getpass.getpass()
    m.update(pwd.encode('utf-8'))
    return m.hexdigest()


def stringtobinary(txt):
    out = ""
    for c in list(txt):
        tmp = bin(ord(c))[2:]
        out += "0" * (8 - len(tmp)) + tmp
    return out


def bytexor(a, b):
    '''
    0   0   0
    0   1   1
    1   0   1
    1   1   0
    '''
    return a ^ b


def main():
    print(stamp(), "Initiating")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input Filename which will be either encrypted or decrypted", type=str)
    args = parser.parse_args()
    if args.input:
        print(stamp(), "Searching for the file", args.input)
        if os.path.isfile(args.input):
            print(stamp(), "The file", args.input, "Found")
            password = getpasswordhash()
            num = 0
            target = args.input
            print(stamp(), "Opening file", args.input)
            file_op = open(target, "r+b")
            loop = True
            print(stamp(), "Encrypting/Decrypting Initiated")
            while loop:
                temp_read = file_op.read(1)
                if temp_read != b"":
                    file_op.seek(file_op.tell() - 1)
                    xored = bytexor(temp_read[0], ord(password[file_op.tell() % len(password)]))
                    file_op.write(bytes([xored]))
                else:
                    loop = False

            file_op.close()
            print(stamp(), "Encrypting/Decrypting Completed")
            print(stamp(), "Exiting program")
            return
        else:
            print(stamp(2), "The file", args.input, "was not found")
            print(stamp(), "Exiting program")
            return
    else:
        print(stamp(2), "No input file is provided")
        print(stamp(), "Exiting Program")
        return


if __name__ == "__main__":
    main()
