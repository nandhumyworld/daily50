import os

class Config:
    """Configuration class for Flask application"""
    
    # Server configuration
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # You can add more configuration options here
    # For example:
    # SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    # DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    PORT = 5000

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    PORT = int(os.environ.get('PORT', 8080))

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    PORT = 5001

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}