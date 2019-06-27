from flask import Flask, render_template
import Board as bd
import json

# Create the application instance
app = Flask(__name__, template_folder="templates")

@app.route('/')
def player_game():
  
   #plays the game and creates the file
   #info = bd.playSimpleGame()
   #with open('templates/test.json', 'w') as outfile:  
   #   json.dump(info, outfile)

   with open("templates/test.json", "r") as f:
    content = f.read()

   converted = json.loads(content)

   return render_template('Visualizer.html', contents=converted)


if __name__ == '__main__':
   app.run(debug = True)