# 一、Linux

## 1.vim编辑器

- y 复制

- w 选择单词

- p 粘贴

- : noh 取消高亮模式

- : set nu 显示行号 

- /单词 查找单词（n 下一个 N 上一个）

- : %s/old单词/new单词/g 替换全部单词

## 2.系统管理

- systemctl start | stop | restart | status | disable 服务名称

- ls /usr/lib/systemd/system 查看系统服务

- 查看进程：ps -ef |grep python

- netstat -tunlp |grep 端口号，用于查看指定的端口号的进程情况

- 增加防火墙端口： iptables -I INPUT -p tcp --dport 80 -j ACCEPT

## 3.文件处理

- 上传：rz
- 下载：sz xxx
- 解压
  - tar -zxvf 
  - unzip
- 截取文件路径：dirname
  - 获取父路径：pdir=$(cd -P $(dirname $file); pwd)


## 4.安装gcc编译器

```shell
yum -y install gcc
```

## 5.安装Python3

安装开发时对应的Python版本

1.下载Pyhton3.9.1到/usr/local 目录并解压

```shell
cd /usr/local
wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz tar -zxvf Python-3.9.1.tgz
```

2.进入 Python-3.9.1路径,编译安装到指定路径,依次执行以下命令

```shell
cd /usr/local/Python-3.9.1
./configure --with-ssl --prefix=/usr/local/python3
make
make install
```

3.安装完成之后 建立软链接 添加变量 方便在终端中直接使用python3

```shell
ln -s /usr/local/python3/bin/python3.9 /usr/bin/python3
```

4.安装pip3

```shell
rpm -qa | grep zlib
yum -y install zlib* 

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py

ln -s /usr/local/python3/bin/pip3.9 /usr/bin/pip3

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

zlib安装成功再次安装setuptools还是提示“zipimport.ZipImportError: can‘t decompress data; zlib not available”，google上有人说只能重新编译安装python了，不过在编译的时候修改编辑Modules/Setup.dist文件，将#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz 
这行的注释去掉，然后在次编译安装



5.导出并安装项目依赖包

```bash
pip install pipreqs
进入项目的根目录
pipreqs --force ./ --encoding=utf-8

pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



6.PyInstaller

1.在Python打包的上下文中，似乎Pipfile / Pipfile.lock旨在替换requirements.txt。
Pipenv是一个包和虚拟环境管理工具，它使用Pipfile和Pipfile.lock文件来实现这些目标。具体来说他是pip、pipfile、virtualenv的结合体。让包安装、包依赖管理、和虚拟环境管理更加方便

pip install pipenv 

使用`pipenv  --python 3.6 install`命令为当前的项目创建虚拟环境

在pipenv中，可以使用`pipenv shell`命令显式地激活虚拟环境

> https://blog.csdn.net/qq_42402648/article/details/112168712

Pyinstaller -F setup.py 打包exe

Pyinstaller -F -w setup.py 不带控制台的打包

Pyinstaller -F -i xx.ico setup.py 打包指定exe图标打包

pyinstaller 打包报错： AttributeError: ‘str‘ object has no attribute ‘decode‘

```
if encoding:
    # out = out.decode(encoding)
    if type(out) == type('string'):
        pass
    else:
        out = out.decode(encoding)
```

## 6.挂起任务

screen可以将窗口挂起，做到即使你下线，你的django项目还会保持运行。 

screen的安装

yum -y install screen 
 安装之后查看版本

screen -v 
Screen version 4.00.03 (FAU)  
显示版本即安装成功。

 首先创建创建窗口

screen - S name
 创建完成后他会直接进入，之后在该窗口使用cd指令进入项目目录启动服务器。

之后使用CTRL+a+d先按a再按d即可挂起，这次关掉连接，进入你的ip地址或者是域名，如果看到你的网站说明你成功了

其实还有其他常用指令

查看当前作业

screen -ls （使用此条命令你可以查看当前存在的作业有哪些以及他们的id）

重新连接

screen -r id/name (重新进入到运行的项目窗口)

删除作业

screen -X -S id/name quit

## 7.docker

- 编写docker文件

  ```dockerfile
  FROM python:3.9
  WORKDIR /fileload
  COPY fileload /fileload
  RUN pip install -r /fileload/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  CMD ["/bin/bash","-c","python /fileload/manage.py runserver 0.0.0.0:80 "]
  ```

- 打包项目：docker build -t app:1.0 .

- 启动容器： docker run -it -p99:80 app:1.0

- 查看容器：docker images

- 打包：docker save imageID > app.tar

#### 1.ipv4报错

	在建容器时 报如下错误:   WARNING: IPv4 forwarding is disabled. Networking will not work

解决方法:

第一步：找到文件 ：vim /usr/lib/sysctl.d/00-system.conf

 添加代码：net.ipv4.ip_forward=1

第二步：重启network服务和docker服务：

 systemctl restart network && systemctl restart docker

第三步：重启建容器

## 8.vmware虚拟机关闭防火墙

1. systemctl stop firewalld.service #停止firewall 
2. systemctl disable firewalld.service #禁止firewall开机启动

## 9.基本命令

### 1.帮助命令

1.帮助手册命令：man

2.内置帮助信息命令（shell的内嵌命令）：help

### 2.文件目录

1.pwd：显示当前工作目录的绝对路径

2.cd：cd .. 上一级，cd - 切换为上一个目前

3.ls：列出当前目录，ls -l 列出详细的每一行文件信息 == ll 命令

# 二、jiacrontab

1.

mkdir /opt
cd /opt
wget https://jiacrontab.iwannay.cn/download/jiacrontab-master-linux-amd64.zip
unzip jiacrontab-master-linux-amd64.zip

2.

cd /opt/jiacrontab/jiacrontab_admin
nohup ./jiacrontab_admin &>> /opt/jiacrontab/jiacrontab_admin/jiacrontab_admin.log &
cd /opt/jiacrontab/jiacrontabd
nohup ./jiacrontabd &>> /opt/jiacrontab/jiacrontabd/jiacrontabd.log &

ps -ef | grep jiacrontab #查看进程

日志路径：/opt/jiacrontab/jiacrontabd/logs/crontab_task
打开浏览器查看
http://IP:20000/
创建管理员账户密码

# 三、Git

## 1.配置个人的用户名称和电子邮件地址：



##### Git global setup

```
$ git config --global user.name "runoob"
$ git config --global user.email test@runoob.com
```

##### Create a new repository

```
git clone http://gitlab.shidaoffice.vip/xxx/fileload.git
cd fileload
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

##### Push an existing folder

```
cd existing_folder
git init
git remote add origin http://gitlab.shidaoffice.vip/xxx/fileload.git
git add .
git commit -m "Initial commit"
git push -u origin master
```

##### Push an existing Git repository

```
cd existing_repo
git remote rename origin old-origin
git remote add origin http://gitlab.shidaoffice.vip/momingshen/fileload.git
git push -u origin --all
git push -u origin --tags
```

# 四、vba

## 1.excel

ctrl+G：定位条件快捷键

## 2.语法

F8：单步调试

' ：注释

cells(x,y)：第x行第y列

range("A1")：第A列第1行

定义对象：set i = Sheets("aaa")

定义变量：Dim i

定义过程：sub 

定义函数：Function aaa()

去掉两边空格：Trim(aaa)

替换：Replace(aaa,"xx","x")

小写变大写：UCase("aaa")，大写变小写：LCase("aaa")

切割：Left(x,6)，Right(x,6)，mid（x,2,4）截取：Mid(x, 6, 2)

查找：InStr(x, "aaa")

日期格式转换：DateSerial（年，月，日） ，字符串格式

```vb
Sub aaa()
    Dim i
    For i = 2 To 7 Step 1 
    	If Range("A" & i) = "a" then
            Range("B" & i) = "b"
        Else
            Range("B" & i) = "b"
        End if
    	'Exit For
	Next i
Do While Range("A"& i ) <> ""
    i = i + 1
Loop
End Sub
```

for循环工作表：For Each i in Worksheets

## 3.工作表

取消对话框提示：Excel.Application.DisplayAlerts = False

取消屏幕刷新：Excel.Application.ScreenUpdating = False

弹出消息框：MsgBox Sheets.Count 表格的数量

选择工作表：Sheets().Select/Sheets("aaa")

删除工作表：Sheets("aaa").Delete

复制工作表：Sheets("aaa").Copy

重命名：Sheets("Sheet1").Name = "aaa"

当前工作表命名：ActiveSheet.Name = "aaa"

增加工作表：Sheets.Add before/after := Sheets("aaa")，在aaa表前面/后面追加

当前工作表：

​	名称：ThisWorkbook.Name

​	路径：ThisWorkbook.Path

​	带路径的名称：ThisWorkbook.FullName

## 4.工作簿

增加打开：Workbooks.add /open ""

保存：activeworkbook.save / activeworkbook.saveas filename := "aa.xlsx"

离开：activeworkbook.close



# 五、HTML

```html
<!DOCTYPE html>
```

## head

### 1.注释

<!-- 内容 -->

### 2.声明字符集

```html
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
```

### 3.标题

	<title>标题</title>

### 4.关键词

```html
<meta name="keywords" content="关键词1，关键词2"/>
```

### 5.详细描述

```html
<meta name="description" content="网站的内容描述"/>
```

## body

### 1.换行标签

```html
<br />
```

### 2.空格符号

```html
&nbsp;
```

### 3.表格标签

```html
<table>
    <tr>
    	<th></th>
    </tr>
    <tr>
    	<td></td>
    	<td></td>
    </tr>
