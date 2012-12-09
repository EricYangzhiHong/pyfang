#!/usr/bin/python
""" 
    

"""

# Takes string of ASCII chars, encodes in chosen encoding.
def encode(string, encoding):
    if encoding == 'hex-individual':
        return '0x' + '0x'.join([i.encode('hex') for i in list(string)])
    elif encoding == 'hex':
        return '0x' + ''.join([i.encode('hex') for i in list(string)])
    else:
        return string

if __name__ == '__main__':
    print encode("<>/", 'hex')

