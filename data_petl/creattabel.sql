/*
--------------------------------------------------------
--  文件创建 07-2016 liang
--------------------------------------------------------

*/

DROP TABLE IF EXISTS `PRODUCT_INFO`;
DROP TABLE IF EXISTS `PRODUCT_HISTOR`;

/* 创建PRODUCT_INFO表结构 */
CREATE TABLE `PRODUCT_INFO` (
	`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
	`category` varchar(255) COMMENT '种类',
	`brand` varchar(255) COMMENT '品牌',
	`model` varchar(255) COMMENT '型号',
	`place_of_origin` varchar(255) COMMENT '产地',
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 创建PRODUCT_HISTOR表结构 */
CREATE TABLE `PRODUCT_HISTOR` (
	`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
	`year` varchar(255) COMMENT '年',
	`prince` varchar(255) COMMENT '价格',
	`unit` varchar(255) COMMENT '单位',
	`product_id` varchar(255) COMMENT '产品ID',
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