</table>
```

### 4.列表标签

  ```html
  <!-- 无序列表 -->
  <ul>
      <li></li>
      <li></li>
  </ul>
  <!-- 有序列表 -->
  <ol>
      <li></li>
      <li></li>
  </ol>
  ```

### 5.表单标签

  ```html
  <form action="" method="" novalidate>
      
  </form>
  ```

### 6.输入标签
  - text 文本输入
  - password 密码输入
  - radio 单选按钮输入
  - checkbox 复选框
  - submit 提交按钮
  - button 按钮
  - date 日期
  - fieldset 表单外边框
  - select 下拉框 <option>
  - textarea 容纳更多的文本
  - button 按钮
  - label 定义标签

### 7.音乐播放

- audio ：src，音乐文件链接



## CSS

### 1.初始化

- 注释：/* 注释内容 */

- 设置字符集：@charset "utf-8"

- <style></style>

- <link rel="stylesheet" href=""></link>

- 设置内外边距为0：

```html
* {
	margin:0;
	padding:0;
}
```

### 2.选择器

- id选择器：#div
- class选择器：.div
- 属性选择器：div
- 匹配选择器：[class ~= 名称]，~模糊匹配，^匹配开头，$匹配结尾
  - 伪类：#div :hover{}（当鼠标悬浮在元素上方时，向元素增加样式）

- 派生选择器：.div #div div 

### 3.样式优先级

- 内联样式（1000）>id（100）>类（10）>元素（1）
- !importamt，提升样式优先级

### 2.属性

- 边框实体线颜色:border: 1px solid black;

- 图片菱角变圆：border-radius:50%;

- 取消外部边框：outline:none;

- 背景颜色：background: blue; 

- 背景图片：background-image:url(../img/1.png);
  - 图片自适应：background-size:cover;
  - 图片填充(水平填充)：background-repeat:repeat-x;
  - 图片定位：background-position
  - 图片透明度：opacity(1-0.0)
  - 阴影部分：box-shadow:1px 1px 1px 1px black;

- 颜色：color

- 字体：font-family ，大小：font-size ，风格：font-style ，加粗：font-weight

- 文本对齐方式：text-align
  - left
  - right
  - center

- 文本上下划线：text-decoration
  - underline
  - overline
  - line-through
  - none

- 文本缩进：text-indent:2em;

- 列表样式：list-style
  - none无样式
  - disc认样式实心圆
  - circle空心圆
  - square实心方块
  - decimal数字
  - decimal-leading-zero以0开头的数字
  - lower-roman小写罗马数字
  - upper-roman大写罗马数字
  - lower-alpha小写英文字母
  - upper-alpha大写英文字母

- 内边距宽度：padding

- 外边距宽度：margin：auto居中

- 变块级元素：display:block;

- 使用定位：position(top,bottom,left,right)
  - 绝对定位：absolute（绝对定位,一直寻找上级元素，最上级为body）
  - 相对定位：relative（控制子元素使用定位不会超出父元素）
  - 浏览器绝对定位：fixed

- 设置鼠标样式：cursor:pointer;

- 设置元素显示优先级：z-index

- 控制元素流浮动：float：left/right

- display：none隐藏，block显示，不占用位置

- visibility：hidden隐藏，visible显示

  

## JavaScript

### 1.基础语法

- 引用方式

  - <script type="text/javascript" src=""></script>

- 变量和函数名提升

  编译时会先定义变量或函数名后再赋值

#### 1.数据类型

  数值（number）、字符串（string）、布尔值（boolean）、undefined（未定义）、null（空）、object（对象：集合，数组，函数）

#### 2.类型转换
	- 转数字：parseInt()、parseFloat()、Number()
	- 转字符串：toString、String()
	- 转布尔：Boolean()

#### 3.控制语句

```javascript
if(){}  else if(){} else{}
```

```javascript
switch(num){
    case 1:xxxx;break;
    case 2:xxxx;break;
    default:xxxx;break;
}
```

```javascript
while(){}
do{}while();
```

```javascript
for(;;){}
for(var i in list){}
array.forEach(funtion(elements,index,arr){});
```

#### 4.数组操作

- arr.push(1)		增加元素到最后
- arr.unshift('xx')	增加元素到最前
- arr.pop()         删除最后一项
- arr.shift()         删除第一项
- arr.reverse()        数组翻转
- arr.join()           数组连接
- arr.indexOf()    获取元素索引
- arr.slice(1,3)       截取数组
- arr.splice(1,1,'一','二')       替换原数组下标1的位置为一二
- arr.concat()              数组合并,原数组不改变

#### 5.函数

##### 1.间接调用方式

```javascript
var obj ={
    c:5,
    d:7
    };
function add(a,b){
    return a+b+this.c+this.d;//this代表调用者本身
    };
console.log(add.call(obj,3,2));
console.log(add.apply(obj,[3,2]));
```

##### 2.匿名函数方式

```javascript
(function(){
   var xxxxx; 
})()
```

#### 6.内置对象

- arguments：返回调用当前函数的实际参数
  - arguments.name：函数名称
  - arguments.length：形参个数
  - arguments.toString()：返回函数的源码

#### 7.闭包

- 闭包调用执行返回内置函数

### 2.内置函数

##### 1.String

- charAt()		返回指定位置的字符串
- indexOf() 	返回子字符串的位置，找不到返回-1		
- substr(m,n)    	返回字符串从m位置开始，取n个字符
- substring(m,n)		返回字符串从m位置开始，取到n位置结束
- toLowerCase()        全部字符转小写
- toUpperCase()        全部字符转大写
- replace('x',y')            字符串将x替换成y，replace(/x/g,'y')，x为正则表达式

##### 2.Math

- Math.random()，生成大于0小于1的随机数
- Math.ceil()，向上取整
- Math.floor()，向下取整
- Math.round()，四舍五入

##### 3.Date

- new Date()
  - getTime()，获取时间戳
  - toLocaleString()，时间转字符串
  - setTime()，设置时间

##### 4.eval()

- 将参数字符串解析成js代码执行
- 加上园括号是使eval函数在处理时强制将括号内的表
  达式转化为对象而不作为语句来执行。eval('('+string+')')

##### 5.JSON

- JSON格式序列化和反序列化
  - JSON.parse()，字符串转对象，键采用双引号
  - JSON.stringify()，对象转字符串

##### 6.中文编解码

- encodeURIComponent()
- decodeURIComponent()

##### 7.正则写法(RegExp)

- new RegExp('\d','g')

- /xxxxx/g，xxxxx为正则表达式，g为全局匹配多个，i忽略大小写
  - 字符串.match()，返回多次结果
  - 字符串.exec()，返回第一次结果

### 3.常见事件

- onload:当页面或图像加载完后立即触发
- onclick:鼠标点击某个对象
- onblur:元素失去焦点
- onfocus:元素获得焦点
- onchange:用户改变域的内容
- onmouseover:鼠标移动到某个元素上
- onmouseout:鼠标从某个元素上高开
- onkeyup:某个键盘的键被松开
- onkeydown:某个键盘的键被按下，event.keyCode获取键盘按键对应的值

### 4.事件处理

- DOM0级事件处理（执行一次）

  ```javascript
  document.getElementById().onclick=function(){}
  ```

- DOM2级事件处理（执行两次）

  ```javascript
  document.getElementById().addEventListener('click',function(){},false)
  ```

### 5.windows对象

#### 1.系统对话框

- 消息框：alert()
- 输入框：prompt()
- 确认框：confirm()，返回boolean值

#### 2.窗口

- 新窗口打开链接：window.open('url','_blank')
- 打开空白页面：window.open('about:blank','_self')

#### 3.时间函数定时

- 设置定时执行函数：task = window.setTimeout(func,10)\
- 清除定时任务：window.clearInterval(task)

### 6.history

- 页面前进：window.history.forward()
- 页面后退：window.history.back() / window.history.go(-1)

### 7.location

- 重新加载页面：window.location.reload()
- 查看当前页面路径：window.location.href()

### 8.DOM节点

#### 1.获取节点

- document.getElementssByName，name属性
- document.getElementsByTagName()[索引]，标签名

- document.getElementById，id属性
  - length
  - value,内容
  - getAttribute
  - firstChild，元素的第一个节点
  - lastChild，元素的最后一个子节点
  - nextSibling，元素的下一个兄弟节点
  - parentNode，元素的父节点
  - parent().siblings().children()，获取父级的同辈兄弟节点的孩子节点
  - replaceChild(newnode,oldnode)，用新节点替换旧节点
  - cloneNode(true)，复制节点并返回
  - removeChild()，删除子节点

#### 2.创建节点

- document.createElement()，创建元素
- document.createTextNode()，创建文本
- appendChild()，元素增加子元素
- innerHTML = 文本，元素增加子元素内容

### 9.JQuery

#### 1.jquery对象

- $("xxxx")，xxxx为元素选择器（类，id，元素名称，组合选择器(逗号隔开)）
- jquery对象转DOM对象，$("")[0]
- DOM对象转jquery对象，$(this)，this为DOM对象

#### 2.操作属性

- attr('属性','属性值')，一个参数时为获取属性，两个参数时为设置属性的值
- each()，循环遍历元素，参数function(index,emement){}
- removeAttr()，删除元素的属性
- remove()，删除元素
- removeClass()，删除类元素
- addClass()，增加类元素
- empty()，清空元素的内容
- css()，增加样式，参数为css样式字典
- html()，获取元素的结构，传参数则为设置元素结构
- text()，获取元素的文本，传参数则为设置元素文本
- val()，获取文本框的value属性
- append(xxx)，元素后面增加xxx元素,xxx为已有元素则为移动
- prepend(xxx)，元素前面增加xx元素,xxx为已有元素则为移动
- show()，显示元素
- hide()，隐藏元素
- eq(index)，选取元素的索引元素

#### 3.事件

- bind(‘click’,func)，第一个参数为绑定的事件类型，第二个参数为具体的事件调用函数，可链式编程:bind().bind()，也可写成集合格式bind({})
- get(0).play()，播放音乐，pause() 暂停音乐
- animate()，样式移动

### 10.Ajax

#### 1.基础原型

- 创建XMLHTTPRequest对象：var xhr = new XMLHTTPRequest();
- 打开请求：xhr.open(obj.type, obj.url, obj.async);
- 发送请求：xhr.send();
  - GET请求：传的参数为null
  - POST请求：传的参数为键=值，&来连接

- 接收数据：xhr.responseText;

#### 2.JQuery_Ajax

- 格式：$.ajax({});
- 参数：
  type:请求方式GET/POST,
  url:请求地址url,
  async:是否异步，默认是true表示异步，
  data:发送到服务器的数据，
  dataType:预期服务器返回的数据类型，'jsonp'解决GET跨域 或者 'json'
  contentType:设置请求头，
  success:请求成功时调用此函数，
  error:请求失败时调用此函数

#### 3.JQuery_Get/Post

- $.get/post(url[, data, callback], 数据类型)


# 六、Django

 ## 一、初始化（创建并启动）

### 1.安装Django

````bash
pip install django
````

### 2.创建项目（终端执行）

```bash
django-admin startproject fileweb
```

### 3.创建app（进入项目文件夹）

```bash
python manage.py startapp app
```

### 4.在settings里注册app

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app.apps.AppConfig",  # 注册app
]
```

