#!/usr/bin/env python

import wave
import sys

fp = wave.open(sys.argv[1])
print fp.getparams()
