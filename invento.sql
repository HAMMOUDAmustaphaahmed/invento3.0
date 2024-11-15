-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: invento
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `achats`
--

DROP TABLE IF EXISTS `achats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `achats` (
  `code_demande` varchar(255) NOT NULL,
  `code_article` varchar(255) NOT NULL,
  `libelle_article` varchar(255) NOT NULL,
  `quantite` int NOT NULL,
  `prix_achat` float NOT NULL,
  `assignation` varchar(255) NOT NULL,
  `date` datetime NOT NULL,
  `fournisseur` varchar(255) NOT NULL,
  `lot` varchar(255) NOT NULL,
  `vendue` int NOT NULL DEFAULT '0',
  `quantite_restante` int DEFAULT NULL,
  PRIMARY KEY (`lot`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `achats`
--

LOCK TABLES `achats` WRITE;
/*!40000 ALTER TABLE `achats` DISABLE KEYS */;
/*!40000 ALTER TABLE `achats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articles` (
  `id_article` int NOT NULL AUTO_INCREMENT,
  `code_article` varchar(20) NOT NULL,
  `libelle_article` varchar(255) NOT NULL,
  `prix_achat` float NOT NULL,
  `assignation` varchar(255) NOT NULL,
  `quantite` int NOT NULL,
  `fournisseur` varchar(255) NOT NULL,
  `date` datetime NOT NULL,
  `quantite_min` int NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_article`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (1,'ADF001','Adhésif',2.58824,'Sahel',34,'fournisseur_adhésif','2024-10-30 08:19:23',12,'None');
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demande_achat`
--

DROP TABLE IF EXISTS `demande_achat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demande_achat` (
  `code_demande` int NOT NULL AUTO_INCREMENT,
  `code_article` varchar(50) NOT NULL,
  `libelle_article` varchar(20) NOT NULL,
  `quantite` int NOT NULL,
  `prix_achat` decimal(6,3) DEFAULT NULL,
  `assignation` varchar(20) NOT NULL,
  `date` datetime DEFAULT NULL,
  `demandeur` varchar(20) DEFAULT NULL,
  `vers` varchar(20) DEFAULT NULL,
  `commande` varchar(20) DEFAULT NULL,
  `etat` int NOT NULL,
  `reception` int NOT NULL,
  `commentaire` varchar(255) DEFAULT NULL,
  `fournisseur` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code_demande`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demande_achat`
--

LOCK TABLES `demande_achat` WRITE;
/*!40000 ALTER TABLE `demande_achat` DISABLE KEYS */;
/*!40000 ALTER TABLE `demande_achat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `demande_vente`
--

DROP TABLE IF EXISTS `demande_vente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `demande_vente` (
  `code_demande` int NOT NULL AUTO_INCREMENT,
  `code_article` varchar(50) NOT NULL,
  `libelle_article` varchar(20) NOT NULL,
  `quantite` int NOT NULL,
  `prix_vente` decimal(6,3) DEFAULT NULL,
  `assignation` varchar(20) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `demandeur` varchar(20) DEFAULT NULL,
  `vers` varchar(20) NOT NULL,
  `commande` varchar(20) DEFAULT NULL,
  `etat` int NOT NULL,
  `reception` int NOT NULL,
  `commentaire` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code_demande`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `demande_vente`
--

