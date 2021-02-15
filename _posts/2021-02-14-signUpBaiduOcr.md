---
layout: post
cover: 'assets/images/tree.jpg'
title: 使用BaiduOcr识别图片文字
date: 2021-02-14
tags: web ai
author: sjh
description: 包含注册申请以及使用例！
---

# 使用BaiduOcr识别图片文字

百度AI平台提供了很多AI接口，大部分都提供了免费的调用额度，如果是个人使用可以获得很大的便利，这里将介绍如何使用百度提供的文字识别接口。

## 注册并申请使用权

[BaiduAI官网](https://ai.baidu.com/)进入后点击右上角控制台进行登录

### 注册百度账号

百度账号注册这里不再赘述，进入控制台登陆时即可注册。

### 实名认证

1. 登入控制台后会要求填写以下信息来激活账号，只需要填写`*`号信息栏。

   <img src="https://i.loli.net/2021/02/14/SK3zbi5NUAHoPOj.jpg" alt="#1" style="zoom: 67%;" />

2. 完成后点击左侧工具栏的文字识别，如下图所示

   <img src="https://i.loli.net/2021/02/14/bAF5XQBje4CSOHR.jpg" alt="#2" style="zoom: 50%;" />

3. 点击**立即认证**，填入姓名和身份后点击下一步，无需刷脸验证，直接返回上一步的页面即可

   <img src="https://i.loli.net/2021/02/14/YUC32t7WH6xpiID.jpg" alt="#3" style="zoom:80%;" />

### 创建文字识别应用

1. 回到控制台后点击 **创建应用**，填一些信息，**不需要包名**并选择所属为**个人**

   <img src="https://i.loli.net/2021/02/14/uIH4jaeSwGJxEXp.jpg" alt="#4"  />

2. 创建完成后点击 **应用详情** ，进入页面后请记住`API Key`和`Secret Key`

   <img src="https://i.loli.net/2021/02/14/xZ8SFYnuoUJwRgp.jpg" alt="#5" style="zoom:80%;" />

## 调用API识别图片

### 获取Token

每隔一段时间使用前都需要获取`Token`，一个Token的有效期为30分钟

通过发送`HTTP Get`请求token：

- url：`https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_Key}&client_secret={Secret_Key}`

- 请求中携带参数API_key和Secret_key替换为你刚才申请的两个值，当然`{}`需要删除！

- 请求成功将获得一串`Json`，例如

  ```json
  {
    "refresh_token": "25.b55fe1d287227ca97aab219bb249b8ab.315360000.1798284651.282335-8574074",
    "expires_in": 2592000,
    "scope": "public wise_adapt",
    "session_key": "9mzdDZXu3dENdFZQurfg0Vz8slgSgvvOAUebNFzyzcpQ5EnbxbF+hfG9DQkpUVQdh4p6HbQcAiz5RmuBAja1JJGgIdJI",
    "access_token": "24.6c5e1ff107f0e8bcef8c46d3424a0e78.2592000.1485516651.282335-8574074",
    "session_secret": "dfac94a3489fe9fca7c3221cbf7525ff"
  }
  ```

  我们只需要获取`access_token`即可

  若返回失败则会得到包含`error_description`的`Json`信息

### 调用所需接口

文字识别分为通用文字识别、通用文字识别（高精度），不同的接口有不同的免费额度

通过发送`HTTP POST`上传图片数据或者地址进行文字识别

- url：`https://aip.baidubce.com/rest/2.0/ocr/v1/{ocr_type}?access_token={token}`

  此处ocr_type根据不同的识别方式变化，可以用“general_basic”或者“accurate_basic”替换.

  token是上一步获取的`access_token`

- post的请求体为表单类型，分为两种方式

  1. 图片数据

     图片数据必须使用Base64编码，并用以下格式作为请求体

     | key   | value      |
     | ----- | ---------- |
     | image | base64数组 |

  2. 图片地址

     | key  | value     |
     | ---- | --------- |
     | url  | url字符串 |

     仅`general_basic`支持用网络图片

- 请求完成后将返回 Json 数据

  ```json
  {
      "log_id": 2471272194,
      "words_result_num": 2,
      "words_result": [
          {"words": " example"},
          {"words": "helloworld"}
      ]
  }
  ```

  出错则会返回包含`err_msg`的 Json 数据，具体错误类型可见[官方文档](https://ai.baidu.com/ai-doc/OCR/dkibizxnx)

### Python使用例

[点此到Github中查看](https://github.com/838239178/tk-auto-study/blob/master/ocr.py)上述介绍的内容分别对应`def _get_token()`和`def general_ocr(img_b64)`

### 额外选择

百度ocr还包含很多种类型具体请查看 [官方文档](https://ai.baidu.com/ai-doc/OCR/1k3h7y3db)，调用api时也可传入其他参数，如是否检测图片方向、图片需要识别的语言等，这里就不多介绍，入门后看官方文档就没有任何问题了。