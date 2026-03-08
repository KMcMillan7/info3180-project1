"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from app.models import Property
from app.forms import PropertyForm
import uuid


###
# Routing for your application.
###
bp = Blueprint('main', __name__)
@bp.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@bp.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Viewing Property")

@bp.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()
    if form.validate_on_submit():
        # Handle file upload
        file = form.photo.data
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))

        # Create new property record
        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            location=form.location.data,
            price=form.price.data,
            currency=form.currency.data,
            property_type=form.property_type.data,
            photo_filename=new_filename
        )
        db.session.add(new_property)
        db.session.commit()
        flash('Property created successfully!', 'success')
        return redirect(url_for('main.list_properties'))
    return render_template('create_property.html', form=form)


@bp.route('/properties')
def list_properties():
    properties= Property.query.order_by(Property.created_at.desc()).all()
    return render_template('properties.html', properties=properties)

@bp.route('/properties/<int:property_id>')
def view_property(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property.html', property=property)


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@bp.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return current_app.send_static_file(file_dot_text)


@bp.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@bp.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
