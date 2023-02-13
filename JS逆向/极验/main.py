"""
    @Author :  莫明伸
    @Date   : 2022-04-19
"""
from PIL import Image
import requests
import time
import re 
import json
import cv2
import math
import random
import execjs


def retry(times=5):
    def wrapper(func):
        def decorator(*args, **kwargs):
            t = 0
            while t < times:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(e)
                    # raise Exception
                finally:
                    time.sleep(1)
                    t += 1
        return decorator
    return wrapper

@retry()
def get_parms():
    """
        获取滑块的参数和图片链接
    """
    #step1 
    t=int(time.time()*1000)
    url = "https://www.geetest.com/demo/gt/register-slide"
    headers = {
    'authority': 'www.geetest.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221803a91260b729-034d53a5d21147-7b422e27-2073600-1803a91260cd58%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fwww.geetest.com%2F%22%7D%2C%22%24device_id%22%3A%221803a91260b729-034d53a5d21147-7b422e27-2073600-1803a91260cd58%22%7D; Hm_lvt_25b04a5e7a64668b9b88e2711fb5f0c4=1650250033; hy_data_2020_id=1803a91265714-02a986b6db5ad7-7b422e27-2073600-1803a912658cce; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%221803a91265714-02a986b6db5ad7-7b422e27-2073600-1803a912658cce%22%2C%22site_id%22%3A2369%2C%22user_company%22%3A84%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%221803a91265714-02a986b6db5ad7-7b422e27-2073600-1803a912658cce%22%7D',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://www.geetest.com/demo/slide-float.html',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
    'x-requested-with': 'XMLHttpRequest',
    }
    params = (
    ('t', t),
    )
    response = session.get(url, headers=headers, params=params,timeout=8).json()
    challenge = response['challenge']
    gt = response['gt']

    #step2
    t=int(time.time()*1000)
    url = "https://apiv6.geetest.com/gettype.php"
    params = {
        'gt': gt,
        'callback': f'geetest_{t}'
    }
    response = session.get(url, params=params, headers=headers,timeout=8)

    #step3  
    t=int(time.time()*1000)
    url = "https://apiv6.geetest.com/get.php"
    params = {
        'gt': gt,
        'challenge': challenge,
        'lang': 'zh-cn',
        'pt': '0',
        'client_type': 'web',
        'w': '',
        'callback': f'geetest_{t}'
    }
    response = session.get(url, params=params, headers=headers,timeout=8)

    #step4
    # time.sleep(10)
    t=int(time.time()*1000)
    url = "https://api.geetest.com/ajax.php"
    params = {
        'gt': gt,
        'challenge': challenge,
        'lang': 'zh-cn',
        'pt': '0',
        'client_type': 'web',
        'w': '',
        'callback': f'geetest_{t}'
    }
    response = session.get(url, params=params, headers=headers,timeout=8)
    # print(response.text)

    #step5
    t=int(time.time()*1000)
    url = "https://api.geetest.com/get.php"
    params = (
        ('is_next', 'true'),
        ('type', 'slide3'),
        ('gt', gt),
        ('challenge', challenge),
        ('lang', 'zh-cn'),
        ('https', 'false'),
        ('protocol', 'https://'),
        ('offline', 'false'),
        ('product', 'embed'),
        ('api_server', 'api.geetest.com'),
        ('isPC', 'true'),
        ('autoReset', 'true'),
        ('width', '100%'),
        ('callback', f'geetest_{t}'),
    )
    response = session.get(url, params=params, headers=headers,timeout=8)
    content = re.findall('.*?\((.*?)\)',response.text)[0]
    content = json.loads(content)
    c = content['c']
    s = content['s']
    challenge_f = content['challenge']
    gt = content['gt']
    bg_pic = 'https://static.geetest.com/'+content['bg']
    slice_pic = 'https://static.geetest.com/'+content['slice']
    fullbg_pic = 'https://static.geetest.com/'+content['fullbg']
    return c,s,challenge_f,gt,bg_pic,slice_pic,fullbg_pic

def save_pic(pic_path):
    if pic_path.find('bg')>-1:
        pic_name='bg.png'
    elif pic_path.find('slice')>-1:
        pic_name='slice.png'
    else:
        pic_name='fullbg.png'
    response = session.get(pic_path).content
    with open(pic_name,'wb') as f:
        f.write(response)
    # print(f'图片{pic_name}保存成功')

def bg_true(pic_read):
    #pic_read   读取的图片
    pic_write=pic_read.split('.')[0]+'_true.'+pic_read.split('.')[1]  #保存转换后的图片
    #转换的逻辑顺序
    img = Image.open(pic_read)
    standard_img = Image.new("RGBA",(260,160))
    positon = [39,38,48,49,41,40,46,47,35,34,50,51,33,32,28,29,27,26,36,37,31,30,44,45,43,42,12,13,23,22,14,15,21,20,8,9,25,24,6,7,3,2,0,1,11,10,4,5,19,18,16,17]
    a = int(160/2)
    for _ in range(52):
        c = positon[_] % 26 * 12 + 1
        u = a if 25 < positon[_] else 0
        l = img.crop(box=(c, u, c+10, u+a))
        standard_img.paste(l, box=(_ % 26 * 10, a if 25 < _ else 0))
    standard_img.save(pic_write)
    # print(f'图片{pic_write}还原完成')

