import json
import base64
import argparse
import os
from typing import List

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

IMAGE_URL = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general'
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

verbose = False


def fetch_token():
  if not os.path.exists('apikey.json'):
    print('No "apikey.json", cannot run.')
    exit()
  with open('apikey.json', mode='r', encoding='utf-8') as f:
    con = json.load(f)
    API_KEY = con['API Key']
    SECRET_KEY = con['Secret Key']
  params = {'grant_type': 'client_credentials',
            'client_id': API_KEY,
            'client_secret': SECRET_KEY}
  post_data = urlencode(params)
  post_data = post_data.encode('utf-8')
  req = Request(TOKEN_URL, post_data)
  try:
    f = urlopen(req, timeout=5)
    result_str = f.read()
  except URLError as err:
    print(err)
  result_str = result_str.decode()

  result = json.loads(result_str)

  if ('access_token' in result.keys() and 'scope' in result.keys()):
    if not 'brain_all_scope' in result['scope'].split(' '):
      print ('please ensure has check the  ability')
      exit()
    return result['access_token']
  else:
    print ('please overwrite the correct API_KEY and SECRET_KEY')
    exit()


def token_cat():
  token = fetch_token()
  image_url = IMAGE_URL + "?access_token=" + token
  return image_url


def read_file(image_path):
  f = None
  try:
    f = open(image_path, 'rb')
    return f.read()
  except:
    print('read image file fail')
    return None
  finally:
    if f:
      f.close()


def request(url, data):
  req = Request(url, data.encode('utf-8'))
  try:
    f = urlopen(req)
    result_str = f.read()
    result_str = result_str.decode()
    return result_str
  except  URLError as err:
    print(err)


def get_from_one_img(file:str, image_url='') -> dict:

  '''
  Get json result(one in a list) from a single image.
  When used by get_from_folder(), image_url is needed.
  '''

  if not image_url:
    image_url = token_cat()

  file_content = read_file(file)

  result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

  result_json = json.loads(result)

  if verbose:
    print(result)
  
  return result_json


def get_from_folder(folder:str) -> List[dict]:

  '''
  Get a list of json result from a folder.
  '''

  image_url = token_cat()
  res = []

  for item in os.listdir(folder):
    if verbose:
      print(item)
    res.append(get_from_one_img(f'{folder}/{item}', image_url))
  
  if verbose:
    print(res)
  
  return res


def simple_result(res:List[dict]) -> List[str]:

  '''
  Given the results list, return every first word in results as a dict.
  '''

  ret = []
  for d in res:
    item = d['result'][0]['keyword']
    ret.append(item)
  return ret


if __name__ == '__main__':

  parser = argparse.ArgumentParser('python imagedetect.py')
  parser.add_argument('-i', metavar='"..."', type=str, help='input the folder or file')
  parser.add_argument('-v', '-verbose', action="store_true", help='whether or not output in verbose')
  args = parser.parse_args()

  if args.v:
    verbose = True
  if args.i:

    if not os.path.exists(args.i):
      print('File or folder not exist.')
      exit()
    
    if os.path.isdir(args.i):
      res = get_from_folder(args.i)
    else:
      res = [get_from_one_img(args.i)]

    if not verbose:
      print(simple_result(res))