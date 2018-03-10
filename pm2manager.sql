/*
 Navicat Premium Data Transfer

 Source Server         : 10.211.55.12
 Source Server Type    : MySQL
 Source Server Version : 50540
 Source Host           : 10.211.55.12
 Source Database       : pm2manager

 Target Server Type    : MySQL
 Target Server Version : 50540
 File Encoding         : utf-8

 Date: 03/08/2018 17:52:04 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `proccesmgr`
-- ----------------------------
DROP TABLE IF EXISTS `proccesmgr`;
CREATE TABLE `proccesmgr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `host` varchar(100) NOT NULL,
  `pid` int(11) NOT NULL,
  `status` int(1) NOT NULL,
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=gbk;

SET FOREIGN_KEY_CHECKS = 1;
