from flask import Flask, render_template, request, redirect, url_for, session
import os  # For generating a secret key, and potentially file storage if needed

app = Flask(__name__)

# Set a secret key for session management (important for security!)
app.secret_key = os.urandom(24)  # Generate a random 24-byte key


# --- Data Structures and Helper Functions ---

def create_bracket(size):
    """Creates a bracket data structure.

    Args:
        size:  The number of entries in the bracket (e.g., 4, 8, 16, etc.)

    Returns:
        A dictionary representing the bracket. The keys are round numbers
        (starting from 1) and the values are lists of matches. Each match
        is a list containing the two competing items (or None initially).  For example:

        {
            1: [ [None, None], [None, None] ],  # Round 1 for a size 4 bracket
            2: [ [None, None] ]
        }
    """
    bracket = {}
    round_num = 1
    num_matches = size // 2
    total_entries = size
    while num_matches > 0:
        matches = [[None, None] for _ in range(num_matches)]
        bracket[round_num] = matches
        num_matches //= 2
        round_num += 1
    return bracket


def get_bracket_size_options():
  """Returns a list of valid bracket sizes."""
  return [4, 8, 12, 16, 32, 64, 128]



# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In a real app, hash and salt this!

        # Basic authentication check (replace with a more robust system)
        if username == 'user' and password == 'password':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('choose_bracket'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    """Logs the user out."""
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('bracket_size', None) # Clear bracket on logout.
    session.pop('bracket_data', None)
    return redirect(url_for('login'))


@app.route('/choose_bracket', methods=['GET', 'POST'])
def choose_bracket():
    """Allows the user to choose the bracket size."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            bracket_size = int(request.form['bracket_size'])
            if bracket_size not in get_bracket_size_options():
                return render_template('choose_bracket.html', error="Invalid bracket size. Choose from 4, 8, 12 ,16, 32, 64, or 128.", bracket_sizes = get_bracket_size_options())


            session['bracket_size'] = bracket_size
            return redirect(url_for('enter_items'))
        except ValueError:
            return render_template('choose_bracket.html', error="Please enter a valid number.", bracket_sizes = get_bracket_size_options())


    return render_template('choose_bracket.html', bracket_sizes = get_bracket_size_options())



@app.route('/enter_items', methods=['GET', 'POST'])
def enter_items():
    """Allows the user to enter the items for the bracket."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    bracket_size = session.get('bracket_size')
    if not bracket_size:
        return redirect(url_for('choose_bracket'))

    if request.method == 'POST':
        items = []
        for i in range(bracket_size):
            item = request.form.get(f'item{i+1}')
            if not item:
                return render_template('enter_items.html', bracket_size=bracket_size, error="Please enter all items.", items = ["" for _ in range(bracket_size)]) #Re-render with empty values to prevent loss of data
            items.append(item)

        # Initialize the bracket data structure
        bracket_data = create_bracket(bracket_size)

        # Populate the first round with the entered items
        items_iter = iter(items)
        for match in bracket_data[1]:
            try:
                match[0] = next(items_iter)
                match[1] = next(items_iter)
            except StopIteration:
                break  # Should not happen if the number of items matches bracket_size

        session['bracket_data'] = bracket_data  # Store bracket data in session
        return redirect(url_for('view_bracket'))

    else:
        return render_template('enter_items.html', bracket_size=bracket_size, items = ["" for _ in range(bracket_size)])  # Pass the size to the template



@app.route('/view_bracket')
def view_bracket():
    """Displays the bracket and allows users to select winners."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    bracket_data = session.get('bracket_data')
    if not bracket_data:
        return redirect(url_for('enter_items'))  # Go back to entering items if data is missing

    return render_template('view_bracket.html', bracket=bracket_data)


@app.route('/update_bracket', methods=['POST'])
def update_bracket():
    """Updates the bracket with the winners selected by the user."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    bracket_data = session.get('bracket_data')
    if not bracket_data:
        return redirect(url_for('enter_items'))

    # Go through each round and update the bracket with the winners
    for round_num, matches in bracket_data.items():
        for i, match in enumerate(matches):
            winner = request.form.get(f'winner_round{round_num}_match{i}')
            if winner:
                # Determine the next round and match index
                next_round = round_num + 1
                next_match_index = i // 2  # Integer division

                # If it's the final round, there's no next round
                if next_round not in bracket_data:
                    continue

                # Determine which position (0 or 1) in the next match to place the winner
                position = i % 2

                # Update the next match with the winner
                bracket_data[next_round][next_match_index][position] = winner

    session['bracket_data'] = bracket_data # Save the updated bracket data

    return redirect(url_for('view_bracket'))




@app.route('/reset_bracket')
def reset_bracket():

    """Resets the bracket data, allowing the user to start over."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Remove bracket data from the session
    session.pop('bracket_data', None)

    # Redirect to the enter_items page to re-enter data, or choose_bracket to choose a new size
    return redirect(url_for('enter_items')) #Or redirect to 'choose_bracket' if you want them to also re-choose the bracket size



# --- Main ---

if __name__ == '__main__':
    app.run(debug=True)
