# root 用来创建 删除 数据库
show databases;
drop  database  if exists meiduo;
create database meiduo charset=utf8;
drop user  if exists yuanhaomeiduo;
FLUSH PRIVILEGES;
SELECT User, Host FROM mysql.user;
create user yuanhaomeiduo identified by 'meiduo123yuanhao';
grant all on meiduo.* to 'yuanhaomeiduo'@'%';
flush privileges;
show databases;
use meiduo;
show tables;

# 最后别忘了迁移