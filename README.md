# 史记注译

## 文本来源
[子夜星的注释本史记](http://www.ziyexing.com/files-5/shiji/shiji_index.htm)

## 制作方法
1. 收集史记文本
2. `python3 convert.py`生成`shiji.md`
3. `pandoc shiji.md -o shiji.epub`生成`shiji.epub`（带有跳转式注释）
4. 解压`shiji.epub`,在解压后的目录下`python3 replace.py`生成带有弹出式注释的史记
5. 使用`calibre`的编辑功能调整css, 封面等细节

## 需要用到的工具
python3, pandoc, calibre

## 版权申明
所有文本搜集自网络。
