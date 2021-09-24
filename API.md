# API接口

## 1 安全帽与人体检测

### 1.1 描述

传入base64格式单张图片，对图片进行安全帽人体检测，检测图中所有检测出的人体框、人体置信度、安全帽框、安全帽置信度

图片传入图片为方形

算法：YOLOV5

### 1.2请求

调用地址：tcp://127.0.0.1:5559 

接口ID：38

请求方式：zmq

请求类型：json message

频率控制：无  

| 是否必选 |    参数名    |  类型  |                参数说明                |
| :------: | :----------: | :----: | :------------------------------------: |
|   必选   |  interface   | String |           调用此API的API ID            |
|   可选   |  request_id  | String |    用于区分每一次请求的唯一的字符串    |
|   必选   |   api_key    | String |         调用此 API 的 API Key          |
|   必选   | image_base64 | String |            图片 base64 编码            |
|   可选   |  conf_thres  | Float  |   0-1，安全帽/人体的阈值，默认为0.25   |
|   可选   |  iou_thres   | Float  | 0-1，检测框阈值，默认为0.5。不推荐修改 |

### 1.3返回

返回类型：JSON  

|           参数名            |  类型  |                         参数说明                          |
| :-------------------------: | :----: | :-------------------------------------------------------: |
|         request_id          | String |             用于区分每一次请求的唯一的字符串              |
|          error_id           |  Int   |                        0则检测成功                        |
|        error_message        | String |             "helmet detect success" 检测成功              |
|          time_used          |  Int   |             整个请求所花费的时间，单位为毫秒              |
|         detect_info         | Array  |          检测结果，包含单张图片多个目标检测结果           |
|     detect_info[i].type     | String | 第【i+1】个检测结果类别类别，若存在则为"person"或"helmet" |
|  detect_info[i].confidence  | float  |                 第【i+1】个检测目标置信度                 |
|  detect_info[i].left_up_x   |  int   |              第【i+1】个检测目标左上角x坐标               |
|  detect_info[i].left_up_y   |  int   |              第【i+1】个检测目标左上角y坐标               |
| detect_info[i].right_down_x |  int   |              第【i+1】个检测目标右下角x坐标               |
| detect_info[i].right_down_y |  int   |              第【i+1】个检测目标右下角y坐标               |
|       ### 1.4返回示例       |        |                                                           |

```json
{
    "detect_info": [
        {
            "type": "person",
            "confidence": 0.9091164469718933,
            "left_up_x": 303,
            "left_up_y": 199,
            "right_down_x": 519,
            "right_down_y": 684
        }
    ],
    "request_id": "10",
    "time_used": 52,
    "error_id": 0,
    "error_message": "helmet detect success"
}
```



## 2人体姿态估计

### 2.1 描述

传入base64格式单张图片和该图片中的需要进行姿态估计的人体框信息，对图片进行安全帽人体检测，检测人体框对应人体的17个人体关键点信息

图片传入图片为方形

算法：基于mmpose的hrnet

### 2.2请求

调用地址：tcp://127.0.0.1:5559 

接口ID：40

请求方式：zmq

请求类型：json message

频率控制：无  

| 是否必选 |    参数名    |  类型  |                           参数说明                           |
| :------: | :----------: | :----: | :----------------------------------------------------------: |
|   必选   |  interface   | String |                      调用此API的API ID                       |
|   可选   |  request_id  | String |               用于区分每一次请求的唯一的字符串               |
|   必选   |   api_key    | String |                    调用此 API 的 API Key                     |
|   必选   | image_base64 | String |                       图片 base64 编码                       |
|   可选   | person_boxes | Array  | 图片中所有的人体框坐标 ，格式：[[person_1_center_x,person_1_center_y,person_1_w,person_1_h]，[person_2_center_x,person_2_center_y,person_2_w,person_2_h]],不指定时person_boxes默认为整个图片框 |

### 2.3返回

返回类型：JSON  