LOCK TABLES `demande_vente` WRITE;
/*!40000 ALTER TABLE `demande_vente` DISABLE KEYS */;
INSERT INTO `demande_vente` VALUES (1,'ADF001','Adhésif',10,1.000,NULL,'2024-11-06 14:59:55',NULL,'bsp','x',1,0,NULL),(2,'ADF001','Adhésif',10,5.000,NULL,'2024-11-06 16:55:10',NULL,'bsp','x',0,0,NULL),(3,'ADF001','Adhésif',10,2.000,NULL,'2024-11-06 16:54:36',NULL,'bsp','x',0,0,NULL);
/*!40000 ALTER TABLE `demande_vente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fournisseur`
--

DROP TABLE IF EXISTS `fournisseur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fournisseur` (
  `id_fournisseur` int NOT NULL AUTO_INCREMENT,
  `nom_fournisseur` varchar(255) NOT NULL,
  `matricule_fiscale` varchar(50) DEFAULT NULL,
  `adresse` varchar(255) DEFAULT NULL,
  `telephone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_fournisseur`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fournisseur`
--

LOCK TABLES `fournisseur` WRITE;
/*!40000 ALTER TABLE `fournisseur` DISABLE KEYS */;
INSERT INTO `fournisseur` VALUES (5,'Fournisseur_x','1234','x','12345');
/*!40000 ALTER TABLE `fournisseur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `id_history` int NOT NULL AUTO_INCREMENT,
  `code_demande` int DEFAULT NULL,
  `code_article` varchar(50) DEFAULT NULL,
  `libelle_article` varchar(255) DEFAULT NULL,
  `quantite` int DEFAULT NULL,
  `prix` float DEFAULT NULL,
  `fournisseur` varchar(20) DEFAULT NULL,
  `emplacement` varchar(20) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `user` varchar(20) DEFAULT NULL,
  `details` varchar(255) DEFAULT NULL,
  `usine` varchar(20) DEFAULT NULL,
  `date_action` timestamp NULL DEFAULT NULL,
  `date_approuver_demande` timestamp NULL DEFAULT NULL,
  `date_reception` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id_history`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
INSERT INTO `history` VALUES (1,NULL,NULL,NULL,NULL,NULL,'Fournisseur_x',NULL,'ajout d\'un nouveau fournisseur',NULL,' matricule fiscale : 1234 addresse : x telephone : 1234',NULL,NULL,NULL,NULL),(2,NULL,NULL,NULL,NULL,NULL,'Fournisseur_a',NULL,'ajout d\'un nouveau fournisseur',NULL,' matricule fiscale : 12345 addresse : Benetton Sahel x telephone : 12345',NULL,NULL,NULL,NULL),(3,NULL,NULL,NULL,NULL,NULL,'Fournisseur_x',NULL,'ajout d\'un nouveau fournisseur',NULL,' matricule fiscale : 1234 addresse : x telephone : 1234',NULL,NULL,NULL,NULL),(4,NULL,NULL,NULL,NULL,NULL,'Fournisseur_x',NULL,'ajout d\'un nouveau fournisseur',NULL,' matricule fiscale : 1234 addresse : x telephone : 12345',NULL,NULL,NULL,NULL),(5,NULL,'test001','test',NULL,2,'x','Sahel','ajout d\'un nouveau article',NULL,'date : 2024-11-04 11:33:18.874698+00:00quantite_min : 5',NULL,NULL,NULL,NULL),(6,NULL,NULL,NULL,NULL,NULL,'a',NULL,'ajout d\'un nouveau fournisseur',NULL,' matricule fiscale : 12 addresse : a telephone : 1',NULL,NULL,NULL,NULL),(7,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-05 15:01:21.400235+00:00',NULL,NULL,NULL,NULL),(8,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 10:12:33.047642+00:00',NULL,NULL,NULL,NULL),(9,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 10:19:03.413691+00:00',NULL,NULL,NULL,NULL),(10,NULL,'test001','test',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 10:58:00.464445+00:00',NULL,NULL,NULL,NULL),(11,NULL,'test001','test',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 11:01:12.848397+00:00',NULL,NULL,NULL,NULL),(12,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 11:07:47.388951+00:00',NULL,NULL,NULL,NULL),(13,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 11:11:21.787057+00:00',NULL,NULL,NULL,NULL),(14,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 11:15:15.387039+00:00',NULL,NULL,NULL,NULL),(15,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 12:28:53.015816+00:00',NULL,NULL,NULL,NULL),(16,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 12:29:09.232641+00:00',NULL,NULL,NULL,NULL),(17,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 12:36:06.218414+00:00',NULL,NULL,NULL,NULL),(18,NULL,'ADF001','Adhésif',NULL,NULL,NULL,'Sahel','ajout d\'un nouveau demande d\'achat',NULL,'date : 2024-11-06 12:38:16.027437+00:00',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `emplacement` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  `numero_telephone` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (4,'administrateur','pbkdf2:sha256:600000$8UfOir72bKr4G16n$b6e30a2bc99c12b8c1386ab005aa2a9b6c3b94763667ca726991e4d7f2f59e6f','sahel','admin',54391747);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usine`
--

DROP TABLE IF EXISTS `usine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usine` (
  `id_usine` int NOT NULL AUTO_INCREMENT,
  `nom_usine` varchar(20) NOT NULL,
  `region` varchar(20) NOT NULL,
  `adresse` varchar(20) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `etat` varchar(20) NOT NULL,
  PRIMARY KEY (`id_usine`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usine`
--

LOCK TABLES `usine` WRITE;
/*!40000 ALTER TABLE `usine` DISABLE KEYS */;
INSERT INTO `usine` VALUES (1,'lavage','sahel','Benetton Sahel','10.680606648122179','35.77832307588124','1234','interne');
/*!40000 ALTER TABLE `usine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventes`
--

DROP TABLE IF EXISTS `ventes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventes` (
  `id_vente` int NOT NULL AUTO_INCREMENT,
  `code_demande` int DEFAULT NULL,
  `code_article` varchar(255) DEFAULT NULL,
  `libelle_article` varchar(20) DEFAULT NULL,
  `quantite` int DEFAULT NULL,
  `prix_vente` decimal(6,3) DEFAULT NULL,
  `assignation` varchar(20) DEFAULT NULL,
  `vers` varchar(20) DEFAULT NULL,
  `demandeur` varchar(20) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id_vente`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventes`
--

LOCK TABLES `ventes` WRITE;
/*!40000 ALTER TABLE `ventes` DISABLE KEYS */;
INSERT INTO `ventes` VALUES (1,3,'ADF001','Adhésif',10,2.000,NULL,'bsp',NULL,'2024-11-06 16:54:36'),(2,2,'ADF001','Adhésif',10,5.000,NULL,'bsp',NULL,'2024-11-06 16:55:10');
/*!40000 ALTER TABLE `ventes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-06 17:08:01
