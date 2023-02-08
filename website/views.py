from flask import Blueprint, render_template, request
from flask_login import login_required, current_user 
from .models import Note
from . import db
from flask import flash
import json
import jsonify
#defines a "template" 
views = Blueprint('views', __name__)
#This is defining the root directory
@views.route('/', methods=['GET', 'POST'])
#can not get to login page without being logged out.
# Must be logged in
@login_required 
def home():
    #if method is a post
    if request.method == 'POST':
        #gets the note from the database
        note = request.form.get('note')
        #if note is empty it gives an error
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            #if note is > 1 we add the note to the data base
            #this sends the note to fill the data field and
            #fills the user_id field with the current user
            new_note = Note(data=note, user_id = current_user.id)
            #this adds the new note to the database
            db.session.add(new_note)
            #Officially sends the note to the database
            db.session.commit()
            #Flashes that the note was added with a category of success
            flash("Note added", category="success")
    
    # This renders home.html when route is /
    #Also sends the current user to the home.html template
    return render_template("home.html", user=current_user) 

#Defines a route called delete-note that gets posted to
@views.route('/delete-note', methods=["POST"])
def delete_note():
    #Loads the data sent through the request and stores it in note
    note = json.loads(request.data)
    #sets nodeId = to the request.data[note id field]
    noteId = note['noteId']
    #then it retrieves the noteId from the database
    note = Note.query.get(noteId)
    #if we have a note
    if note:
        #if the note.user_id from the database that we just retrieved
        #is equal to the id of the user that is currently logged in 
        if note.user_id == current_user.id:
            #it deletes the note that was retrieved
            db.session.delete(note)
            #finalizes the session
            db.session.commit()
    #returns empty json object
    return jsonify({})

