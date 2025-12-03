Configuration Module
====================

Developer: Mahtab Ahmed

File: ``config.py``

Description
-----------
This module contains all configuration settings for the application including database connection, session management, and security settings.

Class: Config
-------------

.. py:class:: Config

   Base configuration class with default settings.

   .. py:attribute:: SECRET_KEY
      
      Security key for session encryption

   .. py:attribute:: MYSQL_HOST
      
      MySQL database host (default: localhost)

   .. py:attribute:: MYSQL_USER
      
      MySQL database user (default: root)

   .. py:attribute:: MYSQL_PASSWORD
      
      MySQL database password

   .. py:attribute:: MYSQL_DB
      
      MySQL database name (default: medilink_db)

   .. py:attribute:: MYSQL_CURSORCLASS
      
      Cursor class for MySQL queries (DictCursor)

   .. py:attribute:: SESSION_COOKIE_SECURE
      
      Enable secure cookies (False for development)

   .. py:attribute:: SESSION_COOKIE_HTTPONLY
      
      HTTP only cookies (True)

   .. py:attribute:: SESSION_COOKIE_SAMESITE
      
      SameSite cookie policy (Lax)

   .. py:attribute:: PERMANENT_SESSION_LIFETIME
      
      Session timeout in seconds (3600 = 1 hour)

Class: DevelopmentConfig
------------------------

.. py:class:: DevelopmentConfig(Config)

   Development environment configuration.

   .. py:attribute:: DEBUG
      
      Enable debug mode (True)

   .. py:attribute:: TESTING
      
      Testing mode (False)

Class: ProductionConfig
-----------------------

.. py:class:: ProductionConfig(Config)

   Production environment configuration.

   .. py:attribute:: DEBUG
      
      Disable debug mode (False)

   .. py:attribute:: SESSION_COOKIE_SECURE
      
      Enable secure cookies for HTTPS (True)

Configuration Dictionary
------------------------

.. py:data:: config

   Dictionary for accessing configurations::

      config = {
          'development': DevelopmentConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig
      }

