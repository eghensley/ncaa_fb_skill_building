-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: ncaa
-- ------------------------------------------------------
-- Server version	5.7.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `baseratings`
--

DROP TABLE IF EXISTS `baseratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `baseratings` (
  `teamname` varchar(50) NOT NULL,
  `basedate` date NOT NULL,
  `predictive-by-other` float(7,4) DEFAULT NULL,
  `home-by-other` float(7,4) DEFAULT NULL,
  `away-by-other` float(7,4) DEFAULT NULL,
  `neutral-by-other` float(7,4) DEFAULT NULL,
  `home-adv-by-other` float(7,4) DEFAULT NULL,
  `schedule-strength-by-other` float(7,4) DEFAULT NULL,
  `future-sos-by-other` float(7,4) DEFAULT NULL,
  `season-sos-by-other` float(7,4) DEFAULT NULL,
  `sos-basic-by-other` float(7,4) DEFAULT NULL,
  `in-conference-sos-by-other` float(7,4) DEFAULT NULL,
  `non-conference-sos-by-other` float(7,4) DEFAULT NULL,
  `last-5-games-by-other` float(7,4) DEFAULT NULL,
  `last-10-games-by-other` float(7,4) DEFAULT NULL,
  `in-conference-by-other` float(7,4) DEFAULT NULL,
  `non-conference-by-other` float(7,4) DEFAULT NULL,
  `luck-by-other` float(7,4) DEFAULT NULL,
  `consistency-by-other` float(7,4) DEFAULT NULL,
  `vs-1-10-by-other` float(7,4) DEFAULT NULL,
  `vs-11-25-by-other` float(7,4) DEFAULT NULL,
  `vs-26-40-by-other` float(7,4) DEFAULT NULL,
  `vs-41-75-by-other` float(7,4) DEFAULT NULL,
  `vs-76-120-by-other` float(7,4) DEFAULT NULL,
  `first-half-by-other` float(7,4) DEFAULT NULL,
  `second-half-by-other` float(7,4) DEFAULT NULL,
  PRIMARY KEY (`teamname`,`basedate`),
  CONSTRAINT `fk_base_teamname` FOREIGN KEY (`teamname`) REFERENCES `mydb`.`teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-11 15:11:54
