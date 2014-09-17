from models import *
import sys

def load_db(db_session):
  from datetime import datetime
  # load a db session with the data
  print("Creating 6 users, 2 for each role")
  userdata = [("ben", "admin@victorianhumour.com", 0, "adas"),
           ("tom", "tom@victorianhumour.com", 0, "adas"),
           ("dick", "dick@victorianhumour.com", 1, "adas"),
           ("diane", "diane@victorianhumour.com", 1, "adas"),
           ("harry", "harry@victorianhumour.com", 2, "adas"),
           ("harriet", "harriet@victorianhumour.com", 2, "adas"),]

  # Users:
  users = []
  for item in userdata:
    users.append(User(*item))
    db_session.add(users[-1])
  db_session.commit()

  # example transcription data
  transcriptiondata = [(33, """<j> <t> THE COUNTRY HOUSE. </t> - (What our architect has to put up with.) - Fair Client: I want it to be nice and baronial, Queen Anne and Elizabethan, and all that; kind of quaint and Nurembergy, you know - regular old English, with French windows opening to the lawn, and venetian blinds, and sort of Swiss balconies, and a loggia. But I'm sure *you* know what I mean! <a> Punch. </a> </j>

<j> <t>OLD AND CRUSTY. </t> - Fussy old Director: Lemme see, porter-er-how do the Brighton trains run this month? - Crusty Old Porter (snappily): On wheels. [Sacked.] <a> Judy. </a> </j>

<j> <t> AGREED. </t> The Tailor (with great firmness): I tell you, captain, unless you pay that bill at once I must put it into other hands. - Captain Hardup (grasping his hand with fervour): My dear friend, I'm eternally obliged to you! I don't care whose hands you put it into so long as you take it out of mine. <a> Moonshine </a> </j>

<j> <t> POMPOUS </t> POMPOUS Husband (whose wife has just stolen up and kissed him): Madam, I consider your conduct most indecorous. - She: I'm so sorry, but I didn't know it was you. <a> Ariel. </a> </j>

<j> <t> OVER ON BUSINESS. </t> Jones: I always make a point of telling my wife everything that happens. - Brown: My dear fellow, I tell my wife lots of things that never happen. <a> Ariel. </a> </j>

<j> <t> [Untitled] </t> "There's no place like home", says the song. We all know that; but unfortunately we never appreciate it until the time comes when we haven't got one. <a> Judy. </a> </j>

<j> <t> AN AMBIGUOUS ASSURANCE </t> Mature but Moneyed Young Lady: I know that from the way the fellows do crowd around me you'd think I was a flirt. But I assure you it's not my fault. - Immature but Impecunious Young Lady: No, dear, it's your fortune. <a> Ariel </a> </j>

<j> <t>[Untitled]</t> Judge: Gentlemen of the jury, have you agreed upon your verdict? - The Jury: Yes, sor; we've had a stiff fight over it, but we're all o' one moind now. <a>Fun.</a> </j>

<j> <t>A 'STOCK' ACTOR.</t> - Manager (to old actor): No; I'm afraid we've nothing in your way. Old Actor: But, my dear sir, do you know what is my way? I go from Shakespeare to a monkey on a tight rope, and that's a pretty long range, I should think. <a>Fun.</a> </j>

<j> <t>"AND A GOOD JUDGE, TOO".</t> - Amateur Composer (to musical justice of the peace): Er - by the bye, have you ever tried one of my songs? - Musical J.P. (significantly): No - but I'd like to. <a>Funny Folks.</a> </j>

<j> <t>A CHECK.</a> - Huntsman: Seen the fox, my boy? - Boy: No, I ain't! - Huntsman: Then, what are you hollarin' for? - Boy (who has been scaring rooks): 'Cos I'm paid for it! <a>Punch.</a> </j>

<j> <t>"O'SHEA-MEFUL</t> Alas! That one in whom poor Erin placed

Full faith and credit, she at last discovers

To be continued, deservedly disgraced,

Basest of friends, and paltriest of lovers.

Whether Erin's cause may suffer, who can tell.

But he, at least, has rung his own (Par)knell!"

<a>Fun.</a> </j>""", datetime.now(), users[0]),
           (34, """<j> <t>THAT APPLE AGAIN.</t> - Jack: Look here, Winny!- an apple weighing thirty-two ounces. - Winny: Dear me! It must have been the dying effort of the tree. <a>Judy</a> </j>

<j> <t>[Untitled]</t> Can Messrs. Dillon and O'Brien by arrested in Canada? We hope not; surely there is no such hurry as that to get them home again. <a>Moonshine.</a> </j>

<j> <t>[Untitled]</t> At Hatfield last week policemen and burglars, armed with revolvers, three to three, fired at one another for quite a long time. At last one of the policemen got his finger hurt. Then the three burglars went away - honour was satisfied. <a>Moonshine</a> </j>

<j> <t>SPRINGING A 'MINE'.</t> - Lord Lackland: Miss Vandenboom, I love you. Say you will be mine. - Miss Vandenboom (American millionairess): Well, my lord, I reckon I can never be any man's; but you can be mine, if you like. <a>Funny Folks</a> </j>

<j> <t>[Untitled]</t> Boulanger is going to start a paper, and be his own editor. Aut scissors aut nullus! Disaster has not quenched his aspirations. <a>Moonshine</a> </j>

<j> <t>[Untitled]</t> I don't know what it is, Mark, but I can't hit a bird to-day. - Let me see your gun, sir. Ah! - well, I'd try what you could do with some cartridges in it, if I was you, sir. <a>Punch.</a> </j>

<j> <t>SHORTLY TO APPEAR.</t> - Companion volume to "Oceana." New work, by C. S. P-rn-ll, entitled, "O'Sheana." <a>Punch. </a> </j>

<j> <t>[Untitled]</t> Mr. Stanley and his Troup have been giving daily performances to large audiences. <a>Punch</a> </j>

<j> <t>PRESSING.</t> - Mr. Truelove: Now I'll go. I'm afraid I've taken up too much your time already. - Lady Novelist: I'm so glad to have seen you. I'm busy now with the opening chapters of my next three-volume novel. You must come again when I've finished it. <a>Judy</a> </j>

<j> <t>[Untitled]</t> "Bark," a colour resembling the sails of fishing boats, is the fashionable tint for autumn. With a favourable breeze no doubt the bark will have a good sail. <a>Moonshine</a> </j>

<j> <t>Why Mr. Parnell Will "Go" If He Does "Go."</t> - For "divorce" reasons, to be sure. <a>Funny Folks</a> </j>

<j> <t>ALL RIGHT NOW.</t> - Well, how is your little boy, mrs. Wiggles? - Oh, much better now, mum. I took him to the doctor, who said it was only a rash broke out all over his body, and he gave him some medicine to putrify his blood. <a>Judy</a> </j>

<j> <t>A ROUNDABOUT ROLE.</t> - A rigmarole. <a>Funny Folks</a> </j>

<j> <t>RUS IN URBE.</t> Old Lady (from the country, as train is nearing Cannon-street): It is wonderful 'ow they knows which line to go on; 'an all so much alike. But (brightening) - I suppose they 'as a compass. <a>Judy</a> </j>

<j> <t>IMITATION IS THE SINCEREST, &c.</t> - D'you know, your paintings remind me most forcibly of Carlo Zetti. - The deuce they do! And who the deuce is Carlo Zetti? - Carlo Zetti is the poor artist who draws in chalks on the pavements of Euston-square. - The deuce he does! <a>Judy</a> </j>

<j> <t>NOT SO BAD AFTER ALL.</t> - Mrs McFadden: I'm very queer again, doctor. My cough bothers me so: I'm afraid I'm going to die. - Genial Medical Person: Never mind, it's not a very difficult thing to do. The last year of our life is much easier than the first. You see, there's no teething. <a>Judy</a> </j>""", datetime.now(), users[-1])]

  transcriptions = []
  for item in transcriptiondata:
    transcriptions.append(Transcription(*item))
    db_session.add(transcriptions[-1])
  db_session.commit()


if __name__ == "__main__":
  if sys.flags.interactive:
    from database import init_test_db
    db_session = init_test_db()
    load_db(db_session)
    print("All models have been imported, and 'db_session' is the db entrypoint.")
  else:
    print("This will load the data into an inmemory SQLite db. Please open this with an interactive shell.")
    print("Eg 'python -i test_load_test_data.py'")
    print("Quitting.")
