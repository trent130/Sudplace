from flask import Blueprint, flash, jsonify,render_template,request
from flask_login import login_required,  current_user
from website.models import Note
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    from . import db 
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note= Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully', category='success')
    return render_template("index.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    from . import db 
    note = json.load(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        
    return jsonify({})
