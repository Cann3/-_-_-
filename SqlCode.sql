#创建数据库
CREATE DATABASE student;

#打开数据库
USE student;

#创建学生表
CREATE TABLE student(
  stuid INT PRIMARY KEY AUTO_INCREMENT COMMENT '编号，主键自增',
  sname VARCHAR(50) NOT NULL COMMENT '姓名',
  gender VARCHAR(4) DEFAULT '男' COMMENT '性别',
  address VARCHAR(300) COMMENT '地址',
  birthday DATE COMMENT '生日',
  classname VARCHAR(50) COMMENT '班级',
  note LONGTEXT COMMENT '备注'	
);
#向表中插入数据
INSERT INTO student(sname,gender,address,birthday,classname,note)
VALUES('丁宗参','男','河南','2002-12-11','python8班','计算机'),
('马超','男','兰州','2002-1-11','python8班','战士'),
('关羽','男','运城','2002-2-11','python8班','战士'),
('赵云','男','常山','2002-3-12','python2班','打野'),
('黄忠','男','荆州','2002-4-15','python2班','射手'),
('刘备','男','户县','2002-5-15','python1班','打野'),
('曹操','男','洛阳','2002-2-22','python1班','战士'),
('许褚','男','长安','2002-3-21','python8班','打野');

#修改
UPDATE student SET sname='丁开心',gender='女',address='河南',note='小孩' WHERE sname='关羽';

#删除
DELETE FROM student WHERE sname='黄忠'
#查找
SELECT * FROM student WHERE classname='python8班'
SELECT * FROM student s1 WHERE classname 
IN (SELECT classname FROM student s2 WHERE s2.sname='曹操')
SELECT * FROM student
#删除数据库
DROP DATABASE studb;