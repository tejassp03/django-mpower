-- MySQL dump 10.13  Distrib 8.0.33, for macos13.3 (arm64)
--
-- Host: localhost    Database: mpowertest
-- ------------------------------------------------------
-- Server version	8.0.33

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `aid` int NOT NULL AUTO_INCREMENT,
  `aname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `arole` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `log_id_id` int DEFAULT NULL,
  PRIMARY KEY (`aid`),
  KEY `admin_log_id_id_1548a1f3_fk_login_log_id` (`log_id_id`),
  CONSTRAINT `admin_log_id_id_1548a1f3_fk_login_log_id` FOREIGN KEY (`log_id_id`) REFERENCES `login` (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=931921109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (29204354,'Aravinda','CEO','7894561232','ceo@mpower.in',30),(542764094,'Jai','HR','7777777777','jai48@gmail.com',72);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `allskills`
--

DROP TABLE IF EXISTS `allskills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `allskills` (
  `id` int NOT NULL AUTO_INCREMENT,
  `skill` varchar(750) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `allskills`
--

LOCK TABLES `allskills` WRITE;
/*!40000 ALTER TABLE `allskills` DISABLE KEYS */;
INSERT INTO `allskills` VALUES (1,'Angular JS / Node Js'),(2,'App Development(iOS,Android,Windows)'),(3,'C / C++'),(4,'Networking / CCNA'),(5,'c#'),(6,'Big Data / Hadoop'),(7,'Cloud Computing'),(8,'Embedded Systems'),(9,'Java / J2EE'),(10,'Linux / Unix'),(11,'MySQL / Database'),(12,'Data Analytics/Data Science/Machine Learning'),(13,'MongoDB'),(14,'Django'),(15,'Animation / Multimedia'),(16,'Data Warehousing'),(17,'Computer Hardware'),(18,'Ethical Hacking'),(19,'Oracle'),(20,'PHP'),(21,'Python'),(22,'Red Hat'),(23,'PLC/Automation/SCADA'),(24,'Ruby on Rails'),(25,'SAP/SAS/ERP'),(26,'Software Testing'),(27,'Web Desigining'),(28,'Mainframe'),(29,'.Net'),(30,'VLSI'),(31,'IOT'),(32,'DevOps'),(33,'UI/UX Designing'),(34,'System Admin'),(35,'PCB Design'),(36,'Solaris'),(37,'Accounting & Finance'),(38,'Autocad / CAD'),(39,'HR / Admin'),(40,'Industrial Training'),(41,'Graphic Design'),(42,'Digital Marketing'),(43,'Business Analyst'),(44,'Microsoft Office'),(45,'Access'),(46,'Accounting Software'),(47,'Accounts payable'),(48,'Acrobat'),(49,'Acute care'),(50,'Ad design'),(51,'Advanced Cardiac Life Support (ACLS)'),(52,'Agile Business Analysis'),(53,'AJAX'),(54,'Algebra'),(55,'Analysis'),(56,'Analytical skills'),(57,'API ( Application Programming Interface)'),(58,'ASP.NET'),(59,'Assessment'),(60,'Big Data Analysis & SQL'),(61,'Bookkeeping through Excel or TurboTax'),(62,'Brand management'),(63,'Business Continuity Planning'),(64,'Business Process Modeling'),(65,'C'),(66,'C++'),(67,'Calculus'),(68,'Cash Flow Management'),(69,'Cloud networking and file sharing'),(70,'Cognos Analytics (IBM)'),(71,'Communication'),(72,'Comparative analyses'),(73,'Content Management Systems (CMS)'),(74,'Copywriting'),(75,'Corel Draw'),(76,'Cost-assessment'),(77,'CPR'),(78,'Critical thinking'),(79,'CRO and A/B Testing'),(80,'CSS'),(81,'Customer Interaction'),(82,'Customer Relationship Management (CRM)'),(83,'Data analysis'),(84,'Data entry'),(85,'Data Mapping'),(86,'Decision-making'),(87,'Digital printing'),(88,'Docs'),(89,'Dreamweaver'),(90,'Editing'),(91,'Email'),(92,'Email marketing'),(93,'Employee time tracking'),(94,'Enterprise Resource Planning'),(95,'Enterprise Resource Planning ERPs like SAP'),(96,'Entity Relationship Diagrams'),(97,'Excel'),(98,'Forms'),(99,'Free Hand'),(100,'Geometry'),(101,'GUI'),(102,'Hive'),(103,'HR Recruiter'),(104,'HR'),(105,'HTML'),(106,'InDesign'),(107,'Infographics'),(108,'Invoicing'),(109,'Java'),(110,'Javascript'),(111,'Journalism'),(112,'Logo creation'),(113,'Machine learning'),(114,'Marketing'),(115,'Mathematics'),(116,'Matlab'),(117,'Microsoft Excel (Advanced)'),(118,'Microsoft Visio'),(119,'MS Office'),(120,'Networking'),(121,'Objective-C'),(122,'OneNote'),(123,'OpenOffice'),(124,'Outlook'),(125,'Patient care and assistance'),(126,'Payment Processing'),(127,'Payroll'),(128,'Perl'),(129,'Photo editing'),(130,'Photoshop'),(131,'Pivot tables'),(132,'Powerpoint'),(133,'Problem-solving'),(134,'Public speaking'),(135,'Publisher'),(136,'R Programing'),(137,'Record keeping'),(138,'Recording'),(139,'Reports'),(140,'Research & Data analysis'),(141,'Risk Management'),(142,'Ruby with SQL'),(143,'Sales'),(144,'SAS'),(145,'Scala'),(146,'Scrum'),(147,'Search Engine and Keyword Optimization'),(148,'SEO'),(149,'SEO/SEM'),(150,'Social media'),(151,'Social media and mobile marketing'),(152,'Spreadsheets'),(153,'SPSS'),(154,'SQL'),(155,'STATA'),(156,'Statistics'),(157,'Storyboarding'),(158,'Storytelling'),(159,'Stress management'),(160,'Surgery preparation'),(161,'System Context Diagrams'),(162,'Task management'),(163,'Technical and non-technical communication'),(164,'Technical writing'),(165,'Technological & digital literacy'),(166,'Telemetry'),(167,'Testing'),(168,'Todoist'),(169,'Trello'),(170,'Trigonometry'),(171,'Typography'),(172,'Vertical lookups'),(173,'Visual Basic'),(174,'Voicemail'),(175,'Web analytics'),(176,'Web scraping'),(177,'Wireframes'),(178,'Word'),(179,'Wordpress'),(180,'XML'),(181,'Yoast'),(182,'Zapier');
/*!40000 ALTER TABLE `allskills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `application` (
  `apply_id` int NOT NULL AUTO_INCREMENT,
  `status` int DEFAULT NULL,
  `date_applied` datetime(6) NOT NULL,
  `job_id_id` int DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  `eid_id` int DEFAULT NULL,
  `test_id` int DEFAULT NULL,
  `why_desc` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`apply_id`),
  KEY `application_job_id_id_f9a4cc6f_fk_jobs_jobid` (`job_id_id`),
  KEY `application_user_id_id_2a17fce3_fk_jobseeker_user_id` (`user_id_id`),
  KEY `application_eid_id_f22c798f_fk_employer_eid` (`eid_id`),
  KEY `application_test_id_dcef4565_fk_testinfo_testinfoid` (`test_id`),
  CONSTRAINT `application_eid_id_f22c798f_fk_employer_eid` FOREIGN KEY (`eid_id`) REFERENCES `employer` (`eid`),
  CONSTRAINT `application_job_id_id_f9a4cc6f_fk_jobs_jobid` FOREIGN KEY (`job_id_id`) REFERENCES `jobs` (`jobid`),
  CONSTRAINT `application_test_id_dcef4565_fk_testinfo_testinfoid` FOREIGN KEY (`test_id`) REFERENCES `testinfo` (`testinfoid`),
  CONSTRAINT `application_user_id_id_2a17fce3_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (6,3,'2023-07-15 05:26:15.760326',4,268576603,788024608,3,'skills'),(27,7,'2023-08-24 09:11:14.179922',788024618,373315377,833965419,7,'dfs'),(28,7,'2023-08-24 09:11:22.767770',788024617,373315377,833965419,4,'dfsd'),(29,5,'2023-08-25 18:27:32.810953',788024618,720061200,833965419,7,'d'),(30,3,'2023-08-28 11:21:29.285939',788024617,720061200,833965419,7,'sdf');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add employer',7,'add_employer'),(26,'Can change employer',7,'change_employer'),(27,'Can delete employer',7,'delete_employer'),(28,'Can view employer',7,'view_employer'),(29,'Can add jobs',8,'add_jobs'),(30,'Can change jobs',8,'change_jobs'),(31,'Can delete jobs',8,'delete_jobs'),(32,'Can view jobs',8,'view_jobs'),(33,'Can add job seeker',9,'add_jobseeker'),(34,'Can change job seeker',9,'change_jobseeker'),(35,'Can delete job seeker',9,'delete_jobseeker'),(36,'Can view job seeker',9,'view_jobseeker'),(37,'Can add login',10,'add_login'),(38,'Can change login',10,'change_login'),(39,'Can delete login',10,'delete_login'),(40,'Can view login',10,'view_login'),(41,'Can add selection',11,'add_selection'),(42,'Can change selection',11,'change_selection'),(43,'Can delete selection',11,'delete_selection'),(44,'Can view selection',11,'view_selection'),(45,'Can add application',12,'add_application'),(46,'Can change application',12,'change_application'),(47,'Can delete application',12,'delete_application'),(48,'Can view application',12,'view_application'),(49,'Can add experience job',13,'add_experiencejob'),(50,'Can change experience job',13,'change_experiencejob'),(51,'Can delete experience job',13,'delete_experiencejob'),(52,'Can view experience job',13,'view_experiencejob'),(53,'Can add education',14,'add_education'),(54,'Can change education',14,'change_education'),(55,'Can delete education',14,'delete_education'),(56,'Can view education',14,'view_education'),(57,'Can add profile visits',15,'add_profilevisits'),(58,'Can change profile visits',15,'change_profilevisits'),(59,'Can delete profile visits',15,'delete_profilevisits'),(60,'Can view profile visits',15,'view_profilevisits'),(61,'Can add threads',16,'add_threads'),(62,'Can change threads',16,'change_threads'),(63,'Can delete threads',16,'delete_threads'),(64,'Can view threads',16,'view_threads'),(65,'Can add messages',17,'add_messages'),(66,'Can change messages',17,'change_messages'),(67,'Can delete messages',17,'delete_messages'),(68,'Can view messages',17,'view_messages'),(69,'Can add resume analysis',18,'add_resumeanalysis'),(70,'Can change resume analysis',18,'change_resumeanalysis'),(71,'Can delete resume analysis',18,'delete_resumeanalysis'),(72,'Can view resume analysis',18,'view_resumeanalysis'),(73,'Can add liked jobs',19,'add_likedjobs'),(74,'Can change liked jobs',19,'change_likedjobs'),(75,'Can delete liked jobs',19,'delete_likedjobs'),(76,'Can view liked jobs',19,'view_likedjobs'),(77,'Can add notifications',20,'add_notifications'),(78,'Can change notifications',20,'change_notifications'),(79,'Can delete notifications',20,'delete_notifications'),(80,'Can view notifications',20,'view_notifications'),(81,'Can add test',21,'add_test'),(82,'Can change test',21,'change_test'),(83,'Can delete test',21,'delete_test'),(84,'Can view test',21,'view_test'),(85,'Can add test info',22,'add_testinfo'),(86,'Can change test info',22,'change_testinfo'),(87,'Can delete test info',22,'delete_testinfo'),(88,'Can view test info',22,'view_testinfo'),(89,'Can add test ques',23,'add_testques'),(90,'Can change test ques',23,'change_testques'),(91,'Can delete test ques',23,'delete_testques'),(92,'Can view test ques',23,'view_testques'),(93,'Can add test user',24,'add_testuser'),(94,'Can change test user',24,'change_testuser'),(95,'Can delete test user',24,'delete_testuser'),(96,'Can view test user',24,'view_testuser'),(97,'Can add interview',25,'add_interview'),(98,'Can change interview',25,'change_interview'),(99,'Can delete interview',25,'delete_interview'),(100,'Can view interview',25,'view_interview'),(101,'Can add feedback',26,'add_feedback'),(102,'Can change feedback',26,'change_feedback'),(103,'Can delete feedback',26,'delete_feedback'),(104,'Can view feedback',26,'view_feedback'),(105,'Can add newsletter',27,'add_newsletter'),(106,'Can change newsletter',27,'change_newsletter'),(107,'Can delete newsletter',27,'delete_newsletter'),(108,'Can view newsletter',27,'view_newsletter'),(109,'Can add all skills',28,'add_allskills'),(110,'Can change all skills',28,'change_allskills'),(111,'Can delete all skills',28,'delete_allskills'),(112,'Can view all skills',28,'view_allskills'),(113,'Can add course',29,'add_course'),(114,'Can change course',29,'change_course'),(115,'Can delete course',29,'delete_course'),(116,'Can view course',29,'view_course'),(117,'Can add role details',30,'add_roledetails'),(118,'Can change role details',30,'change_roledetails'),(119,'Can delete role details',30,'delete_roledetails'),(120,'Can view role details',30,'view_roledetails'),(121,'Can add admin',31,'add_admin'),(122,'Can change admin',31,'change_admin'),(123,'Can delete admin',31,'delete_admin'),(124,'Can view admin',31,'view_admin'),(125,'Can add email address',32,'add_emailaddress'),(126,'Can change email address',32,'change_emailaddress'),(127,'Can delete email address',32,'delete_emailaddress'),(128,'Can view email address',32,'view_emailaddress'),(129,'Can add email confirmation',33,'add_emailconfirmation'),(130,'Can change email confirmation',33,'change_emailconfirmation'),(131,'Can delete email confirmation',33,'delete_emailconfirmation'),(132,'Can view email confirmation',33,'view_emailconfirmation'),(133,'Can add social account',34,'add_socialaccount'),(134,'Can change social account',34,'change_socialaccount'),(135,'Can delete social account',34,'delete_socialaccount'),(136,'Can view social account',34,'view_socialaccount'),(137,'Can add social application',35,'add_socialapp'),(138,'Can change social application',35,'change_socialapp'),(139,'Can delete social application',35,'delete_socialapp'),(140,'Can view social application',35,'view_socialapp'),(141,'Can add social application token',36,'add_socialtoken'),(142,'Can change social application token',36,'change_socialtoken'),(143,'Can delete social application token',36,'delete_socialtoken'),(144,'Can view social application token',36,'view_socialtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$SkjVqUXSMndarJ9M1jlL9o$SygX1E6wHqrPCsvM2ZafU9VVC877pyVAEaWFmicVyJ8=','2023-08-26 10:11:48.304424',1,'aditya','','','',1,1,'2023-08-26 10:07:30.165345');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `institution_type` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'Bachelor of Arts (BA)','',''),(2,'Bachelor of Science (BSc)','',''),(3,'Bachelor of Commerce (BCom)','',''),(4,'Bachelor of Business Administration (BBA)','',''),(5,'Bachelor of Engineering (BE)','',''),(6,'Bachelor of Technology (B.Tech)','',''),(7,'Bachelor of Architecture (B.Arch)','',''),(8,'Bachelor of Fine Arts (BFA)','',''),(9,'Bachelor of Design (B.Des)','',''),(10,'Bachelor of Pharmacy (B.Pharm)','',''),(11,'Bachelor of Medicine, Bachelor of Surgery (MBBS)','',''),(12,'Bachelor of Dental Surgery (BDS)','',''),(13,'Bachelor of Ayurvedic Medicine and Surgery (BAMS)','',''),(14,'Bachelor of Homoeopathic Medicine and Surgery (BHMS)','',''),(15,'Bachelor of Physiotherapy (BPT)','',''),(16,'Bachelor of Occupational Therapy (BOT)','',''),(17,'Bachelor of Veterinary Science (BVSc)','',''),(18,'Bachelor of Laws (LLB)','',''),(19,'Bachelor of Education (B.Ed)','',''),(20,'Bachelor of Hotel Management (BHM)','',''),(21,'Bachelor of Fashion Design (BFD)','',''),(22,'Master of Arts (MA)','',''),(23,'Master of Science (MSc)','',''),(24,'Master of Commerce (MCom)','',''),(25,'Master of Business Administration (MBA)','',''),(26,'Master of Technology (M.Tech)','',''),(27,'Master of Engineering (ME)','',''),(28,'Master of Architecture (M.Arch)','',''),(29,'Master of Fine Arts (MFA)','',''),(30,'Master of Design (M.Des)','',''),(31,'Master of Pharmacy (M.Pharm)','',''),(32,'Master of Medicine (MD)','',''),(33,'Master of Surgery (MS)','',''),(34,'Master of Dental Surgery (MDS)','',''),(35,'Master of Ayurvedic Medicine (MAM)','',''),(36,'Master of Homoeopathic Medicine (MHM)','',''),(37,'Master of Physiotherapy (MPT)','',''),(38,'Master of Occupational Therapy (MOT)','',''),(39,'Master of Veterinary Science (MVSc)','',''),(40,'Master of Laws (LLM)','',''),(41,'Master of Education (M.Ed)','',''),(42,'Master of Hotel Management (MHM)','',''),(43,'Master of Fashion Design (MFD)','','');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-08-26 10:29:25.110351','1','main',1,'[{\"added\": {}}]',35,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (32,'account','emailaddress'),(33,'account','emailconfirmation'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(31,'main','admin'),(28,'main','allskills'),(12,'main','application'),(29,'main','course'),(14,'main','education'),(7,'main','employer'),(13,'main','experiencejob'),(26,'main','feedback'),(25,'main','interview'),(8,'main','jobs'),(9,'main','jobseeker'),(19,'main','likedjobs'),(10,'main','login'),(17,'main','messages'),(27,'main','newsletter'),(20,'main','notifications'),(15,'main','profilevisits'),(18,'main','resumeanalysis'),(30,'main','roledetails'),(11,'main','selection'),(21,'main','test'),(22,'main','testinfo'),(23,'main','testques'),(24,'main','testuser'),(16,'main','threads'),(6,'sessions','session'),(34,'socialaccount','socialaccount'),(35,'socialaccount','socialapp'),(36,'socialaccount','socialtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-01-14 15:28:08.896213'),(2,'auth','0001_initial','2023-01-14 15:28:09.345217'),(3,'admin','0001_initial','2023-01-14 15:28:09.470450'),(4,'admin','0002_logentry_remove_auto_add','2023-01-14 15:28:09.480425'),(5,'admin','0003_logentry_add_action_flag_choices','2023-01-14 15:28:09.489700'),(6,'contenttypes','0002_remove_content_type_name','2023-01-14 15:28:09.545493'),(7,'auth','0002_alter_permission_name_max_length','2023-01-14 15:28:09.593705'),(8,'auth','0003_alter_user_email_max_length','2023-01-14 15:28:09.608663'),(9,'auth','0004_alter_user_username_opts','2023-01-14 15:28:09.618641'),(10,'auth','0005_alter_user_last_login_null','2023-01-14 15:28:09.659756'),(11,'auth','0006_require_contenttypes_0002','2023-01-14 15:28:09.663743'),(12,'auth','0007_alter_validators_add_error_messages','2023-01-14 15:28:09.674992'),(13,'auth','0008_alter_user_username_max_length','2023-01-14 15:28:09.691050'),(14,'auth','0009_alter_user_last_name_max_length','2023-01-14 15:28:09.706894'),(15,'auth','0010_alter_group_name_max_length','2023-01-14 15:28:09.726279'),(16,'auth','0011_update_proxy_permissions','2023-01-14 15:28:09.735256'),(17,'auth','0012_alter_user_first_name_max_length','2023-01-14 15:28:09.752224'),(18,'main','0001_initial','2023-01-14 15:28:10.237029'),(19,'sessions','0001_initial','2023-01-14 15:28:10.265055'),(20,'main','0002_alter_jobseeker_photo','2023-01-30 16:49:58.375268'),(21,'main','0003_alter_jobseeker_photo','2023-01-30 16:49:58.385755'),(22,'main','0004_alter_employer_logo_alter_jobseeker_resume_and_more','2023-01-30 16:49:58.401729'),(23,'main','0005_alter_application_date_applied_alter_jobs_postdate_and_more','2023-01-30 16:49:58.467184'),(24,'main','0006_jobseeker_about_jobseeker_title_experiencejob_and_more','2023-01-30 16:49:58.641197'),(25,'main','0007_profilevisits','2023-01-30 16:49:58.740375'),(26,'main','0008_threads_messages','2023-01-30 16:49:58.814795'),(27,'main','0009_alter_messages_receiver_user_and_more','2023-01-30 16:49:59.268395'),(28,'main','0010_alter_messages_receiver_user_and_more','2023-01-30 16:49:59.304501'),(29,'main','0011_resumeanalysis','2023-01-30 16:49:59.373026'),(30,'main','0012_alter_resumeanalysis_recommendations','2023-01-30 16:49:59.389495'),(31,'main','0013_jobs_jobtype','2023-01-30 16:49:59.415524'),(32,'main','0014_alter_jobs_basicpay','2023-01-30 16:49:59.466240'),(33,'main','0015_likedjobs','2023-01-30 16:49:59.637159'),(34,'main','0016_notifications','2023-01-30 16:49:59.757028'),(35,'main','0017_notifications_readed','2023-01-30 16:49:59.783141'),(36,'main','0018_remove_application_emp_id','2023-01-30 16:50:01.228976'),(37,'main','0019_alter_application_date_applied','2023-01-30 16:50:01.290350'),(38,'main','0020_jobs_skills','2023-02-13 16:41:34.522015'),(39,'main','0021_jobs_careerlevel','2023-02-13 16:41:34.549940'),(40,'main','0022_employer_city_employer_fblink_employer_inlink_and_more','2023-02-13 16:41:34.693712'),(41,'main','0023_alter_employer_logo','2023-02-13 16:41:34.706927'),(42,'main','0024_employer_cover','2023-02-13 16:41:34.726120'),(43,'main','0025_alter_employer_website','2023-02-13 16:41:34.738091'),(44,'main','0026_notifications_job_id','2023-02-13 16:41:34.806417'),(45,'main','0027_profilevisits_user_type','2023-02-13 16:41:34.826288'),(46,'main','0028_application_eid','2023-02-13 16:41:34.893143'),(47,'main','0029_threads_date','2023-02-13 16:41:34.917727'),(48,'main','0030_alter_jobs_basicpay','2023-02-13 16:41:34.977507'),(49,'main','0031_employer_about','2023-03-20 18:00:12.922491'),(50,'main','0032_jobs_requirements_jobs_responsibilities','2023-03-20 18:00:12.962499'),(51,'main','0033_quiz_questions_options','2023-03-20 18:00:13.192658'),(52,'main','0034_quiz_eid','2023-03-20 18:00:13.272985'),(53,'main','0035_remove_options_ques_id_remove_questions_quiz_id','2023-03-20 18:00:15.010366'),(54,'main','0036_delete_options_delete_questions','2023-03-20 18:00:15.049541'),(55,'main','0037_remove_quiz_eid_remove_quiz_job_id','2023-03-20 18:00:15.318257'),(56,'main','0038_delete_quiz','2023-03-20 18:00:15.326263'),(57,'main','0039_test_testinfo_testques','2023-03-20 18:00:15.572430'),(58,'main','0040_testinfo_time_limit','2023-03-20 18:00:15.612770'),(59,'main','0041_testuser','2023-03-20 18:00:15.749186'),(60,'main','0042_alter_testuser_correct_answers_and_more','2023-03-20 18:00:15.785870'),(61,'main','0043_application_test','2023-03-20 18:00:15.914239'),(62,'main','0044_notifications_testuser_id','2023-03-20 18:00:16.009722'),(63,'main','0045_interview','2023-03-20 18:00:16.161738'),(64,'main','0046_interview_schedule_date','2023-03-20 18:00:16.210063'),(65,'main','0047_application_why_desc','2023-03-20 18:00:16.242068'),(66,'main','0048_interview_c_feedback_interview_e_feedback','2023-03-20 18:00:16.306029'),(67,'main','0049_interview_is_done','2023-03-20 18:00:16.346522'),(68,'main','0050_remove_interview_c_feedback_and_more','2023-03-20 18:00:16.402483'),(69,'main','0051_interview_cand_feedback_feedback','2023-03-20 18:00:16.518938'),(70,'main','0052_interview_is_feedgiven','2023-03-20 18:00:16.570442'),(71,'main','0053_feedback_name','2023-03-20 18:00:16.594431'),(72,'main','0054_alter_jobs_postdate','2023-03-20 18:00:16.665913'),(73,'main','0055_newsletter','2023-03-20 18:00:16.681905'),(74,'main','0056_jobs_num_of_visits','2023-03-20 18:00:16.729872'),(75,'main','0057_interview_testuser_id','2023-05-11 16:02:36.507785'),(76,'main','0058_allskills_course_roledetails','2023-05-11 16:02:36.539785'),(77,'main','0059_remove_jobs_careerlevel_jobs_notice_period','2023-05-29 15:07:02.852204'),(78,'main','0060_remove_jobseeker_about_remove_jobseeker_title_and_more','2023-05-29 15:37:51.800332'),(79,'main','0061_admin','2023-07-15 04:12:50.307210'),(80,'account','0001_initial','2023-08-26 10:23:14.262588'),(81,'account','0002_email_max_length','2023-08-26 10:23:14.275552'),(82,'account','0003_alter_emailaddress_create_unique_verified_email','2023-08-26 10:23:14.294159'),(83,'account','0004_alter_emailaddress_drop_unique_email','2023-08-26 10:23:14.314239'),(84,'socialaccount','0001_initial','2023-08-26 10:23:14.396301'),(85,'socialaccount','0002_token_max_lengths','2023-08-26 10:23:14.423322'),(86,'socialaccount','0003_extra_data_default_dict','2023-08-26 10:23:14.433251'),(87,'socialaccount','0004_app_provider_id_settings','2023-08-26 10:23:14.479023');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1r9mn2yhwbgdjzk182zn2dg49vlyw918','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIiwiZW1haWwiOiJqYWk0OEBnbWFpbC5jb20iLCJub3RpZm51bSI6MH0:1qZOzG:s8EkDhtvQityqUqhNYOeVz4vGqR2V0tlAw7VNK8A5GU','2023-09-08 05:03:58.449463'),('1x8d61wdz70r5ufte0afm3j74e4rsb7u','.eJwVj11rwjAUhv9L6KW2IUtTLQirWDeKiJtublclW9I0a_OxJepE9t-XnIsD7_sceDg3wBWVIyjBF5V4di9iSj-NAhNgqXMX88MCtB8D61DreopykhAYJ1l2NapXdqbE8P564pcux5szTxyEa7NvmrvDcHxRy0Ovd4g9VPv56vf7eV0_FmOVO1xti7enRbBoqngwNFRG5QDKHKOCYDjHE-CvNjLKlNSR9sabkDPFmaTZaIRxGSHtlgvT7s4-bTeehRX6Nrxgqb5O49E0T60W0WW87PRJgRL-_QNFlU8z:1qYUvy:Y7ab8pfiTfQ7CWLH5DrZx7QXJd6QE9gs4dcC7J7NQUs','2023-09-05 17:12:50.479756'),('2mi1nrlsjrqi62uuokf5uoa3xkvhwyfa','e30:1qXF6X:O3-49-u9LSrXMq_49Fttif0ub7nF_5qg5wjWd-1wFAM','2023-09-02 06:06:33.958161'),('4fo4udou1to3q1e4h1b7l0v4j61nkuui','.eJwljW9rgzAQxr9L8N1K_ZNqrDCYXdnqKK6UMUrfSNSEZDWeLGndHP3uTdZ78XB3zz33-0NMUdmhDI1UUQF8kcRPl3Aa5w0oNEMD1XqE79YeDPWp5VGlBY3ixEsCV94zDre74oxXZFMS-fa62pL1R-rV-7wsxQP7mVrcHT_rYkpNsQheaH4ozSbl3dJ_51GXLyd4tJSeKmYJX6DZIBz1hDJMMA5jTMgMmd_B2Y1zBBiwva9YK6n_P2qfBNU9W-3couL0Ihvo51bcdzCS92eFsjC63gBSBkv-:1qZ7xU:-rONuGV0YioWdzw9lp_s0yumF6lyhJBcwV4LTK6UXMk','2023-09-07 10:53:00.486313'),('4gk7d4yy9z51xiqahaezsqtq6yip34m4','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIn0:1qXLsN:Ssq0QRLXYZAjFshoYXKfPL4OMObburshB4QQBZgKfXs','2023-09-02 13:20:23.932175'),('4n1rrewassd67t4dkmdakh36h3rai1a4','.eJwVj2trwjAUhv-KhH7U3pNeYLCKdUOK6HS6fQrZmrahzWUmWmXsv685nw7nfXgfzi-gnLAB5ECxi7zDIAnS55FRTpn7LTmYA0W0HuWltshXXzch1h0JIXKQb8dZNmVYrlTK2_7zdKVjA-PqRh3t-2t52GyiY39-58tjJ3Zh_VIcstX9521dviZDAXVcbJOP_dNkEYTTybClrZztbsadVaZ2rb0HeRpFGYJxkM2BeSiLUZt00shp9zitGfEG2UrtIYRtBbYV2Fbgarrj6RNFxGNhoQV0lWitUhrWiCsHefD3D3DDUxQ:1qTlRs:9o9niLq1jKAf3EhpdW4E91e2E7l8LMaecSSZWN9D2xE','2023-08-23 15:50:12.970725'),('4xe7epy9sorhjq6h9j1s1s6qlmzwxtq6','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIiwiZW1haWwiOiJqYWk0OEBnbWFpbC5jb20iLCJub3RpZm51bSI6MH0:1qZWLn:IdMqQy2HdANcQjnmCbvzXRR_Yh6E_KD_WCNlLXQP1rU','2023-09-08 12:55:43.503429'),('6zt6fr6x00n7aaw6dbfira94wdsa7l7q','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIiwiZW1haWwiOiJqYWk0OEBnbWFpbC5jb20ifQ:1qaW37:K5Kb52N_us_dTx1PFRoSl6u_EKKchLtknEzD7rArCco','2023-09-11 06:48:33.281025'),('8kmn2ll4in7wc1g4g2t1ggil7x3o7sup','.eJwVzdsKgjAAgOFXieGdofNYE4Iy6OBFWbOwq1jbomWauFlp9O7pf_3B_wU8J-IBAmAxZUMqLR9OmSQqNzirDVGAISiJlO9nxTpUXjJ2tc_yRmzP1xwEuzR1sFbNe4R37ZqnTYTa0PnwUMN6HW8X2f44Q4n-2eFUFGZF5zpeRpi6ib3xXpTGmTDFadJdCpLz7pDwO5EDHPffDAQORCNkuWNvCFRT9oD29qnEtahzEMDfHyIXO3U:1q7TtZ:J5L0HE75hLTp6Kgur9uLkln_tHJ6zdt4YKey7-jsEqk','2023-06-23 04:38:41.003306'),('9cqnxjg81j4vls4zzwdcgb9q83tlbmdy','.eJwVzU0LgjAAxvGvEsNjlPMtFYLAOiRpShroJaZuTm1qTTOKvnvzuT38D78vwAxVd2CDAdeI78r5rfKOgSXoEedT9yxE7LOmIMqNU6TohqRaspg0yjA1wz1xvJcf6iZGxSlJAykz3WP2dvAVZrU_WK7prUtIOYtSdzoQP49hcqb08Qn1eCuUFjEshGjmF5dgdhtg69DYyKqmid4NFWlHBmz59wcGxjZG:1pRbqU:PFASUs7tcC0KKstM206LNuv2DNON4RQnWiereSbr0P0','2023-02-27 16:38:26.716097'),('bps5hshuh3x848ghudyvhz2ao7qt4r9b','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIn0:1qXFDa:HgpQPOcSO-RA5KTIxX3JSi9-ufFHWs45o1DxIi2e9KQ','2023-09-02 06:13:50.774577'),('cs2uuv83zf9xal7ds1asgzrprcslkhkj','.eJxVjEEOwiAQRe_C2hCmggwu3XuGZmYAqRpISrsy3l2bdKHb_977LzXSupRx7Wkep6jOCtThd2OSR6obiHeqt6al1WWeWG-K3mnX1xbT87K7fweFevnWHtgJQhKMhDF7JJctEGcZ0GS0NhAMlnxkskcIPok5EQrnwMZlL-r9AQF5OMU:1qZqES:lctEChHJmKmMuPw7Z1kS6505j5wXfrm-nEGVqlnPk1w','2023-09-09 10:09:28.786194'),('d3eyudflegderbf2ptb2fb0fzisgno6i','.eJwljW9rgzAQxr9L8N1K_ZNqrDCYXdnqKK6UMUrfSNSEZDWeLGndHP3uTdZ78XB3zz33-0NMUdmhDI1UUQF8kcRPl3Aa5w0oNEMD1XqE79YeDPWp5VGlBY3ixEsCV94zDre74oxXZFMS-fa62pL1R-rV-7wsxQP7mVrcHT_rYkpNsQheaH4ozSbl3dJ_51GXLyd4tJSeKmYJX6DZIBz1hDJMMA5jTMgMmd_B2Y1zBBiwva9YK6n_P2qfBNU9W-3couL0Ihvo51bcdzCS92eFsjC63gBSBkv-:1qbdab:op2IZ8LNeEuYGId7dYpSH1r0CU8oPQOQc0s_272bBmU','2023-09-14 09:03:45.329716'),('fubhffp3o806xh1jqg38k57fqimph8tm','.eJwVjt0KgjAARl8lhndJ-FM2hSAlhIrM_IHqJlbO1DldaqVF7972XR4OnO8LMEV5CSzQ4QK1LVP05V2Qya2mQAaMs3fdJFxgV5Kk2qXNkDYzJN1U-CRvXZad6QboE8apk9HDEKlOK236ikRNUuBXf7J9lsEzgcHDdqv93PS9_riKhx3JtmOWxgteqRDFvBCJC6PQF10CrDmEijY1FCiDbmBCwMKtuzytnhRY6u8PPP48cA:1qKYJ3:bi8Sd__HiXkkkbnXyUfDt4KpHhvC48u0kVBYrfNxqaI','2023-07-29 05:59:01.841621'),('gq0ywir3lajseg63xhbg4zh3v63y4928','e30:1qXF70:SRESgoCtjM8twko7hqX94kNXON8CtZtcTw-as5pQ2-c','2023-09-02 06:07:02.735969'),('imu4v6vqvoahdbrlwlavcxaczzckti6u','.eJwdztsKgkAUheF3GbxLQkcNFIIOkChhkkXZTWx1pEFnO3hEo3fPWrf_xbfehAngJXFIyqqNkNXA6iVHohIJTTNUdTYnmRRZTp_NC6i1Ugxbm6fEZeBOfThdaHwe8SQPyPWHpyBrYnYFzqJ7ecy7CBN_7PW9t2j9HPQgCnV7d0sluJCuZwVBsFnY1tBzzODnFsShNtVMwzJV0o7y1yET_1NYtTzHThBH-3wBkmQ8KQ:1qKXPf:Tz-GUHd8SIgQ35c4B_GEfu4kXZUIRpDIPRUwrCyORCk','2023-07-29 05:01:47.900542'),('kd3ey5ne1hruk8zxlvnaj19q9hl470ha','.eJw1zU0LgjAAxvHvMjxGie6lCUEdglILBKPwElMnmm_LbcyKvnt66Ln-H_h9AG9Z1QAPKP5gctuK3vBhWXVgAQST0vRDPkWR1nnh3GXJHIQtl9rTrDgL-sZECaURsrU6BYkhN24pqHfssF_FTqFDMzzl0Q9hfE6uI3FhKegFvceUYOpDuJmUjrX8z89oDTwHrxHB2HYXQL3EXLP52Kuq6HQLPPv7AygYOOg:1qKXdu:5ayFP6aIN9Ur-OuyXvsTO6tT0nm6ae5GImmhgtCrFO0','2023-07-29 05:16:30.195027'),('m99fqo61j2neme5ohjgz9to20r5uujx2','.eJxVjEEOwiAQRe_C2hCmggwu3XuGZmYAqRpISrsy3l2bdKHb_977LzXSupRx7Wkep6jOCtThd2OSR6obiHeqt6al1WWeWG-K3mnX1xbT87K7fweFevnWHtgJQhKMhDF7JJctEGcZ0GS0NhAMlnxkskcIPok5EQrnwMZlL-r9AQF5OMU:1qZqGi:xS0Ij5rjBgrVhN_vPVO90ARFLrjnwxmC76m7vli1npo','2023-09-09 10:11:48.305800'),('new71oz4cqzgu9nmb0pnukm851gjnkre','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIiwibm90aWZudW0iOjAsImVtYWlsIjoiamFpNDhAZ21haWwuY29tIn0:1qXMkd:ZRyTcCdkpCoyQkdHzb6p8RD9KkmmB-RPjkZmL-gXjWA','2023-09-02 14:16:27.369238'),('nr8plnymeib6mjnyvjsagd7kgtls2vg8','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIn0:1qXFXZ:CN7u9KDnz2jysH-fi_m31gtom9NS6UI3wIG7qKOmJtM','2023-09-02 06:34:29.402370'),('puferngspbchsondrytfjz7xc1yxbka9','.eJwVjt0KgjAARl8lhndFLCubQpARQUVm_kB1Eyu31DlduUqL3r3tuzwcON8XEI6zAjhAkhzXtYDD2U2T_rXioAeEYu_qkShBXFhCzXOdYnNsGUMbqhneqiikvQzwJ4zpPOX7NhrMa2PdlCx6JDl5NUfXFyk6MRTc3WW5m9i-1xwWcbtl6aYraDxVlRJzogqRvtAJfd1lwJkgBM2RBVEPyFZogWi3khktnxw48PcHPPw8bw:1pzTEq:EAe5dv9aho5GXY7R5mkHep9DQ8FpOhvwDGUbJ1bMkiE','2023-06-01 02:19:32.929740'),('svvl7nlu6rz25gwrx9zmveaglcrjjx8f','e30:1qXExv:rdPheHFnCQlja2aXWJRrMTnJ8b8npEHUmCc20zzLAns','2023-09-02 05:57:39.158927'),('tamzi2q3mqv0keqtiyzlyeg8kgzts5h1','.eJwVjt0KgjAARl8lhndJ-FM2hSAlhIrM_IHqJlbO1DldaqVF7972XR4OnO8LMEV5CSzQ4QK1LVP05V2Qya2mQAaMs3fdJFxgV5Kk2qXNkDYzJN1U-CRvXZad6QboE8apk9HDEKlOK236ikRNUuBXf7J9lsEzgcHDdqv93PS9_riKhx3JtmOWxgteqRDFvBCJC6PQF10CrDmEijY1FCiDbmBCwMKtuzytnhRY6u8PPP48cA:1q6oq3:ESS4lQ8M9jY4SEx4XUFuzpD0ToR2A4IIdJ4xXlO-YYE','2023-06-21 08:48:19.770647'),('tpyk8lt67b9g88we3blb3z4116mp4msl','e30:1qXFBk:lqxsBGSV9ug9ac7WFxSz2Z5GC_Lxyiqy14zpLBZ4chs','2023-09-02 06:11:56.335891'),('u8xdl8fuofxo498e6dak6xy19sbpp774','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIiwiZW1haWwiOiJqYWk0OEBnbWFpbC5jb20iLCJub3RpZm51bSI6MH0:1qYO11:9gPZSx4AZyD9kV9kFu_6Hx8DGkEWjV4XibRMJ4Fk780','2023-09-05 09:49:35.060840'),('vgwww1taqqb1mv2hd1i2ogb4v4j851pp','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIn0:1qXFaN:lBOAHMa04mKucxO1SF6kq99XcbAT2U6xFb7-Op-pG8A','2023-09-02 06:37:23.137747'),('ws2aip1d5tomp6f2dje2uguftbu2yyh5','eyJuYW1lIjoiSmFpIiwicGsiOjU0Mjc2NDA5NCwidHlwZSI6ImFkbWluIn0:1qXFVK:qt3vtHPT3voptP-pI903pO2UHDcWcUP6-1I8boPcbyQ','2023-09-02 06:32:10.129939'),('ygysdufpkko7tuab3kzas1qumojxauuz','.eJwVjt0KgjAARl8lhndJ-FM2hSAlhIrM_IHqJlbO1DldaqVF7972XR4OnO8LMEV5CSzQ4QK1LVP05V2Qya2mQAaMs3fdJFxgV5Kk2qXNkDYzJN1U-CRvXZad6QboE8apk9HDEKlOK236ikRNUuBXf7J9lsEzgcHDdqv93PS9_riKhx3JtmOWxgteqRDFvBCJC6PQF10CrDmEijY1FCiDbmBCwMKtuzytnhRY6u8PPP48cA:1qLe7N:x3-oj-fvCb3k-xDbGKfqzfhkg--d6FjvT5J76zW7-v8','2023-08-01 06:23:29.388783');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `education`
--

DROP TABLE IF EXISTS `education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `education` (
  `edu_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `school` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `time_period` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  PRIMARY KEY (`edu_id`),
  KEY `education_user_id_id_1a7f30a2_fk_jobseeker_user_id` (`user_id_id`),
  CONSTRAINT `education_user_id_id_1a7f30a2_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `education`
--

LOCK TABLES `education` WRITE;
/*!40000 ALTER TABLE `education` DISABLE KEYS */;
/*!40000 ALTER TABLE `education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employer`
--

DROP TABLE IF EXISTS `employer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employer` (
  `eid` int NOT NULL AUTO_INCREMENT,
  `ename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `etype` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `pincode` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `executive` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `profile` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `logo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `log_id_id` int DEFAULT NULL,
  `city` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fblink` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `inlink` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `lnlink` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `size` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `twlink` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `website` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `yearfounded` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cover` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `about` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`eid`),
  KEY `employer_log_id_id_e795f862_fk_login_log_id` (`log_id_id`),
  CONSTRAINT `employer_log_id_id_e795f862_fk_login_log_id` FOREIGN KEY (`log_id_id`) REFERENCES `login` (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=833965420 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employer`
--

LOCK TABLES `employer` WRITE;
/*!40000 ALTER TABLE `employer` DISABLE KEYS */;
INSERT INTO `employer` VALUES (1,'Infosys Pvt Ltd','Company','Software Services','Infosys,\r\nIT Zone,\r\n4 - BE,\r\nBangalore','458796','Ajith','9145512345','India,Karnataka,Bengaluru','Infosys is a global leader in consulting, technology, and outsourcing and next-generation services. We enable clients in more than 50 countries to outperform the competition and stay ahead of the innovation curve.','logos/65_fly_high_Logo_company-logo-4.png',18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'Microsoft','Company','Software Services','Microsoft, Bangalore, Karnataka','456987','Arun','78945612332','India,Karnataka,Bommasandra',NULL,'logos/65_fly_high_Logo_company-logo-4.png',23,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(195855682,'New solutions','Private Limited Companies','Engineering & Construction','jaipur','302005','xyz','+917777777777','jaipur','Building future.','images/company-logo-4.png',60,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','Not Specified'),(244046007,'Adidas','Public Limited Companies','Energy','Hyderabad','460000','Adarsh','+917777777777','Hyderabad','Advancement','',63,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','Not Specified'),(465937626,'Nike','Private Limited Companies','Engineering & Construction','123,crystle park','400000','Rohit','+917777777777','Mumbai','Awesome new','',62,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','Not Specified'),(561320412,'Jack solutions','Public Limited Companies','Engineering & Construction','123,xyz','302005','Jack jacob','+917777777777','Delhi','Company','logos/61_Jack_solutions_Logo_jack.png',61,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','Not Specified'),(690818567,'fly high','Private Limited Companies','Engineering & Construction','W.B','456789','Raghav','+917777777777','W.B','sdf','logos/65_fly_high_Logo_company-logo-4.png',65,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','Not Specified'),(788024608,'Tejas SP','Partnership','Technology','#1980, 3rd floor, BSK 3rd Stage,','560070','Tejas Solutions','+917892210440','Bengaluru','I am the CEO of the company','',25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'','Not Specified'),(833965419,'Nego Pvt. Ltd.','Limited Liability Partnership','Business Services','23, WTC','560000','Mr. Paul','+917777777777','Bengaluru','Software Solutions.','logos/66_Nego_Pvt._Ltd._Logo_company-logo-5.png',66,'','','','','1','','','','cover/833965419_Nego_Pvt._Ltd._Cover_Screenshot_2023-07-27_at_6.25.28_PM-removebg-preview.png','Not Specified');
/*!40000 ALTER TABLE `employer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiencejob`
--

DROP TABLE IF EXISTS `experiencejob`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencejob` (
  `exp_id` int NOT NULL AUTO_INCREMENT,
  `job_title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `company` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `time_period` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  PRIMARY KEY (`exp_id`),
  KEY `experiencejob_user_id_id_dd124db4_fk_jobseeker_user_id` (`user_id_id`),
  CONSTRAINT `experiencejob_user_id_id_dd124db4_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiencejob`
--

LOCK TABLES `experiencejob` WRITE;
/*!40000 ALTER TABLE `experiencejob` DISABLE KEYS */;
/*!40000 ALTER TABLE `experiencejob` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feed_id` int NOT NULL AUTO_INCREMENT,
  `emp_feedback` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `int_id_id` int DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`feed_id`),
  KEY `feedback_int_id_id_bd444828_fk_interview_int_id` (`int_id_id`),
  CONSTRAINT `feedback_int_id_id_bd444828_fk_interview_int_id` FOREIGN KEY (`int_id_id`) REFERENCES `interview` (`int_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,'asdfsd',7,'modified',3),(2,'dsfsd',8,'Aditya vyas',NULL);
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interview`
--

DROP TABLE IF EXISTS `interview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interview` (
  `int_id` int NOT NULL AUTO_INCREMENT,
  `int_link` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `eid_id` int DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  `schedule_date` datetime(6) NOT NULL,
  `is_done` tinyint(1) NOT NULL,
  `cand_feedback` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `is_feedgiven` tinyint(1) NOT NULL,
  `testuser_id_id` int DEFAULT NULL,
  `apply_id_id` int DEFAULT NULL,
  `panel_req` int DEFAULT '0',
  PRIMARY KEY (`int_id`),
  KEY `interview_eid_id_4dd247b1_fk_employer_eid` (`eid_id`),
  KEY `interview_user_id_id_68eb00db_fk_jobseeker_user_id` (`user_id_id`),
  KEY `interview_testuser_id_id_3017b5a9_fk_testuser_testuser_id` (`testuser_id_id`),
  CONSTRAINT `interview_eid_id_4dd247b1_fk_employer_eid` FOREIGN KEY (`eid_id`) REFERENCES `employer` (`eid`),
  CONSTRAINT `interview_testuser_id_id_3017b5a9_fk_testuser_testuser_id` FOREIGN KEY (`testuser_id_id`) REFERENCES `testuser` (`testuser_id`),
  CONSTRAINT `interview_user_id_id_68eb00db_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interview`
--

LOCK TABLES `interview` WRITE;
/*!40000 ALTER TABLE `interview` DISABLE KEYS */;
INSERT INTO `interview` VALUES (2,'https://ad-30.github.io',833965419,720061200,'2023-08-23 16:05:00.000000',0,NULL,0,NULL,NULL,0),(3,'https://ad-30.github.io/SyncX',833965419,450211284,'2023-08-12 14:30:00.000000',1,NULL,0,NULL,NULL,0),(7,'https://ad-30.github.io',833965419,373315377,'2023-08-24 14:34:00.000000',1,NULL,1,NULL,27,0),(8,'https://ad-30.github.io',833965419,373315377,'2023-08-24 17:00:00.000000',1,NULL,1,NULL,28,0),(14,'https://ad-30.github.io/Syncx',833965419,720061200,'2023-08-26 00:03:00.000000',0,NULL,0,NULL,29,0);
/*!40000 ALTER TABLE `interview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `jobid` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `jobdesc` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `vacno` int DEFAULT NULL,
  `experience` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `basicpay` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fnarea` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `industry` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ugqual` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `pgqual` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `profile` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `postdate` datetime(6) NOT NULL,
  `eid_id` int DEFAULT NULL,
  `jobtype` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `skills` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `requirements` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `responsibilities` varchar(700) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `num_of_visits` int NOT NULL,
  `notice_period` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` int DEFAULT '3',
  `suggestions` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '[]',
  PRIMARY KEY (`jobid`),
  KEY `jobs_eid_id_f7ade560_fk_employer_eid` (`eid_id`),
  CONSTRAINT `jobs_eid_id_f7ade560_fk_employer_eid` FOREIGN KEY (`eid_id`) REFERENCES `employer` (`eid`)
) ENGINE=InnoDB AUTO_INCREMENT=788024625 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,'Network Administrator','Consulting with clients to specify system requirements and design solutions\nBudgeting for equipment and assembly costs\nAssembling new systems\nMaintaining existing software and hardware and upgrading any that have become obsolete\nWorking in tandem with IT support personnel\nProviding network administration and support',3,'7','2','Marketing & Communication','India,Karnataka,Bengaluru','Software Services','B.Tech/B.E.','M.Tech','Patience,\r\nTechnical skills.\r\nIT skills,\r\nInterpersonal skills,\r\nEnthusiasm,\r\nTeamworking skills,\r\nInitiative,\r\nCommitment to quality,\r\nAttention to detail.','2023-06-15 00:00:00.000000',2,'Internship','php,mysql','btech','dsgsdg,dfg,dgdfg,fdg',663,'15 Week',3,'[[603839799, 51.78], [858532288, 51.78], [986316475, 51.78], [81570264, 51.13], [373315377, 51.13], [450211284, 51.13], [824712288, 51.13], [503284360, 50.46], [567825742, 45.92], [794246454, 45.92], [379358397, 43.84], [395157575, 43.72], [672634308, 43.72], [673070026, 43.72], [762552912, 43.72], [720061200, 43.57], [165026623, 41.92], [856298255, 41.92], [823140842, 39.78], [712589075, 39.55]]'),(3,'Software Engineer','The focus of this position is the design and development of the core V-PIL services infrastructure, including custom automation software, job schedulers, data analysis, data visualization, and web development.',3,'5','2','Network Virtualizing','India,Karnataka,Bengaluru','Software Services','B.Tech/B.E.','M.Tech','Strong ability in JavaScript.\r\nStrong ability in database design.\r\nExperience developing and executing performance test suites.\r\nStrong test suite development, execution and automation experience.\r\nFamiliarity with Jenkins and knowledge of existing cloud test suites, including Tempest and Rally.\r\nExperience with continuous integration practices.\r\nExperience with Juju, Charms and MAAS.','2015-04-16 00:00:00.000000',1,'Remote','php,mysql','btech','dfgdfgdfg,dgd,fgdfgd,',69,'20',3,'[[720061200, 42.64], [395157575, 42.46], [379358397, 41.88], [856298255, 41.88], [603839799, 41.07], [165026623, 40.66], [567825742, 40.66], [672634308, 40.66], [673070026, 40.66], [762552912, 40.66], [794246454, 40.66], [81570264, 40.65], [373315377, 40.65], [450211284, 40.65], [858532288, 40.65], [986316475, 40.64], [824712288, 40.21], [503284360, 39.78], [268576603, 34.66], [731095221, 34.12]]'),(4,'Web Developer','Development of interactive websites at microfost',5,'3','3','Web Development','India,Kerala,Ernakulam','Software Services','B.Tech/B.E.','Not Pursuing Post Graduation','Knowledge in ASP.NET, SQL server','2016-04-16 00:00:00.000000',1,'Remote','php,mysql','btech','fgdfgd,gdfgdfg,fgd',168,'20',3,'[[395157575, 47.59], [567825742, 47.59], [672634308, 47.59], [673070026, 47.59], [762552912, 47.59], [794246454, 47.59], [860445751, 46.49], [165026623, 45.65], [379358397, 45.65], [856298255, 45.65], [81570264, 44.34], [373315377, 44.34], [450211284, 44.34], [603839799, 44.34], [824712288, 44.34], [986316475, 44.34], [503284360, 43.04], [309791485, 42.58], [720061200, 37.59], [435001728, 36.9]]'),(788024617,'Front-end Web deveoper','We are seeking a skilled and creative Frontend Web Developer to join our dynamic team. The ideal candidate will possess a strong foundation in web development technologies and techniques, with a focus on creating visually appealing and user-friendly interfaces. You will collaborate closely with our design and backend development teams to bring engaging and responsive web experiences to life.',NULL,'0','1','Front-end Developer','Bengaluru',NULL,NULL,NULL,NULL,'2023-08-24 03:38:58.935592',833965419,'Full Time','html,css,javascript,React.js,angular.js,figma,wordpress','Bachelor\'s degree in Computer Science, Web Development, or a related field (or equivalent experience).\r\nProven experience as a Frontend Web Developer or similar role.\r\nProficiency in HTML, CSS, JavaScript, and related frontend technologies.\r\nStrong experience with frontend frameworks such as React, Angular, or Vue.js.\r\nFamiliarity with version control systems (e.g., Git) and collaborative development workflows.\r\nExperience with responsive and mobile-first design principles.','Collaborate with designers and backend developers to translate wireframes and mockups into interactive web applications.\r\nDevelop and maintain efficient, reusable, and high-performance frontend code using HTML, CSS, and JavaScript frameworks.\r\nImplement responsive design principles to ensure seamless user experiences across various devices and screen sizes.\r\nOptimize application performance by identifying bottlenecks and finding solutions to improve loading times and overall responsiveness.',4,NULL,7,'[]'),(788024618,'Back-end Developer','We are in search of a skilled and motivated Backend Developer to join our dynamic team. The ideal candidate will have a strong background in server-side development, databases, and API integration. You will work closely with our frontend and design teams to architect and build robust and scalable backend systems that power our web applications.',NULL,'0','1','Back-end Developer','Jaipur',NULL,NULL,NULL,NULL,'2023-08-24 03:40:46.937120',833965419,'Full Time','Node.js,javascript,python,django,mongodb,php,mysql','Bachelor\'s degree in Computer Science, Software Engineering, or a related field (or equivalent experience).\r\nProven experience as a Backend Developer or similar role.\r\nStrong proficiency in server-side programming languages such as Python, Java, Ruby, or Node.js.\r\nExperience with backend frameworks like Django, Flask, Ruby on Rails, or Express.js.\r\nSolid understanding of RESTful API design principles.\r\nProficiency in database management systems, both SQL (e.g., PostgreSQL, MySQL) and NoSQL (e.g., MongoDB, Redis).','Collaborate with frontend developers, designers, and other cross-functional teams to design, develop, and maintain efficient backend systems.\r\nBuild and maintain APIs for seamless communication between the frontend and backend components of our applications.\r\nDevelop secure and scalable server-side logic, handling data storage, user authentication, and application logic.\r\nDesign and optimize databases, ensuring efficient data retrieval and storage while maintaining data integrity.',13,NULL,4,'[[373315377, 55.13], [450211284, 54.84], [309791485, 47.24], [603839799, 45.64], [567825742, 43.9], [672634308, 43.9], [762552912, 43.9], [794246454, 43.9], [856298255, 43.9], [165026623, 43.68], [379358397, 43.68], [673070026, 43.68], [395157575, 43.26], [81570264, 36.16], [268576603, 36.0], [969454803, 35.67], [824712288, 35.6], [819924985, 35.52], [435001728, 35.48], [606572057, 35.48]]');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobseeker`
--

DROP TABLE IF EXISTS `jobseeker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobseeker` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `experience` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `skills` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `basic_edu` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `master_edu` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `other_qual` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dob` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Resume` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `photo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `log_id_id` int DEFAULT NULL,
  `cursal` int NOT NULL,
  `expsal` int NOT NULL,
  `notice_period` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `role` varchar(750) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `jobseeker_log_id_id_7dfa8485_fk_login_log_id` (`log_id_id`),
  CONSTRAINT `jobseeker_log_id_id_7dfa8485_fk_login_log_id` FOREIGN KEY (`log_id_id`) REFERENCES `login` (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=986316476 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobseeker`
--

LOCK TABLES `jobseeker` WRITE;
/*!40000 ALTER TABLE `jobseeker` DISABLE KEYS */;
INSERT INTO `jobseeker` VALUES (81570264,'NewUser','+911111111111','123,xyz','1','Angular JS / Node Js,C / C++,MySQL / Database,PHP,Python,','Bachelor of Engineering (BE)','Master of Technology (M.Tech)','Bachelor of Technology (B.Tech)','2000-02-02','resumes/67_NewUser_Resume_AdityaVyasResume.__1.pdf','photos/67_NewUser_Photo_6BF937FD-41E9-4095-A19E-8B53A5E516F8_1_105_c-fotor-2023062421402_10.png',67,50000,400000,'15 Week','Web Developer'),(165026623,'testuser21','+917777777777','123,xyz','0','PHP,','Bachelor of Arts (BA)','Bachelor of Engineering (BE)','Bachelor of Technology (B.Tech)','2000-02-02','resumes/52_testuser21_Resume_AdityaVyasResume._.pdf','',52,0,1,'2 Month',NULL),(237615633,'testuser5','+915555555555','123,xyz','0','App Development(iOS,Android,Windows),','Bachelor of Business Administration (BBA)','Bachelor of Business Administration (BBA)','Bachelor of Technology (B.Tech)','2004-04-23','resumes/237615633_testuser5_Resume_AdityaVyasResume._.pdf','',37,0,180,'4 Month',NULL),(268576603,'tejas','+917894561233','#36, 2nd floor, 4th cross, Kanaka Layout','0','Angular JS / Node Js,C / C++,Java / J2EE,','Bachelor of Engineering (BE)','Bachelor of Technology (B.Tech)','Bachelor of Business Administration (BBA)','1998-03-03','resumes/31_tejas_Resume_Tejas_S_P_Resume.pdf','',31,300000,1000000,NULL,NULL),(309791485,'Tejas SP','+917892210440','#1980, 3rd floor, BSK 3rd Stage,','0','C / C++,Python,','Bachelor of Technology (B.Tech)',NULL,NULL,'2003-03-03','resumes/24_Tejas_SP_Resume_Bhaviks_Resume_W86cWv5.pdf','',24,250000,600000,NULL,NULL),(373315377,'joseph','+915555555555','Jaipur','0','Angular JS / Node Js,C / C++,MySQL / Database,Django,PHP,Python,CSS,HTML,','Bachelor of Technology (B.Tech)','Master of Technology (M.Tech)','Bachelor of Engineering (BE)','2000-02-02','resumes/70_joseph_Resume_AdityaVyasResume.__1.pdf','photos/70_joseph_Photo_favicon.ico',70,0,1,'15 Week','Web Developer'),(379358397,'Aditya','+917777777777','123,xyz','0','PHP,','Bachelor of Business Administration (BBA)','Bachelor of Business Administration (BBA)','Bachelor of Technology (B.Tech)','2000-02-02','resumes/53_Aditya_Resume_AdityaVyasResume._.pdf','',53,0,1,'2 Month',NULL),(395157575,'testuser19','+917777777777','123,xyz','0','PHP,','Bachelor of Commerce (BCom)','Bachelor of Arts (BA)','Bachelor of Medicine, Bachelor of Surgery (MBBS)','2000-02-02','resumes/50_testuser19_Resume_AdityaVyasResume._.pdf','',50,0,1,'2 Month',NULL),(435001728,'testuser10','+917777777777','123,xyz','1','App Development(iOS,Android,Windows),','Bachelor of Engineering (BE)','Bachelor of Commerce (BCom)','Bachelor of Arts (BA)','2000-02-20','resumes/42_testuser10_Resume_AdityaVyasResume.__LQ9NclK.pdf','',42,0,1,'2 Month',NULL),(450211284,'TestUser','+910000000000','Jaipur','0','C / C++,MySQL / Database,Django,PHP,Python,','Bachelor of Technology (B.Tech)','Master of Technology (M.Tech)','Bachelor of Engineering (BE)','2000-02-02','resumes/71_TestUser_Resume_AdityaVyasResume.__1.pdf','photos/71_TestUser_Photo_IMG_20230630_133025_vnkw0j2.jpg',71,0,1,'15 Week','Web Developer'),(464175163,'testuser','+911111111111','123,xyz','0','Angular JS / Node Js,C / C++,','Bachelor of Arts (BA)','Bachelor of Commerce (BCom)','Bachelor of Engineering (BE)','2001-03-30','resumes/34_testuser_Resume_AdityaVyasResume._.pdf','',34,0,1000000,NULL,NULL),(503284360,'testuser24','+917777777777','123,xyz','1','PHP,Acrobat,','Bachelor of Technology (B.Tech)','Master of Technology (M.Tech)','Bachelor of Engineering (BE)','2000-02-02','resumes/57_testuser24_Resume_39_testuser7_Resume_AdityaVyasResume._.pdf','',57,0,500000,'15 Week',NULL),(567825742,'testuser20','+917777777777','123,xyz','1','PHP,','Bachelor of Science (BSc)','Bachelor of Business Administration (BBA)','Bachelor of Engineering (BE)','2000-02-20','resumes/51_testuser20_Resume_AdityaVyasResume.__Zw6k4hf.pdf','',51,0,1,'1 Month',NULL),(603839799,'Always','+914444444444','Bengaluru','0','Angular JS / Node Js,C / C++,MySQL / Database,PHP,','Bachelor of Technology (B.Tech)','Master of Technology (M.Tech)','Bachelor of Engineering (BE)','2000-02-20','resumes/69_Always_Resume_AdityaVyasResume.__1.pdf','photos/69_Always_Photo_Screenshot_2023-07-27_at_6.25.28_PM-removebg-preview.png',69,0,1,'15 Week','Front-end Developer'),(604117780,'testuser8','+913333333333','123,xyz','0','App Development(iOS,Android,Windows),C / C++,','Bachelor of Engineering (BE)','Bachelor of Arts (BA)','Bachelor of Engineering (BE)','2000-01-10','resumes/40_testuser8_Resume_AdityaVyasResume._.pdf','',40,0,11,'2 Month',NULL),(606572057,'testuser12','+917777777777','123,xyz','2','App Development(iOS,Android,Windows),','Bachelor of Business Administration (BBA)','Bachelor of Engineering (BE)','Bachelor of Business Administration (BBA)','2000-02-02','resumes/44_testuser12_Resume_AdityaVyasResume.__6iVeE9W.pdf','',44,0,1,'2 Week',NULL),(672634308,'testuser16','+917777777777','123,xyz','0','PHP,','Bachelor of Arts (BA)','Bachelor of Science (BSc)','Bachelor of Engineering (BE)','2000-02-20','resumes/48_testuser16_Resume_AdityaVyasResume._.pdf','',48,0,1,'2 Week',NULL),(673070026,'testuser14','+917777777777','123,xyz','0','PHP,','Bachelor of Engineering (BE)','Bachelor of Commerce (BCom)','Bachelor of Commerce (BCom)','2000-02-02','resumes/46_testuser14_Resume_AdityaVyasResume.__qdfD9cy.pdf','',46,0,1,'2 Month',NULL),(710946856,'testuser6','+910000000000','123,xyz','2','App Development(iOS,Android,Windows),','Bachelor of Engineering (BE)','Bachelor of Engineering (BE)','Bachelor of Engineering (BE)','2003-03-30','resumes/38_testuser6_Resume_AdityaVyasResume.__ku3KXPr.pdf','',38,0,1,'1 Month',NULL),(712589075,'testuser23','+917777777777','123,xyz','0','MySQL / Database,PHP,','Bachelor of Technology (B.Tech)','Master of Technology (M.Tech)','Bachelor of Technology (B.Tech)','2000-02-02','resumes/56_testuser23_Resume_55_Aditya_Resume_AdityaVyasResume._.pdf','',56,0,6000000,'15 Week',NULL),(720061200,'user123','+911111111111','123,xyz','0','Angular JS / Node Js,C / C++,,php,CSS','Bachelor of Science (BSc)','Bachelor of Science (BSc)','Bachelor of Arts (BA)','2000-10-01','resumes/33_user123_Resume_AdityaVyasResume.__CFCXr5k.pdf','',33,0,1000000,NULL,NULL),(731095221,'testuser7','+919999999999','123,xyz','1','Networking / CCNA,c#,Big Data / Hadoop,Cloud Computing,','Bachelor of Science (BSc)','Bachelor of Business Administration (BBA)','Bachelor of Business Administration (BBA)','2000-01-10','resumes/39_testuser7_Resume_AdityaVyasResume._.pdf','',39,0,1,'34 Month',NULL),(762552912,'Aditya','+917777777777','123,xyz','2','PHP,','Bachelor of Science (BSc)','Bachelor of Arts (BA)','Bachelor of Engineering (BE)','2000-02-02','resumes/54_Aditya_Resume_AdityaVyasResume._.pdf','',54,0,1,'1 Week',NULL),(794246454,'testuser15','+917777777777','123,xyz','0','PHP,','Bachelor of Science (BSc)','Bachelor of Business Administration (BBA)','Bachelor of Engineering (BE)','2000-02-02','resumes/47_testuser15_Resume_AdityaVyasResume._.pdf','',47,0,1,'2 Month',NULL),(819924985,'testuser13','+917777777777','123,xyz','0','App Development(iOS,Android,Windows),','Bachelor of Arts (BA)','Bachelor of Commerce (BCom)','Bachelor of Technology (B.Tech)','2000-02-20','resumes/45_testuser13_Resume_AdityaVyasResume._.pdf','',45,0,1,'2 Week',NULL),(823140842,'Aditya','+917777777777','123,xyz','0','C / C++,Python,','Bachelor of Technology (B.Tech)','Master of Technology (M.Tech)','Bachelor of Engineering (BE)','2000-02-02','resumes/58_Aditya_Resume_57_testuser24_Resume_39_testuser7_Resume_AdityaVyasResume._.pdf','',58,0,500000,'15 Week',NULL),(824712288,'Never','+913333333333','123,xyz','0','Angular JS / Node Js,MySQL / Database,PHP,Bookkeeping through Excel or TurboTax,CSS,HTML,Javascript,','Bachelor of Engineering (BE)','Master of Technology (M.Tech)','Bachelor of Technology (B.Tech)','2000-02-02','resumes/68_Never_Resume_AdityaVyasResume.__1.pdf','',68,0,100000,'15 Week','Front-end Developer'),(856298255,'Aditya','+917777777777','123,xyz','0','PHP,','Bachelor of Science (BSc)','Bachelor of Arts (BA)','Bachelor of Technology (B.Tech)','2000-02-02','resumes/55_Aditya_Resume_AdityaVyasResume._.pdf','',55,0,1,'1 Month',NULL),(858532288,'testuser24','+917777777777','India,Karnataka,Bengaluru','1','C / C++,MongoDB,Django,','Bachelor of Technology (B.Tech)','Master of Technology (M.Tech)','Bachelor of Engineering (BE)','2000-02-02','resumes/59_testuser24_Resume_58_Aditya_Resume_57_testuser24_Resume_39_testuser7_Resume_A_lRTuweg.pdf','',59,0,500000,'15 Week','Web Developer'),(858846653,'testuser9','+917777777777','123,xyz','1','Angular JS / Node Js,','Bachelor of Science (BSc)','Bachelor of Technology (B.Tech)','Bachelor of Business Administration (BBA)','2000-02-20','resumes/41_testuser9_Resume_AdityaVyasResume.__hfgGoWT.pdf','',41,0,1,'3 Month',NULL),(860445751,'testuser3','+914444444444','123,xyz','3','C / C++,','Bachelor of Engineering (BE)','Bachelor of Engineering (BE)','Bachelor of Engineering (BE)','2000-10-01','resumes/35_testuser3_Resume_AdityaVyasResume._.pdf','',35,0,1,NULL,NULL),(948142271,'testuser11','+917777777777','123,xyz','1','Angular JS / Node Js,','Bachelor of Business Administration (BBA)','Bachelor of Engineering (BE)','Bachelor of Commerce (BCom)','2000-02-20','resumes/43_testuser11_Resume_AdityaVyasResume._.pdf','',43,0,1,'2 Week',NULL),(969454803,'Aditya Vyas','+917777777777','123,xyz','0','App Development(iOS,Android,Windows),','Bachelor of Commerce (BCom)','Bachelor of Science (BSc)','Bachelor of Engineering (BE)','2000-02-02','resumes/49_Aditya_Vyas_Resume_AdityaVyasResume.__9B0P10j.pdf','',49,0,1,'2 Month',NULL),(986316475,'Fly high','+917777777777','bengaluru','0','MySQL / Database,PHP,CSS,HTML,Javascript,','Bachelor of Engineering (BE)','Master of Technology (M.Tech)','Bachelor of Technology (B.Tech)','2000-02-02','resumes/64_Fly_high_Resume_AdityaVyasResume.__1.pdf','',64,0,500000,'15 Week','Front-end Developer');
/*!40000 ALTER TABLE `jobseeker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likedjobs`
--

DROP TABLE IF EXISTS `likedjobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likedjobs` (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `likedate` datetime(6) NOT NULL,
  `job_id_id` int DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  PRIMARY KEY (`like_id`),
  KEY `likedjobs_job_id_id_e6daa0c5_fk_jobs_jobid` (`job_id_id`),
  KEY `likedjobs_user_id_id_bfde263c_fk_jobseeker_user_id` (`user_id_id`),
  CONSTRAINT `likedjobs_job_id_id_e6daa0c5_fk_jobs_jobid` FOREIGN KEY (`job_id_id`) REFERENCES `jobs` (`jobid`),
  CONSTRAINT `likedjobs_user_id_id_bfde263c_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likedjobs`
--

LOCK TABLES `likedjobs` WRITE;
/*!40000 ALTER TABLE `likedjobs` DISABLE KEYS */;
INSERT INTO `likedjobs` VALUES (8,'2023-06-06 15:43:59.277309',1,309791485),(9,'2023-07-15 05:39:44.644736',1,268576603);
/*!40000 ALTER TABLE `likedjobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `user_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` int DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (14,'akshay@gmail.com','$2y$10$3/cBmurjZzBYUkaLYE.Y..skkTdBT/YVCZb51Q3yWx73xd.Eyr13e','jobseeker',1),(18,'info@infosys.com','$2y$10$/TP7ishP6SRCroPNfWcVqO1V0mMH47X.Qsft1u/Ed9xFtmietk2ga','employer',0),(20,'sreelal.c@live.com','$2y$10$MfycE3o6lgrM92f5sB8kPu7c38XQkT6FeL5YF3pgx/MM/Jy12xM5i','jobseeker',1),(21,'abc@gmail.com','$2y$10$ZWYhKrFT9B9m0CaysgRy5e1XMZ/e130v0LGkqw4QpkXbJ3WIV.YYe','jobseeker',1),(22,'jishnnuks@live.com','$2y$10$VKC/bSdNBZWJ6PrOwnJ6xezAj1aq5VioW9YjFUsjxnAJHUkZHRWBq','jobseeker',1),(23,'info@microsoft.com','$2y$10$q.xafcSTYUoKtz2FIhrf7OX1x0weMZRzY3beiqoO2NGe0PUKJlzga','employer',1),(24,'1dt20cs160@dsatm.edu.in','pbkdf2_sha256$390000$tU1Hyw7SQzIeXyJ9zB3xeB$S+uPOFkRVA9T+xQSXin/rcC+SGJSc4T2N5vccPki/iY=','candidate',1),(25,'tejassp03@gmail.com','pbkdf2_sha256$390000$NIllt9FRazSUfBhmQyT1Bs$JxnkTrdjevxYAPph8Zk8RqAFnO79PNxXDUyMkhK+pfU=','employer',1),(30,'ceo@mpower.in','pbkdf2_sha256$390000$YlNGzvPzT2YRynOpFni1ZI$nesYeUaieSXlLfuSnbJyv1CI+tJfa1NSP19BWcpaGac=','admin',1),(31,'tejas@mpower.in','pbkdf2_sha256$390000$TcKolwQZ99Q50utMKZw7Xe$t4uAaHE/T2fuLwrqsIJL4TNZWx734hp9U5zxb769J44=','candidate',0),(32,'sample@mpower.in','pbkdf2_sha256$390000$yJtptA9m0WOwMMa8eZXYwq$WGiU7Km05FBrC7YDcaUwV5krcMMjXRVkOjtTzRCW9mQ=','candidate',NULL),(33,'user123@gmail.com','pbkdf2_sha256$600000$lVtDtDaVVCO3XSeiDQ37fg$7Lwn/9uPd4TAStCJWaKBb3RWBMncOUH9o+snGSHqqUI=','candidate',0),(34,'testuser@gmail.com','pbkdf2_sha256$600000$t7KMaHTBDWAUv57ftT126e$ZnJ1bN9L1M7rzndCZe+UpMcEjESlt+NJVwBUzu9D0VM=','candidate',0),(35,'testuser3@gmail.com','pbkdf2_sha256$600000$niyBOm603m7nfLbRDBNXHq$IyxV3kAtNj4OGJHCqHpL7i2jltyh6ClHpJFA4UiFkoU=','candidate',0),(36,'testuser4@gmail.com','pbkdf2_sha256$600000$AwIf1daawQbRCiREPtBriT$mGJ75LNfOEsaQvS0yY9vTHl72SnNSspccbqJigyIZns=','candidate',0),(37,'testuser5@gmail.com','pbkdf2_sha256$600000$b5CseG7cWvildj4IfXDRWy$gSngElcD7tfPg/f19tFltJ+wABMu5ofxBmBoH9sgtx4=','candidate',0),(38,'testuser6@gmail.com','pbkdf2_sha256$600000$1tvOwtjrJaHRDARZrSCT0r$xSfjtFd4seTEkqkLiGByZNwkaCJUyfhZYOlebV+IUww=','candidate',0),(39,'testuser7@gmail.com','pbkdf2_sha256$600000$FCGUUTksJ4TtitKU8RtdCV$7WPCW6PF/7XeBUI8tCCrxLX2o2qvalFlfKHAPlc4mGQ=','candidate',0),(40,'testuser8@gmail.com','pbkdf2_sha256$600000$u76Nu4L28q4uNUy7RqJswi$w4rBUtW8LySzAx9P1bzeFsp6e3f0dlZdbbQu6g0AM9w=','candidate',0),(41,'testuser9@gmail.com','pbkdf2_sha256$600000$73559RmTdpm98OwHjdlELO$/nGBOuJbQHVchkniXBINtGuGKN84QtQlTIETJ5g6EFU=','candidate',0),(42,'testuser10@gmail.com','pbkdf2_sha256$600000$9nrmoxkkrgT91ueMZMjMDL$aQCt/GT4F5K/XQbWEYCyD6hOGdgUkg23KntQV1hkirQ=','candidate',0),(43,'testuser11@gmail.com','pbkdf2_sha256$600000$S8QFh3LRUAs8HLjs90G9jv$c6drI8rWQZm6/57MpUfivFR9wriMO9s+YhYZsZ5L5SQ=','candidate',0),(44,'testuser12@gmail.com','pbkdf2_sha256$600000$rgLK5OYLQwWwP53J4pZYGA$DUjtnvwSzA9P7VbRvDFuWzI5A/Ofd4meFIpEZeRzNAw=','candidate',0),(45,'testuser13@gmail.com','pbkdf2_sha256$600000$jDlphe4MhxOFNncL1n6FYb$FeMQs6JlnLKr7WSSVwSd1bxeFXyDdOHUiyWD2KnSHDg=','candidate',0),(46,'testuser14@gmail.com','pbkdf2_sha256$600000$OIatnxbKCk1KIR6W5IgZyn$uQ642k1Wy2+p1Pd8cqdPSIWPI4qpmkZWFFK75BEeGqg=','candidate',0),(47,'testuser15@gmail.com','pbkdf2_sha256$600000$yJLF9bVfPUxxvhcI5zEhIH$68fUae2U6ySKaYjlOEsq0s+w+hHjeVaFmH9nyD/tWMQ=','candidate',0),(48,'testuser16@gmail.com','pbkdf2_sha256$600000$vN263VmDJXt2ueFQ0U8K94$Y8l0HiA3ISEkZamKs6YDB8mWfuW7qG5gspjgp/SmdF8=','candidate',0),(49,'niriji7293@wiemei.com','pbkdf2_sha256$600000$DJosqDn5OLk7zzHngMBt9a$2TreVQikpwuzZ+1mj3trq7g7c8qCCspGJTAIUIG37XA=','candidate',0),(50,'falot13849@sportrid.com','pbkdf2_sha256$600000$XEftjjji2P0X59eSHcWVHB$8x7upJtin1siJy926QtPHOeQPGvbNv2T/7Fcx+F1/J0=','candidate',0),(51,'kogame2533@quipas.com','pbkdf2_sha256$600000$9024vEoGHGsp9XXzzCuAM9$r1Gv5d7xTIDPYGSfo3b5KUYxn4tXxnNWnOogzjlIXMg=','candidate',0),(52,'nebow90234@wiemei.com','pbkdf2_sha256$600000$ltBgTbsCCIEWNNLNssvb7n$ILNYEq82Q3mPupUB9WWpkQRycgRtK7ZKhmnZ43tnbwU=','candidate',0),(53,'fidowar440@quipas.com','pbkdf2_sha256$600000$IsONyt7qmB2LWvbNI25VXn$wSjOeTO36f/+U3I8UXZf/y2ueYTzg9g3gfacMfmMNnU=','candidate',0),(54,'bavigak479@sportrid.com','pbkdf2_sha256$600000$HkJFSwlmIfy1SiwsZKxOMP$mPmDTAC7+iviwIaX0ku5KzPii0ycw4/ZT91t3t4g/3c=','candidate',0),(55,'vejec89354@weizixu.com','pbkdf2_sha256$600000$viF2CatdHSkx3wxU7FmkiQ$DKiq2g1fOwMdydo8fGYPRphpJc+eJw4SbBpqu/7szJs=','candidate',0),(56,'wexafe2296@weizixu.com','pbkdf2_sha256$600000$eQNggrLM3nzfLTF7KuIJVl$40yVvj40MBT+rtSShZlqHwCUoB6yqcBLdn6LonZXXNU=','candidate',0),(57,'litodi1380@sportrid.com','pbkdf2_sha256$600000$0mM33646UsQY8PDTpT50iZ$KXjkL70Jh1nLHmuPBb1f2ny0fLDlnNdI9NZMkEql6qQ=','candidate',0),(58,'sefoxak368@sportrid.com','pbkdf2_sha256$600000$SoH1OoWnbzkp1abcX5QyW8$HhiX1Cfwj8XBojhXRynZoYrukcAn0GMHDKHc3FfIs6w=','candidate',0),(59,'xinarox357@sportrid.com','pbkdf2_sha256$600000$b7PKU2FNVdJt55eqju67Af$eaiSArklBlg9BWMpRMDKbeni3T9czBS/JdQ+aMyhukg=','candidate',0),(60,'dixege7617@sportrid.com','pbkdf2_sha256$600000$TZUzNBU6fosEGjhU0nIV9E$XoIO1D2EyYCwHqRQmh4m6yselOh8DY4xrf0wc2jvT94=','employer',0),(61,'nocis48480@sportrid.com','pbkdf2_sha256$600000$Qwzc6ORucO2ZrswYp4IqDY$X77KGQLNk0+IkGKlfrGJSBQoIKAKpIpZvM4f/nhIy38=','employer',0),(62,'fayocep994@weizixu.com','pbkdf2_sha256$600000$cP3PVWD559dUUciLzFT2Uu$G6TFZpB2LAU+t7aK4S4xetu+3TJq3bq+iX/BOvvdNvw=','employer',0),(63,'sidepo8272@sportrid.com','pbkdf2_sha256$600000$IErnG12sH386PlLyOsaFBM$fR0Yg2gasP5rUB5nXCZnmGROeXUPtfycU1JSdGWrlMw=','employer',0),(64,'regona5329@weizixu.com','pbkdf2_sha256$600000$uVSwB2kenSZbN3Fi5Erund$V6455KSdQcsyGlphp5IQqchkG6SZJvx4qvarHD7EMRA=','candidate',0),(65,'jagasif238@wiemei.com','pbkdf2_sha256$600000$M3faFI3lznL4MgV3Goh6ML$r233G/BZ7wQ2WVzjITifgi6ybkvUgpwgFKN5Rh8R8Rk=','employer',0),(66,'pirox51718@wiemei.com','pbkdf2_sha256$600000$e80piX8h3dsmHpEQXRiCm2$fcsZScafEnc2gjNzvJU7o4mu0wEoloGyWNtrhuBtSb8=','employer',0),(67,'nakide9076@weishu8.com','pbkdf2_sha256$600000$IKfMITSezkQ9DY2Y0t4xKt$X4zIovm9+z5WPmRzR0Ib+FjEZdFHuSbW1Lu9MjQr5M4=','candidate',0),(68,'texeh41711@weishu8.com','pbkdf2_sha256$600000$tUofWBtDAgW2gb0agSIt5l$/JjC/1nXcsKC8Q2RX/plEs2xVpAJManWhihC3+zxsTQ=','candidate',0),(69,'limoxel841@v1zw.com','pbkdf2_sha256$600000$D9QMurGtjJlSdiT22e5rv0$JPl0yNfMFW0ikcgRbC9DKvSPj0TN+QUgHwwJYsGPwyU=','candidate',0),(70,'wamahof465@v1zw.com','pbkdf2_sha256$600000$C31LPIu3B7HN7iJGBL7DT8$bRANNh+exzd3lZVbIz8tI40FaAXNtH8fl9/Of2lA9zo=','candidate',1),(71,'testuser40@gmail.com','pbkdf2_sha256$600000$r4eKNoSizBy5ZAMmFimCkH$Fd3gMCpwjZT+8acKw992qH2ZfLAruTAwgzs6hM00gag=','candidate',0),(72,'jai48@gmail.com','pbkdf2_sha256$600000$aWalCU3UgYCyzP8jNEdEoW$6x0jDDXtRUjsFfzFHDwRPrHntKPMfNGCw0gcSwsMK2k=','admin',0);
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sender_user_id` int NOT NULL,
  `receiver_user_id` int NOT NULL,
  `body` varchar(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `msg_id_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `messages_msg_id_id_6b591511_fk_threads_msg_id` (`msg_id_id`),
  KEY `messages_receiver_user_id_ee038ac2` (`receiver_user_id`),
  KEY `messages_sender_user_id_b1b10099` (`sender_user_id`),
  CONSTRAINT `messages_msg_id_id_6b591511_fk_threads_msg_id` FOREIGN KEY (`msg_id_id`) REFERENCES `threads` (`msg_id`),
  CONSTRAINT `messages_receiver_user_id_ee038ac2_fk_login_log_id` FOREIGN KEY (`receiver_user_id`) REFERENCES `login` (`log_id`),
  CONSTRAINT `messages_sender_user_id_b1b10099_fk_login_log_id` FOREIGN KEY (`sender_user_id`) REFERENCES `login` (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,25,24,'hey','','2023-06-06 15:45:56.599822',1,1),(2,25,24,'send resume quick','','2023-06-06 15:56:56.158257',1,1),(3,24,25,'ok','','2023-06-06 15:57:11.797382',1,1),(4,25,31,'hi','','2023-07-15 05:23:03.553523',1,2),(5,66,67,'Hello','','2023-08-10 07:34:32.963669',0,3),(6,66,67,'hy','','2023-08-19 05:37:17.094486',0,3);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newsletter`
--

DROP TABLE IF EXISTS `newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `newsletter` (
  `news_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `newsletter`
--

LOCK TABLES `newsletter` WRITE;
/*!40000 ALTER TABLE `newsletter` DISABLE KEYS */;
/*!40000 ALTER TABLE `newsletter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notif_id` int NOT NULL AUTO_INCREMENT,
  `datetime` datetime(6) NOT NULL,
  `notif_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rece_id_id` int DEFAULT NULL,
  `send_id_id` int DEFAULT NULL,
  `readed` tinyint(1) NOT NULL,
  `job_id_id` int DEFAULT NULL,
  `testuser_id_id` int DEFAULT NULL,
  PRIMARY KEY (`notif_id`),
  KEY `notifications_rece_id_id_c9a284b5_fk_login_log_id` (`rece_id_id`),
  KEY `notifications_send_id_id_95032d97_fk_login_log_id` (`send_id_id`),
  KEY `notifications_job_id_id_ddeb746c_fk_jobs_jobid` (`job_id_id`),
  KEY `notifications_testuser_id_id_60b1e680_fk_testuser_testuser_id` (`testuser_id_id`),
  CONSTRAINT `notifications_job_id_id_ddeb746c_fk_jobs_jobid` FOREIGN KEY (`job_id_id`) REFERENCES `jobs` (`jobid`),
  CONSTRAINT `notifications_rece_id_id_c9a284b5_fk_login_log_id` FOREIGN KEY (`rece_id_id`) REFERENCES `login` (`log_id`),
  CONSTRAINT `notifications_send_id_id_95032d97_fk_login_log_id` FOREIGN KEY (`send_id_id`) REFERENCES `login` (`log_id`),
  CONSTRAINT `notifications_testuser_id_id_60b1e680_fk_testuser_testuser_id` FOREIGN KEY (`testuser_id_id`) REFERENCES `testuser` (`testuser_id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,'2023-06-06 15:45:56.606784','M',24,25,1,NULL,NULL),(2,'2023-06-06 15:56:56.165684','M',24,25,1,NULL,NULL),(3,'2023-06-06 15:57:11.805754','M',25,24,0,NULL,NULL),(4,'2023-07-15 05:17:33.421721','T',24,25,0,NULL,NULL),(5,'2023-07-15 05:23:03.571047','M',31,25,1,NULL,NULL),(6,'2023-07-15 05:23:30.924235','T',31,25,1,NULL,NULL),(8,'2023-07-15 05:24:23.447545','V',31,25,1,NULL,NULL),(9,'2023-07-15 05:29:36.959810','T',31,25,1,NULL,NULL),(10,'2023-07-18 06:23:33.057374','V',31,25,0,NULL,NULL),(11,'2023-08-09 15:47:35.422330','V',33,66,1,NULL,NULL),(12,'2023-08-09 15:49:05.534870','T',33,66,1,NULL,NULL),(13,'2023-08-09 15:49:50.152568','T',66,33,1,NULL,4),(14,'2023-08-10 03:23:33.942263','V',33,66,1,NULL,NULL),(15,'2023-08-10 03:43:05.690015','V',67,66,0,NULL,NULL),(16,'2023-08-10 03:45:15.138679','V',33,66,1,NULL,NULL),(17,'2023-08-10 03:52:53.785815','V',67,66,0,NULL,NULL),(18,'2023-08-10 07:24:51.584029','V',67,66,0,NULL,NULL),(19,'2023-08-10 07:27:47.694609','V',67,66,0,NULL,NULL),(20,'2023-08-10 07:28:33.775979','V',33,66,1,NULL,NULL),(21,'2023-08-10 07:28:39.692986','V',33,66,1,NULL,NULL),(22,'2023-08-10 07:28:43.340012','V',67,66,0,NULL,NULL),(23,'2023-08-10 07:33:10.338844','V',67,66,0,NULL,NULL),(24,'2023-08-10 07:33:17.677653','V',67,66,0,NULL,NULL),(25,'2023-08-10 07:34:19.016085','V',67,66,0,NULL,NULL),(26,'2023-08-10 07:34:32.980451','M',67,66,0,NULL,NULL),(27,'2023-08-10 07:43:04.614050','V',67,66,0,NULL,NULL),(28,'2023-08-10 07:44:07.688330','V',33,66,1,NULL,NULL),(29,'2023-08-10 07:45:10.306561','V',33,66,1,NULL,NULL),(30,'2023-08-10 07:55:32.798012','V',33,66,1,NULL,NULL),(31,'2023-08-10 07:55:47.485285','V',67,66,0,NULL,NULL),(32,'2023-08-10 07:57:29.458116','V',67,66,0,NULL,NULL),(33,'2023-08-10 07:57:53.287368','V',67,66,0,NULL,NULL),(34,'2023-08-10 08:07:17.539242','T',33,66,1,NULL,NULL),(35,'2023-08-10 08:08:52.345652','V',67,66,0,NULL,NULL),(36,'2023-08-10 08:08:57.403252','V',67,66,0,NULL,NULL),(37,'2023-08-10 08:25:36.403893','V',67,66,0,NULL,NULL),(38,'2023-08-10 08:40:42.045852','V',67,66,0,NULL,NULL),(39,'2023-08-10 08:43:30.195634','V',33,66,1,NULL,NULL),(40,'2023-08-10 08:44:13.907067','V',67,66,0,NULL,NULL),(41,'2023-08-10 08:44:59.047034','T',67,66,0,NULL,NULL),(42,'2023-08-10 08:47:28.215748','T',66,33,1,NULL,5),(43,'2023-08-10 08:48:47.956218','T',66,67,1,NULL,6),(44,'2023-08-10 08:50:01.982103','V',67,66,0,NULL,NULL),(45,'2023-08-10 08:58:40.899399','V',67,66,0,NULL,NULL),(46,'2023-08-10 08:58:54.387298','V',67,66,0,NULL,NULL),(47,'2023-08-10 08:59:15.868346','V',67,66,0,NULL,NULL),(48,'2023-08-10 09:12:39.285394','V',67,66,0,NULL,NULL),(49,'2023-08-10 09:27:20.858854','V',67,66,0,NULL,NULL),(50,'2023-08-10 09:55:09.689947','V',67,66,0,NULL,NULL),(51,'2023-08-10 09:59:13.338896','V',67,66,0,NULL,NULL),(52,'2023-08-10 09:59:53.674193','V',67,66,0,NULL,NULL),(53,'2023-08-10 10:00:32.487321','V',67,66,0,NULL,NULL),(54,'2023-08-10 10:00:56.173259','V',67,66,0,NULL,NULL),(55,'2023-08-10 10:02:45.989849','V',67,66,0,NULL,NULL),(56,'2023-08-10 10:11:08.049966','V',33,66,1,NULL,NULL),(57,'2023-08-10 10:14:15.999489','V',33,66,1,NULL,NULL),(58,'2023-08-10 10:15:09.699033','V',33,66,1,NULL,NULL),(59,'2023-08-10 10:15:22.895781','V',67,66,0,NULL,NULL),(60,'2023-08-10 10:16:56.949055','V',67,66,0,NULL,NULL),(61,'2023-08-10 10:17:33.447916','V',67,66,0,NULL,NULL),(62,'2023-08-10 10:24:28.138912','V',33,66,1,NULL,NULL),(63,'2023-08-10 10:31:30.997557','V',67,66,0,NULL,NULL),(64,'2023-08-10 10:31:38.619820','V',68,66,0,NULL,NULL),(65,'2023-08-10 10:40:51.051223','V',67,66,0,NULL,NULL),(66,'2023-08-10 10:44:10.847760','V',68,66,0,NULL,NULL),(67,'2023-08-10 10:44:30.379958','V',68,66,0,NULL,NULL),(68,'2023-08-10 10:44:32.347149','V',68,66,0,NULL,NULL),(69,'2023-08-10 10:44:37.456335','V',68,66,0,NULL,NULL),(70,'2023-08-10 10:44:39.894031','V',68,66,0,NULL,NULL),(71,'2023-08-10 10:46:51.846326','V',68,66,0,NULL,NULL),(72,'2023-08-10 10:46:58.216999','V',68,66,0,NULL,NULL),(73,'2023-08-10 10:47:31.315536','V',33,66,1,NULL,NULL),(74,'2023-08-10 10:51:00.848911','V',67,66,0,NULL,NULL),(75,'2023-08-10 10:55:18.860742','V',68,66,0,NULL,NULL),(76,'2023-08-10 11:00:59.258124','V',68,66,0,NULL,NULL),(77,'2023-08-11 06:16:49.242695','T',68,66,0,NULL,NULL),(78,'2023-08-11 06:17:53.854318','T',67,66,0,NULL,NULL),(79,'2023-08-11 06:18:03.785242','T',68,66,0,NULL,NULL),(80,'2023-08-11 06:18:59.885418','T',66,67,1,NULL,8),(81,'2023-08-11 06:20:27.842534','I',67,66,0,NULL,NULL),(82,'2023-08-11 06:24:57.774206','I',33,66,1,NULL,NULL),(83,'2023-08-11 07:47:20.227309','T',69,66,0,NULL,NULL),(84,'2023-08-11 10:41:46.906185','T',70,66,1,NULL,NULL),(85,'2023-08-12 07:53:07.268511','T',71,66,1,NULL,NULL),(86,'2023-08-12 08:15:29.601861','T',66,71,1,NULL,12),(87,'2023-08-12 08:36:28.051226','I',71,66,1,NULL,NULL),(88,'2023-08-12 10:13:06.870122','T',70,66,1,NULL,NULL),(89,'2023-08-12 10:33:59.540042','T',69,66,0,NULL,NULL),(90,'2023-08-12 10:34:28.819825','T',70,66,1,NULL,NULL),(91,'2023-08-12 10:34:47.828940','V',70,66,1,NULL,NULL),(92,'2023-08-12 10:55:45.739838','V',66,70,1,NULL,NULL),(93,'2023-08-12 11:02:36.533407','T',66,70,1,NULL,15),(94,'2023-08-12 11:02:56.332211','T',66,70,1,NULL,13),(95,'2023-08-12 11:03:50.074493','I',70,66,1,NULL,NULL),(96,'2023-08-17 10:37:23.929650','V',33,66,1,NULL,NULL),(97,'2023-08-18 07:50:08.943125','V',70,66,1,NULL,NULL),(98,'2023-08-18 07:51:25.560255','V',54,66,0,NULL,NULL),(99,'2023-08-18 07:51:34.570935','V',41,66,0,NULL,NULL),(100,'2023-08-18 07:51:38.688496','V',44,66,0,NULL,NULL),(101,'2023-08-18 07:51:46.090179','V',39,66,0,NULL,NULL),(102,'2023-08-18 10:50:19.945678','V',64,66,0,NULL,NULL),(103,'2023-08-19 05:37:17.117255','M',67,66,0,NULL,NULL),(104,'2023-08-22 09:46:26.456964','I',70,66,1,NULL,NULL),(105,'2023-08-22 10:13:55.794135','V',70,66,1,NULL,NULL),(107,'2023-08-23 09:38:42.872007','T',33,66,1,NULL,NULL),(108,'2023-08-23 10:14:58.695196','T',33,66,1,NULL,NULL),(109,'2023-08-23 10:20:06.837084','T',33,66,1,NULL,NULL),(110,'2023-08-23 10:22:07.538562','T',33,66,1,NULL,NULL),(111,'2023-08-23 10:24:05.473058','T',33,66,1,NULL,NULL),(112,'2023-08-23 10:27:19.709656','T',33,66,1,NULL,NULL),(113,'2023-08-23 10:31:00.074138','T',66,33,1,NULL,21),(114,'2023-08-23 11:09:18.034974','I',33,66,0,NULL,NULL),(115,'2023-08-23 11:38:10.293569','T',33,66,0,NULL,NULL),(116,'2023-08-23 11:59:09.367084','T',70,66,0,NULL,NULL),(117,'2023-08-23 11:59:49.443357','T',66,70,1,NULL,23),(118,'2023-08-24 02:52:08.881327','T',70,66,0,NULL,NULL),(119,'2023-08-24 02:57:50.363276','T',70,66,0,NULL,NULL),(121,'2023-08-24 03:42:15.234709','T',70,66,0,NULL,NULL),(122,'2023-08-24 03:42:59.749460','T',70,66,0,NULL,NULL),(123,'2023-08-24 03:44:18.345633','T',66,70,1,NULL,26),(124,'2023-08-24 03:44:32.320913','T',66,70,1,NULL,27),(125,'2023-08-24 08:23:11.908503','V',52,66,0,NULL,NULL),(126,'2023-08-24 08:23:15.780456','V',55,66,0,NULL,NULL),(127,'2023-08-24 08:23:18.576804','V',47,66,0,NULL,NULL),(128,'2023-08-24 08:23:22.904183','V',70,66,0,NULL,NULL),(129,'2023-08-24 08:23:41.618100','V',71,66,0,NULL,NULL),(130,'2023-08-24 08:23:57.768129','V',70,66,0,NULL,NULL),(131,'2023-08-24 08:56:39.279428','V',70,66,0,NULL,NULL),(132,'2023-08-24 09:05:34.360730','I',70,66,0,NULL,NULL),(133,'2023-08-24 09:12:07.804811','V',70,66,0,NULL,NULL),(134,'2023-08-24 09:12:13.651105','V',70,66,0,NULL,NULL),(135,'2023-08-24 10:49:34.347704','I',70,66,0,NULL,NULL),(136,'2023-08-25 10:06:48.140642','V',67,66,0,NULL,NULL),(137,'2023-08-25 12:58:02.110353','V',33,66,0,NULL,NULL),(138,'2023-08-25 12:58:25.200558','T',33,66,0,NULL,NULL),(139,'2023-08-25 13:00:09.194800','T',66,33,1,NULL,28),(140,'2023-08-25 13:01:58.465522','I',33,66,0,NULL,NULL),(141,'2023-08-25 13:24:01.587903','I',33,66,0,NULL,NULL),(142,'2023-08-25 13:27:40.653129','I',33,66,0,NULL,NULL),(143,'2023-08-25 13:29:55.210872','I',33,66,0,NULL,NULL),(144,'2023-08-25 13:31:39.948513','I',33,66,0,NULL,NULL),(145,'2023-08-25 13:33:28.168283','I',33,66,0,NULL,NULL),(146,'2023-08-28 05:52:18.242593','T',33,66,0,NULL,NULL);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profilevisits`
--

DROP TABLE IF EXISTS `profilevisits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profilevisits` (
  `visit_id` int NOT NULL AUTO_INCREMENT,
  `visiting_time` datetime(6) NOT NULL,
  `e_id_id` int DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  `user_type` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`visit_id`),
  KEY `profilevisits_e_id_id_bd7a08aa_fk_employer_eid` (`e_id_id`),
  KEY `profilevisits_user_id_id_333734c7_fk_jobseeker_user_id` (`user_id_id`),
  CONSTRAINT `profilevisits_e_id_id_bd7a08aa_fk_employer_eid` FOREIGN KEY (`e_id_id`) REFERENCES `employer` (`eid`),
  CONSTRAINT `profilevisits_user_id_id_333734c7_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profilevisits`
--

LOCK TABLES `profilevisits` WRITE;
/*!40000 ALTER TABLE `profilevisits` DISABLE KEYS */;
INSERT INTO `profilevisits` VALUES (1,'2023-07-15 05:24:23.433762',788024608,268576603,'c'),(2,'2023-07-18 06:23:32.959257',788024608,268576603,'c'),(3,'2023-08-09 15:47:35.419482',833965419,720061200,'c'),(4,'2023-08-10 03:23:33.939048',833965419,720061200,'c'),(5,'2023-08-10 03:43:05.687104',833965419,81570264,'c'),(6,'2023-08-10 03:45:15.136694',833965419,720061200,'c'),(7,'2023-08-10 03:52:53.782051',833965419,81570264,'c'),(8,'2023-08-10 07:24:51.577312',833965419,81570264,'c'),(9,'2023-08-10 07:27:47.693170',833965419,81570264,'c'),(10,'2023-08-10 07:28:33.774301',833965419,720061200,'c'),(11,'2023-08-10 07:28:39.690936',833965419,720061200,'c'),(12,'2023-08-10 07:28:43.338083',833965419,81570264,'c'),(13,'2023-08-10 07:33:10.337099',833965419,81570264,'c'),(14,'2023-08-10 07:33:17.675077',833965419,81570264,'c'),(15,'2023-08-10 07:34:19.013781',833965419,81570264,'c'),(16,'2023-08-10 07:43:04.611706',833965419,81570264,'c'),(17,'2023-08-10 07:44:07.686649',833965419,720061200,'c'),(18,'2023-08-10 07:45:10.304582',833965419,720061200,'c'),(19,'2023-08-10 07:55:32.794886',833965419,720061200,'c'),(20,'2023-08-10 07:55:47.483251',833965419,81570264,'c'),(21,'2023-08-10 07:57:29.456604',833965419,81570264,'c'),(22,'2023-08-10 07:57:53.285910',833965419,81570264,'c'),(23,'2023-08-10 08:08:52.343884',833965419,81570264,'c'),(24,'2023-08-10 08:08:57.401205',833965419,81570264,'c'),(25,'2023-08-10 08:25:36.402733',833965419,81570264,'c'),(26,'2023-08-10 08:40:42.043769',833965419,81570264,'c'),(27,'2023-08-10 08:43:30.192265',833965419,720061200,'c'),(28,'2023-08-10 08:44:13.904032',833965419,81570264,'c'),(29,'2023-08-10 08:50:01.980507',833965419,81570264,'c'),(30,'2023-08-10 08:58:40.897648',833965419,81570264,'c'),(31,'2023-08-10 08:58:54.385160',833965419,81570264,'c'),(32,'2023-08-10 08:59:15.866416',833965419,81570264,'c'),(33,'2023-08-10 09:12:39.282246',833965419,81570264,'c'),(34,'2023-08-10 09:27:20.854615',833965419,81570264,'c'),(35,'2023-08-10 09:55:09.688351',833965419,81570264,'c'),(36,'2023-08-10 09:59:13.336604',833965419,81570264,'c'),(37,'2023-08-10 09:59:53.672047',833965419,81570264,'c'),(38,'2023-08-10 10:00:32.485061',833965419,81570264,'c'),(39,'2023-08-10 10:00:56.171565',833965419,81570264,'c'),(40,'2023-08-10 10:02:45.988191',833965419,81570264,'c'),(41,'2023-08-10 10:11:08.047683',833965419,720061200,'c'),(42,'2023-08-10 10:14:15.997029',833965419,720061200,'c'),(43,'2023-08-10 10:15:09.696943',833965419,720061200,'c'),(44,'2023-08-10 10:15:22.894169',833965419,81570264,'c'),(45,'2023-08-10 10:16:56.946851',833965419,81570264,'c'),(46,'2023-08-10 10:17:33.445668',833965419,81570264,'c'),(47,'2023-08-10 10:24:28.136208',833965419,720061200,'c'),(48,'2023-08-10 10:31:30.993671',833965419,81570264,'c'),(49,'2023-08-10 10:31:38.616502',833965419,824712288,'c'),(50,'2023-08-10 10:40:51.048238',833965419,81570264,'c'),(51,'2023-08-10 10:44:10.845781',833965419,824712288,'c'),(52,'2023-08-10 10:44:30.378108',833965419,824712288,'c'),(53,'2023-08-10 10:44:32.345382',833965419,824712288,'c'),(54,'2023-08-10 10:44:37.452055',833965419,824712288,'c'),(55,'2023-08-10 10:44:39.891740',833965419,824712288,'c'),(56,'2023-08-10 10:46:51.844655',833965419,824712288,'c'),(57,'2023-08-10 10:46:58.214572',833965419,824712288,'c'),(58,'2023-08-10 10:47:31.313244',833965419,720061200,'c'),(59,'2023-08-10 10:51:00.846267',833965419,81570264,'c'),(60,'2023-08-10 10:55:18.857796',833965419,824712288,'c'),(61,'2023-08-10 11:00:59.255761',833965419,824712288,'c'),(62,'2023-08-12 10:34:47.818856',833965419,373315377,'c'),(63,'2023-08-12 10:55:45.731672',833965419,373315377,'e'),(64,'2023-08-17 10:37:23.830592',833965419,720061200,'c'),(65,'2023-08-18 07:50:08.934624',833965419,373315377,'c'),(66,'2023-08-18 07:51:25.556134',833965419,762552912,'c'),(67,'2023-08-18 07:51:34.569146',833965419,858846653,'c'),(68,'2023-08-18 07:51:38.685944',833965419,606572057,'c'),(69,'2023-08-18 07:51:46.088127',833965419,731095221,'c'),(70,'2023-08-18 10:50:19.937644',833965419,986316475,'c'),(71,'2023-08-22 10:13:55.792049',833965419,373315377,'c'),(72,'2023-08-24 08:23:11.900637',833965419,165026623,'c'),(73,'2023-08-24 08:23:15.778366',833965419,856298255,'c'),(74,'2023-08-24 08:23:18.575229',833965419,794246454,'c'),(75,'2023-08-24 08:23:22.902548',833965419,373315377,'c'),(76,'2023-08-24 08:23:41.615795',833965419,450211284,'c'),(77,'2023-08-24 08:23:57.765327',833965419,373315377,'c'),(78,'2023-08-24 08:56:39.273067',833965419,373315377,'c'),(79,'2023-08-24 09:12:07.802705',833965419,373315377,'c'),(80,'2023-08-24 09:12:13.648237',833965419,373315377,'c'),(81,'2023-08-25 10:06:48.136473',833965419,81570264,'c'),(82,'2023-08-25 12:58:02.107309',833965419,720061200,'c');
/*!40000 ALTER TABLE `profilevisits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumeanalysis`
--

DROP TABLE IF EXISTS `resumeanalysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resumeanalysis` (
  `any_id` int NOT NULL AUTO_INCREMENT,
  `resume_score` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date` date NOT NULL,
  `no_of_pages` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `predicted_field` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `user_level` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `actual_skills` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `reco_skills` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `reco_courses` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `recommendations` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `jobseeker_id_id` int DEFAULT NULL,
  PRIMARY KEY (`any_id`),
  KEY `resumeanalysis_jobseeker_id_id_cd189ff7_fk_jobseeker_user_id` (`jobseeker_id_id`),
  CONSTRAINT `resumeanalysis_jobseeker_id_id_cd189ff7_fk_jobseeker_user_id` FOREIGN KEY (`jobseeker_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumeanalysis`
--

LOCK TABLES `resumeanalysis` WRITE;
/*!40000 ALTER TABLE `resumeanalysis` DISABLE KEYS */;
INSERT INTO `resumeanalysis` VALUES (2,'20','2023-05-16','1','Web Development','Fresher',',Java,Django,Mobile,Operations,Engineering,Website,Mathematics,C++,Php,Machine learning,Html,Algorithms,System,Analysis,Css,Javascript,Python,Mining,Mysql,Health,Ordering,Design',',React,Django,Node JS,React JS,php,laravel,Magento,wordpress,Javascript,Angular JS,c#,Flask,SDK',',Become a React Developer by Udacity,Front End Web Developer by Udacity,Node.js and Express.js [Free],Full Stack Web Developer by Udacity',',According to our recommendation please add your career objective, it will give your career intension to the Recruiters,According to our recommendation please add Declaration. It will give the assurance that everything written on your resume is true and fully acknowledged by you,Awesome! You have added Hobbies,According to our recommendation please add Achievements. It will show that you are capable for the required position.,According to our recommendation please add Projects. It will show that you have done work related the required position or not.',309791485),(3,NULL,'2023-07-26',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,710946856),(4,NULL,'2023-07-26',NULL,NULL,NULL,'Networking / CCNA,c#,Big Data / Hadoop,Cloud Computing,',NULL,NULL,NULL,731095221),(5,NULL,'2023-07-27',NULL,NULL,NULL,'App Development(iOS,Android,Windows),C / C++,',NULL,NULL,NULL,604117780),(6,NULL,'2023-07-27',NULL,NULL,NULL,'Angular JS / Node Js,App Development(iOS,Android,Windows),',NULL,NULL,NULL,858846653),(7,NULL,'2023-07-27',NULL,NULL,NULL,'Angular JS / Node Js,App Development(iOS,Android,Windows),',NULL,NULL,NULL,858846653),(8,NULL,'2023-07-27',NULL,NULL,NULL,'Angular JS / Node Js,',NULL,NULL,NULL,858846653),(9,NULL,'2023-07-27',NULL,NULL,NULL,'Angular JS / Node Js,',NULL,NULL,NULL,858846653),(10,NULL,'2023-07-27',NULL,NULL,NULL,'Angular JS / Node Js,',NULL,NULL,NULL,858846653),(11,NULL,'2023-07-27',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,435001728),(12,NULL,'2023-07-27',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,435001728),(13,NULL,'2023-07-27',NULL,NULL,NULL,'Angular JS / Node Js,',NULL,NULL,NULL,948142271),(14,NULL,'2023-07-27',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,606572057),(15,NULL,'2023-07-27',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,606572057),(16,NULL,'2023-07-27',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,819924985),(17,NULL,'2023-07-27',NULL,NULL,NULL,'MySQL / Database,PHP,',NULL,NULL,NULL,673070026),(18,NULL,'2023-07-27',NULL,NULL,NULL,'MySQL / Database,PHP,',NULL,NULL,NULL,673070026),(19,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(20,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(21,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(22,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(23,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(24,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(25,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(26,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(27,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(28,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(29,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(30,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(31,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(32,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(33,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(34,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(35,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(36,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,673070026),(37,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,794246454),(38,NULL,'2023-07-27',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,672634308),(39,NULL,'2023-07-28',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,969454803),(40,NULL,'2023-07-28',NULL,NULL,NULL,'App Development(iOS,Android,Windows),',NULL,NULL,NULL,969454803),(41,NULL,'2023-07-28',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,395157575),(42,NULL,'2023-07-28',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,567825742),(43,NULL,'2023-07-28',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,567825742),(44,NULL,'2023-07-29',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,165026623),(45,NULL,'2023-07-29',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,379358397),(46,NULL,'2023-07-29',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,762552912),(47,NULL,'2023-07-29',NULL,NULL,NULL,'PHP,',NULL,NULL,NULL,856298255),(48,NULL,'2023-08-01',NULL,NULL,NULL,'MySQL / Database,PHP,',NULL,NULL,NULL,712589075),(49,NULL,'2023-08-01',NULL,NULL,NULL,'PHP,Acrobat,',NULL,NULL,NULL,503284360),(50,NULL,'2023-08-02',NULL,NULL,NULL,'C / C++,Python,',NULL,NULL,NULL,823140842),(51,NULL,'2023-08-03',NULL,NULL,NULL,'C / C++,MongoDB,Django,',NULL,NULL,NULL,858532288),(52,NULL,'2023-08-04',NULL,NULL,NULL,'MySQL / Database,PHP,CSS,HTML,Javascript,',NULL,NULL,NULL,986316475),(53,NULL,'2023-08-10',NULL,NULL,NULL,'Angular JS / Node Js,C / C++,MySQL / Database,PHP,Python,',NULL,NULL,NULL,81570264),(54,NULL,'2023-08-10',NULL,NULL,NULL,'Angular JS / Node Js,MySQL / Database,PHP,Bookkeeping through Excel or TurboTax,CSS,HTML,Javascript,',NULL,NULL,NULL,824712288),(55,NULL,'2023-08-11',NULL,NULL,NULL,'Angular JS / Node Js,C / C++,MySQL / Database,PHP,',NULL,NULL,NULL,603839799),(56,NULL,'2023-08-11',NULL,NULL,NULL,'Angular JS / Node Js,C / C++,MySQL / Database,Django,PHP,Python,CSS,HTML,',NULL,NULL,NULL,373315377),(57,NULL,'2023-08-12',NULL,NULL,NULL,'C / C++,MySQL / Database,Django,PHP,Python,',NULL,NULL,NULL,450211284);
/*!40000 ALTER TABLE `resumeanalysis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ResumeFeedback`
--

DROP TABLE IF EXISTS `ResumeFeedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ResumeFeedback` (
  `feed_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `job_id_id` int DEFAULT NULL,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`feed_id`),
  UNIQUE KEY `feed_id` (`feed_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ResumeFeedback`
--

LOCK TABLES `ResumeFeedback` WRITE;
/*!40000 ALTER TABLE `ResumeFeedback` DISABLE KEYS */;
INSERT INTO `ResumeFeedback` VALUES (1,788024617,5);
/*!40000 ALTER TABLE `ResumeFeedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roledetails`
--

DROP TABLE IF EXISTS `roledetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roledetails` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role` varchar(750) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roledetails`
--

LOCK TABLES `roledetails` WRITE;
/*!40000 ALTER TABLE `roledetails` DISABLE KEYS */;
INSERT INTO `roledetails` VALUES (1,'3D Artist'),(2,'Accountant'),(3,'Administrative Assistant'),(4,'AI Specialist'),(5,'Android Developer'),(6,'Architect'),(7,'Art Director'),(8,'Artificial Intelligence Specialist'),(9,'Automation Engineer'),(10,'Brand Manager'),(11,'Blockchain Developer'),(12,'Business Analyst'),(13,'Business Intelligence Analyst'),(14,'Chef'),(15,'Civil Engineer'),(16,'Cloud Architect'),(17,'Cloud Solutions Architect'),(18,'Content Writer'),(19,'Customer Service Rep'),(20,'Cybersecurity Analyst'),(21,'Data Analyst'),(22,'Data Engineer'),(23,'Data Scientist'),(24,'Database Administrator'),(25,'Designer'),(26,'DevOps Engineer'),(27,'Digital Marketing Specialist'),(28,'Economist'),(29,'Electrician'),(30,'Environmental Engineer'),(31,'Ethical Hacker'),(32,'Event Planner'),(33,'Fashion Designer'),(34,'Financial Advisor'),(35,'Financial Analyst'),(36,'Fitness Trainer'),(37,'Front-end Developer'),(38,'Game Designer'),(39,'Game Developer'),(40,'GIS Analyst'),(41,'Graphic Designer'),(42,'Health Informatics Analyst'),(43,'Healthcare Administrator'),(44,'HR Manager'),(45,'Information Security Analyst'),(46,'Industrial Engineer'),(47,'Interior Designer'),(48,'iOS Developer'),(49,'IT Support Specialist'),(50,'Java Developer'),(51,'Java Programmer'),(52,'Java Architect'),(53,'Journalist'),(54,'Kitchen Designer'),(55,'Kitchen Manager'),(56,'Landscape Architect'),(57,'Landscape Designer'),(58,'Lawyer'),(59,'Market Research Analyst'),(60,'Market Strategist'),(61,'Marketing Coordinator'),(62,'Marketing Manager'),(63,'Mechanical Engineer'),(64,'Mobile App Developer'),(65,'Network Administrator'),(66,'Network Engineer'),(67,'Network Security Specialist'),(68,'Nurse'),(69,'Occupational Health Specialist'),(70,'Occupational Therapist'),(71,'Operations Manager'),(72,'Paralegal'),(73,'Patent Attorney'),(74,'Patent Examiner'),(75,'Product Manager'),(76,'Project Manager'),(77,'Psychologist'),(78,'QA Tester'),(79,'Quality Assurance'),(80,'Quality Control Specialist'),(81,'Recruiter'),(82,'Research Analyst'),(83,'Robotic Process Automation Specialist'),(84,'Robotics Engineer'),(85,'Sales Executive'),(86,'Sales Manager'),(87,'Sales Representative'),(88,'Social Media Coordinator'),(89,'Social Worker'),(90,'Software Architect'),(91,'Software Engineer'),(92,'Software Tester'),(93,'Teacher'),(94,'Technical Support Specialist'),(95,'Technical Writer'),(96,'UI Designer'),(97,'UI/UX Designer'),(98,'UX Designer'),(99,'VFX Artist'),(100,'Video Editor'),(101,'Visual Effects Supervisor'),(102,'Web Designer'),(103,'Web Developer'),(104,'Writer'),(105,'Yoga Instructor'),(106,'Zoologist'),(107,'Zoology Researcher'),(216,'Back-end Developer');
/*!40000 ALTER TABLE `roledetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `selection`
--

DROP TABLE IF EXISTS `selection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `selection` (
  `sel_id` int NOT NULL AUTO_INCREMENT,
  `status` int DEFAULT NULL,
  `date` date NOT NULL,
  `emp_id_id` int DEFAULT NULL,
  `job_id_id` int DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  PRIMARY KEY (`sel_id`),
  KEY `selection_emp_id_id_51a293fb_fk_employer_eid` (`emp_id_id`),
  KEY `selection_job_id_id_d82bc959_fk_jobs_jobid` (`job_id_id`),
  KEY `selection_user_id_id_75fe9d5c_fk_jobseeker_user_id` (`user_id_id`),
  CONSTRAINT `selection_emp_id_id_51a293fb_fk_employer_eid` FOREIGN KEY (`emp_id_id`) REFERENCES `employer` (`eid`),
  CONSTRAINT `selection_job_id_id_d82bc959_fk_jobs_jobid` FOREIGN KEY (`job_id_id`) REFERENCES `jobs` (`jobid`),
  CONSTRAINT `selection_user_id_id_75fe9d5c_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `selection`
--

LOCK TABLES `selection` WRITE;
/*!40000 ALTER TABLE `selection` DISABLE KEYS */;
/*!40000 ALTER TABLE `selection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `created_date` datetime(6) NOT NULL,
  PRIMARY KEY (`test_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (3,'2023-06-07 03:32:51.670177'),(4,'2023-08-09 15:33:53.764605'),(7,'2023-08-09 15:40:51.847780');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testinfo`
--

DROP TABLE IF EXISTS `testinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testinfo` (
  `testinfoid` int NOT NULL AUTO_INCREMENT,
  `test_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `eid_id` int DEFAULT NULL,
  `test_id_id` int DEFAULT NULL,
  `time_limit` int NOT NULL,
  PRIMARY KEY (`testinfoid`),
  KEY `testinfo_eid_id_d4cfd7c7_fk_employer_eid` (`eid_id`),
  KEY `testinfo_test_id_id_255b8b22_fk_test_test_id` (`test_id_id`),
  CONSTRAINT `testinfo_eid_id_d4cfd7c7_fk_employer_eid` FOREIGN KEY (`eid_id`) REFERENCES `employer` (`eid`),
  CONSTRAINT `testinfo_test_id_id_255b8b22_fk_test_test_id` FOREIGN KEY (`test_id_id`) REFERENCES `test` (`test_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testinfo`
--

LOCK TABLES `testinfo` WRITE;
/*!40000 ALTER TABLE `testinfo` DISABLE KEYS */;
INSERT INTO `testinfo` VALUES (3,'Sample',788024608,3,20),(4,'Aditya vyas',833965419,4,15),(7,'New',833965419,7,1);
/*!40000 ALTER TABLE `testinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testques`
--

DROP TABLE IF EXISTS `testques`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testques` (
  `ques_id` int NOT NULL AUTO_INCREMENT,
  `ques_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `option1` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `option2` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `option3` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `option4` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `correct` int NOT NULL,
  `testinfoid_id` int DEFAULT NULL,
  PRIMARY KEY (`ques_id`),
  KEY `testques_testinfoid_id_75d4e17c_fk_testinfo_testinfoid` (`testinfoid_id`),
  CONSTRAINT `testques_testinfoid_id_75d4e17c_fk_testinfo_testinfoid` FOREIGN KEY (`testinfoid_id`) REFERENCES `testinfo` (`testinfoid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testques`
--

LOCK TABLES `testques` WRITE;
/*!40000 ALTER TABLE `testques` DISABLE KEYS */;
INSERT INTO `testques` VALUES (3,'What is django','d','d','f','d',2,3),(4,'Language','Python','Java','C++','C',1,4),(5,'Skills','Front-end','Back-end','AWS','None',3,4),(8,'Moon','Planet','Galaxy','Star','Moon',4,7);
/*!40000 ALTER TABLE `testques` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testuser`
--

DROP TABLE IF EXISTS `testuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testuser` (
  `testuser_id` int NOT NULL AUTO_INCREMENT,
  `correct_answers` int NOT NULL,
  `total_ques` int NOT NULL,
  `answers` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `test_id_id` int DEFAULT NULL,
  `user_id_id` int DEFAULT NULL,
  `emp_id_id` int DEFAULT NULL,
  `apply_id_id` int DEFAULT NULL,
  PRIMARY KEY (`testuser_id`),
  KEY `testuser_test_id_id_dfd8e2b7_fk_test_test_id` (`test_id_id`),
  KEY `testuser_user_id_id_d446b8f9_fk_jobseeker_user_id` (`user_id_id`),
  CONSTRAINT `testuser_test_id_id_dfd8e2b7_fk_test_test_id` FOREIGN KEY (`test_id_id`) REFERENCES `test` (`test_id`),
  CONSTRAINT `testuser_user_id_id_d446b8f9_fk_jobseeker_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `jobseeker` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testuser`
--

LOCK TABLES `testuser` WRITE;
/*!40000 ALTER TABLE `testuser` DISABLE KEYS */;
INSERT INTO `testuser` VALUES (1,0,0,NULL,'2023-07-15 05:17:33.321729',3,309791485,NULL,NULL),(3,0,0,NULL,'2023-07-15 05:29:36.957305',3,268576603,NULL,NULL),(4,1,1,'4,','2023-08-09 15:49:50.137776',7,720061200,NULL,NULL),(5,1,2,'1,1,','2023-08-10 08:47:28.200631',4,720061200,NULL,NULL),(6,1,1,'4,','2023-08-10 08:48:47.946670',7,81570264,NULL,NULL),(7,0,0,NULL,'2023-08-11 06:16:49.235172',7,824712288,NULL,NULL),(8,1,2,'1,4,','2023-08-11 06:18:59.871841',4,81570264,NULL,NULL),(9,0,0,NULL,'2023-08-11 06:18:03.779605',4,824712288,NULL,NULL),(10,0,0,NULL,'2023-08-20 16:45:00.000000',4,603839799,NULL,NULL),(12,1,2,'1,1,','2023-08-12 08:15:29.585999',4,450211284,NULL,NULL),(13,1,1,'4,','2023-08-12 11:02:56.318187',7,373315377,NULL,NULL),(14,0,0,NULL,'2023-08-12 16:30:00.000000',7,603839799,NULL,NULL),(15,1,2,'1,2,','2023-08-12 11:02:36.516814',4,373315377,NULL,NULL),(21,1,1,'4,','2023-08-23 10:31:00.065955',4,720061200,833965419,NULL),(22,1,1,'4,','2023-08-23 11:56:07.192877',7,720061200,833965419,NULL),(23,1,2,'1,2,','2023-08-23 11:59:49.436325',4,373315377,833965419,NULL),(26,1,1,'4,','2023-08-24 03:44:18.330974',7,373315377,833965419,27),(27,1,2,'1,1,','2023-08-24 03:44:32.308318',4,373315377,833965419,28),(28,1,1,'4,','2023-08-25 13:00:09.180662',7,720061200,833965419,29),(29,0,0,NULL,'2023-08-29 05:51:00.000000',7,720061200,833965419,30);
/*!40000 ALTER TABLE `testuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `threads`
--

DROP TABLE IF EXISTS `threads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `threads` (
  `msg_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int NOT NULL,
  `receiver_id` int NOT NULL,
  `has_unread` tinyint(1) NOT NULL,
  `date` datetime(6) NOT NULL,
  PRIMARY KEY (`msg_id`),
  KEY `threads_receiver_id_7483d49e` (`receiver_id`),
  KEY `threads_sender_id_47112132` (`sender_id`),
  CONSTRAINT `threads_receiver_id_7483d49e_fk_login_log_id` FOREIGN KEY (`receiver_id`) REFERENCES `login` (`log_id`),
  CONSTRAINT `threads_sender_id_47112132_fk_login_log_id` FOREIGN KEY (`sender_id`) REFERENCES `login` (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `threads`
--

LOCK TABLES `threads` WRITE;
/*!40000 ALTER TABLE `threads` DISABLE KEYS */;
INSERT INTO `threads` VALUES (1,25,24,0,'2023-06-06 15:45:36.606745'),(2,25,31,0,'2023-07-15 05:22:58.791081'),(3,66,67,0,'2023-08-10 07:34:23.505650'),(4,66,33,0,'2023-08-10 09:31:21.151714'),(5,66,68,0,'2023-08-10 10:31:09.983046'),(6,66,70,0,'2023-08-22 09:47:52.032208'),(7,66,71,0,'2023-08-25 10:13:38.569369');
/*!40000 ALTER TABLE `threads` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-04 21:53:02
