from flask import Flask, render_template, request
from pikrMaker import PikrMaker
import contextlib
import io
import unittest
import testpikrMaker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/unittest')
def unittestindex():
    text = None
    
    with open("testpikrMaker.py") as file:
        text = file.read(None)

    testResult = None
    suite = unittest.TestLoader().loadTestsFromModule(testpikrMaker)
    with io.StringIO() as buf:
        # run the tests
        with contextlib.redirect_stdout(buf):
            unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
        # process (in this case: print) the results
        testResult =  buf.getvalue()
        
    return render_template('unittest.html', text=text, testResult=testResult)
    
@app.route('/pikr', methods = ['POST'])
def do_pick():
   
    formData = request.form

    SameFamily = 'SameFamily' in formData

    firstNames = formData.getlist("FirstName")
    lastNames = formData.getlist("LastName")

    participants = []
    
    for index in range(len(firstNames)): 
        participants.append({"id":firstNames[index],"groupName":lastNames[index]})

    try:
        pm = PikrMaker()
        pm.setParticipants(participants)
        results = pm.getResults(pickSameGroup=SameFamily)
    except Exception as e:
        htmlError = f'<article class="message is-warning"> \
                          <div class="message-header"> \
                              <p>Warning</p> \
                                  <button class="delete" aria-label="delete"></button> \
                          </div> \
                          <div class="message-body"> \
                              {e} \
                          </div> \
                      </article>'

        return htmlError

    htmlResponse = ""
    
    for result in results:
        giver = f'{result["giver"]["id"]} {result["giver"]["groupName"]}'
        receiver = f'{result["receiver"]["id"]} {result["receiver"]["groupName"]}'
        
        response = f'<div class="columns is-vcentered is-centered"> \
                         <div class="column is-4"> \
                             <input class="input" type="text" value="{giver}" readonly> \
                         </div> \
                              Gives To \
                         <div class="column is-4"> \
                            <input class="input" type="text" value="{receiver}" readonly> \
                         </div> \
                     </div>'
    
        htmlResponse = htmlResponse + response
    
    return htmlResponse

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)