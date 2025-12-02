-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 02, 2025 at 06:50 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `medilink_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `username`, `password`, `full_name`, `email`, `phone`, `created_at`, `updated_at`, `is_active`) VALUES
(1, 'admin', 'scrypt:32768:8:1$dlfI4Hhpf8AJnrbv$5fa5bb05021b6f244153411de40698d604ea66496fed2587430c64ca3231cd80852c9354a504f0df6e7330711d3493badf7accfe7208bc41d82f525ed2e31689', 'System Administrator', 'admin@medilink.com', '01700000000', '2025-11-28 17:54:22', '2025-11-28 17:54:22', 1);

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `status` enum('Scheduled','Completed','Cancelled','No-Show') DEFAULT 'Scheduled',
  `reason` text DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointment_id`, `patient_id`, `doctor_id`, `appointment_date`, `appointment_time`, `status`, `reason`, `notes`, `created_at`, `updated_at`) VALUES
(1, 2, 1, '2025-11-30', '09:00:00', 'Scheduled', 'I have fever', NULL, '2025-11-28 21:52:16', '2025-11-28 21:52:16'),
(2, 2, 1, '2025-11-30', '10:00:00', 'Scheduled', 'I have headache', NULL, '2025-11-28 21:56:12', '2025-11-28 21:56:12'),
(3, 2, 2, '2025-11-30', '10:30:00', 'Completed', 'I have  leg pain', NULL, '2025-11-28 22:11:27', '2025-11-29 07:26:59'),
(4, 4, 2, '2025-11-30', '10:00:00', 'Cancelled', 'i have fever', NULL, '2025-11-29 14:43:27', '2025-11-29 14:43:36'),
(5, 4, 2, '2025-11-30', '11:30:00', 'Completed', 'i have fever', NULL, '2025-11-29 14:44:04', '2025-11-29 14:44:40'),
(6, 5, 3, '2025-12-02', '11:00:00', 'Cancelled', 'ytjhty htyh tjt y', NULL, '2025-12-01 15:40:58', '2025-12-01 15:41:07');

-- --------------------------------------------------------

--
-- Table structure for table `chat_messages`
--