def get_distance(pic_read,pic_read1):
    #pic_read   # 读取背景图片
    #pic_read1  # 读取缺口图片
    pic_write='match.png'   # 保存匹配最优图
    bg_img = cv2.imread(pic_read) # 背景图片
    tp_img = cv2.imread(pic_read1) # 缺口图片

    result_list=[]
    for i in range(100,500,50): #300,350
        # 识别图片边缘
        bg_edge = cv2.Canny(bg_img, i, i+50)
        tp_edge = cv2.Canny(tp_img, i, i+50)
        # 转换图片格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        # 缺口匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 寻找最优匹配
        result_list.append([res.max(),max_loc])

    #取最优参数
    maxx=0
    for i in result_list:
        if i[0]>maxx:
            maxx=i[0]
            max_loc=i[1]

    # 绘制方框
    th, tw = tp_pic.shape[:2] #40,40
    tl = max_loc # 左上角点的坐标
    br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
    # print(f'左上角的坐标为{tl},右上角的坐标为{br}')

    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形
    # cv2.imshow(pic_write,bg_img)
    cv2.imwrite(pic_write,bg_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows() #摧毁全部窗口
    # print('计算距离完成，已保存最优匹配缺口图',maxx)
    return tl[0]   

def get_slider_offset_method(pic_path, cut_pic_path, threshold=60):
    """比较两张图片的像素点RGB的绝对值是否小于阈值60,如果在阈值内则相同,反之不同"""
    bg_img = cv2.imread(pic_path) # 背景图片
    pic_img = Image.open(pic_path)
    cut_img = Image.open(cut_pic_path)
    width, height = pic_img.size
    
    for x in range(40, width - 40):  # 从左往右
        for y in range(5, height - 10):  # 从上往下 5,10
            pixel1 = pic_img.load()[x, y]
            pixel2 = cut_img.load()[x, y]
            if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
                continue
            else:
                # cv2.rectangle(bg_img, (x,y), (x+40,y+40), (0, 0, 255), 2) # 绘制矩形
                # cv2.imwrite('match_image.png',bg_img)
                return x-5

def get_trace(slice_x,bg_true_pic):
    cv2_bg = cv2.imread(bg_true_pic)
    bg_s = cv2_bg.shape[1]
    slice_s = 40
    max_s = bg_s - slice_s
    sum_t = 3000    #滑块移动的最大毫秒数
    
    slice_x_1 = slice_x / max_s    #归一化：最大最小化
    slice_t_1 = math.log(slice_x_1/(1-slice_x_1))    #sigmoid函数求解t
    slice_t_1 = (slice_t_1-(-6))/(6-(-6))    #求t在[-6,6]的缩放
    slice_t = int(sum_t*slice_t_1)    #轨迹移动的总时长ms

    slice_T_0 = [random.randint(-35,-31),random.randint(-35,-31),0]
    slice_T = [slice_T_0,[0,0,0]]
    random_t = random.randint(100,180) #每一次滑动后的总时间，这里是第一次点击滑块的时间
    random_x = 0
    while random_t < slice_t and random_x < slice_x:
        random_add_t = random.randint(7,20) #每次滑动的时间间隔
        random_t += random_add_t
        random_t_1 = 12*random_t/slice_t-6
        slice_x_t = math.ceil(1/(1+math.exp(-random_t_1))*slice_x)  #sigmoid函数求解y
        if slice_x_t > random_x:
            random_x = slice_x_t    
            slice_T.append([slice_x_t,0,random_t])
    random_add_t = random.randint(800,1200) #每次滑动的时间间隔
    random_t += random_add_t
    slice_T.append([slice_x_t,0,random_t])
    # print(slice_T)
    return slice_T

@retry()
def get_finall(w,gt,challenge):
    t=int(time.time()*1000)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
    }

    params = (
        ('gt', gt),
        ('challenge', challenge),
        ('lang', 'zh-cn'),
        ('$_BBF', '0'),
        ('client_type', 'web'),
        ('w', w),
        ('callback', f'geetest_{t}'),
    )
    # print(params)
    response = session.get('https://api.geetest.com/ajax.php', headers=headers, params=params,timeout=8)
    return response.text

if __name__ == '__main__':
    count = 0
    for i in range(10):
        session = requests.Session()
        c,s,challenge_f,gt,bg_url,slice_url,fullbg_url = get_parms()
        for pic_path in [bg_url,slice_url,fullbg_url]:
            save_pic(pic_path)

        for bg_pic in ['bg.png','fullbg.png']:     #乱序图
            bg_true(bg_pic)     #还原正确图函数
        distance_s = get_slider_offset_method('bg_true.png','fullbg_true.png') #计算缺口距离方法1
        # bg_true_pic = 'bg_true.png'    #背景缺口还原图
        # slice_pic = 'slice.png'    #滑块图
        # distance_s = get_distance(bg_true_pic,slice_pic)        #计算缺口距离方法2
        t = get_trace(distance_s,'bg_true.png')     #移动轨迹数据方法1
        # t=slide_track.get(distance_s) or slide_track.get(distance_s-1) or slide_track.get(distance_s +1) or slide_track.get(distance_s +2) or slide_track.get(distance_s -2) #移动轨迹数据方法2
        with open('w.js','r',encoding='utf-8') as f:
            js_code = f.read()
        w = execjs.compile(js_code).call('get_w',t,c,s,gt,challenge_f)
        result = get_finall(w,gt,challenge_f)
        print(result)
        success = re.findall('"success": (\d+),',result)[0]
        if success == '1':
            count +=1
    print(count)

        


    