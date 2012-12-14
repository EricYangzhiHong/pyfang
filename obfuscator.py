#!/usr/bin/python

class Obfuscator:
    """ Handles various types of obfuscation.
        Currently only encodes in hex or pads to avoid a MS IIS error
    """

    def __init__(self):
        self.params = ''
        self.pad_length = 2048

    def by_encoding(self, string, encoding):
        """ Takes a string as input and returns that string in the given encoding.
            :string: String to convert.
            :encoding: Chosen encoding for string. Currently hex is supported.
            :returns: String. Input string encoded in correct encoding.
        """
        if encoding == 'hex-individual':
            return '0x' + '0x'.join([i.encode('hex') for i in list(string)])
        elif encoding == 'hex':
            return '0x' + ''.join([i.encode('hex') for i in list(string)])
        else:
            return string

    def by_padding(self, string, pad):
        """ Takes string to obfuscate and padding character to obfuscate with.
            Some versions of MS IIS and other database servers will turn long queries into
            '...' inside logs, so padding can avoid detection.
            :string: String to pad.
            :pad: String. Character or string to pad with.
            :returns: String. Padded input.
        """

        return (pad * self.pad_length) + string



