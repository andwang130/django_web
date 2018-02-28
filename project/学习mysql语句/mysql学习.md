## 一、介绍
>Mysql是最流行的关系型数据库管理系统，是最好的RDBMS(Relational Database Management System：关系数据库管理系统)应用软件之一

>RDBMS即关系数据库管理系统(Relational Database Management System)的特点：
>
- 数据以表格的形式出现
- 每行为各种记录名称
- 每列为记录名称所对应的数据域
- 许多的行和列组成一张表单
- 若干的表单组成database

>RDBMS的一些术语：
>
- 数据库: 数据库是一些关联表的集合。.
- 数据表: 表是数据的矩阵。在一个数据库中的表看起来像一个简单的电子表格。
- 列: 一列(数据元素) 包含了相同的数据, 例如邮政编码的数据。
- 行：一行（=元组，或记录）是一组相关的数据，例如一条用户订阅的数据。
- 冗余：存储两倍数据，冗余降低了性能，但提高了数据的安全性。
- 主键：主键是唯一的。一个数据表中只能包含一个主键。你可以使用主键来查询数据。
- 外键：外键用于关联两个表。
- 复合键：复合键（组合键）将多个列作为一个索引键，一般用于复合索引。
- 索引：使用索引可快速访问数据库表中的特定信息。索引是对数据库表中一列或多列的值进行排序的一种结构。类似于书籍的目录。
- 参照完整性: 参照的完整性要求关系中不允许引用不存在的实体。与实体完整性是关系模型必须满足的完整性约束条件，目的是保证数据的一致性，参照完整性又称引用完整性。

**最重要的是mysql是开源的，并且使用标准的SQL数据语言形式**


## 二、语法
1、cmd连接
	mysql -u root -p

2、创建数据库
	create database database_name;

3、选择数据库
	use database_name;

4、删除数据库
	drop database db_test;

5、创建表格
数据类型：
以下的数值类型分有符号和无符号(>=0)，譬如TINYINT是(0,255)包括0和255 或 (-128,127)包括-128和127
TINYINT	     1 字节	  	小整数值
SMALLINT	 2 字节	    大整数值
MEDIUMINT	 3 字节     大整数值
INT或INTEGER	 4 字节     大整数值
BIGINT	     8 字节	    极大整数值
FLOAT	     4 字节	    单精度浮点数值，1位符号，8位指数，23位小数
DOUBLE	     8 字节	    双精度浮点数值，1位符号，11位指数，52位小数
DECIMAL	     DECIMAL(M,D) ，如果M>D，为M+2否则为D+2             小数值

DATE	     3 字节     YYYY-MM-DD  日期值
TIME	     3 字节     HH:MM:SS	    时间值或持续时间
YEAR	     1 字节     YYYY        	年份值
DATETIME	 8 字节     YYYY-MM-DD HH:MM:SS	混合日期和时间值
TIMESTAMP 	 4 字节     YYYYMMDD HHMMSS	 混合日期和时间值，时间戳

CHAR	     0-255字节	         定长字符串
VARCHAR	     0-65535 字节	     变长字符串
TINYBLOB	 0-255字节	         不超过 255 个字符的二进制字符串
TINYTEXT	 0-255字节	         短文本字符串
BLOB	     0-65 535字节	     二进制形式的长文本数据
TEXT	     0-65 535字节	     长文本数据
MEDIUMBLOB	 0-16 777 215字节	 二进制形式的中等长度文本数据
MEDIUMTEXT	 0-16 777 215字节	 中等长度文本数据
LONGBLOB	 0-4 294 967 295字节	 二进制形式的极大文本数据
LONGTEXT	 0-4 294 967 295字节	 极大文本数据

最常用的有：int, date, datatime，varchar

	CREATE TABLE IF NOT EXISTS `tb_test`(
	   `id` INT UNSIGNED AUTO_INCREMENT,
	   `title` VARCHAR(100) NOT NULL,
	   `content` VARCHAR(500) NOT NULL,
	   PRIMARY KEY ( `id` )
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;

6、删除表格
	DROP TABLE tb_test ;

7、插入数据
	INSERT INTO tb_test(id, title, content) VALUES(2, '测试标题', '测试内容');
	INSERT INTO tb_test(title, content) VALUES("测试标题1", "测试内容2");

8、查询数据
	SELECT title,content FROM tb_test;
	SELECT title,content FROM tb_test where title like "%1";

where操作符:<,>,<=,>=,!=,<>,like

9、修改数据
	UPDATE tb_test SET title='测试修改标题' where title='测试标题';

10、删除数据
	DELETE FROM tb_test where title='测试标题';

## 三、使用pymysql
见代码
PS：另外推荐一个PyMqsqlPool，一个基于pymysql的连接池管理库