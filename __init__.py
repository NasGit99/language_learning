from flask import Flask,jsonify
import os
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required


from templates.blueprints.main_bp import main_bp 
from templates.blueprints.file_translation_bp import file_translation_bp
from templates.blueprints.user_profile_bp import user_profile_bp

def create_app(test_config=None):
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'flask_uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance'))
    app = Flask(__name__, instance_path=instance_path)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config.from_mapping(JWT_SECRET_KEY ='dev')
    app.config["ALLOWED_EXTENSIONS"] = {'txt'}   

    app.register_blueprint(main_bp)
    app.register_blueprint(file_translation_bp)
    app.register_blueprint(user_profile_bp) 

    jwt = JWTManager(app)


    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app

@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
   program = create_app()
   program.run(host="0.0.0.0", port=8000, debug=True)
   
