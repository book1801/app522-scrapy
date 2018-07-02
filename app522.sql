/*
Navicat MySQL Data Transfer

Source Server         :  Localhost
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : app522

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2018-06-29 15:08:54
*/

SET FOREIGN_KEY_CHECKS=0;


create database app522 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use app522

-- ----------------------------
-- Table structure for `app`
-- ----------------------------
DROP TABLE IF EXISTS `app`;
CREATE TABLE `app` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `appname` varchar(255) DEFAULT NULL,
  `downloadcount` varchar(255) DEFAULT NULL,
  `size` varchar(255) DEFAULT NULL,
  `updated` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `tag` varchar(255) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of app
-- ----------------------------

-- ----------------------------
-- Table structure for `news`
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of news
-- ----------------------------
