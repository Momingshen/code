$(function () {
    layui.use(['upload', 'element', 'layer', 'table', 'laydate'], function () {

var $ = layui.jquery
            , upload = layui.upload
            , element = layui.element
            , layer = layui.layer;
        //文件上传
        var uploadListIns = upload.render({
            elem: '#testList'
            , elemList: $('#demoList') //列表元素对象
            , url: '/upload/list/' //此处用的是第三方的 http 请求演示，实际使用时改成您自己的上传接口即可。
            , accept: 'file'
            , multiple: true
            , number: 3
            , auto: false
            , bindAction: '#testListAction'
            , choose: function (obj) {

                var that = this;
                var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
                //读取本地文件
                obj.preview(function (index, file, result) {
                    $("#result")[0].innerHTML = "请点击开始上传，若上传进度条完成后还未提示，为文件正在数据清洗中";
                    var tr = $(['<tr id="upload-' + index + '">'
                        , '<td>' + file.name + '</td>'
                        , '<td>' + (file.size / 1014).toFixed(1) + 'kb</td>'
                        , '<td><div class="layui-progress" lay-filter="progress-demo-' + index + '"><div class="layui-progress-bar" lay-percent=""></div></div></td>'
                        , '<td>'
                        , '<button class="layui-btn layui-btn-xs demo-reload layui-hide">重传</button>'
                        , '<button class="layui-btn layui-btn-xs layui-btn-danger demo-delete">删除</button>'
                        , '</td>'
                        , '</tr>'].join(''));

                    //单个重传
                    tr.find('.demo-reload').on('click', function () {

                        obj.upload(index, file);

                    });

                    //删除
                    tr.find('.demo-delete').on('click', function () {
                        delete files[index]; //删除对应的文件
                        tr.remove();
                        uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
                    });

                    that.elemList.append(tr);
                    element.render('progress'); //渲染新加的进度条组件

                    // document.getElementById("result").innerHTML = "";
                });
            }
            , done: function (res, index, upload) { //成功的回调
                var that = this;
                if (res['code'] == 1) {
                    if (res['result_code'] == "") {
                        $("#result")[0].innerHTML = "请上传正确的文件格式";
                    } else if (res['result_code'].indexOf('清洗成功') > -1) {
                        $("#result")[0].innerHTML = "上传成功------->" + res['result_code'];
                    } else {
                        $("#result")[0].innerHTML = "清洗出错------->" + res['result_code'];
                    }
                    // console.log(res)
                }
                // console.log(res)
                //if(res.code == 0){ //上传成功
                var tr = that.elemList.find('tr#upload-' + index)
                    , tds = tr.children();
                tds.eq(3).html(''); //清空操作
                delete this.files[index]; //删除文件队列已经上传成功的文件
                return;
                //}
                this.error(index, upload);
            }
            , allDone: function (obj) { //多文件上传完毕后的状态回调

                // console.log(obj)
                // alert("清洗并导入数据库完成")


            }
            , error: function (index, upload) { //错误回调
                var that = this;
                var tr = that.elemList.find('tr#upload-' + index)
                    , tds = tr.children();
                tds.eq(3).find('.demo-reload').removeClass('layui-hide'); //显示重传
            }
            , progress: function (n, elem, e, index) { //注意：index 参数为 layui 2.6.6 新增
                element.progress('progress-demo-' + index, n + '%'); //执行进度条。n 即为返回的进度百分比
            }
        });

    });
});




$("#upload_tag").click(
    function () {
        $("#download_content")[0].style.display = 'none';
        $("#people_content")[0].style.display = 'none';
        $("#dituContent")[0].style.display = 'none';
        $("#upload_content")[0].style.display = 'block';

    }
)
$("#empower").click(
    function () {
        $("#upload_content")[0].style.display = 'none';
        $("#download_content")[0].style.display = 'none';
        $("#dituContent")[0].style.display = 'none';
        $("#people_content")[0].style.display = 'block';

    }
)

$("#top_logo").click(
    function () {
        $("#upload_content")[0].style.display = 'none';
        $("#people_content")[0].style.display = 'none';
        $("#download_content")[0].style.display = 'none';
        $("#dituContent")[0].style.display = 'none';
    }
)
$("#catchCat").click(
    function () {
        $("#upload_content")[0].style.display = 'none';
        $("#people_content")[0].style.display = 'none';
        $("#download_content")[0].style.display = 'none';
        $("#dituContent")[0].style.display = 'block';
    }
)