|                  参数名                  |  类型  |                          参数说明                          |
| :--------------------------------------: | :----: | :--------------------------------------------------------: |
|                request_id                | String |              用于区分每一次请求的唯一的字符串              |
|                 error_id                 |  Int   |                        0则检测成功                         |
|              error_message               | String |               "pose detect success" 检测成功               |
|                time_used                 |  Int   |              整个请求所花费的时间，单位为毫秒              |
|               detect_info                | Array  |         姿态检测结果，包含所有传入人体框人体的姿态         |
|      detect_info[i].person_info[17]      | Array  |  图中第【i+1】个人体框对应人体的姿态信息，包含17个关键点   |
| detect_info[i].person_info[j].confidence | float  | 图中第【i+1】个人体框对应人体的第【j+1】个姿态关键点置信度 |
|     detect_info[i].person_info[j].x      |  int   | 图中第【i+1】个人体框对应人体的第【j+1】个姿态关键点横坐标 |
|     detect_info[i].person_info[j].y      |  int   | 图中第【i+1】个人体框对应人体的第【j+1】个姿态关键点纵坐标 |

### 2.4返回示例

```json
{
    "detect_info": [
        {
            "pose_info": [
                {
                    "confidence": 0.9747129678726196,
                    "x": 43,
                    "y": 27
                },
                {
                    "confidence": 0.9790713787078857,
                    "x": 48,
                    "y": 22
                },
                {
                    "confidence": 0.9570357799530029,
                    "x": 38,
                    "y": 22
                },
                {
                    "confidence": 0.9667567014694214,
                    "x": 56,
                    "y": 23
                },
                {
                    "confidence": 0.9651912450790405,
                    "x": 33,
                    "y": 23
                },
                {
                    "confidence": 0.9323450326919556,
                    "x": 68,
                    "y": 44
                },
                {
                    "confidence": 0.9376048445701599,
                    "x": 21,
                    "y": 45
                },
                {
                    "confidence": 0.8932996988296509,
                    "x": 78,
                    "y": 74
                },
                {
                    "confidence": 0.9190618991851807,
                    "x": 12,
                    "y": 75
                },
                {
                    "confidence": 0.9507601857185364,
                    "x": 82,
                    "y": 104
                },
                {
                    "confidence": 0.9447977542877197,
                    "x": 8,
                    "y": 104
                },
                {
                    "confidence": 0.9096292853355408,
                    "x": 58,
                    "y": 103
                },
                {
                    "confidence": 0.8167489171028137,
                    "x": 27,
                    "y": 105
                },
                {
                    "confidence": 0.7555119395256042,
                    "x": 65,
                    "y": 131
                },
                {
                    "confidence": 0.9004912376403809,
                    "x": 27,
                    "y": 161
                },
                {
                    "confidence": 0.9107222557067871,
                    "x": 64,
                    "y": 175
                },
                {
                    "confidence": 0.8501875400543213,
                    "x": 27,
                    "y": 221
                }
            ]
        }
    ],
    "request_id": "10",
    "time_used": 67,
    "error_id": 0,
    "error_message": "pose detect success"
}
```





## 3抽烟打电话分类

### 3.1描述

传入base64格式多张图片，对图片进行是否抽烟与是否打电话判断

推荐传入人体上半身的方形图片

### 3.2请求

调用地址：tcp://127.0.0.1:5559 

接口ID：42

请求方式：zmq

请求类型：json message

频率控制：无  

| 是否必选 |    参数名    |  类型  |             参数说明             |
| :------: | :----------: | :----: | :------------------------------: |
|   必选   |  interface   | String |        调用此API的API ID         |
|   必选   |   api_key    | String |      调用此 API 的 API Key       |
|   必选   | image_base64 | Array  |       图片 base64 编码数组       |
|   可选   |  request_id  | String | 用于区分每一次请求的唯一的字符串 |

### 3.3返回

返回类型：JSON  

|              参数名               |  类型  |                           参数说明                           |
| :-------------------------------: | :----: | :----------------------------------------------------------: |
|            request_id             | String |               用于区分每一次请求的唯一的字符串               |
|             error_id              |  Int   |                         0则检测成功                          |
|           error_message           | String |        "people smoke&phone classify success" 检测成功        |
|             time_used             |  Int   |               整个请求所花费的时间，单位为毫秒               |
|            detect_info            | Array  |                       多张图片检测结果                       |
|     detect_info[i].smoke_res      |  json  |                第【i+1】张图片的抽烟判断结果                 |
|   detect_info[i].smoke_res.type   | string | 第【i+1】张图片的抽烟判断结果:person表示没抽烟，smoke表示在抽烟 |
| detect_info[i].smoke_res.accuracy | float  |             第【i+1】张图片的抽烟判断结果置信度              |
|     detect_info[i].phone_res      |  json  |               第【i+1】张图片的打电话判断结果                |
|   detect_info[i].phone_res.type   | string | 第【i+1】张图片的打电话判断结果:person表示没打电话，phone表示在打电话 |
| detect_info[i].phone_res.accuracy | float  |            第【i+1】张图片的打电话判断结果置信度             |

