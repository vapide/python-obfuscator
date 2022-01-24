import obfuscate

filename = 'obfuscated'
code = (
'''
input('hi')
'''
)

obfuscate.obfuscate(filename, code, clearvars = True)
