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

--
-- Table structure for table `bassetratings`
--

DROP TABLE IF EXISTS `bassetratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bassetratings` (
  `teamname` varchar(50) NOT NULL,
  `bassetdate` date NOT NULL,
  `bassetrank` int(11) NOT NULL,
  PRIMARY KEY (`teamname`,`bassetdate`),
  CONSTRAINT `fk_basset_teamname` FOREIGN KEY (`teamname`) REFERENCES `mydb`.`teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfrcratings`
--

DROP TABLE IF EXISTS `cfrcratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfrcratings` (
  `teamname` varchar(50) NOT NULL,
  `cfrcdate` date NOT NULL,
  `cfrcrank` int(11) NOT NULL,
  PRIMARY KEY (`teamname`,`cfrcdate`),
  CONSTRAINT `fk_cfrc_teamname` FOREIGN KEY (`teamname`) REFERENCES `mydb`.`teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `oddsdata`
--

DROP TABLE IF EXISTS `oddsdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oddsdata` (
  `oddsdate` date NOT NULL,
  `favorite` varchar(50) NOT NULL,
  `underdog` varchar(50) NOT NULL,
  `line` float(7,4) DEFAULT NULL,
  `juice` float(7,4) DEFAULT NULL,
  `overunder` float(7,4) DEFAULT NULL,
  `oujuice` float(7,4) DEFAULT NULL,
  `favmoneyline` float(7,2) DEFAULT NULL,
  `dogmoneyline` float(7,2) DEFAULT NULL,
  `favscore` int(11) DEFAULT NULL,
  `dogscore` int(11) DEFAULT NULL,
  PRIMARY KEY (`oddsdate`,`favorite`,`underdog`),
  KEY `fk_odds_favorite` (`favorite`),
  KEY `fk_odds_underdog` (`underdog`),
  CONSTRAINT `fk_odds_favorite` FOREIGN KEY (`favorite`) REFERENCES `mydb`.`teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_odds_underdog` FOREIGN KEY (`underdog`) REFERENCES `mydb`.`teamnames` (`teamname`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teamnames`
--

DROP TABLE IF EXISTS `teamnames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teamnames` (
  `teamname` varchar(50) NOT NULL,
  PRIMARY KEY (`teamname`),
  UNIQUE KEY `teamname_UNIQUE` (`teamname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'ncaa'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_reset_tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_reset_tables`()
BEGIN
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

DROP TABLE IF EXISTS `bassetratings`;
DROP TABLE IF EXISTS `cfrcratings`;
DROP TABLE IF EXISTS `baseratings`;
DROP TABLE IF EXISTS `oddsdata`;
-- -----------------------------------------------------
-- Table `mydb`.`teamnames`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `teamnames`;
CREATE TABLE IF NOT EXISTS `ncaa`.`teamnames` (
  `teamname` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`teamname`),
  UNIQUE INDEX `teamname_UNIQUE` (`teamname` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`bassetratings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncaa`.`bassetratings` (
  `teamname` VARCHAR(50) NOT NULL,
  `bassetdate` DATE NOT NULL,
  `bassetrank` INT NOT NULL,
  PRIMARY KEY (`teamname`, `bassetdate`),
  CONSTRAINT `fk_basset_teamname`
    FOREIGN KEY (`teamname`)
    REFERENCES `mydb`.`teamnames` (`teamname`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`cfrcratings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncaa`.`cfrcratings` (
  `teamname` VARCHAR(50) NOT NULL,
  `cfrcdate` DATE NOT NULL,
  `cfrcrank` INT NOT NULL,
  PRIMARY KEY (`teamname`, `cfrcdate`),
  CONSTRAINT `fk_cfrc_teamname`
    FOREIGN KEY (`teamname`)
    REFERENCES `mydb`.`teamnames` (`teamname`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`baseratings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncaa`.`baseratings` (
  `teamname` VARCHAR(50) NOT NULL,
  `basedate` DATE NOT NULL,
  `predictive-by-other` FLOAT(7,4),
  `home-by-other` FLOAT(7,4),
  `away-by-other` FLOAT(7,4),
  `neutral-by-other` FLOAT(7,4),
  `home-adv-by-other` FLOAT(7,4),
  `schedule-strength-by-other` FLOAT(7,4),
  `future-sos-by-other` FLOAT(7,4),
  `season-sos-by-other` FLOAT(7,4),
  `sos-basic-by-other` FLOAT(7,4),
  `in-conference-sos-by-other` FLOAT(7,4),
  `non-conference-sos-by-other` FLOAT(7,4),
  `last-5-games-by-other` FLOAT(7,4),
  `last-10-games-by-other` FLOAT(7,4),
  `in-conference-by-other` FLOAT(7,4),
  `non-conference-by-other` FLOAT(7,4),
  `luck-by-other` FLOAT(7,4),
  `consistency-by-other` FLOAT(7,4),
  `vs-1-10-by-other` FLOAT(7,4),
  `vs-11-25-by-other` FLOAT(7,4),
  `vs-26-40-by-other` FLOAT(7,4),
  `vs-41-75-by-other` FLOAT(7,4),
  `vs-76-120-by-other` FLOAT(7,4),
  `first-half-by-other` FLOAT(7,4),
  `second-half-by-other` FLOAT(7,4),
  PRIMARY KEY (`teamname`, `basedate`),
  CONSTRAINT `fk_base_teamname`
    FOREIGN KEY (`teamname`)
    REFERENCES `mydb`.`teamnames` (`teamname`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`oddsdata`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ncaa`.`oddsdata` (
  `oddsdate` DATE NOT NULL,
  `favorite` VARCHAR(50) NOT NULL,
  `underdog` VARCHAR(50) NOT NULL,
  `line` FLOAT(7,4),
  `juice` FLOAT(7,4),
  `overunder` FLOAT(7,4),
  `oujuice` FLOAT(7,4),
  `favmoneyline` FLOAT(7,2),
  `dogmoneyline` FLOAT(7,2),
  `favscore` INT,
  `dogscore` INT,
  PRIMARY KEY (`oddsdate`,`favorite`, `underdog`),
  CONSTRAINT `fk_odds_favorite`
    FOREIGN KEY (`favorite`)
    REFERENCES `mydb`.`teamnames` (`teamname`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_odds_underdog`
	FOREIGN KEY (`underdog`)
    REFERENCES `mydb`.`teamnames`(`teamname`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-11 21:53:14
