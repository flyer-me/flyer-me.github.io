---
title: "Jenkins配置Linux子节点常见问题"
date: 2022-09-27 16:17:23 +0800
categories: [软件]
tags: [软件, CI/CD, linux]
---

### 1. mvn command not found / node: No such file or directory
本地使用mvn、npm正常，而jenkins运行命令失败，创建软链接解决：

```bash
# node
ln -s "$(which node)" /usr/bin/node
# maven
ln -s "$(which mvn)" /usr/bin/mvn
ln -s "$(which mvn)" /usr/local/bin/mvn
```
### 2. No compiler is provided in this environment. Perhaps you are running on a JRE rather than…

Jenkins 默认使用系统自带 openjdk ： `/usr/lib/jvm/java…` 该目录下是只有JRE的。
需要将 java 路径添加到 pipeline 中：

```bash
environment {
	PATH = "/usr/local/jdk1.8/bin:$PATH" #定义java的环境变量
}
```

### 3. Jenkins执行脚本发生Permission denied
请保证配置 linux 构建环境时使用用户与 Jenkins 运行时用户一致，保证Jenkins 调用命令涉及的文件(夹)均为本用户所有。

修改所有权示例：更改maven文件(夹)所属用户为 admin，使用 root 用户执行：

```bash
chown -R admin maven
```

### 4. Permission denied(publickey). fatal:Could not read from remote repository

如果本地 `git push` 等命令正常，则通常是将 Jenkins agent 安装为服务后，服务使用的用户与 sshkey 不一致引起的。

查看运行用户：Dashboard -> Nodes -> 某节点 -> System Information -> user.name 
更改服务运行用户：

Linux环境下，使用相同用户运行jenkins-agent.jnlp、安装服务即可；
Windows环境下，服务 -> Jenkins agent -> 属性 -> 登录 -> 登录身份 -> 修改，重启服务。