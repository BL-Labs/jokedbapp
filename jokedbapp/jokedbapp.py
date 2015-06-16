from models import *
from database import db_session
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, send_file

from render_joke import ICanHaz

from utils.tumblr_post import tumblr_imagepost
from utils.twitter_post import twitter_imagepost
from utils.tumblrcreds import blog

from utils.handle_transcript import TranscriptionParser as TP

import tempfile

# app-wide configuration
DEBUG = True
SECRET_KEY = "thisisasupersekritkeyunassailablewithmoderntechniques0120847119579"

# create our app and load in the config
app = Flask(__name__)
app.config.from_object(__name__)

def _render_joke_to_file(j):
  renderer = ICanHaz()
  if j != None:
    t = j.from_transcription
    b = t.biblio
    page = t.pagestart
    if t.pagestart != t.pageend:
      page = u"{0}-{1}".format(t.pagestart, t.pageend)

    lines = renderer.markup_text(j.title, j.joketext, j.attribution, "DEFAULT")
    attribution_lines = renderer.markup_attribution_box(b.title, b.date, page, column_title = t.article_title, partname = 'ATTRIB')

    _, fn = tempfile.mkstemp(suffix=".png", dir="/tmp")
    renderer.render_basic_vertical(lines, attribution_lines, fn, jokeid=j.id)
    return fn, attribution_lines

def _render_joke_w_jokester_to_file(j):
  renderer = ICanHaz()
  if j != None:
    t = j.from_transcription
    b = t.biblio
    page = t.pagestart
    if t.pagestart != t.pageend:
      page = u"{0}-{1}".format(t.pagestart, t.pageend)

    lines = renderer.markup_text(j.title, j.joketext, j.attribution, "DEFAULT")
    attribution_lines = renderer.markup_attribution_box(b.title, b.date, page, column_title = t.article_title, partname = 'ATTRIB', source_attrib=j.attribution)

    _, fn = tempfile.mkstemp(suffix=".png", dir="/tmp")
    renderer.render_basic_vertical(lines, attribution_lines, fn, jokeid=j.id)
    return fn, attribution_lines

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html"), 404

@app.route("/", methods=['GET', 'POST'])
def home_page():
  offset, paging = 0, 40
  if request.method == "GET":
    get_offset = request.args.get("offset", offset)
    get_paging = request.args.get("paging", paging)
    try:
      paging = int(get_paging)
      offset = int(get_offset)
    except ValueError as e:
      flash('Not a valid offset')
  if offset:
    latest_added = Joke.query.order_by(Joke.id)[offset:offset+paging]
  else:
    latest_added = Joke.query.order_by(Joke.id)[:paging]

  back = offset-paging
  if back<0: back = 0

  forward = offset+paging
  if forward<0: forward = 0
  return render_template('home_page.html', latest=latest_added, offset=offset, paging=paging, \
                                           back=back, forward=forward)

@app.route("/joke", methods=['GET'])
def joke_page():
  # Show an 'add joke' form?
  return redirect(url_for('home_page'))

@app.route("/joke/<int:joke_id>", methods=['GET'])
def display_joke(joke_id):
  j = Joke.query.get(joke_id)
  if not j:
    abort(404)
  return render_template('display_joke_page.html', j=j, tumblr_account="http://victorianhumour.tumblr.com/post/") # FIXME

