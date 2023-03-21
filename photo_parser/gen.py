import json
from random import randrange, choice

def read_json_file(filename):
  with open(filename, 'r') as infile:
    return json.loads(infile.read())

def fmt(x, width):
  return f'''{'0'* (width - len(str(x)))}{x}'''

def gen_name():
  cams_spec = read_json_file('cams.json')
  cam = choice(cams_spec)
  if cam['spec'] == 6:
    return f'''{ cam['prefix'] }{ hex(randrange(13))[2:] }{ fmt(randrange(31), 2) }.jpg'''
  elif cam['spec'] == 6:
    strthou = fmt(randrange(3),2)
    return f'''{cam['prefix']}{strthou}-{strthou}.jpg'''
  name = cam['prefix']
  name += fmt(randrange(cam['range']), cam['width'])
  return ''.join([name, '.jpg'])

# if __name__ == '__main__':
#   print([gen_name() for i in range(20)])
