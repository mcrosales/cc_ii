SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for historical_data
-- ----------------------------
DROP TABLE IF EXISTS `historical_data`;
CREATE TABLE `historical_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `measure_date` datetime DEFAULT NULL,
  `temperature` decimal(10,4) DEFAULT NULL,
  `humidity` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
