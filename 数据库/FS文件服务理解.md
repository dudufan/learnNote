##Mstp-FS 大致上传流程
- 解析multipart参数到requestParamsMap，同时保存上传的文件到磁盘（临时文件）
请求主要参数有params参数（字符串），文件流，
- 解析params参数到 requestParamsMap
主要参数有文件md5值，缩略图策略
- 根据md5值在gridfs中检索文件
找到文件直接返回object_id
未找到继续
- 保存文件到gridfs中
得到rawFIleId(object_id)
- 存储缩略图
若缩略图不存在，将rawFileId作为parentId字段，同时保存缩略图imgPolicy
##朋友圈缩略图处理
首先windows安装GraphicsMagick


##Mstp非断点下载流程
- 请求体 原始文件id:objectid imgPolicy
- 解析参数 不同于上传请求的multipartstreamparser，而是普通参数解析
    未加密  request.getParameter(key)
    参数加密 得到sercretKey密文秘钥 ==> secretKey 明文秘钥字节流，解密

主要参数有文件id，请求缩略图时有imPolicy
- 根据rawFileId检索文件元数据
    如果请求源图（imgPolicy空），直接检索rawFileId

    如果请求缩略图，把rawFileId当做parentId，同时使用imgPolicy字段检索
- 响应。附件形式返回文件流
    首先设置Content-Type：application/octet-stream

         设置Accpet-Ranges:bytes

         设置Content-Dispositon:attachment:filename=xxx

     得到response的outputStream
    普通下载或 断点下载
    ###普通下载

    设置Content-Length为gridFSDBFile.getLength()

    根据rawFileId得到gridFSDBFile.writeTo(outputStream), 可以选择加密
    更新该文件下载次数等统计字段





得到图像信息

gm identify -format "width=%w\nheight=%h" D:\test.jpg
gm identify -format "width=%w\n%[EXIF:*]" D:\test.jpg

gm identify -format "width=%w\n%[EXIF:Orientation]" D:\test.jpg



快速生成缩略图
gm convert -sample "200x200" -quality 50 -rotate 90 D:\test.jpg D:testThumb1.jpg


##请求解密
- 从请求体中得到
     REQ_PARAM_CIPHER_TEXT键值对应的加密参数文本
    REQ_PARAM_SHARD_SK_CIPER 共享秘钥(密文）
- 得到共享秘钥（明文)
     从session中查询共享秘钥（明文）SESSION_SHARD_SK，
    若 找到则返回
    若未找到，在秘钥缓存队列中找明文秘钥
         若秘钥队列中有，返回

         若秘钥队列中没有， 解密出秘钥明文放入skQueue
     秘钥明文放入 session   
- symetricDecode调用cryptDecrype进行对称算法解密


##文件解密
使用共享秘钥byte[]（明文）和文件输入流初始化 CipherInputStream，写入buffer，再写入目标文件（临时生成一个路径）