@app.route("/transcription/<int:transcription_id>", methods=["POST"])
def edit_update_transcription(transcription_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    t = Transcription.query.get(transcription_id)
    if not t:
      abort(404)
    # update the joke db with the edited text
    text = request.values.get("rawtext", "")
    if text:
      # TODO only admins? Seeing as we only have admins...
      t.raw = text
      db_session.add(t)
      db_session.commit()
      flash("Saved edited text for this Transcription. (Jokes created from the original transcription are unaffected. Please regenerate the Jokes to delete them and create new ones.)")
    else:
      flash("NO TEXT ENTERED. No change will be made to the DB.")

    return redirect(url_for('display_transcription', trans_id=t.id))

def _get_jokes(t):
    tp = TP()
    #try:
    if True:
      tp.fromstring(t.raw)
      if tp.parsed():
        return tp
    #except Exception as e:
    #  flash(e)
      return []
    
@app.route("/dry_run_regenerate_jokes/<int:transcription_id>", methods=["POST"])
def dry_run_regenerate_jokes(transcription_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    t = Transcription.query.get(transcription_id)
    if not t:
      abort(404)
    # dry run!
    jokes = _get_jokes(t)
    if jokes:
      flash("\n".join(["Title:{0.title} --=-- {0.text} \n({0.attribution})".format(j) for j in jokes]))
      flash("{0} jokes found".format(len(jokes)))
    else:
      flash("No Jokes detected!")
    return redirect(url_for('display_transcription', trans_id=t.id))
    

@app.route("/regenerate_jokes/<int:transcription_id>", methods=["POST"])
def regenerate_jokes(transcription_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    t = Transcription.query.get(transcription_id)
    if not t:
      abort(404)
    # get list of jokes derived from this one and delete them
    jokes = _get_jokes(t)
    if jokes:
      flash("Found {0} jokes within the transcription.".format(len(jokes)))
      jokes_deleted = []
      for deadjoke in t.joke_children:
        jokes_deleted.append(deadjoke.id)
        db_session.delete(deadjoke)
      flash("Deleted {0} jokes - IDs:({1})".format(len(jokes_deleted), jokes_deleted))
      for idx, joke in enumerate(jokes):
        j = Joke(transcription = t, text = joke.text, transcription_position = idx, title=joke.title, attribution=joke.attribution, joketext = joke.text)
        db_session.add(j)
        # Do all jokes, then commit?
        db_session.commit()
      flash("{0} jokes generated from this transcription".format(idx+1))
  return redirect(url_for('display_transcription', trans_id=t.id))

@app.route("/works", methods=["POST"])
def create_new_work():
  if session['logged_in'] != True:
    abort(401)
  b = Biblio()
  _update_and_store(b, request)
  flash("Created new bibliographic work and updated information.")
  return redirect(url_for('display_work', work_id=b.id))

@app.route("/works", methods=["DELETE"])
def delete_work(work_id):
  # TODO
  pass
  
@app.route("/works", methods=['GET'])
def display_work_admin():
  offset, paging = 0, 10
  if request.method == "GET":
    get_offset = request.args.get("offset", offset)
    get_paging = request.args.get("paging", paging)
    try:
      paging = int(get_paging)
      offset = int(get_offset)
      if offset < 0:
        offset = 0
      if paging < 0:
        paging = 10
    except ValueError as e:
      flash('Not a valid parameter')

  # should be fine with small numbers of works... FIXME
  works_list = Biblio.query.all()[offset:offset+paging]
  back = offset-paging
  if back<0: back = 0

  forward = offset+paging
  if forward<0: forward = 0

  return render_template('display_works.html', offset=offset, paging=paging, \
                                               back=back, forward=forward, works_list=works_list, b=[])


@app.route("/works/<int:work_id>", methods=["POST"])
def edit_update_work(work_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    b = Biblio.query.get(work_id)
    if not b:
      abort(404)

    _update_and_store(b, request)
    flash("Saved edited bibliographic information for this work.")
    return redirect(url_for('display_work', work_id=b.id))

def _update_and_store(b, request):
    # update the joke db with the edited text
    b.title = request.values.get("title", "")
    b.author= request.values.get("author", "")
    b.editor = request.values.get("editor", "")
    b.publisher = request.values.get("publisher", "")
    b.date = request.values.get("date", "")
    b.city = request.values.get("city", "")
    b.country = request.values.get("country", "")
    b.rights = request.values.get("rights", "")
    b.rightsholder = request.values.get("rightsholder", "")
    b.periodical_freq = request.values.get("periodical_freq", "NA")
    b.itemtype = request.values.get("itemtype", "periodical")
    b.citation = request.values.get("citation", "")
    b.blshelfmark = request.values.get("blshelfmark", "")
    b.gale = request.values.get("gale", "")
    
    db_session.add(b)
    db_session.commit()

@app.route("/joke/<int:joke_id>", methods=["POST"])
def edit_update_joke(joke_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    j = Joke.query.get(joke_id)
    if not j:
      abort(404)
    # update the joke db with the edited text
    text = request.values.get("joketext", "")
    title = request.values.get("title", "")
    attrib = request.values.get("attrib", "")
    if text:
      # TODO only admins? Seeing as we only have admins...
      j.joketext = text
      if title:
        j.title = title
      if attrib:
        j.attrib = attrib
      db_session.add(j)
      db_session.commit()
      flash("Saved edited text for this Joke. (Original Transcription is unaffected. NB Browser will cache the image, so you will not see changes until the page is refreshed.)")

    return render_template('display_joke_page.html', j=j, tumblr_account="http://victorianhumour.tumblr.com/post/") # FIXME

@app.route("/remove_from_tumblr/<int:joke_id>", methods=["POST"])
def remove_from_tumblr(joke_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    j = Joke.query.get(joke_id)
    if not j:
      abort(404)
    if j.published_at:
      user_id = session['logged_in_user']
      u = User.query.get(user_id)
      flash("Removed connection to {0}{1} NB TUMBLR POST STILL EXISTS!".format(blog, j.tumblr_id))
      j.published_at = None
      j.tumblr_id = None
      j.published_by_id = None
      db_session.add(j)
      db_session.add(u)
      db_session.commit()
      # Delete file?
      return redirect(url_for('display_joke', joke_id=j.id))
     
@app.route("/tweet_joke/<int:joke_id>", methods=["POST"])
def tweet_joke(joke_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    j = Joke.query.get(joke_id)
    if not j:
      abort(404)

    # Make temp file
    fn, attribution = _render_joke_to_file(j)

    if not j.published_at:
      #publish to tumblr first
      user_id = session['logged_in_user']
      u = User.query.get(user_id)
      if fn:
#        adapted = tumblr_imagepost(j, fn, attribution=attribution, url=url_for("display_joke", joke_id=j.id))
        adapted = tumblr_imagepost(j, fn, attribution=attribution)
        if adapted:
          adapted.published_by_id = u.id
          db_session.add(adapted)
          db_session.add(u)
          db_session.commit()
          flash("Published to {0}/{1}".format(blog, j.tumblr_id))
    
    tumblr_id = j.tumblr_id
    tweet_text, resp = twitter_imagepost(j, fn, tumblr_id = tumblr_id)
    if resp:
      flash(u"Successfully tweeted -> <a href=\"https://twitter.com/VictorianHumour/status/{1}\">'{0}'</a>".format(tweet_text, str(resp['id'])))
      j.twitter_id = resp['id']
      db_session.add(j)
      db_session.commit()
    return redirect(url_for('display_joke', joke_id=j.id))

@app.route("/publish_joke/<int:joke_id>", methods=["POST"])
def publish_to_tumblr(joke_id):
  if session['logged_in'] != True:
    abort(401)
  else:
    j = Joke.query.get(joke_id)
    if not j:
      abort(404)
    if not j.published_at:
      user_id = session['logged_in_user']
      u = User.query.get(user_id)
      fn, attribution = _render_joke_to_file(j)
      if fn:
        adapted = tumblr_imagepost(j, fn, attribution=attribution, url=url_for("display_joke", joke_id=j.id))
        if adapted:
          adapted.published_by_id = u.id
          db_session.add(adapted)
          db_session.add(u)
          db_session.commit()
          flash("Published to {0}/{1}".format(blog, j.tumblr_id))
          # Delete file?
          return redirect(url_for('display_joke', joke_id=j.id))
    else:
      flash("Already published")
      return redirect(url_for('display_joke', joke_id=j.id))

@app.route("/search", methods=['GET','POST'])
def search():
  offset, paging = 0, 30
  if request.method == "GET":
    get_offset = request.args.get("offset", offset)
    get_paging = request.args.get("paging", paging)
    query = request.args.get("q", "")
  else:
    get_offset = request.form.get("offset", offset)
    get_paging = request.form.get("paging", paging)
    query = request.form.get("q", "")
    
  try:
    paging = int(get_paging)
    offset = int(get_offset)
  except ValueError as e:
    flash('Not a valid offset')

  if query:
    joke_list = Joke.query.filter(Joke.text.like("%"+query+"%"))[offset:offset+paging]
    back = offset-paging
    if back<0: back = 0

    forward = offset+paging
    if forward<0: forward = 0
    return render_template('display_search.html', offset=offset, paging=paging, \
                                           back=back, forward=forward, query=query, jokes = joke_list)

  else:
    return redirect(url_for('home_page'))

@app.route("/works/<int:work_id>", methods=['GET'])
def display_work(work_id):
  b = Biblio.query.get(work_id)
  offset, paging = 0, 30
  if request.method == "GET":
    get_offset = request.args.get("offset", offset)
    get_paging = request.args.get("paging", paging)
    try:
      paging = int(get_paging)
      offset = int(get_offset)
    except ValueError as e:
      flash('Not a valid offset')
  #if offset:
  #  latest_added = Joke.query.order_by(Joke.id)[offset:offset+paging]
  #else:
  #  latest_added = Joke.query.order_by(Joke.id)[:paging]
  transcription_list = Transcription.query.filter(Transcription.biblio_id == b.id).order_by(Transcription.id)[offset:offset+paging]
  back = offset-paging
  if back<0: back = 0

  forward = offset+paging
  if forward<0: forward = 0
  if not b:
    abort(404)
  return render_template('display_work.html', b=b, offset=offset, paging=paging, \
                                           back=back, forward=forward, transcription_list=transcription_list)

@app.route("/transcription/<int:trans_id>", methods=['GET'])
def display_transcription(trans_id):
  t = Transcription.query.get(trans_id)
  if not t:
    abort(404)
  return render_template('display_transcription.html', b=t.biblio, t=t)

@app.route("/render_w_image/<int:joke_id>", methods=['GET'])
def render_joke_w_image(joke_id):
  j = Joke.query.get(joke_id)
  if j != None:
    fn, _ = _render_joke_w_jokester_to_file(j)
    if fn:
      return send_file(fn, mimetype="image/png")
  else:
    abort(404)

@app.route("/render/<int:joke_id>", methods=['GET'])
def render_joke(joke_id):
  j = Joke.query.get(joke_id)
  if j != None:
    fn, _ = _render_joke_to_file(j)
    if fn:
      return send_file(fn, mimetype="image/png")
  else:
    abort(404)

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    user = User.query.filter(User.name == request.form['username']).first()
      
    if user == None:
      error = 'Invalid username or password'
    elif request.form['password'] != user.pw_hash:
      error = 'Invalid username or password'
    else:
      session['logged_in'] = True
      session['logged_in_user'] = user.id
      flash('You were logged in, {0}'.format(user.name))
      return redirect(url_for('home_page'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home_page'))

if __name__ == "__main__":
  app.run(host="0.0.0.0")
