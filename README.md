# BJFU_login

### `wired_network_login.py`: 模拟登录bjfu有线网络.Based on [link](https://blog.cother.org/%E8%BD%AF%E4%BB%B6/2015/12/31/Python-Login-NetManager.html)

- 定义主函数:

```python
def main():
    bjfu = BJFULOGIN('username', 'password') #filled with username, password
    bjfu.login()
    bjfu.connect()
    bjfu.info()
```

- 命令行添加参数:

> Location\wired_network_login.py username password

### `newjwxt.py`: 模拟登录bjfu教务系统

### `qq_login.py`: 模拟登录青桥网

### `pingjiao.py`: 一键评教
