import obfuscate

filename = 'obfuscated'
code = (
'''
input('hi')
'''
)


























code += '\nsys.modules[__name__].__dict__.clear()'
obfuscate.obfuscate(filename, code)