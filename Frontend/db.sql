CREATE DATABASE `pollution`;
USE `pollution`;

CREATE TABLE `users` (
    `id` INT PRIMARY KEY AUTO_INCREMENT, 
    `name` VARCHAR(1000),
    `email` VARCHAR(1000),
    `password` VARCHAR(225)
);
