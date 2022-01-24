import obfuscate

filename = 'obfuscated'

code = (
'''
x="HELLO"
print(x)
'''
)

obfuscate.obfuscate(filename, code, compile = True, clearvars = True)
