CREATE TABLE `novel` (
   `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
   `title` varchar(100) NOT NULL COMMENT '标题',
   `content` text NOT NULL COMMENT '内容',
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;