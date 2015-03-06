# 史记注译

## 文本来源
[子夜星的注释本史记](http://www.ziyexing.com/files-5/shiji/shiji_index.htm)

## 制作方法
+ 制作带弹出式注释的epub电子书，适用于多看系统

  `python3 generate.py` 或者是 `python3 generate.py -t duokan` 在当前目录下生成目标文件`shiji.epub`。

+ 制作带弹出式注释的mobi电子书，适用于原生的Kindle系统

  `python3 generate.py -t kindle` 在当前目录下生成目标文件`shiji.epub`。再使用Calibre将EPUB格式转化为MOBI格式。

## 需要用到的工具
python3, pandoc, calibre(用于将EPUB转换为MOBI)

## 版权申明
所有文本搜集自网络。