### 5.在urls绑定URL和视图函数的关系（写一个页面）

```python
from django.urls import path, re_path as url
from app.views import user

urlpatterns = [
    path("login/", user.login_index, name="login"),
    url("^$", user.login_index),
    path("logout/", user.loginout),
]
```

```python
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login

def loginout(request):
    """实现退出登录逻辑"""
    # 清理session
    logout(request)
    # 退出登录，重定向到登录页
    return redirect("/login/")
```

### 6.启动django

```bash
python manage.py runserver
```

## 二、网页模板和静态文件

### 1.创建网页模板（templates文件夹）

>- templates
>  - login.html

### 2.创建静态文件（static文件夹）

>- static
>  - css
>  - img
>  - js
>  - plugins

### 3.网页模板里面加载静态文件（模板语法）

```html
{% load static %}
<head>
    <meta charset="UTF-8">
    <title>文件处理系统</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
```

### 4.模板继承

- 创建模板

  ```html
  <!DOCTYPE html>
  <html>
      <head>
         {% block css %}{% endblock %} 
      </head>
      <body>
          {% block content %}{% endblock content %}
          {% block js %}{% endblock js %}
      </body>
  </html>
  ```
  
  - 其他页面继承模板
  
    ```html
    {% extends "layout.html" %}
    {% block content %}
    	<dic></dic>
    {% endblock content %}
    ```
  
    

## 三、数据库操作

### 1.设置数据库连接

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 2.同步表更新到数据库

> 绑定数据库表

```python
class MyPower(models.Model):
    power = models.CharField(max_length=256, verbose_name="权限列表")
    class Meta:
        db_table = "powerlist"          # 在数据库创建表时的表名, 默认是 "应用名_模型类名"
```

- python manage.py makemigrations

- python manage.py migrate

### 3.数据库ORM操作

```python
from app.models import MyUser as User
User.objects.create(name='xxx')
User.objects.get(id=pk)
User.objects.all()
User.objects.filter(id=id).delete()
User.objects.filter(id=id).update(name='')
```

## 四、User账号密码校验

```python
from django.contrib.auth import authenticate
authenticate(username=username, password=password)
```

## 五、扩展User表

### 1.model.py

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class MyUser(AbstractUser):
      department_name = models.CharField(max_length=20, verbose_name=u'部门')
      power_list = models.CharField(max_length=256, verbose_name=u'权限')
      power_id = models.CharField(max_length=256, verbose_name=u'权限id',default=None)
```

### 2.settings.py

```python
AUTH_USER_MODEL = "app.MyUser"
ROOT_URLCONF = "fileload.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
```

### 3.admin.py

```python
from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from app.models import MyUser

ADDITIONAL_FIELDS = ((None, {'fields': ('department_name','real_name','power_list')}),)

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS
    add_fieldsets = UserAdmin.fieldsets + ADDITIONAL_FIELDS

admin.site.register(MyUser, MyUserAdmin)
```



## 六、解决Django设置debug=False静态文件获取不到的问题

1.修改settings.py文件

```
STATIC_URL = '/static/'   # 静态文件的别名
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

2.修改url.py文件

```python
from django.views import static ##新增
from django.conf import settings ##新增
from django.urls import path, re_path as url ##新增
urlpatterns = [
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
]
```

3.生成static文件夹

> 将所有的静态文件搜集到指定的`STATIC_ROOT`目录下，可以使用`python manage.py collectstatic`将静态文件收集到`STATIC_ROOT`目录下

## 七、设置csrftoken

```javascript
function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    // function csrfSafeMethod(method) {
    //     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    // }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {   //这部分也可以写在$.ajax里面
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
```

## 八、RESTFUL API

```python
from rest_framework.views import View
class PowerViews(View):
    """查询"""

    def get(self, request):
        """查询用户的权限，返回权限id"""
        if "powerList" in request.GET.keys():
            powerList = request.GET.get('powerList')
            powerId = Power.objects.values_list()
            power_id = []
            for i in powerId:
                if '导出' == i[1]:
                    continue
                temp = i[1].replace('导出-', '')
                if temp in powerList:
                    power_id.append(i[0])
            return JsonResponse(power_id)

        """查询权限表的权限"""
        power_read = Power.objects.order_by('id').values_list()
        spread_list = ['导出']
        res = [{'title': '权限管理'
                   , 'id': 0
                   , 'spread': True
                   , 'children': []}]
        for i in power_read:
            if i[1] in spread_list:
                res[0]['children'].append({'id': i[0], 'title': i[1], 'spread': True, 'children': []})
            elif i[1].split('-')[0] in spread_list:
                res[0]['children'][-1]['children'].append({'id': i[0], 'title': i[1]})
            else:
                res[0]['children'].append({'id': i[0], 'title': i[1]})
        # return HttpResponse(json.dumps({"code": 1, "res": res}))
        return JsonResponse({"code": 1, "res": res})

    """新增"""
    # @csrf_protect
    def post(self, request):
        json_dict = request.POST
        """查询权限对应的id"""
        if "powerList" in json_dict.keys():
            powerList = json_dict.get('powerList')
            powerId = Power.objects.values_list()
            power_id = []
            for i in powerId:
                if '导出' == i[1]:
                    continue
                temp = i[1].replace('导出-', '')
                if temp in powerList:
                    power_id.append(i[0])
            print(json.dumps({"code": 1, "power_id": power_id}))
            return HttpResponse(json.dumps({"code": 1, "power_id": power_id}))
        """增加权限表的权限"""
        if "key" in json_dict.keys():
            # 创建模型对象并保存
            power = Power(power=json_dict['key'])
            power.save()
            power_dict = {
                'power_id': power.id,
                'power': power.power
            }
            return JsonResponse({"code": 1, "res": power_dict})

    """修改"""
    def put(self, request):
        import urllib
        body = urllib.parse.unquote(request.body)
        data = {}
        for i in body.split('&'):
            data[i.split('=')[0]] = i.split('=')[1]
        pk = data.get('power_id')
        if data.get('power_res') == '[]':
            powerList_res = ''
            User.objects.filter(id=pk).update(power_list=powerList_res)
        else:
            powerList = data.get('power_res')
            powerList = json.loads(powerList)
            powerList_res = ''
            for i in powerList[0]['children']:
                tar = i['title']
                if 'spread' in i:
                    powerList_temp = ''
                    for j in i['children']:
                        powerList_temp += j['title'] + '，'
                    powerList_res += tar + '(' + powerList_temp[:-1] + ')' + '，'
                else:
                    powerList_res += tar + '，'
            if ')' != powerList_res[-1]:
                powerList_res = powerList_res[:-1]
            User.objects.filter(id=pk).update(power_list=powerList_res)
        user_dict = {
            'user_id': pk,
            'power_list': powerList_res
        }
        return JsonResponse(user_dict,safe=False)
```

- setting.py

  ```python
  INSTALLED_APPS = [
      "django.contrib.admin",
      "django.contrib.auth",
      "django.contrib.contenttypes",
      "django.contrib.sessions",
      "django.contrib.messages",
      "django.contrib.staticfiles",
      "app.apps.AppConfig",  # 注册app
      "rest_framework",    # 固定注册方式
  ]
  ```

  

