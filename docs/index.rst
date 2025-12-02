Patient Authentication Module
=============================

**Student:** Mahtab Ahmed

**Project:** Medilink Hospital Management System

**Feature:** Patient Login, Registration & Dashboard Redirect

Overview
--------

This module handles patient authentication for the Medilink Hospital Management System.
It follows the MVC (Model-View-Controller) architecture pattern.

Features
--------

1. **Patient Registration** - New patients can create accounts
2. **Patient Login** - Secure authentication with password hashing
3. **Dashboard Redirect** - Protected route after login
4. **Session Management** - Secure session handling
5. **Logout** - Clear session and redirect

Architecture
------------

The module follows MVC pattern:

* **Model:** ``models/patient.py`` - Database operations
* **View:** ``templates/patient/*.html`` - User interface
* **Controller:** ``Mahtabapp.py`` - Route handlers

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   mahtabapp
   modules
   patient_model
   routes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

