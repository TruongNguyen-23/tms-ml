from Src.train import trip_for_machine_learning

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/trip/ml')
def get_data_trip():
    return trip_for_machine_learning()

if __name__ == '__main__':
    app.run(debug=True)
