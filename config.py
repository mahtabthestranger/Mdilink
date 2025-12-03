"""
Configuration Module - Medilink Hospital Management System.

Developer: Mahtab Ahmed

This module contains all configuration settings for the application
including database connection, session management, and security settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Base configuration class.

    Contains default settings for the application that can be
    overridden by environment-specific configurations.
    """

    # Security key for session encryption
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # MySQL Database Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'medilink_db')
    MYSQL_CURSORCLASS = 'DictCursor'

    # Session Cookie Configuration
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour in seconds


class DevelopmentConfig(Config):
    """
    Development environment configuration.

    Enables debug mode for detailed error messages during development.
    """

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """
    Production environment configuration.

    Disables debug mode and enables secure cookies for HTTPS.
    """

    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
