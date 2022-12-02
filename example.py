import imagedetect
import json

if __name__ == '__main__':

  # 单个图片 imagedetect.get_from_one_img()
  print('单个图片')
  res = imagedetect.get_from_one_img('./img/img_01.webp')
  json_str = json.dump(res)
  print(json_str, end='\n\n')

  # 多个图片 imagedetect.get_from_folder()
  print('多个图片/文件夹')
  res = imagedetect.get_from_folder('./img')
  json_str = json.dump(res)
  print(json_str, end='\n\n')
