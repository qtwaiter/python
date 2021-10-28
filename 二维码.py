

from MyQR import myqr #MyQR 制作二维码 从库中调用一个方法 方法是用来生成二维码
# 库的使用 公式：叫库名 + 点 点后面跟上方法 mypr.run
# myqr.run(words='I love you') # run 个性化 需要在括号里设置东西
txt_1 = 'https://youtu.be/E2X1DHeWTT4'
img_1 = '../../../Downloads/ylzx.png'
img_2 = '../../../Downloads/color_code.png'
myqr.run(words=txt_1, picture=img_1, colorized=True, save_name=img_2)
# words 你扫了二维码 出现的页面 可以文字，网址， 扫完出现网址
# picture 二维码长啥样
# 变成彩色的参数 colorized 默认是黑白的
# 自定义文件名 save_name 后面可以定义你生成的二维码名字以及在哪里

