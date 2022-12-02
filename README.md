# 图像识别

用法：

将 `apikey.json` 放在项目目录下（该文件默认被 gitignore）

```shell
# 简略输出
python imagedetect.py -i [file/folder]

# 详细输出
python imagedetect.py -i [file/folder]
```

简单的用例在 `example.py` 中

每个请求返回一个json (样例在 example.json 中):

```json
{
  "result_num": 5,
  "result": [
    {
      "keyword": "尖叫功能饮料",
      "score": 0.990062,
      "root": "商品-饮料"
    },
    {
      "keyword": "饮料-尖叫功能饮料",
      "score": 0.762067,
      "root": "商品-饮料"
    },
    ......
  ],
  "log_id": 1598645843625443975
}
```