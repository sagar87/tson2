
NUC = ['A', 'C', 'G', 'T']
SUB = ['[C>A]', '[C>G]', '[C>T]', '[T>A]', '[T>C]', '[T>G]']
SNV = [ a+b+c for b in SUB for a in NUC for c in NUC]