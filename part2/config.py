#!/usr/bin/python3
"""Configuration settings for the HBnB application."""

import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
