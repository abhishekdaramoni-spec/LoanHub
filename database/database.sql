-- LoanSphere Banking Loan Management System Database Setup Schema
-- Feel free to run this in your MySQL instance to create the database structure manually.

CREATE DATABASE IF NOT EXISTS loansphere_db;
USE loansphere_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    address TEXT,
    photo VARCHAR(255) NOT NULL DEFAULT 'default_user.png',
    is_admin BOOLEAN DEFAULT FALSE,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(100),
    reset_token VARCHAR(100),
    reset_token_expiry DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    KEY idx_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Loan Types Table
CREATE TABLE IF NOT EXISTS loan_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    min_amount DECIMAL(15, 2) NOT NULL,
    max_amount DECIMAL(15, 2) NOT NULL,
    min_interest_rate DECIMAL(5, 2) NOT NULL,
    max_interest_rate DECIMAL(5, 2) NOT NULL,
    processing_fee_pct DECIMAL(4, 2) NOT NULL,
    min_tenure_months INT NOT NULL,
    max_tenure_months INT NOT NULL,
    eligibility_criteria TEXT NOT NULL,
    approval_time VARCHAR(50) NOT NULL,
    icon_class VARCHAR(50) NOT NULL DEFAULT 'fa-wallet',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Loan Applications Table
CREATE TABLE IF NOT EXISTS loan_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    loan_type_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    occupation VARCHAR(100) NOT NULL,
    employer VARCHAR(100) NOT NULL,
    monthly_income DECIMAL(15, 2) NOT NULL,
    loan_amount DECIMAL(15, 2) NOT NULL,
    tenure_months INT NOT NULL,
    pan_number VARCHAR(20) NOT NULL,
    aadhar_number VARCHAR(20) NOT NULL,
    pan_doc VARCHAR(255) NOT NULL,
    aadhar_doc VARCHAR(255) NOT NULL,
    salary_slip_doc VARCHAR(255) NOT NULL,
    bank_statement_doc VARCHAR(255) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    remarks TEXT,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (loan_type_id) REFERENCES loan_types(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. EMI History Table
CREATE TABLE IF NOT EXISTS emi_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    loan_application_id INT NOT NULL,
    amount_paid DECIMAL(15, 2) NOT NULL,
    principal_paid DECIMAL(15, 2) NOT NULL,
    interest_paid DECIMAL(15, 2) NOT NULL,
    balance_remaining DECIMAL(15, 2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'Paid',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (loan_application_id) REFERENCES loan_applications(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Interest Rates Table
CREATE TABLE IF NOT EXISTS interest_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loan_type_id INT NOT NULL,
    tenure_months INT NOT NULL,
    rate_pct DECIMAL(5, 2) NOT NULL,
    effective_from DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (loan_type_id) REFERENCES loan_types(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Contact Messages Table
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. FAQs Table
CREATE TABLE IF NOT EXISTS faqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'General',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
