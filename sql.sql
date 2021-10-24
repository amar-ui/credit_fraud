/*
SQLyog Community v13.0.1 (64 bit)
MySQL - 5.5.20-log : Database - credit card fraud
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`credit card fraud` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `credit card fraud`;

/*Table structure for table `bill` */

DROP TABLE IF EXISTS `bill`;

CREATE TABLE `bill` (
  `bill_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `tot_amt` bigint(20) NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY (`bill_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `bill` */

insert  into `bill`(`bill_id`,`user_id`,`tot_amt`,`date`) values 
(1,1,159999,'2021-06-11'),
(2,1,2000,'2021-06-11'),
(3,1,20000,'2021-06-11');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `cmp_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `complaint` varchar(50) NOT NULL,
  `date` varchar(20) NOT NULL,
  `reply` varchar(50) NOT NULL,
  PRIMARY KEY (`cmp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

/*Table structure for table `dealer` */

DROP TABLE IF EXISTS `dealer`;

CREATE TABLE `dealer` (
  `d_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(30) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`d_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `dealer` */

insert  into `dealer`(`d_id`,`login_id`,`fname`,`lname`,`dob`,`gender`,`place`,`post`,`pin`,`email`,`phone`) values 
(1,3,'Ankita','Ram','2021-06-11','Female','Kannur','Kannur',670000,'ankita@gmail.com',9876543211);

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feed_id` int(11) NOT NULL AUTO_INCREMENT,
  `u_id` int(11) DEFAULT NULL,
  `feedback` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`feed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`login_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`user_name`,`password`,`user_type`) values 
(1,'rahul','rahul','user'),
(2,'admin','admin','admin'),
(3,'ankita','ankita','dealer');

/*Table structure for table `order_detiles` */

DROP TABLE IF EXISTS `order_detiles`;

CREATE TABLE `order_detiles` (
  `ord_id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `prod_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `ord_date` date NOT NULL,
  `del_date` date NOT NULL,
  `booking_satus` varchar(50) NOT NULL,
  `quantity` bigint(20) NOT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`ord_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `order_detiles` */

insert  into `order_detiles`(`ord_id`,`bill_id`,`prod_id`,`user_id`,`ord_date`,`del_date`,`booking_satus`,`quantity`,`amount`) values 
(1,0,1,1,'2021-06-11','0000-00-00','pending',1,159999),
(2,2,2,1,'2021-06-11','0000-00-00','pending',1,2000),
(3,3,2,1,'2021-06-11','0000-00-00','pending',2,2000),
(4,3,2,1,'2021-06-11','0000-00-00','pending',1,2000),
(5,3,2,1,'2021-06-11','0000-00-00','cart',2,2000),
(6,3,2,1,'2021-06-11','0000-00-00','cart',1,2000),
(7,3,2,1,'2021-06-11','0000-00-00','pending',1,2000),
(8,3,2,1,'2021-06-11','0000-00-00','pending',1,2000),
(9,3,2,1,'2021-06-11','0000-00-00','pending',1,2000),
(10,3,2,1,'2021-06-11','0000-00-00','pending',1,2000),
(11,4,2,1,'2021-06-11','0000-00-00','pending',1,2000);

/*Table structure for table `pin` */

DROP TABLE IF EXISTS `pin`;

CREATE TABLE `pin` (
  `pin_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `card_no` bigint(20) NOT NULL,
  `expiry_date` varchar(20) NOT NULL,
  `pin_no` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `balance` bigint(20) NOT NULL,
  `ifsc_code` varchar(50) NOT NULL,
  PRIMARY KEY (`pin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `pin` */

insert  into `pin`(`pin_id`,`user_id`,`card_no`,`expiry_date`,`pin_no`,`date`,`balance`,`ifsc_code`) values 
(1,1,34567893456,'2026-07-16',7527,'2021-06-10',0,'SDF4567');

/*Table structure for table `product` */

DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_name` varchar(30) NOT NULL,
  `price` varchar(11) NOT NULL,
  `details` varchar(50) NOT NULL,
  `image` varchar(500) NOT NULL,
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `product` */

insert  into `product`(`p_id`,`p_name`,`price`,`details`,`image`) values 
(1,'Samsung Mobile Phone','159999','64 GB,Navy Blue, 4GB RAM,6000mah Battery','samsungm31.jpg'),
(2,'Dress','2000','Cotton Salwar Material','DRESS.jpg');

/*Table structure for table `security_question` */

DROP TABLE IF EXISTS `security_question`;

CREATE TABLE `security_question` (
  `sec_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `question` varchar(50) NOT NULL,
  `answer` varchar(50) NOT NULL,
  PRIMARY KEY (`sec_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `security_question` */

insert  into `security_question`(`sec_id`,`user_id`,`date`,`question`,`answer`) values 
(1,1,'2021-06-11','Enter secret number','3456');

/*Table structure for table `stock` */

DROP TABLE IF EXISTS `stock`;

CREATE TABLE `stock` (
  `stk_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_id` int(11) DEFAULT NULL,
  `no_of_product` int(11) DEFAULT NULL,
  PRIMARY KEY (`stk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `stock` */

insert  into `stock`(`stk_id`,`p_id`,`no_of_product`) values 
(1,1,11),
(2,2,4);

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `id` int(11) DEFAULT NULL,
  `studentname` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `student` */

insert  into `student`(`id`,`studentname`,`place`) values 
(1,'shana','kkd'),
(2,'ahaana','kkd'),
(3,'thesni','kkd'),
(4,'shafna','kkd');

/*Table structure for table `transaction` */

DROP TABLE IF EXISTS `transaction`;

CREATE TABLE `transaction` (
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `bill_id` int(11) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `date` varchar(10) NOT NULL,
  `time` varchar(10) NOT NULL,
  `finished` varchar(20) NOT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `transaction` */

insert  into `transaction`(`transaction_id`,`bill_id`,`latitude`,`longitude`,`date`,`time`,`finished`) values 
(1,0,0,0,'2021-06-11','00:36:44','success'),
(2,2,11.3568,75.3456,'2021-06-11','00:42:19','success'),
(3,3,0,0,'2021-06-11','00:43:43','fake'),
(4,3,0,0,'2021-06-11','00:45:01','fake'),
(5,3,0,0,'2021-06-11','00:59:10','fake'),
(6,3,11.3568,75.3456,'2021-06-11','09:48:30','fake'),
(7,3,11.3568,75.3456,'2021-06-11','09:51:30','success'),
(8,4,11.3568,75.3456,'2021-06-11','10:02:03','success');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `u_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(50) DEFAULT NULL,
  `lname` varchar(50) DEFAULT NULL,
  `dob` varchar(20) DEFAULT NULL,
  `gender` varchar(30) DEFAULT NULL,
  `house_name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`u_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`u_id`,`login_id`,`fname`,`lname`,`dob`,`gender`,`house_name`,`place`,`post`,`pin`,`email`,`phone`) values 
(1,1,'Rahul','Raj','11/6/2000','Male','Rahul','Kannur','Kannur',670000,'rahul@gmail.com',9876543210);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
