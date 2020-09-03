import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from attendance import app, mail 

# function to change pfp
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # gets a random 8 bit string for filename so no files clash
    _, f_ext = os.path.splitext(form_picture.filename) # find out if file is a jpg or png ''' here s'''
    picture_fn = random_hex + f_ext # makes the pictures filename equal to the random hex and the file extension (jpg or png)
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # concatonates path for profile pics with picture path 
    
    output_size = (125, 125) # tuple that contains file sizes h/w
    i = Image.open(form_picture)
    i.thumbnail(output_size) # resizes the image to i h/w 
    i.save(picture_path) # saves image to the picture path 

    return picture_fn 

# function to send an email to the user 
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                 sender="dtptestemail@gmail.com",
                 recipients=[user.email]) # subect, sender, recipiants
    msg.body = f''' to reset your password, visit the following link:
{url_for('users.reset_token',token=token, _external=True)}

If you did not request a password change then please ignore this email
'''
    mail.send(msg)
