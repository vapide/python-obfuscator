import obfuscate

filename = 'obfuscated'
code = (
'''
input('hi')
x = 5
'''
)

obfuscate.obfuscate(filename, code, clearvars = True)
