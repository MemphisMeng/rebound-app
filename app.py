from flask import Flask, jsonify, request, render_template
from joblib import load
import pandas as pd
import matplotlib.pyplot as plt

# initialize flask application
app = Flask(__name__)
# ML model
LDA = load('LDA.joblib')

def preprocess(locations):
    input = pd.DataFrame(
        {
            'AtShot_loc_x_off_player_1': [locations[0][0]],
            'AtShot_loc_y_off_player_1': [locations[0][1]],
            'AtShot_loc_x_off_player_2': [locations[1][0]],
            'AtShot_loc_y_off_player_2': [locations[1][1]],
            'AtShot_loc_x_off_player_3': [locations[2][0]],
            'AtShot_loc_y_off_player_3': [locations[2][1]],
            'AtShot_loc_x_off_player_4': [locations[3][0]],
            'AtShot_loc_y_off_player_4': [locations[3][1]],
            'AtShot_loc_x_off_player_5': [locations[4][0]],
            'AtShot_loc_y_off_player_5': [locations[4][1]],
            'AtShot_loc_x_def_player_1': [locations[5][0]],
            'AtShot_loc_y_def_player_1': [locations[5][1]],
            'AtShot_loc_x_def_player_2': [locations[6][0]],
            'AtShot_loc_y_def_player_2': [locations[6][1]],
            'AtShot_loc_x_def_player_3': [locations[7][0]],
            'AtShot_loc_y_def_player_3': [locations[7][1]],
            'AtShot_loc_x_def_player_4': [locations[8][0]],
            'AtShot_loc_y_def_player_4': [locations[8][1]],
            'AtShot_loc_x_def_player_5': [locations[9][0]],
            'AtShot_loc_y_def_player_5': [locations[9][1]]
        }
    )

    input[[col for col in input.columns if '_y_' in col]] = (input[
        [col for col in input.columns if '_y_' in col]] - 5) / (335 - 5)
    input[[col for col in input.columns if '_x_' in col]] = (input[
        [col for col in input.columns if '_x_' in col]] - 0) / (325 - 0)
    return input

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        try:
            locations=[[] for _ in range(10)]
            split_res = request.form['hidden'].split('<br>')
            for i in range(10):
                x = split_res[i].split(', ')[0]
                y = split_res[i].split(', ')[1]
                locations[i].append(int(x))
                locations[i].append(int(y))

            # pre-processing
            input = preprocess(locations)

            ## predict
            # individual
            individual_prediction = LDA.predict_proba(input)[0]
            # team
            offensive_proba = sum(individual_prediction[:5])
            defensive_proba = sum(individual_prediction[5:])

            fig, ax = plt.subplots()
            ax.bar(['offensive %', 'defensive %'], [offensive_proba * 100, defensive_proba * 100])
            fig.savefig('static/bar.png')

            results = pd.DataFrame(
                {
                    'Players': ['Offensive Player 1', 'Offensive Player 2', 'Offensive Player 3', 'Offensive Player 4', 'Offensive Player 5',
                                'Defensive Player 1', 'Defensive Player 2', 'Defensive Player 3', 'Defensive Player 4', 'Defensive Player 5'],
                    'Probability': individual_prediction
                }
            ).sort_values(by=['Probability'], ascending=False)

            return render_template('output.html', 
                player1=results['Players'].iloc[0], proba1=round(results['Probability'].iloc[0], 3),
                player2=results['Players'].iloc[1], proba2=round(results['Probability'].iloc[1], 3),
                player3=results['Players'].iloc[2], proba3=round(results['Probability'].iloc[2], 3),
                player4=results['Players'].iloc[3], proba4=round(results['Probability'].iloc[3], 3),
                player5=results['Players'].iloc[4], proba5=round(results['Probability'].iloc[4], 3),
                player6=results['Players'].iloc[5], proba6=round(results['Probability'].iloc[5], 3),
                player7=results['Players'].iloc[6], proba7=round(results['Probability'].iloc[6], 3),
                player8=results['Players'].iloc[7], proba8=round(results['Probability'].iloc[7], 3),
                player9=results['Players'].iloc[8], proba9=round(results['Probability'].iloc[8], 3),
                player10=results['Players'].iloc[9], proba10=round(results['Probability'].iloc[9], 3))
        except:
            return render_template('output2.html')


if __name__ == '__main__':
    app.run(debug=True)