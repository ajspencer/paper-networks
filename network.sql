-- MySQL dump 10.13  Distrib 5.6.25, for osx10.8 (x86_64)
--
-- Host: localhost    Database: network
-- ------------------------------------------------------
-- Server version	5.6.25

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
-- Table structure for table `network`
--

DROP TABLE IF EXISTS `network`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `network` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `adjacency` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `network`
--

LOCK TABLES `network` WRITE;
/*!40000 ALTER TABLE `network` DISABLE KEYS */;
INSERT INTO `network` VALUES (1,'P. Erd s','u\'Of A Graph\', u\'A Hajnal\''),(2,'A. S rkzy','u\'P. Erd s\''),(3,'D. F. Shanno','u\'G. A. Neufeld\', u\'J. Tartar\''),(4,'G. A. Neufeld','u\'D. F. Shanno\', u\'J. Tartar\''),(5,'J. Tartar','u\'D. F. Shanno\', u\'G. A. Neufeld\''),(6,'Paul Erdijs','u\'Gutti Jogesh\', u\'Babu\''),(7,'Anthony B. Evans','u\'Paul Erdijs\''),(8,'T L Lov sz','u\'P. Erd s\', u\'K. Vesztergombi\''),(9,'K. Vesztergombi','u\'P. Erd s\', u\'T L Lov sz\''),(11,'A Hajnal','u\'Of A Graph\', u\'P. Erd s\''),(12,'K. Alladi',''),(13,'J. D. Vaaler',''),(14,'A. Kro',''),(15,'J. Szabados',''),(16,'Janos Pach','u\'Richard Pollack\', u\'Z~olt Twa\''),(17,'Richard Pollack','u\'Janos Pach\', u\'Z~olt Twa\''),(18,'Z~olt Twa','u\'Janos Pach\', u\'Richard Pollack\''),(19,'P. Erdijs','u\'A. Gyarfzcis\', u\'E. T. Ordmanz\', u\'Y. Zalcstein\''),(20,'A. Gyarfzcis','u\'P. Erdijs\', u\'E. T. Ordmanz\', u\'Y. Zalcstein\''),(21,'E. T. Ordmanz','u\'P. Erdijs\', u\'A. Gyarfzcis\', u\'Y. Zalcstein\''),(22,'Y. Zalcstein','u\'P. Erdijs\', u\'A. Gyarfzcis\', u\'E. T. Ordmanz\''),(23,'Carsten Thomassen','u\'Paul Erdijs\', u\'Yousef Alavi\', u\'Paresh J. Malde\', u\'Allen J. Schwenk\''),(24,'Yousef Alavi','u\'Carsten Thomassen\', u\'Paul Erdijs\', u\'Paresh J. Malde\', u\'Allen J. Schwenk\''),(25,'Paresh J. Malde','u\'Carsten Thomassen\', u\'Paul Erdijs\', u\'Yousef Alavi\', u\'Allen J. Schwenk\''),(26,'Allen J. Schwenk','u\'Carsten Thomassen\', u\'Paul Erdijs\', u\'Yousef Alavi\', u\'Paresh J. Malde\''),(27,'S. Burr','u\'P. Erdijs\', u\'R. J. Faudree\', u\'C. C. Rousseau\', u\'R. H. Schelpt\''),(28,'R. J. Faudree','u\'S. Burr\', u\'P. Erdijs\', u\'C. C. Rousseau\', u\'R. H. Schelpt\''),(29,'C. C. Rousseau','u\'S. Burr\', u\'P. Erdijs\', u\'R. J. Faudree\', u\'R. H. Schelpt\''),(30,'R. H. Schelpt','u\'S. Burr\', u\'P. Erdijs\', u\'R. J. Faudree\', u\'C. C. Rousseau\''),(31,'Paul Erd s','u\'Peter Salamon\''),(32,'Hans Riesel','u\'Paul Erd s\''),(33,'Erd s C',''),(34,'B Lacampagne',''),(35,'P Erd s','u\'C. L. Stewart\', u\'R Tudeman\''),(36,'C. L. Stewart','u\'P Erd s\', u\'R Tudeman\''),(37,'R Tudeman','u\'P Erd s\', u\'C. L. Stewart\''),(38,'Peter Salamon','u\'Paul Erd s\''),(39,'Schelp D','u\'M Simonovitse\''),(40,'M Simonovitse','u\'Schelp D\''),(41,'P. Erd  s','u\'P. Erd s\''),(42,'Of A Graph','u\'P. Erd s\', u\'A Hajnal\''),(43,'Melvyn B. Nathanson','u\'Commumcafed The\''),(44,'Commumcafed The','u\'Melvyn B. Nathanson\''),(45,'Gutti Jogesh','u\'Babu\', u\'Paul Erdijs\''),(46,'Babu','u\'Gutti Jogesh\', u\'Paul Erdijs\''),(47,'Paul Erd','u\'I March\''),(48,'I March','u\'Paul Erd\''),(49,'P. Hell','u\'P. Erdijs\', u\'P. Winkler\''),(50,'P. Winkler','u\'P. Erdijs\', u\'P. Hell\''),(51,'P. Erdiis','u\'R. Faudree\', u\'R. H. Schelp\''),(52,'R. Faudree','u\'P. Erdiis\', u\'R. H. Schelp\''),(53,'R. H. Schelp','u\'P. Erdiis\', u\'R. Faudree\''),(54,'P. Erdgs','');
/*!40000 ALTER TABLE `network` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-01 21:55:00
