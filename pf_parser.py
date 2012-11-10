#!/usr/bin/python
"""
    Parses data gleaned from injections.

"""

# Takes dictionary of lists:
#   keys are injected SQL strings.
#   values are data leaked from injection.
def parse(data):

    for key in data:
        print key, data[key]
        print



    # Thinking at the moment of parsing in many different ways and taking the most common intersection as the answer.

