-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 19, 2018 at 07:05 PM
-- Server version: 5.5.58-0ubuntu0.14.04.1-log
-- PHP Version: 5.5.9-1ubuntu4.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `trade`
--

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE IF NOT EXISTS `reports` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `symbol` varchar(100) NOT NULL,
  `date` varchar(100) NOT NULL,
  `openPrice` varchar(100) NOT NULL,
  `highPrice` varchar(100) NOT NULL,
  `lowPrice` varchar(100) NOT NULL,
  `closePrice` varchar(100) NOT NULL,
  `volume` varchar(100) NOT NULL,
  `vwap` varchar(100) NOT NULL,
  `ema` varchar(100) NOT NULL,
  `relativeVolume` varchar(100) NOT NULL,
  `trend` varchar(100) NOT NULL,
  `tradePosition` varchar(100) NOT NULL,
  `entryPrice` varchar(100) NOT NULL,
  `entryPriceWithCushion` varchar(100) NOT NULL,
  `sl` varchar(100) NOT NULL,
  `slWithCushion` varchar(100) NOT NULL,
  `plPoints` varchar(100) NOT NULL,
  `exitPrice` varchar(100) NOT NULL,
  `target1Pos` varchar(100) NOT NULL,
  `target1Entry` varchar(100) NOT NULL,
  `target1Price` varchar(100) NOT NULL,
  `target1Exit` varchar(100) NOT NULL,
  `target1PL` varchar(100) NOT NULL,
  `target2Pos` varchar(100) NOT NULL,
  `target2Entry` varchar(100) NOT NULL,
  `target2Price` varchar(100) NOT NULL,
  `target2Exit` varchar(100) NOT NULL,
  `target2PL` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`id`, `symbol`, `date`, `openPrice`, `highPrice`, `lowPrice`, `closePrice`, `volume`, `vwap`, `ema`, `relativeVolume`, `trend`, `tradePosition`, `entryPrice`, `entryPriceWithCushion`, `sl`, `slWithCushion`, `plPoints`, `exitPrice`, `target1Pos`, `target1Entry`, `target1Price`, `target1Exit`, `target1PL`, `target2Pos`, `target2Entry`, `target2Price`, `target2Exit`, `target2PL`) VALUES
(3, 'simgcap', '1515433740000', '10.09', '10.208', '10.08', '10.208', '99198', '0', '0', '0', 'UP', 'LONG', '10.05', '10.16', '0', '0', '0', '0', 'LONG', '10.16', '10.57', '0', '0', 'LONG', '10.16', '11.07', '0', '0');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