# 七、Vue

1.Attribute 绑定 :<div v-bind:id="dynamicId"></div>，简写:id

2.事件监听：<button v-on:click="increment">{{ count }}</button>，简写@click

3.使用 `methods` 选项声明的函数

4.表单绑定：`v-model` 会将被绑定的值与 `<input>` 的值自动同步

5.条件渲染：使用 `v-if` 指令来有条件地渲染元素，也可以使用 `v-else` 和 `v-else-if` 来表示其他的条件分支

6.列表渲染：使用 `v-for` 指令来渲染一个基于源数组的列表

7.计算属性：我们可以使用 `computed` 选项声明一个响应式的属性，它的值由其他属性计算而来

8.生命周期和模板引用：通过ref属性来实现模板引用，使用mounted进行挂载组件之后执行代码的引用this.$refs

9.侦听器：响应性地执行一些“副作用”，使用 `watch` 选项来侦听属性的变化，当属性改变时，侦听回调将被调用，并且接收新值作为参数。

10.嵌套组件：

①导入子组件：import ChildComp from './ChildComp.vue'

②使用 `components` 选项注册组件：components: {    ChildComp  }

③使用组件模板：<ChildComp />

11.组件间传递动态数据：

①子组件声明所接受的props：props: {    msg: String  }

②父组件声明属性传递动态值：<ChildComp :msg="greeting" />

12.组件间触发事件：

①子组件声明事件和事件的参数

```javascript
export default {
  // 声明触发的事件
  emits: ['response'],
  created() {
    // 带参数触发
    this.$emit('response', 'hello from child')
  }
}
```

②父组件使用 `v-on` 监听子组件触发的事件

```javascript
<ChildComp @response="(msg) => childMsg = msg" />
```

13.插槽：除了通过 props 传递数据外，父组件还可以通过插槽 (slots) 将模板片段传递给子组件，`<slot>` 插口中的内容将被当作“默认”内容：它会在父组件没有传递任何插槽内容时显示



# 八、中台

数据仓库的开发：

1.架构方向：

一、数据运营层：ODS（Operational Data Store）

​	来源：业务系统数据：CRM、SAP、外部系统数据接口、工单、客户
​	方式：数据源中的数据，经过抽取、洗净、传输，也就是ETL之后写入
​	结果：数据具有业务数据库的特征，并且满足一定关系型数据库的范式，为原始业务的数据表

二、数据仓库层：DW（Data Warehouse）

	1. 数据明细层：DWD（Data Warehouse Detail）
		做一部分的数据聚合，将相同主题的数据汇集到一张表中，提高数据的可用性
	*2. 数据中间层：DWM（Data WareHouse Middle）
		对数据做轻度的聚合操作，生成一系列的中间表，提升公共指标的复用性，减少重复加工，算出相应的统计指标
	3. 数据服务层：DWS（Data WareHouse Service）
		又名数据集市或宽表，按照业务划分，如订单、名片等，生成字段比较多的宽表，用于提供后续的业务查询，OLAP分析，数据分发等，该层特点表少、表的字段较多。
		一般的做法是，在DWM层先计算出多个小的中间表，然后再拼接成一张DWS的宽表。
		三、数据应用层：ADS（Application Data Service）
		1.主要是提供给数据产品和数据分析使用的数据，一般会存放在Elasticsearch、MySQL、Redis等	uid中供数据分析和数据挖掘使用。比如我们经常说的报表数据，一般就存储在本层
		2.表命名规则：表名称 = 所处分层 + 业务主题 + 子主题 + 表含义 + 更新频率 + [分表：_0、_10]


2.技术方向：

一. 数据采集层

​	1.在离线数据采集中，建议使用DataX和Sqoop相结合。DataX适合用在数据量较小且采用非关系型数据库的场景，部署方式很简单。Sqoop适合用在数据量较大且采用关系型数据库的场景。
​	2.在实时数据采集中，对于数据库的变更数据，如MySQL的binlog、Oracle的OGG，使用Kafka Connect进行数据的实时采集，由Flink进行数据处理

二、数据计算层

​	1.数据计算采用YARN作为各种计算框架部署的执行调度平台，计算框架有MapReduce、Spark及Spark SQL、Flink、Spark MLlib等。
​	2.MapReduce是最早开源的大数据计算框架，虽然现在性能相对较差，但它的资源占用比较小
​	

	3.Spark及SparkSQL是在批处理方面拥有出色性能的成熟技术方案，适合大部分的离线处理场景。特别是在离线数据建模方面，建议使用SparkSQL进行数据处理，既能保证易用性，又能保证处理的性能。Flink是实时数据处理方面的首选，在处理的时效性、性能和易用性方面都有很大优势。
三、数据存储层

​	1.数据存储层所有的存储引擎都基于Hadoop的HDFS分布式存储，从而达到数据多份冗余和充分利用物理层多磁盘的I/O性能。在HDFS上分别搭建Hive、HBase作为存储数据库，在这两个数据库的基础上再搭建Impala、Phoenix、Presto引擎。
​	2.Hive为大数据广泛使用的离线数据存储平台，用于存储数据中台的全量数据，在建模阶段可以使用Hive SQL、Spark SQL进行数据处理和建模。
​	3.HBase为主流的大数据NoSQL，适合数据的快速实时读写。在实时数据处理时，可将数据实时保存到HBase中，并且可以从HBase中实时读取数据，从而满足数据的时效性。
​	4.Impala可以对Hive、HBase等大数据数据库进行准实时的数据分析，能满足对分析结果速度有一定要求的场景。
​	5.Phoenix是构建在HBase上的一个SQL层，能让我们用标准的JDBC API而不是HBase客户端API来创建表、插入数据和对HBase数据进行查询。Presto是一个开源的分布式SQL查询引擎，适用于交互式分析查询。
​	6.Presto支持Hive、HBase、MySQL等多种关系型和大数据数据库的查询，并且支持join表。对于对接自助分析和统一数据服务的场景，可以通过Presto来统一访问具体存储的数据库，从而达到语法统一和数据源统一。





# 九、名词记录

## 1.KISS原则

