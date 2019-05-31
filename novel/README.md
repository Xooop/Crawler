## 监听小说更新
小说更新时，会自动发邮件到邮箱中，提醒小说已更新.

目前监听的是www.biquge5.com这个网站（如果这个网站上找不到的小说，就搞不了233）

### 环境
- pyyaml
- selenium
- yagmail
- cn2an(要求python3.6+）

### 使用
```python
# 发送邮件的邮箱配置
user = "" # xxx@qq.com(其他邮箱请对应修改smtp服务器)
password = "" # 邮箱密码
# 发送更新邮件到哪个邮箱
email_address = ""
```
鉴于我是跑在linux下的，就把任务放到crontab里定时执行就行了，如果是其他的可能需要自己再写个定时任务执行的脚本。