### 3.4返回示例

```json
{
    "detect_info": [
        {
            "smoke_res": {
                "type": "person",
                "accuracy": 0.9986453652381897
            },
            "phone_res": {
                "type": "person",
                "accuracy": 1.0
            }
        }
    ],
    "request_id": "10",
    "time_used": 53,
    "error_id": 0,
    "error_message": "people smoke&phone classify success"
}
```

## 4履带断煤检测

### 4.1描述

传入2张以上图片，返回多个roi对应检测结果，返回1为断煤报警，返回0为正常，返回-1为第一帧，如 [0,1] or [1] or [-1,-1]

> RoI选取原则：
> 1.可在原图上选取多个任意四边形，顶点顺序为 左上->右上->右下->左下
> 2.尽量选取履带上亮度较高、清晰、无遮挡、无抖动的区域
> 3.选取的四边形边界不能超出履带边界，也不能与履带边界重合
> 4.选取的四边形不能太大，以“10#皮带中部”场景为例：
> 左边履带的RoI为[[500,500], [650,500], [580,600], [400,600]]，右边履带的RoI为[[1020,460], [1180,460], [1330,525], [1080,525]]

ROI取样示例，红色点为推荐roi点

![](https://s3.bmp.ovh/imgs/2021/09/9e65bf3c55487b88.jpg)

算法：ViBe背景提取算法

### 4.2请求

调用地址：tcp://127.0.0.1:5559 

接口ID：43

请求方式：zmq

请求类型：json message

频率控制：无  

| 是否必选 |    参数名    |  类型  |                           参数说明                           |
| :------: | :----------: | :----: | :----------------------------------------------------------: |
|   必选   |  interface   | String |                      调用此API的API ID                       |
|   必选   |   api_key    | String |                    调用此 API 的 API Key                     |
|   必选   | image_base64 | Array  |                     图片 base64 编码数组                     |
|   可选   |  request_id  | String |               用于区分每一次请求的唯一的字符串               |
|   必选   |  roi_points  | Array  | RoI任意四边形顶点(可包含多组，顶点从左上角顺时针填入)，如     [    [[500,500], [650,500], [580,600], [400,600]],         [[1020,460], [1180,460], [1330,525], [1080,525]]     ] |
|   可选   |  threshold   | float  | 履带断煤检测阈值设置，若不给则默认设定为0.04（对应无煤才算断煤，有煤就不断煤的场景） |

### 4.3返回

|       参数名       |  类型  |                           参数说明                           |
| :----------------: | :----: | :----------------------------------------------------------: |
|     request_id     | String |               用于区分每一次请求的唯一的字符串               |
|      error_id      |  Int   |                         0则检测成功                          |
|   error_message    | String |             "track coal detect success" 检测成功             |
|     time_used      |  Int   |               整个请求所花费的时间，单位为毫秒               |
|    detect_info     | Array  |                   多张图片多个roi检测结果                    |
|   detect_info[i]   | Array  | 第【i+1】张图片的所有roi检测结果，第一张图片将用于建模，不检测 |
| detect_info[i].[j] |  int   | 第【i+1】张图片的第【j+1】个roi的检测结果，0代表未断煤，1代表断煤 |

### 4.4返回示例

```json
{
    "detect_info": [
        [-1, -1], 
        [0, 1], 
        [0, 1], 
        [0, 1], 
        [0, 1], 
        [0, 1], 
        [0, 1], 
        [0, 1], 
        [0, 1], 
        [0, 1]], 
    "request_id": "2", 
    "time_used": 285, 
    "error_id": 0, 
    "error_message": "track coal detect success"
}
```