>**KISS原则**是英语 **K**eep **I**t **S**imple, **S**tupid 的[首字母缩略字](https://zh.wikipedia.org/wiki/首字母缩略字)，是一种[归纳](https://zh.wikipedia.org/wiki/歸納)过的[经验](https://zh.wikipedia.org/wiki/經驗)原则。KISS 原则是指在设计当中应当**注重简约**的原则。

## 2.DRY原则

>**Don't repeat yourself**（不要重复你自己，简称DRY），或**一个规则，实现一次**（One rule, one place）是[面向对象编程](https://zh.wikipedia.org/wiki/面向对象编程)中的基本原则，程序员的行事准则。旨在软件开发中，减少重复的信息。

## 3.TED原则

- 简洁(Terse)
- 具有表达力(Expressive)
- 只做一件事(Do one thing)

## 4.IPO

>**(IPO模型)**输入-过程-输出模式是[系统分析和](https://en.wikipedia.org/wiki/Systems_analysis)[软件工程](https://en.wikipedia.org/wiki/Software_engineering)中广泛使用的方法，用于描述信息处理程序或其他过程的结构。

## 5.UAT

>UAT，(User Acceptance Test),也就是用户验收测试，或用户可接受测试，是系统开发生命周期方法论的一个阶段。这时相关的用户或独立测试人员根据测试计划和结果对系统进行测试和接收。

## 6.BPO

>BPO即[业务流程外包](https://www.zhihu.com/search?q=业务流程外包&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2584082701})（Business Process Outsourcing），BPO是以业务结果交付为导向

## 7.SSC

>**共享服务中心（Shared Services Center，SSC）**,共享服务中心是通过对人员、技术和[流程](https://wiki.mbalib.com/wiki/流程)的有效[整合](https://wiki.mbalib.com/wiki/整合)，实现[组织](https://wiki.mbalib.com/wiki/组织)内公共流程的标准化和精简化的一种[创新](https://wiki.mbalib.com/wiki/创新)手段。
>
>共享服务是指将组织内原来分散在各业务单元进行的事务性工作和[专业服务](https://wiki.mbalib.com/wiki/专业服务)工作从原业务单元中分离出来，成立专门的部门来运作，从而实现内部服务市场化，通过为内部客户提供统一、专业、标准化的高效服务而创造价值的运作模式。
>
>共享服务实现了[组织整合](https://wiki.mbalib.com/wiki/组织整合)[资源](https://wiki.mbalib.com/wiki/资源)、提高[效率](https://wiki.mbalib.com/wiki/效率)、降低成本的目的。

## 8.SAP FICO

>FICO，是SAP中的财务模块，一块是FI（finance）模块，另一块是CO（controlling）模块，FI模块是外部会计，CO模块是管理会计

## 9.Kaizen原则

>Kaizen 原则是来自日本的一种管理方法，字面意思是“持续（Kay）改进（zen）”。
>
>最初是一个日本管理概念，指逐渐、连续地增加改善。
>
>持续改善被作为系统层面的一部分来加以应用并进行改进。通过流动和拉式系统来改进交货时间、流程的灵活性和对顾客的响应速度，改善活动从头到尾地改进了公司的进程。
>
>KAIZEN 强调以过程为主的思考方式，只有通过对过程的改善才能得到更好的结果

### 9.1	PDCA/SDCA循环

>[SDCA循环](https://wiki.mbalib.com/wiki/SDCA循环)的作用就是将现有的过程标准化并稳定下来，而[PDCA循环](https://wiki.mbalib.com/wiki/PDCA循环)的作用是改善这些过程

- 计划（Plan）就是为了达到改善的目标而制订目标或行动计划。（因为Kaizen是动态的不断完善的过程，所以目标也应不断进行更新）。
- 做（do）就是按计划执行工作。
- 检查（check）就是检验工作是否按计划被执行，并朝所预定的方向发展。
- 调整（adapt）就是指通过对新的工作步骤的标准化来避免原问题的重复发生，并为下一步的改善制订目标。

### 9.2 QCD

>质量、[成本](https://wiki.mbalib.com/wiki/成本)、交货期这三个[企业目标](https://wiki.mbalib.com/wiki/企业目标)中，质量应永远享有优先权。

### 9.3	TQM、TPM、JIT

>全面质量管理（TQM）把总的质量作为主要目标；全员生产维护（TPM）侧重于机器和设备的运行质量；而准时制（JIT）以另外两个非常重要的方面即成本和交货期为控制目标。

## 10	Lean原则

>精益开发Lean，源自精益生产。精益生产是一组原则指导，主要应用在质量、速度和客户关系。
>
>以业务线和产品线为基础，精益的规划，敏捷(Agile)的执行，这样才能最大可能的减少浪费，提高预算计划和执行的有效性。

- 1、Eliminate Waste（消除浪费）

- 2、Build Quality In（嵌入质量）

- 3、Create Knowledge（创造知识）

- 4、Defer Commitment（延迟决策）

- 5、Deliver Fast（快速交付）

- 6、Respect People（尊重他人）

- 7、Optimize the Whole（整体优化）

>不停地（无情地）消除任何不增加价值的工作。只做此刻必要的工作。消除浪费指消除没用的会议、任务和文档。也包括消除此刻不是必须的建造。
>
>消除浪费还包括消除低效的工作方式，例如多任务并行（multitasking），消除浪费才能达成快速交付。





# 十、脚本编写格式规范

## 1	注释

### 1.1	脚本注释

> 在文件最上方需写上注释有（作者，创建/修改时间，描述）

```python
"""
@Author：XX
@Description：xxxxx
@Time：2022/12/16
"""
```

### 1.2	函数注释

>**Doc Strings编写风格的一种风格：re ST风格** 

```python
def add(num1,num2):
  """ 完成传入的两个数之和

  :param num1: 加数1
  :param num2: 加数2
  :return: 和
  """
  return num1 + num2
```

### 1.3	单行注释

>单行注释可以作为单独的一行放在被注释代码行之上，也可以放在语句或表达式之后。

```python
name = 'xxx' # 单行注释

# 单行注释
name = 'xxx'
```

## 2	命名

### 2.1	函数命名

>模块名尽量短小，并且全部使用小写字母，可以使用下划线。例如：name_name

### 2.2	类命名

>类采用单词首字母大写形式（如：Pascal）

### 2.3	有意义命名

>脚本名、函数名、变量名、类名取名必须有意义，严禁用单字母

### 2.4	空行

>类与类，类与函数，函数与函数之间空两行

## 3	脚本修改流程

- 1、脚本留存

  - 修改脚本前把原文件命名为脚本名+日期后缀

  - 保存到本地备份脚本文件夹或者云盘上

- 2、追加脚本注释
- 3、导入的包需按首字母升序进行排序
- 4、函数定义（一个函数实现一个逻辑）
  - 数据库的查询函数，返回查询后的结果
    - 数据库连接的账号密码采用读取账户表
  - 处理逻辑函数，传入参数，数据处理完返回结果
  - 重复使用的语句（如：lambda函数、日期）
- 5、捕获脚本报错
  - 邮件提醒
  - 日志输出到数据库



# 十一、Python

## 1.	操作数据库

```python
import pandas as pd
import pymysql


def batch_insert(df, sql_dic):
    """
        df : pd.DataFrame
        sql_dic = {
            "host": 'xxx',
            "user": 'root',
            "passwd": 'xxx',
            "port": 33606,
            "database": 'db_datacenter',
            "table": "skill_card_crm_id",
            "batch_num": 10000
        }
    """
    batch_num = sql_dic['batch_num']
    column_temp = df.columns
    column_list = ['`' + i + '`' for i in column_temp]
    columns = ','.join(column_list)
    df = df.fillna('')
    df = df.astype(str)
    df = df.replace('', None)
    df = df.replace('NaT', None)
    df = df.replace('nan', None)
    data_list = [tuple(i) for i in df.values]
    value_count = len(data_list[0]) * "%s,"
    sql = "insert into " + sql_dic['table'] + "(" + columns + ") values (" + value_count[:-1] + ")"
    con = pymysql.Connection(host=sql_dic['host'], user=sql_dic['user'], passwd=sql_dic['passwd'], port=sql_dic['port'],
                             database=sql_dic['database'])
    data_len = len(data_list)
    for i in range(0, data_len, batch_num):
        cursor = con.cursor()
        if i + batch_num < data_len:
            j = i + batch_num
        else:
            j = data_len
        cursor.executemany(sql, data_list[i:j])
        con.commit()
        print(f"正在插入第{i}到{j}条数据")
    con.close()


def db_exec(sql, targe, sql_dic):
    """读取数据库并执行sql语句, 返回结果

    Args:
        sql (_type_): sql语句
        targe: 'fetchall',返回执行后数据
        sql_dic = {
            "host": 'xxx',
            "user": 'root',
            "passwd": 'xxx',
            "port": 33606,
            "database": 'db_datacenter',
            "table": "skill_card_crm_id",
            "batch_num": 10000
        }
    Returns:
        result _type_: 返回执行语句后DataFrame结果
    """
    for i in range(5):
        try:
            con = pymysql.Connection(host=sql_dic['host'], user=sql_dic['user'], passwd=sql_dic['passwd'],
                                     port=sql_dic['port'],
                                     database=sql_dic['database'])
            try:
                cursor = con.cursor()
                cursor.execute(sql)
                if targe == 'fetchall':
                    result = cursor.fetchall()
                    col_tuple = cursor.description
                    df = pd.DataFrame(result)
                    col_list = []
                    for i in range(len(col_tuple)):
                        col_list.append(col_tuple[i][0])
                    df.columns = col_list
                    con.close()
                    return df
                else:
                    con.commit()
                    con.close()
                break
            except:
                con.rollback()
        except Exception as e:
            print(e)


def sqlalchemy_sql():
    from sqlalchemy import create_engine
    from urllib.parse import quote_plus as urlquote
    db = create_engine(
        f"mysql+pymysql://root:{urlquote('xxx')}@xxx:33606/db_datacenter?charset=utf8")
    sql = ""
    df = pd.read_sql(sql=sql, con=db)
    df.to_sql(name='', con=db, if_exists='append', index=False)
```

## 2.qq邮箱监控发邮件

```python
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_data(html_msg):
    """发送邮件的脚本"""

    smtp_server = 'smtp.qq.com'
    username = '1732500295@qq.com'
    password = 'doevipneorqeciijx'  # 授权码，企业163的就是登陆密码

    # 邮件发送和接收人
    sender = username
    # receivers = [['vys2835@dingtalk.com']]
    receivers = [['916448718@qq.com'], ['vys2835@dingtalk.com'], ['yoyozpy718@163.com']]
    for i in receivers:
        receiver = i
        # 邮件头信息
        msg = MIMEMultipart('related')
        msg['Subject'] = Header("脚本报错")
        msg["From"] = sender
        msg['To'] = ','.join(receiver)  # 这里要注意

        # html 内容
        content_html = MIMEText(html_msg, "html", "utf-8")
        msg.attach(content_html)

        # 创建客户端，登陆，发送，关闭
        email_client = smtplib.SMTP_SSL(smtp_server, 465)
        email_client.login(username, password)
        try:
            email_client.sendmail(sender, receiver, msg.as_string())
            print('邮箱发送成功')
            email_client.quit()
        except Exception as e:
            print('邮箱发送失败')
            print(e)
            
html_msg = f"""<p>钉钉花名册脚本出现错误，数据获取出现错误，%s</p>""" % e
send_data(html_msg)
```

## 3.MYSQL

```python
import pymysql
from dbutils.pooled_db import PooledDB
import time
POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=1,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=0,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=0,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=4,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='anmat',
    charset='utf8mb4'
)


def read_mysql(db, min, max):
    while True:
        try:
            cursor = db.cursor()  # pymysql.cursors.DictCursor返回指点类型
            cursor.execute(f"select `Expediente`,`DecCertlist`,`id` from `anmat测试` where id>{min} and id<={max} and success is null")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(e)
            db.rollback()
            time.sleep(3)
        finally:
            cursor.close()


def check_null(db, min):
    cursor = db.cursor()  # pymysql.cursors.DictCursor返回指点类型
    while True:
        try:
            cursor.execute(f"select * from `table_name` where id={min}")
            result = cursor.fetchall()
            db.close()
            return result
        except Exception as e:
            print(e)
            db.rollback()
            time.sleep(3)
        finally:
            cursor.close()


def update_insert(db, data, id, num):
    # SQL 插入语句
    update_sql = f'''update `table_name` set
                    `success`={num}
                    where `id`={id}
                     '''
    insert_sql = f'''insert ignore into `table_name`(`url`)
                    values(%s)
                     '''
    while True:
        try:
            cursor = db.cursor()
            cursor.execute(insert_sql, data)
            cursor.execute(update_sql)
            # 提交到数据库执行
            db.commit()
            # 关闭数据库连接
            break
        except Exception as e:
            print(e)
            db.rollback()
            time.sleep(3)
        finally:
            cursor.close()


def update_mysql(db, id, num):
    # SQL 插入语句
    update_sql = f'''update `anmat测试` set
                    `success`={num}
                    where `id`={id}
                     '''
    while True:
        try:
            cursor = db.cursor()
            cursor.execute(update_sql)
            # 提交到数据库执行
            db.commit()
            # 关闭数据库连接
            break
        except Exception as e:
            print(e)
            db.rollback()
            time.sleep(3)
        finally:
            cursor.close()

def insert_mysql(db, data):
    # SQL 插入语句
    insert_sql = f'''insert ignore into `anmat测试`(`Tramite`,`FechaFin`,`RazonSocial`,`Nombre`,`Marca`,`Modelo`,`PM`,`Expediente`,`DecCertlist`)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                     '''
    while True:
        try:
            cursor = db.cursor()
            cursor.executemany(insert_sql, data)
            db.commit()
            break
        except Exception as e:
            print(e)
            db.rollback()
            time.sleep(3)
        finally:
            cursor.close()


def new_table():
    # 打开数据库连接
    db = POOL.connection()

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute(f"DROP TABLE IF EXISTS `anmat测试`")

    # 创建数据表SQL语句
    sql = f"""CREATE TABLE `anmat测试` (
        `id` int primary key auto_increment,
        `Tramite` varchar(128),
        `FechaFin` varchar(128),
        `RazonSocial` varchar(128),
        `Nombre` varchar(128),
        `Marca` varchar(128),
        `Modelo` text,
        `PM` varchar(128),
        `Expediente` varchar(128),
        `DecCertlist` text,
        `success` int
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"""
    cursor.execute(sql)
    db.close()
    
######################################将CSV文件内容存入数据库#############################################
#首先导入PyMySQL库
import pymysql
# 建立连接
conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='123456')
# 自动确认commit True
conn.autocommit(1)
# 设置光标
cursor = conn.cursor()

# 一个根据pandas自动识别type来设定table的type
def make_table_sql(df):
    columns = df.columns.tolist()
    types = df.dtypes
    # 添加id 制动递增主键模式
    make_table = []
    for col in columns:
        if 'int' in str(df[col].dtype):
            char = col + ' INT'
        elif 'float' in str(df[col].dtype):
            char = col + ' FLOAT'
        elif 'object' in str(df[col].dtype):
            char = col + ' VARCHAR(255)'
        elif 'datetime' in str(df[col].dtype):
            char = col + ' DATETIME'          
        make_table.append(char)
    return ','.join(make_table)

# csv 格式输入 mysql 中
def csv2mysql(db_name, table_name, df):
    # 创建database
    cursor.execute('CREATE DATABASE IF NOT EXISTS {}'.format(db_name))
    # 选择连接database
    conn.select_db(db_name)
    # 创建table
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    data_sql = 'CREATE TABLE %s (%s)'%(table_name,make_table_sql(df))
    cursor.execute(data_sql)
    values = df.values.tolist()
    # 根据columns个数
    s = ','.join(['%s' for _ in range(len(df.columns))])
    # executemany批量操作 插入数据 批量操作比逐个操作速度快很多
    cursor.executemany('INSERT INTO {} VALUES ({})'.format(table_name,s), values)
    
path = 'result.csv'
df2 = pd.read_csv(path)
df1 = df2.astype(object).where(pd.notnull(df2), None)
csv2mysql(db_name='test', table_name='movie', df=df1)

```



## 4.重试装饰器

```python
import time

def retry(times=5):
    def wrapper(func):
        def decorator(*args, **kwargs):
            t = 0
            while t < times:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"===出错了！重试:{t+1}次,{e}")
                    # raise Exception
                finally:
                    time.sleep(1)
                    t += 1
        return decorator
    return wrapper

```

## 5.滑块逆向

>main.py
>
>```python
>
>import requests
>import time
>import re 
>import json
>import cv2
>import numpy as np
>import math
>import random
>import execjs
>
>session = requests.Session()
>
>def retry(times=5):
>    def wrapper(func):
>        def decorator(*args, **kwargs):
>            t = 0
>            while t < times:
>                try:
>                    result = func(*args, **kwargs)
>                    return result
>                except Exception as e:
>                    print(e)
>                    raise Exception
>                finally:
>                    time.sleep(1)
>                    t += 1
>        return decorator
>    return wrapper
>
>@retry()
>def get_parms():
>    """
>        获取滑块的参数和图片链接
>    """
>    #step1 不同网站的第三代极验一个步骤和第二步骤一般请求不同
>    t=int(time.time()*1000)
>    url = "https://www.geetest.com/demo/gt/register-slide"
>    headers = {
>    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
>    }
>    params = (
>    ('t', t),
>    )
>    response = session.get(url, headers=headers, params=params,timeout=8).json()
>    challenge = response['challenge']
>    gt = response['gt']
>
>    #step2
>    # session=requests.session()
>    t=int(time.time()*1000)
>    headers = {
>    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
>    }
>    url = "https://apiv6.geetest.com/gettype.php"
>    params = {
>        'gt': gt,
>        'callback': f'geetest_{t}'
>    }
>    response = session.get(url, params=params, headers=headers,timeout=8)
>
>    #step3  
>    t=int(time.time()*1000)
>    url = "https://apiv6.geetest.com/get.php"
>    params = {
>        'gt': gt,
>        'challenge': challenge,
>        'lang': 'zh-cn',
>        'pt': '0',
>        'client_type': 'web',
>        'w': '',
>        'callback': f'geetest_{t}'
>    }
>    response = session.get(url, params=params, headers=headers,timeout=8)
>
>    #step4
>    # time.sleep(10)
>    t=int(time.time()*1000)
>    url = "https://api.geetest.com/ajax.php"
>    params = {
>        'gt': gt,
>        'challenge': challenge,
>        'lang': 'zh-cn',
>        'pt': '0',
>        'client_type': 'web',
>        'w': '',
>        'callback': f'geetest_{t}'
>    }
>    response = session.get(url, params=params, headers=headers,timeout=8)
>    print(response.text)
>
>    #step5
>    t=int(time.time()*1000)
>    headers = {
>    'Connection': 'keep-alive',
>    'Pragma': 'no-cache',
>    'Cache-Control': 'no-cache',
>    'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
>    'sec-ch-ua-mobile': '?0',
>    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
>    'sec-ch-ua-platform': '"Windows"',
>    'Accept': '*/*',
>    'Sec-Fetch-Site': 'cross-site',
>    'Sec-Fetch-Mode': 'no-cors',
>    'Sec-Fetch-Dest': 'script',
>    'Referer': 'https://www.qixin.com/',
>    'Accept-Language': 'zh-CN,zh;q=0.9',
>    }
>    url = "https://api.geetest.com/get.php"
>    params = (
>        ('is_next', 'true'),
>        ('type', 'slide3'),
>        ('gt', gt),
>        ('challenge', challenge),
>        ('lang', 'zh-cn'),
>        ('https', 'false'),
>        ('protocol', 'https://'),
>        ('offline', 'false'),
>        ('product', 'embed'),
>        ('api_server', 'api.geetest.com'),
>        ('isPC', 'true'),
>        ('autoReset', 'true'),
>        ('width', '100%'),
>        ('callback', f'geetest_{t}'),
>    )
>    response = session.get(url, params=params, headers=headers,timeout=8)
>    content = re.findall('.*?\((.*?)\)',response.text)[0]
>    content = json.loads(content)
>    c = content['c']
>    s = content['s']
>    challenge_f = content['challenge']
>    gt = content['gt']
>    bg_pic = 'https://static.geetest.com/'+content['bg']
>    slice_pic = 'https://static.geetest.com/'+content['slice']
>    fullbg_pic = 'https://static.geetest.com/'+content['fullbg']
>    # result_list = [c,s,bg_pic,slice,fullbg_pic]
>    return c,s,challenge_f,gt,bg_pic,slice_pic,fullbg_pic
>
>def save_pic(pic_path):
>    if pic_path.find('bg')>-1:
>        pic_name='bg'+pic_path[-4:]
>    elif pic_path.find('slice')>-1:
>        pic_name='slice'+pic_path[-4:]
>    else:
>        pic_name='fullbg'+pic_path[-4:]
>    response = requests.get(pic_path).content
>    with open(pic_name,'wb') as f:
>        f.write(response)
>    print(f'图片文件{pic_name}保存成功')
>
>def bg_true(pic_read):
>    #pic_read   读取的图片
>    pic_write=pic_read.split('.')[0]+'_true.'+pic_read.split('.')[1]  #保存转换后的图片
>    #转换的逻辑顺序
>    true_cut=[39,38,48,49,41,40,46,47,35,34,50,51,33,32,28,29,27,26,36,37,31,30,44,45,43,42,12,13,23,22,14,15,21,20,8,9,25,24,6,7,3,2,0,1,11,10,4,5,19,18,16,17]
>    # 读取背景图片和缺口图片
>    img = cv2.imread(pic_read) # 背景图片
>    img_arr = np.array(img)
>    img_l=26 #长切割为多少快
>    img_w=2 #宽切割为多少快
>    w_cut=int(img_arr.shape[0]/img_w) 
>    l_cut=int(img_arr.shape[1]/img_l) 
>
>    sum_cut=[]
>    for w in range(img_w):
>        for l in range(img_l):
>            img_cut=img_arr[w*w_cut:(w+1)*w_cut,l*l_cut:(l+1)*l_cut,:]
>            sum_cut.append(img_cut)
>
>    true_sum=[]
>    for i in true_cut:
>        true_sum.append(sum_cut[i])
>
>    # true_arr=np.array(true_sum)
>
>    img_list=[]
>    for w in range(img_w):
>        img_v=cv2.hconcat(true_sum[w*img_l:(w+1)*img_l])
>        img_list.append(img_v)
>
>    img_true=cv2.vconcat(img_list)
>    cv2.imwrite(pic_write,img_true)
>
>    # cv2.imshow(pic_read,img)
>    # cv2.imshow(pic_write,img_true)
>    # cv2.waitKey(0) #0为无限等待，27为Ecs退出键
>    # cv2.destroyAllWindows() #摧毁全部窗口
>    print('背景图片还原完成')
>
>def get_distance(pic_read,pic_read1):
>    #pic_read   # 读取背景图片
>    #pic_read1  # 读取缺口图片
>    pic_write='match.png'   # 保存匹配最优图
>
>    bg_img = cv2.imread(pic_read) # 背景图片
>
>    tp_img = cv2.imread(pic_read1) # 缺口图片
>
>    # tp_h = int(tp_img.shape[1]/2)
>
>
>    result_list=[]
>    for i in range(100,500,20): #300,350
>        # 识别图片边缘
>        bg_edge = cv2.Canny(bg_img, i, i+50)
>        tp_edge = cv2.Canny(tp_img, i, i+50)
>        # 转换图片格式
>        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
>        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
>
>        # cv2.imshow(pic_read+pic_write,bg_img)
>        # cv2.imshow(pic_read,bg_pic)
>        # cv2.imshow(pic_write,tp_pic)
>        # cv2.waitKey(0) #0为无限等待，27为Ecs退出键
>
>        # 缺口匹配
>        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
>        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 寻找最优匹配
>        result_list.append([res.max(),max_loc])
>
>    #取最优参数
>    maxx=0
>    for i in result_list:
>        if i[0]>maxx:
>            maxx=i[0]
>            max_loc=i[1]
>
>    # 绘制方框
>    th, tw = tp_pic.shape[:2]
>    tl = max_loc # 左上角点的坐标
>    br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
>    # print(f'左上角的坐标为{tl},右上角的坐标为{br}')
>
>    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形
>    # cv2.imshow(pic_write,bg_img)
>    cv2.imwrite(pic_write,bg_img)
>    # cv2.waitKey(0)
>    # cv2.destroyAllWindows() #摧毁全部窗口
>    print('计算距离完成，已保存最优匹配缺口图，返回坐标')
>    return tl[0] 
>
>
>def get_trace(slice_x,bg_true_pic,slice_pic):
>    # slice_x = 15
>    cv2_bg = cv2.imread(bg_true_pic)
>    bg_s = cv2_bg.shape[1]
>    cv2_slice = cv2.imread(slice_pic)
>    slice_s = cv2_slice.shape[1]
>    max_s = bg_s - slice_s
>    sum_t = 3000    #滑块移动的最大毫秒数
>    
>    slice_x_1 = slice_x / max_s    #归一化：最大最小化
>    slice_t_1 = math.log(slice_x_1/(1-slice_x_1))    #sigmoid函数求解t
>    slice_t_1 = (slice_t_1-(-6))/(6-(-6))    #求t在[-6,6]的缩放
>    slice_t = int(sum_t*slice_t_1)    #轨迹移动的总时长ms
>
>    slice_T_0 = [random.randint(-35,-31),random.randint(-35,-31),0]
>    slice_T = [slice_T_0,[0,0,0]]
>    random_t = random.randint(100,180) #每一次滑动后的总时间，这里是第一次点击滑块的时间
>    random_x = 0
>    while random_t < slice_t and random_x < slice_x:
>        random_add_t = random.randint(7,20) #每次滑动的时间间隔
>        random_t += random_add_t
>        random_t_1 = 12*random_t/slice_t-6
>        slice_x_t = math.ceil(1/(1+math.exp(-random_t_1))*slice_x)  #sigmoid函数求解y
>        if slice_x_t > random_x:
>            random_x = slice_x_t    
>            slice_T.append([slice_x_t,0,random_t])
>    random_add_t = random.randint(800,1200) #每次滑动的时间间隔
>    random_t += random_add_t
>    slice_T.append([slice_x_t,0,random_t])
>    # print(slice_T)
>    return slice_T
>
>
>@retry()
>def get_finall(w,gt,challenge):
>    t=int(time.time()*1000)
>    headers = {
>        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
>    }
>
>    params = (
>        ('gt', gt),
>        ('challenge', challenge),
>        ('lang', 'zh-cn'),
>        ('$_BBF', '0'),
>        ('client_type', 'web'),
>        ('w', w),
>        ('callback', f'geetest_{t}'),
>    )
>    print(params)
>    response = session.get('https://api.geetest.com/ajax.php', headers=headers, params=params,timeout=8)
>    return response.text
>
>
>if __name__ == '__main__':
>    c,s,challenge_f,gt,bg_url,slice_url,fullbg_url = get_parms()
>    for pic_path in [bg_url,slice_url,fullbg_url]:
>        save_pic(pic_path)
>
>    bg_pic='bg.jpg'     #背景缺口图
>    bg_true(bg_pic)     #还原背景图函数
>
>    bg_true_pic = 'bg_true.jpg'    #背景缺口还原图
>    slice_pic = 'slice.png'    #滑块图
>    distance_s = get_distance(bg_true_pic,slice_pic)
>    print(distance_s)
>    t = get_trace(distance_s,bg_true_pic,slice_pic)
>    print(t)
>
>    with open('w.js','r',encoding='utf-8') as f:
>        js_code = f.read()
>
>    imgload = random.randint(47,80)
>    w = execjs.compile(js_code).call('get_w',t,c,s,gt,challenge_f,imgload)
>    print(len(w))
>
>    result = get_finall(w,gt,challenge_f)
>    print(result)
>
>        
>```
>
>

## 6.matplotlib

```python
import matplotlib.pyplot as plt
##########画图格式：黑体、正常显示负号##########
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus']=False

def display(x,y):
    plt.figure(figsize=(6, 4))  #图片的大小
    plt.plot(x, y, 'g-', label='function')  #颜色符号g-、bo、r*，label标签
    plt.title('solution = {}'.format(x))  #标题
    plt.xlabel('x')   #x轴标签
    plt.ylabel('y')   #y轴标签
    plt.legend()      #呈现画布
    plt.savefig('SA.png', dpi=500)   #保存图片
    plt.show()      #画出图片
    plt.close() 
    
def plt_line(name,pred,true,path):
    plt.figure(figsize=(20, 10),edgecolor='white',facecolor='white')
    plt.plot(pred, '-', label="Predicted", color="blue", linewidth=5,markersize=5)
    plt.plot(true, '--', label="Real", color="red", linewidth=5,markersize=5)
    plt.title(name)
    plt.legend()
    plt.ylabel("ylabel")
    plt.grid()
    path1 = "./result/" + path + "/"
    if(os.path.exists(path1)):
        pass
    else:
        mkdir(path1)
    path2 = path1  + name + ".pdf"
    plt.savefig(path2)
    plt.show()
    
######预测时序时画的图########
pred_test = pred_test.reshape(-1,1)
sample_n = pred_test.shape[0]
feature_n = x_test.shape[1]
a3=calculate(y_test,pred_test,sample_n,feature_n)

plt.figure(figsize=(20, 10))
plt.plot(np.arange(1,len(y_test)+1),y_test, 'r-',label='Test')
plt.plot(np.arange(1,len(pred_test)+1),pred_test, 'g-',label='pred_test')
plt.legend(loc='best')
plt.show()

plt.xlabel('pred_test')
plt.ylabel('y_test')
plt.scatter(pred_test,y_test,marker='.')
plt.show()
```

## 7.seaborn

```python
import seaborn as sns
############直方图、用皮尔逊相关系数计算#############
sns.distplot(df_train.corr()['y'].values,label="pearson",bins=20)
#######提取相关系数大于0.5的特征##################
a=df_train.corr()['y']
b=a[a >=0.5 ].index.tolist()
#######各特征相关系数图##################
sns.heatmap(q.corr(), xticklabels=q.corr().columns, yticklabels=q.corr().columns, cmap='RdYlBu', center=0, annot=True,
            square=True, linewidths=.5,#每个方格外框显示，外框宽度设置
            cbar_kws={"shrink": .5})
plt.title('features of top 10', fontsize=22)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()
############自带颜色的直方图##########
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
sns.barplot(x=x,y=y)
plt.xlabel("model")
plt.plot(x,y,'*-')
```

## 8.sklearn

```python
##############归一化####################
from sklearn.preprocessing import MinMaxScaler
mm = MinMaxScaler()
mm_xdata = mm.fit_transform(df_train.drop(['y'],axis=1))
mm_ydata = mm.fit_transform(df_test.drop(['y'],axis=1))
# origin_data = mm.inverse_transform(mm_data)

x=pd.DataFrame(mm_xdata,index=df_train.drop(['y'],axis=1).index,columns=df_train.drop(['y'],axis=1).columns)
x_train=x.drop(['y'],axis=1)
y_train=x['y'].values.reshape(1,-1)[0]
##############评估指标####################################
from sklearn.metrics import mean_absolute_error,mean_squared_error,median_absolute_error,r2_score,mean_squared_log_error
def calculate(y_true, y_predict, n, p):
    y_true = y_true
    y_predict = y_predict
    mse = mean_squared_error(y_true, y_predict)
    rmse = np.sqrt(mean_squared_error(y_true, y_predict))
    mae = mean_absolute_error(y_true, y_predict)
    r2 = r2_score(y_true, y_predict)
    mad = median_absolute_error(y_true, y_predict)
    mape = np.mean(np.abs((y_true - y_predict) / y_true)) * 100
    r2_adjusted = 1-((1-r2)*(n-1))/(n-p-1)
    print('MSE: ', mse)
    print('RMSE: ', rmse)
    print('MAE: ', mae)
    print('R2: ', r2)
    print('MAD:', mad)
    print('MAPE:', mape)
    print('R2_Adjusted: ',r2_adjusted)
    return mse,rmse,mae,r2,mad,mape,r2_adjusted
```

## 9.selenium

```python
###################无界面有头请求#################
def webdriver(url):
    import time
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')

    driver = Chrome(options=chrome_options)

    with open('./stealth.min.js') as f:         #导入本地js文件
        js = f.read()

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": js
    })

    driver.get(url)    #请求网页
    time.sleep(10)    #等待页面加载
    
    # driver.save_screenshot('a.png')  #截图页面
    source = driver.page_source   #保存网页源码
    path='./path/'
    with open(path,'w',encoding='utf-8') as f:
        f.write(source)
    driver.quit()    #退出网页
    
#############滑动网页最外层滑动条#################
browser=driver
js = "var q=document.getElementsByClassName('sOh CrmLxe')[0].scrollTop = 1000"
browser.execute_script(js)
time.sleep(2)
#############滑动网页内层滑动条#################
browser.execute_script("window.scrollBy(0,500)")
js1 = "var q=document.getElementsByClassName('sOh CrmLxe')[0].scrollTo(0,0)"
browser.execute_script(js1)
#############用css选择器选取节点#################
a=browser.find_element_by_css_selector('#yDmH0d > c-wiz > div > div.FVeGwb.ARbOBb > div.BP0hze > div.y3767c > div > div > div.dzRe8d.pym81b > div > div.sOh.CrmLxe > table > thead > tr > th.oyBoPe.L8R3fc.Q3JyKe.qCOQbc.NmDtHe')
a.click()   #点击
time.sleep(2)
browser.execute_script(js)
```







# 十二、小工具

## 1.激活FinalShell

```java

import java.io.IOException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Scanner;


public class FinalShell {
    public static void main(String[] args) throws NoSuchAlgorithmException, IOException {
        System.out.print("请输入FinalShell的离线机器码：");
        Scanner reader = new Scanner(System.in);
        String machineCode = reader.nextLine();
        reader.close();
        generateKey(machineCode);
    }

    public static void generateKey(String hardwareId) throws NoSuchAlgorithmException {
        String proKey = transform(61305 + hardwareId + 8552);
        String pfKey = transform(2356 + hardwareId + 13593);
        System.out.println("高级版激活码：请将此行复制到离线激活中：" + proKey);
        System.out.println("专业版激活码："+pfKey);
    }

    public static String transform(String str) throws NoSuchAlgorithmException {

        // String md5 = hashMD5(str);

        return hashMD5(str).substring(8, 24);
    }

    public static String hashMD5(String str) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hashed = digest.digest(str.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : hashed) {
            int len = b & 0xFF;
            if (len < 16) {
                sb.append("0");
            }
            sb.append(Integer.toHexString(len));
        }
        return sb.toString();
    }
}
```



## 2.搭建青龙面板

```bash
#######################一键安装docker###############################
curl -sSL https://get.daocloud.io/docker | sh
systemctl enable docker # 开机自动启动docker
systemctl start docker # 启动docker
systemctl restart docker # 重启dokcer
#搭建青龙面板
docker pull whyour/qinglong:latest
docker run -dit \
  -v $PWD/ql/config:/ql/config \
  -v $PWD/ql/log:/ql/log \
  -v $PWD/ql/db:/ql/db \
  -v $PWD/ql/repo:/ql/repo \
  -v $PWD/ql/raw:/ql/raw \
  -v $PWD/ql/scripts:/ql/scripts \
  -v $PWD/ql/jbot:/ql/jbot \
  -v $PWD/ql/ninja:/ql/ninja \
  -p 5700:5700 \
  -p 5701:5701 \
  --name qinglong \
  --hostname qinglong \
  --restart unless-stopped \
  whyour/qinglong:latest

#拉库
docker exec -it qinglong ql repo https://githubfast.com/KingRan/KR.git "jd_|jx_|jdCookie" "activity|backUp" "^jd[^_]|USER|utils|function|sign|sendNotify|ql|JDJR"

######################################搭建ck登录#https://github.com/heiren001/jichi_ninja
docker exec -it qinglong bash
git clone https://githubfast.com/heiren001/jichi_ninja.git /ql/ninja
cd /ql/ninja/backend
pnpm install
cp .env.example .env # 如有需要, 修改.env
pm2 start
cp sendNotify.js /ql/scripts/sendNotify.js
在青龙面板里面配置文件extra.sh增加代码自动拉取
cd /ql/ninja/backend
git checkout .
git pull
pnpm install
pm2 start
cp sendNotify.js /ql/scripts/sendNotify.js

#####################搭建短信获取ck#https://github.com/Serendipper-1/DG-SMS-1-1
mkdir jd-qinglong && cd jd-qinglong
wget -O env.properties https://ghproxy.com/https://raw.githubusercontent.com/rubyangxg/jd-qinglong/master/env.template.properties
sudo docker pull rubyangxg/jd-qinglong

sudo docker run -d -p 5702:8080 --name=webapp --privileged=true \
-v "$(pwd)"/env.properties:/env.properties:ro \
-v "$(pwd)"/go-cqhttp:/go-cqhttp \
rubyangxg/jd-qinglong


####################京东短信自动登录#################https://wep.vipyshy.com/2461.html
bash <(curl -s -S -L https://maiark-1256973477.cos.ap-shanghai.myqcloud.com/kiss.sh)
#####打开防火墙#https://blog.csdn.net/Lucianklx/article/details/125147876
firewall-cmd --zone=public --add-port=8080/tcp --permanent
systemctl restart firewalld.service
firewall-cmd --reload




#########安装谷歌浏览器###########################
cd /
cd etc/yum.repos.d
vim google-chrome.repo

#写入的内容
[google-chrome] 

name=google-chrome 

baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch 

enabled=1

gpgcheck=1 

gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
#下载
yum -y install google-chrome-stable --nogpgcheck
##################################################

#解决Could not resolve host: ghproxy.com 网络问题
route
添加接口信任
sudo firewall-cmd --permanent --zone=trusted --add-interface=docker0
sudo firewall-cmd --reload

# 添加允许ip地址伪装
sudo firewall-cmd --add-masquerade --permanent
sudo firewall-cmd --reload

# 开启端口转发功能
修改/etc/sysctl.conf的net.ipv4.ip_forwar为1：
# 如没有字段：
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf
```

# 十三、大数据

## 1.简介

### 1.1  HDFS定义

HDFS（Hadoop Distributed File System），它是一个文件系统，用于存储文件，通过目录树来定位文件；其次，它是分布式的，由很多服务器联合起来实现其功能，集群中的服务器有各自的角色。

HDFS的使用场景：适合一次写入，多次读出的场景。一个文件经过创建、写入和关闭之后就不需要改变。

### 1.2	HDFS写数据流程

（1）客户端通过Distributed FileSystem模块向NameNode请求上传文件，NameNode检查目标文件是否已存在，父目录是否存在。

（2）NameNode返回是否可以上传。

（3）客户端请求第一个 Block上传到哪几个DataNode服务器上。

（4）NameNode返回3个DataNode节点，分别为dn1、dn2、dn3。

（5）客户端通过FSDataOutputStream模块请求dn1上传数据，dn1收到请求会继续调用dn2，然后dn2调用dn3，将这个通信管道建立完成。

（6）dn1、dn2、dn3逐级应答客户端。

（7）客户端开始往dn1上传第一个Block（先从磁盘读取数据放到一个本地内存缓存），以Packet为单位，dn1收到一个Packet就会传给dn2，dn2传给dn3；dn1每传一个packet会放入一个应答队列等待应答。

（8）当一个Block传输完成之后，客户端再次请求NameNode上传第二个Block的服务器。（重复执行3-7步）。

### 2.1	MapReduce定义

MapReduce是一个分布式运算程序的编程框架，是用户开发“基于Hadoop的数据分析应用”的核心框架。

MapReduce核心功能是将用户编写的业务逻辑代码和自带默认组件整合成一个完整的分布式运算程序，并发运行在一个Hadoop集群上。
