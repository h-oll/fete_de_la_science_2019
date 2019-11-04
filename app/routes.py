import os
from flask import Flask, render_template, request, session, g, redirect
from magicsquare import app
import sqlite3
from contextlib import ExitStack

from pathlib import Path
from cqc.pythonLib import CQCConnection, qubit
from libmagicsquare import MagicSquare
import sqlite3

DB_FILE=os.environ.get("MAGICSQUARE_DB_FILE") or "sessions.db"

# Create DB_FILE if needed:
print("Database file: {}".format(DB_FILE))
folder=os.path.dirname(DB_FILE)
if folder:
    os.makedirs(folder, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.execute('CREATE TABLE IF NOT EXISTS session (id VARCHAR(256), p1line VARCHAR(256), p1val VARCHAR(256), p2col VARCHAR(256), p2val VARCHAR(256), qres1 VARCHAR(256), qres2 VARCHAR(256))')
    conn.commit()
    conn.close()

@app.route('/', defaults={'message': ""})
@app.route('/index', defaults={'message': ""})
def index(message):
    return render_template('accueil.html',message=message, titre='Accueil')


def waiting(idsess):
    conn = sqlite3.connect(DB_FILE)
    curr=conn.cursor()
    items=curr.execute("SELECT * FROM session WHERE id=? ", (idsess,))
    return render_template('waiting.html', items=items.fetchall() )

@app.route('/player1')
def p1():
    return render_template('p1.html', titre='player 1')

@app.route('/waiting1',methods = ["POST"])
def waiting1():
    conn = sqlite3.connect(DB_FILE)
    ids = request.form["numsess"]
    numline = request.form["numline"]
    x1 = request.form["select1"]
    x2 = request.form["select2"]
    x3 = request.form["select3"]
    x=x1+x2+x3
    p2c= ""
    p2x= ""
    curr=conn.cursor()
    curr.execute("INSERT INTO session (id,p1line,p1val,p2col,p2val,qres1,qres2) VALUES (?,?,?,?,?,?,?)",[ids,numline,x,p2c,p2x,"",""] )
    conn.commit()
    return waiting(ids)

@app.route('/player2')
def p2():
    return render_template('p2.html', titre='Player 2')

@app.route('/waiting2',methods = ["POST"])
def waiting2():
    conn = sqlite3.connect(DB_FILE)
    ids = request.form["numsess"]
    numcol = request.form["numline"]
    x1 = request.form["select1"]
    x2 = request.form["select2"]
    x3 = request.form["select3"]
    # Classical
    x=x1+x2+x3
    curr=conn.cursor()
    curr.execute("SELECT * FROM session WHERE id=?", (ids,))
    test= curr.fetchone()
    if test is None:
        return index(message="Il n'y a pas de session existant au numéro indiqué")
    else:
        curr.execute("UPDATE session SET p2col=?, p2val=? WHERE id=? ", (numcol, x, ids))
        conn.commit()
        return waiting(ids)


@app.route('/results/<ids>/',methods = ["GET"])
def results(ids):
    conn = sqlite3.connect(DB_FILE)
    curr=conn.cursor()
    items=curr.execute("SELECT * FROM session WHERE id=? ", (ids,))
    items1=items.fetchone()
    if items1 is None:
        return index(message="Il n'y a pas de résultats à la session indiquée")
    else:
        test2=items1[3]
        if test2 != "":
            numline=int(items1[1])-1
            numcol=int(items1[3])-1
            qres1=items1[5]
            qres2=items1[6]
            if qres1 == "" or qres2 == "":
                # Quantum
                with ExitStack() as global_stack:
                    magic_square = MagicSquare(global_stack, debug=True)
                    ma = magic_square.alice_measurement(numline)
                    str1 = ''.join(str(e) for e in ma)
                    mb = magic_square.bob_measurement(numcol)
                    str2 = ''.join(str(e) for e in mb)
                    conn = sqlite3.connect(DB_FILE)
                    curr=conn.cursor()
                    curr.execute("UPDATE session SET qres1=?, qres2=? WHERE id=? ", (str1, str2, ids))
                    conn.commit()
                    return render_template('resultats.html', items1=items1, ma=ma, mb=mb, titre="Résultats")
            else:
                return render_template('resultats.html', items1=items1, ma=qres1, mb=qres2, titre="Résultats")
        else: 
            return waiting(ids)


