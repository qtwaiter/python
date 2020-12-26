# 寄送139邮箱邮件的程序
# 准备通讯模块设定
import email.message
msg = email.message.EmailMessage()
msg["From"] = "qtwaiter@139.com"
msg["To"] = "qtwaiter@gmail.com"
msg["Subject"] = "测试python发邮件"
# 寄送纯文字的内容
msg.set_content("这是一封来自139邮箱由python程序自动发送的邮件")
# 寄送多样式内容(html)
# msg.add_alternative("<H3>优惠券</H3>满五百送二百哦", subtype="html")
# 连线到SMTP SERVER,验证寄件人身份并发送邮件
import smtplib
# 到网上搜索Email的服务器设定
server = smtplib.SMTP_SSL("smtp.139.com", 465)
server.login("13906782249@139.com", "Password")
server.send_message(msg)
server.close()