CREATE TABLE `chat_messages` (
  `message_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_type` enum('admin','doctor','patient','guest') DEFAULT 'guest',
  `message` text NOT NULL,
  `response` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `chat_messages`
--

INSERT INTO `chat_messages` (`message_id`, `user_id`, `user_type`, `message`, `response`, `created_at`) VALUES
(1, 1, 'admin', 'how can I get appoinment', 'I can help you with:\n            <ul>\n                <li>???? Booking appointments</li>\n                <li>????‍⚕️ Finding doctors</li>\n                <li>???? Viewing medical records</li>\n                <li>❌ Cancelling appointments</li>\n                <li>???? Resetting passwords</li>\n                <li>ℹ️ Hospital information</li>\n            </ul>\n            Just ask me anything!', '2025-11-29 09:05:11'),
(2, 1, 'admin', 'How can I  register', 'I can help you with:\n            <ul>\n                <li>???? Booking appointments</li>\n                <li>????‍⚕️ Finding doctors</li>\n                <li>???? Viewing medical records</li>\n                <li>❌ Cancelling appointments</li>\n                <li>???? Resetting passwords</li>\n                <li>ℹ️ Hospital information</li>\n            </ul>\n            Just ask me anything!', '2025-11-29 09:05:40'),
(3, 2, 'patient', 'hi. How to book appointment as a friend', 'Hello Siam! ???? How can I help you today?', '2025-11-29 13:49:01'),
(4, 2, 'patient', 'How can I book appointment as a patient', 'To book an appointment, click on \'Book Appointment\' in your dashboard or <a href=\'/patient/book-appointment\'>click here</a>. You can choose your preferred doctor, date, and time!', '2025-11-29 13:49:22'),
(5, 2, 'patient', 'How can i book appoinment as a patient', 'To book an appointment, click on \'Book Appointment\' in your dashboard or <a href=\'/patient/book-appointment\'>click here</a>. You can choose your preferred doctor, date, and time!', '2025-11-29 14:33:56'),
(6, 1, 'admin', 'where ami i', 'I\'m here to help! You can ask me about:\n        <ul>\n            <li>Booking appointments</li>\n            <li>Finding doctors</li>\n            <li>Medical records</li>\n            <li>Hospital hours and contact info</li>\n        </ul>\n        What would you like to know?', '2025-11-30 07:44:57'),
(7, 1, 'admin', 'i want to mANAGE PATIENT', 'I\'m here to help! You can ask me about:\n        <ul>\n            <li>Booking appointments</li>\n            <li>Finding doctors</li>\n            <li>Medical records</li>\n            <li>Hospital hours and contact info</li>\n        </ul>\n        What would you like to know?', '2025-11-30 07:45:15'),
(8, 5, 'patient', 'book appointment after login', 'To book an appointment, click on \'Book Appointment\' in your dashboard or <a href=\'/patient/book-appointment\'>click here</a>. You can choose your preferred doctor, date, and time!', '2025-12-01 15:43:00'),
(9, 5, 'patient', 'how to choose doctor', 'To book an appointment, click on \'Book Appointment\' in your dashboard or <a href=\'/patient/book-appointment\'>click here</a>. You can choose your preferred doctor, date, and time!', '2025-12-01 15:43:24');

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `doctor_id` int(11) NOT NULL,
  `doctor_code` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `university` varchar(100) NOT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `qualification` varchar(255) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_active` tinyint(1) DEFAULT 1,
  `created_by` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`doctor_id`, `doctor_code`, `password`, `full_name`, `university`, `specialization`, `qualification`, `email`, `phone`, `address`, `created_at`, `updated_at`, `is_active`, `created_by`) VALUES
(1, 'nghjnghjg', 'scrypt:32768:8:1$Ap8rOWqmvjuBXYRO$05faff826d57e548e89ada99c16ad439e8799c1ed936f5ba32272ba9fe38cd6b39a3824287286f5d6a8a6995144735018a7dc66bf43ce1c7fcd8c48bc62ced06', 'hmghmbmghmjj', 'jmhjmjhm fjm', 'jmjhmjhmjhm', 'hmjmjhmnmn', 'oyon@gmail.com', '01858612302', 'nmjmjhhj,m', '2025-11-28 19:42:29', '2025-11-28 19:42:29', 1, 1),
(2, 'DOC101', 'scrypt:32768:8:1$fcm4Xp3HzFh9AaQy$06cd1232010a027d0f9fb45017faa4bc0a64861dc7c5025ba1eb3cf698f68307f709a6210d4b0e562616c79329d48b4cfc75f30c929b1f60cc700926ed9da701', 'Dr. John Smith', 'Dhaka Medical College', 'Cardiology', 'MBBS,MD', 'foysalkarim531@gmail.com', '01730348494', 'abcfd', '2025-11-28 22:07:54', '2025-12-01 15:37:42', 0, 1),
(3, 'Prottoy', 'scrypt:32768:8:1$JByrkWG1yMxCTv4P$d43c0a0e3cbf0ce63814401fdae73b70b46f3130125475a96dc4c832711cf8ae3d15c4c978459a60ac700a7b9f7aa72ce8c0a23a0759b352135f349e6c0b1202', 'tahrim', 'DMC', 'Ent', 'bsc', 'tahrim@northsouth.edu', '01876732647', 'fefeif hbfhrbfb hbf fh fewjhvf eghvf', '2025-12-01 15:37:13', '2025-12-01 15:37:13', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `medical_records`
--

CREATE TABLE `medical_records` (
  `record_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `appointment_id` int(11) DEFAULT NULL,
  `visit_date` date NOT NULL,
  `diagnosis` text NOT NULL,
  `symptoms` text DEFAULT NULL,
  `prescription` text DEFAULT NULL,
  `tests_recommended` text DEFAULT NULL,
  `follow_up_date` date DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `token_id` int(11) NOT NULL,
  `user_type` enum('admin','doctor','patient') NOT NULL,
  `user_id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`token_id`, `user_type`, `user_id`, `email`, `token`, `expires_at`, `created_at`) VALUES
(1, 'patient', 2, 'sihab4716@gmail.com', 'E20DrFPsq21WOKwOzHJpywVFFSlP8-TQ_obskf4-bqw', '2025-11-29 14:57:05', '2025-11-29 07:57:05'),
(4, 'patient', 3, 'foysalkarim531@gmail.com', '3MwIcRIX1pGjkKZQ7B709GofpndhSNlTYO2BREU5SA0', '2025-11-29 21:39:07', '2025-11-29 14:39:07');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `patient_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `address` text DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `emergency_contact` varchar(15) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`patient_id`, `full_name`, `age`, `gender`, `phone`, `email`, `password`, `address`, `blood_group`, `emergency_contact`, `created_at`, `updated_at`, `is_active`) VALUES
(1, 'Al mamun', 24, 'Male', '01857457546', 'almamun@gmail.com', 'scrypt:32768:8:1$9tE8zs1SxUQsWihz$47346fbc800ac6abd0feb73a17a1079a133b8e1386c297610dfdb5332064a899a299888c2270c1e2d5d5dbcbbf90c9e671d69dcfa7157c358b542e1464901ec6', 'kghkjh,tuikhj uyiyuitykj', 'A+', '01857857766', '2025-11-28 19:20:39', '2025-11-29 07:14:18', 0),
(2, 'Siam', 24, 'Male', '01838483833', 'sihab4716@gmail.com', 'scrypt:32768:8:1$JV1iVdaH779XJZ2i$84b1e0533a773c99dd91c9928a74af14ad2f0ae3f513d11a8a4b4e9ee2bd9cda9fa4b1a616a3e011e0935249f1ca8fdde2cab9ccfa4207687832e0c2600843c2', 'tfdhfhgjhfuio', 'AB+', '01838483833', '2025-11-28 21:04:02', '2025-11-29 14:37:13', 0),
(3, 'abir', 21, 'Male', '01399544595', 'foysalkarim531@gmail.com', 'scrypt:32768:8:1$D2urTrZEJgZjlSYw$3e53dd4928aabbb330008c058eb92c717bd9e3ffd681ca0e5ca4bacce9778e22091515ad347c8a80f148d55266089d07ee0bfe2bafd673eb2d1251d88ebed72f', 'dtgyyhg', 'O+', '01399544595', '2025-11-29 08:04:56', '2025-11-29 08:04:56', 1),
(4, 'Mahtab', 23, 'Male', '09908867655', 'abc@gmail.com', 'scrypt:32768:8:1$TfjDJOcXxE9kyd37$62e6ca9faab745c9ea031a68e519b935e371ad424246ba46d187ceedf6927ae8e39629f67ab2718518a8ceaadfeac9ca3417516e97a602ea576874c309c5e2bc', 'yhgfkjh', 'A+', '98785764344', '2025-11-29 14:42:44', '2025-11-29 14:42:44', 1),
(5, 'Mahtab', 34, 'Male', '01843432444', 'mahtab@gmail.com', 'scrypt:32768:8:1$rZYxZ3usE9lZV7Ci$9aa05d034ebab84c430032c0c73f068d291466117aca80e02b0ca9ad6a32012662ea03be6b6ce0d66742cefba7a975969ac88ac31ec30ac5c244c0042b01d548', 'gfdgvdf', 'AB+', '01988798998', '2025-12-01 15:40:20', '2025-12-01 15:40:20', 1),
(6, 'dfgdfg', 24, 'Female', '01857457546', 'oyon@gmail.com', 'scrypt:32768:8:1$QFmhy8QWsx7E2CvY$f654c9ff031a9a1c8e40c0cb81421f1440781cece5e3836a116d192d9274bbbe3b05e031fcec44e9df2a4d0dec9c51c066a3b1857b117d2dadeabb4b81af42e7', 'dferf', 'AB+', '01857857766', '2025-12-01 16:56:02', '2025-12-01 16:56:02', 1),
(7, 'Dog', 8, 'Other', '01847474745', 'dog@gmail.com', 'scrypt:32768:8:1$AZmUuiypdbP2RquT$025c46f5b495241d8aa3e3ea04a9b46c335ab8155721dde123f8e93bf429b5b9bba8031cdf978914c4f8309bb24ca97026c68e86b02a172b621a76d501a6d021', 'frefrrrrrrrrrrrr', 'O-', '01838383838', '2025-12-01 17:06:53', '2025-12-01 17:06:53', 1),
(8, 'LordBebo', 45, 'Male', '01848484447', 'lord@gmail.com', 'scrypt:32768:8:1$MESJigGamSEQJsP1$2cc43476dbf058b535f73764d7faac1f59be2d6ede1a271735ed4831182c95efcfd16a503e191332b6a2edc6753e90441053cbd042012d2f5f6c60c855b00538', 'ewwef dfgrfgrf', 'O+', '01846666677', '2025-12-02 16:16:13', '2025-12-02 16:16:13', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`),
  ADD UNIQUE KEY `unique_appointment` (`doctor_id`,`appointment_date`,`appointment_time`),
  ADD KEY `patient_id` (`patient_id`);

--
-- Indexes for table `chat_messages`
--
ALTER TABLE `chat_messages`
  ADD PRIMARY KEY (`message_id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`doctor_id`),
  ADD UNIQUE KEY `doctor_code` (`doctor_code`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `medical_records`
--
ALTER TABLE `medical_records`
  ADD PRIMARY KEY (`record_id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `appointment_id` (`appointment_id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`token_id`),
  ADD UNIQUE KEY `token` (`token`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`patient_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `chat_messages`
--
ALTER TABLE `chat_messages`
  MODIFY `message_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `doctor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `medical_records`
--
ALTER TABLE `medical_records`
  MODIFY `record_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `token_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `patient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE;

--
-- Constraints for table `doctors`
--
ALTER TABLE `doctors`
  ADD CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `admins` (`admin_id`) ON DELETE SET NULL;

--
-- Constraints for table `medical_records`
--
ALTER TABLE `medical_records`
  ADD CONSTRAINT `medical_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `medical_records_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `medical_records_ibfk_3` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
