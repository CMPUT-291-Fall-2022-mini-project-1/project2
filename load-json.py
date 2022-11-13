import sys
import os


def insert_data(filename:str, port:str) -> None:
    cmd_str = f"mongoimport --port {port} --db 291db --collection dblp --drop --batchSize 15000 --file {filename}"
    os.system(cmd_str)
    pass



def main() -> None:
    filename:str = input('file name: ')
    port:str = input('port: ')
    insert_data(filename,port)

if __name__ == "__main__":
    main()