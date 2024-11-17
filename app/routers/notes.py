from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Note, db

# Инициализация блупринта для маршрутов, связанных с заметками
notes_bp = Blueprint('notes', __name__)

# Маршрут для отображения всех заметок
@notes_bp.route('/notes', methods=['GET'])
@login_required
def notes_list():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

# Маршрут для создания новой заметки
@notes_bp.route('/notes/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        data = request.form
        new_note = Note(title=data['title'], content=data['content'], user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('notes.notes_list'))
    return render_template('create_note.html')

# Маршрут для редактирования существующей заметки
@notes_bp.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.owner != current_user:
        flash('Unauthorized!')
        return redirect(url_for('notes.notes_list'))

    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('notes.notes_list'))

    return render_template('edit_note.html', note=note)

# Маршрут для удаления существующей заметки
@notes_bp.route('/notes/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.owner != current_user:
        flash('Unauthorized!')
        return redirect(url_for('notes.notes_list'))

    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.notes_list'))