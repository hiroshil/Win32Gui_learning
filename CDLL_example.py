from ctypes import CDLL
# https://stackoverflow.com/questions/75111235/libc-dll-file-is-missing-on-windows-10

crt = CDLL("msvcrt")
crt.printf(b"hello world")