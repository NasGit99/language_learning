from flask import Blueprint, render_template, current_app, request
import sys
import os

main_bp = Blueprint("main", __name__, template_folder='../pages')

@main_bp.route('/')
def home():
    return render_template('home.html')
