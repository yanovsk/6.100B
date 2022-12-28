import copy
import unittest
import ps1

def check_valid_mapping(election_states, move_voters_result, expected_results):
    # case when student returns None
    if move_voters_result is None:
        assert expected_results is None, "There is a possible solution here, but you returned None."
        return True

    if expected_results is None:
        assert move_voters_result is None, "This election cannot be flipped, but you returned something other than None."
        return True

    voters_moved, ec_votes, voter_map = move_voters_result
    staff_voters_moved, staff_ec_votes, staff_voter_map = expected_results
    orig_winner, orig_loser = ps1.election_winner(election_states)
    election_copy = election_states[:]

    # check if the numbers line up
    assert (ec_votes == staff_ec_votes), f"The number of ec_votes gained isn't quite right: expected {staff_ec_votes}, got {ec_votes}."
    assert (voters_moved == staff_voters_moved), f"The number of voters_moved isn't quite right: expected {staff_voters_moved}, got {voters_moved}."

    # maps the state to the index in the list allows for easy access
    election_dict = {}
    for state_index in range(len(election_copy)):
        election_dict[election_copy[state_index].get_name()] = state_index

    # make all of the moves suggested in voter_map
    prohibited_states = ['AL', 'AZ', 'CA', 'TX']
    winner_won_states = ps1.winner_states(election_states)

    for state_from, state_to in voter_map:
        assert state_from not in prohibited_states, f"Your mapping should not have moved voters from an prohibited state ({state_from}), but it turns out it has."
        assert state_from not in winner_won_states, f"Your mapping should not have moved voters from a state won by the original winner ({state_from}), but it turns out it has."

        from_index, to_index = election_dict[state_from], election_dict[state_to]
        from_margin, to_margin = election_copy[from_index].get_margin(), election_copy[to_index].get_margin()
        margin_moved = voter_map[(state_from, state_to)]

        # just flipped a state that was already won
        assert from_margin-margin_moved >= 1, f"Your mapping should not be turning a state won by the original loser into one they now lost or tied, but it turns out it did so for {state_from}."


        #change the results of the election
        election_copy[from_index].subtract_winning_candidate_voters(margin_moved)
        election_copy[to_index].add_losing_candidate_voters(margin_moved)

    # check if after all of the changes are made, the election result has been flipped
    new_winner, new_loser = ps1.election_winner(election_copy)
    assert new_winner == orig_loser, "After making the moves you suggested, your mapping should have flipped the election, but it turns out it has not."
    return True


class TestPS1(unittest.TestCase):
    def test_1_load_election(self):
        # 600_results.txt
        expected_parsed_election = [ps1.State("TX", 1, 2, 530), ps1.State("CA", 4, 5, 3), ps1.State("MA", 7, 8, 5)]
        parsed_election = ps1.load_election("600_results.txt")

        self.assertIsInstance(parsed_election, list, f"load_election should have returned a list, but instead returned an instance of {type(parsed_election)}.")
        self.assertEqual(len(parsed_election), len(expected_parsed_election), f"The length of the list returned by load_election should have been {len(expected_parsed_election)}, but found it returned {len(parsed_election)}.")
        self.assertTrue(all(isinstance(st, ps1.State) for st in parsed_election), f"All items in the list returned by load_election should have been State instances, but found your output was {parsed_election}.")
        for i in range(len(parsed_election)):
            self.assertEqual(expected_parsed_election[i], parsed_election[i], f"Expected the element at index {i} of the returned list be `{expected_parsed_election[i]}`, found it was `{parsed_election[i]}`.")

        # 6100A_results.txt
        expected_parsed_election = [ps1.State("FL", 4, 3, 3), ps1.State("GA", 8, 7, 5), ps1.State("WA", 7, 8, 5), ps1.State("AL", 1, 10, 1)]
        parsed_election = ps1.load_election("6100A_results.txt")

        self.assertIsInstance(parsed_election, list, f"load_election should have returned a list, but instead returned an instance of {type(parsed_election)}.")
        self.assertEqual(len(parsed_election), len(expected_parsed_election), f"The length of the list returned by load_election should have been {len(expected_parsed_election)}, but found it returned {len(parsed_election)}.")
        self.assertTrue(all(isinstance(st, ps1.State) for st in parsed_election), f"All items in the list returned by load_election should have been State instances, but found your output was {parsed_election}.")
        for i in range(len(parsed_election)):
            self.assertEqual(expected_parsed_election[i], parsed_election[i], f"Expected the element at index {i} of the returned list be `{expected_parsed_election[i]}`, found it was `{parsed_election[i]}`.")

    def test_2a_election_winner(self):
        rep_won = ("rep", "dem")
        dem_won = ("dem", "rep")

        # 600_results.txt
        expected_winner = dem_won
        parsed_election = [ps1.State("TX", 2, 1, 100), ps1.State("CA", 1, 2, 1), ps1.State("MA", 1, 2, 2)]
        winner = ps1.election_winner(parsed_election)
        self.assertEqual(expected_winner, winner, f"For the sample election: expected {expected_winner}, got {winner}. You appear to be tallying number of states won rather than number of EC votes won by a state.")

        # 6100A_results.txt
        expected_winner = dem_won
        parsed_election = [ps1.State("FL", 4, 3, 3), ps1.State("GA", 8, 7, 5), ps1.State("WA", 7, 8, 5), ps1.State("AL", 1, 10, 1)]
        winner = ps1.election_winner(parsed_election)
        self.assertEqual(expected_winner, winner, f"For the second sample election: expected {expected_winner}, got {winner}.")

        # 2020_results.txt
        expected_winner = dem_won
        winner = ps1.election_winner(ps1.load_election("2020_results.txt"))
        self.assertEqual(expected_winner, winner, f"For the 2020 election: expected {expected_winner}, got {winner}.")

        # 2016_results.txt
        expected_winner = rep_won
        winner = ps1.election_winner(ps1.load_election("2016_results.txt"))
        self.assertEqual(expected_winner, winner, f"For the 2016 election: expected {expected_winner}, got {winner}.")

        # 2012_results.txt
        expected_winner = dem_won
        winner = ps1.election_winner(ps1.load_election("2012_results.txt"))
        self.assertEqual(expected_winner, winner, f"For the 2012 election: expected {expected_winner}, got {winner}.")

    def test_2b_winner_states(self):
        # 600_results.txt
        expected_winners = set(['TX', 'CA', 'MA'])
        winners = [state.get_name() for state in ps1.winner_states(ps1.load_election("600_results.txt"))]
        self.assertIsInstance(winners, list, f"winner_states should have returned a list, but instead returned an instance of {type(winners)}.")
        self.assertEqual(len(winners), len(set(winners)), "winner_states should have returned a list with no duplicates, but found it had duplicates.")
        self.assertEqual(expected_winners, set(winners), f"For the sample election: expected {expected_winners}, got {winners}.")

        # 6100A_results.txt
        expected_winners = set(['FL', 'GA'])
        winners = [state.get_name() for state in ps1.winner_states(ps1.load_election("6100A_results.txt"))]
        self.assertIsInstance(winners, list, f"winner_states should have returned a list, but instead returned an instance of {type(winners)}.")
        self.assertEqual(len(winners), len(set(winners)), "winner_states should have returned a list with no duplicates, but found it had duplicates.")
        self.assertEqual(expected_winners, set(winners), f"For the second sample election: expected {expected_winners}, got {winners}.")

        # 2020_results.txt
        expected_winners = set(['AZ', 'CA', 'CO', 'CT', 'DE', 'DC', 'GA', 'HI', 'IL', 'ME', 'MD', 'MA', 'MI', 'MN', 'NV', 'NH', 'NJ', 'NM', 'NY', 'OR', 'PA', 'RI', 'VT', 'VA', 'WA', 'WI'])
        winners = [state.get_name() for state in ps1.winner_states(ps1.load_election("2020_results.txt"))]
        self.assertIsInstance(winners, list, f"winner_states should have returned a list, but instead returned an instance of {type(winners)}.")
        self.assertEqual(len(winners), len(set(winners)), "winner_states should have returned a list with no duplicates, but found it had duplicates.")
        self.assertEqual(expected_winners, set(winners), f"For the 2020 election: expected {expected_winners}, got {winners}.")

        # 2016_results.txt
        expected_winners = set(['AL', 'AK', 'AZ', 'AR', 'FL', 'GA', 'ID', 'IN', 'IA', 'KS', 'KY', 'LA', 'MI', 'MS', 'MO', 'MT', 'NE', 'NC', 'ND', 'OH', 'OK', 'PA', 'SC', 'SD', 'TN', 'TX', 'UT', 'WV', 'WI', 'WY'])
        winners = [state.get_name() for state in ps1.winner_states(ps1.load_election("2016_results.txt"))]
        self.assertIsInstance(winners, list, f"winner_states should have returned a list, but instead returned an instance of {type(winners)}.")
        self.assertEqual(len(winners), len(set(winners)), "winner_states should have returned a list with no duplicates, but found it had duplicates.")
        self.assertEqual(expected_winners, set(winners), f"For the 2016 election: expected {expected_winners}, got {winners}.")

        # 2012_results.txt
        expected_winners = set(['CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'HI', 'IL', 'IA', 'ME', 'MD', 'MA', 'MI', 'MN', 'NV', 'NH', 'NJ', 'NM', 'NY', 'OH', 'OR', 'PA', 'RI', 'VT', 'VA', 'WA', 'WI'])
        winners = [state.get_name() for state in ps1.winner_states(ps1.load_election("2012_results.txt"))]
        self.assertIsInstance(winners, list, f"winner_states should have returned a list, but instead returned an instance of {type(winners)}.")
        self.assertEqual(len(winners), len(set(winners)), "winner_states should have returned a list with no duplicates, but found it had duplicates.")
        self.assertEqual(expected_winners, set(winners), f"For the 2016 election: expected {expected_winners}, got {winners}.")

    def test_2c_ec_votes_to_flip(self):
        # 600_results.txt
        expected_ecvotes = 270
        ecvotes = ps1.ec_votes_to_flip(ps1.load_election("600_results.txt"))
        self.assertIsInstance(ecvotes, int, f"ec_votes_to_flip should have returned an int, but instead returned an instance of {type(ecvotes)}.")
        self.assertEqual(expected_ecvotes, ecvotes, f"For the sample election: expected {expected_ecvotes}, got {ecvotes}.")

        # 6100A_results.txt
        expected_ecvotes = 2
        ecvotes = ps1.ec_votes_to_flip(ps1.load_election("6100A_results.txt"), total=14)
        self.assertIsInstance(ecvotes, int, f"ec_votes_to_flip should have returned an int, but instead returned an instance of {type(ecvotes)}.")
        self.assertEqual(expected_ecvotes, ecvotes, f"For the second sample election: expected {expected_ecvotes}, got {ecvotes}.")

        # 2020_results.txt
        expected_ecvotes = 38
        ecvotes = ps1.ec_votes_to_flip(ps1.load_election("2020_results.txt"))
        self.assertIsInstance(ecvotes, int, f"ec_votes_to_flip should have returned an int, but instead returned an instance of {type(ecvotes)}.")
        self.assertEqual(expected_ecvotes, ecvotes, f"For the 2020 election: expected {expected_ecvotes}, got {ecvotes}.")

        # 2016_results.txt
        expected_ecvotes = 37
        ecvotes = ps1.ec_votes_to_flip(ps1.load_election("2016_results.txt"))
        self.assertIsInstance(ecvotes, int, f"ec_votes_to_flip should have returned an int, but instead returned an instance of {type(ecvotes)}.")
        self.assertEqual(expected_ecvotes, ecvotes, f"For the 2016 election: expected {expected_ecvotes}, got {ecvotes}.")

        # 2012_results.txt
        expected_ecvotes = 64
        ecvotes = ps1.ec_votes_to_flip(ps1.load_election("2012_results.txt"))
        self.assertIsInstance(ecvotes, int, f"ec_votes_to_flip should have returned an int, but instead returned an instance of {type(ecvotes)}.")
        self.assertEqual(expected_ecvotes, ecvotes, f"For the 2012 election: expected {expected_ecvotes}, got {ecvotes}.")

    def test_3_brute_swing_states(self):
        # 600_results.txt
        expected_output = set(['TX']), 2
        election_states = ps1.load_election("600_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        raw_swing_states = ps1.brute_force_swing_states(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        swing_states, voters_moved = raw_swing_states
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For Sample Results: expected States {expected_output}, got {actual_output}. Check that you are handling ties correctly.")

        # 6100B_results.txt
        expected_output = set(['BE']), 105412
        election_states = ps1.load_election("6100B_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states, total=14)
        raw_swing_states = ps1.brute_force_swing_states(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        swing_states, voters_moved = raw_swing_states
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For Given Example Results: expected {expected_output}, got {actual_output}. Test your code using the test cases under 'main' in ps1.py.")

        # 2020_results_brute.txt
        expected_output = set(['AZ']), 10458
        election_states = ps1.load_election("2020_results_brute.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states, total=122)
        raw_swing_states = ps1.brute_force_swing_states(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        swing_states, voters_moved = raw_swing_states
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For 2020 Results: expected {expected_output}, got {actual_output}.")

        # 2016_results_brute.txt
        expected_output = set(['IA']), 147315
        election_states = ps1.load_election("2016_results_brute.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states, total=44)
        raw_swing_states = ps1.brute_force_swing_states(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        swing_states, voters_moved = raw_swing_states
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For 2016 Results: expected {expected_output}, got {actual_output}.")

        # 2012_results_brute.txt
        expected_output = set(['MI', 'NV', 'NH', 'VT', 'VA']), 812606
        election_states = ps1.load_election("2012_results_brute.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states, total=98)
        raw_swing_states = ps1.brute_force_swing_states(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        swing_states, voters_moved = raw_swing_states
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For 2012 Results: expected {expected_output}, got {actual_output}.")

    def test_4a_move_max_voters(self):
        # 600_results.txt
        expected_output = set([]), 0
        loser_lost_states = ps1.winner_states(ps1.load_election("600_results.txt"))
        raw_moved_max_voters = ps1.max_voters_moved(loser_lost_states, 2)
        states, voters_moved = raw_moved_max_voters
        names = [state.get_name() for state in states]
        actual_output = set(names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For Sample Results: expected States {expected_output}, got {actual_output}.")

        # 2020_results.txt
        expected_output = set(['CA', 'VA', 'IL', 'OR', 'VT', 'DC', 'WA', 'HI', 'NM', 'MN', 'CO', 'DE', 'MA', 'MI', 'NY', 'ME', 'RI', 'MD', 'NJ', 'CT', 'NH', 'PA']), 14986834
        election_states = ps1.load_election("2020_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        loser_ecvotes = sum(state.get_ecvotes() for state in loser_lost_states)
        raw_moved_max_voters = ps1.max_voters_moved(loser_lost_states, loser_ecvotes-loser_ecvotes_reqd)
        states, voters_moved = raw_moved_max_voters
        names = [state.get_name() for state in states]
        actual_output = set(names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For the 2020 election: expected States {expected_output}, got {actual_output}.")

        # 2016_results.txt
        expected_output = set(['NE', 'WV', 'OK', 'KY', 'TN', 'AL', 'AR', 'MO', 'ND', 'IN', 'LA', 'KS', 'WY', 'SD', 'MS', 'UT', 'SC', 'OH', 'TX', 'ID', 'NC', 'MT', 'IA', 'GA', 'FL', 'AZ', 'AK']), 8491354
        election_states = ps1.load_election("2016_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        loser_ecvotes = sum(state.get_ecvotes() for state in loser_lost_states)
        raw_moved_max_voters = ps1.max_voters_moved(loser_lost_states, loser_ecvotes-loser_ecvotes_reqd)
        states, voters_moved = raw_moved_max_voters
        names = [state.get_name() for state in states]
        actual_output = set(names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For the 2016 election: expected States {expected_output}, got {actual_output}.")

        # 2012_results.txt
        expected_output = set(['NY', 'MA', 'MD', 'DC', 'WA', 'HI', 'VT', 'NJ', 'CA', 'IL', 'CT', 'RI', 'OR', 'MI', 'MN', 'WI', 'NM', 'ME', 'PA', 'IA', 'DE', 'NV', 'CO']), 11353398
        election_states = ps1.load_election("2012_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        loser_ecvotes = sum(state.get_ecvotes() for state in loser_lost_states)
        raw_moved_max_voters = ps1.max_voters_moved(loser_lost_states, loser_ecvotes-loser_ecvotes_reqd)
        states, voters_moved = raw_moved_max_voters
        names = [state.get_name() for state in states]
        actual_output = set(names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For the 2012 election: expected States {expected_output}, got {actual_output}.")

    def test_4b_move_min_voters(self):
        # 600_results.txt
        expected_output = set(['TX']), 2
        election_states = ps1.load_election("600_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        raw_moved_min_voters = ps1.min_voters_moved(loser_lost_states, loser_ecvotes_reqd)
        swing_states, voters_moved = raw_moved_min_voters
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For Sample Results: expected States {expected_output}, got {swing_names}.")

        # 2020_results.txt
        expected_output = set(['AZ', 'WI', 'GA', 'NV']), 76518
        election_states = ps1.load_election("2020_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        raw_moved_min_voters = ps1.min_voters_moved(loser_lost_states, loser_ecvotes_reqd)
        swing_states, voters_moved = raw_moved_min_voters
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For the 2020 election: expected States {expected_output}, got {actual_output}.")

        # 2016_results.txt
        expected_output = set(['MI', 'PA', 'WI']), 77747
        election_states = ps1.load_election("2016_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        raw_moved_min_voters = ps1.min_voters_moved(loser_lost_states, loser_ecvotes_reqd)
        swing_states, voters_moved = raw_moved_min_voters
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For the 2016 election: expected States {expected_output}, got {actual_output}.")

        # 2012_results.txt
        expected_output = set(['FL', 'NH', 'OH', 'VA']), 429526
        election_states = ps1.load_election("2012_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        raw_moved_min_voters = ps1.min_voters_moved(loser_lost_states, loser_ecvotes_reqd)
        swing_states, voters_moved = raw_moved_min_voters
        swing_names = [state.get_name() for state in swing_states]
        actual_output = set(swing_names), voters_moved
        self.assertEqual(expected_output, actual_output, f"For the 2012 election: expected States {expected_output}, got {actual_output}.")

    def test_5_relocate_voters(self):
        # 600_results.txt
        example = None
        election_states = ps1.load_election("600_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        swing_states = ps1.min_voters_moved(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        results_dp = ps1.relocate_voters(copy.deepcopy(election_states), copy.deepcopy(swing_states[0]))
        self.assertTrue(check_valid_mapping(election_states, results_dp, example), f"Your relocate_voters results did not give the correct result.\nFor the sample election you got {results_dp}\nOne valid solution is {example}.")

        # 2020_results.txt
        example = (76518, 43, {('AK', 'AZ'): 10458, ('AK', 'GA'): 11780, ('AK', 'NV'): 13802, ('AR', 'NV'): 19795, ('AR', 'WI'): 20683})
        election_states = ps1.load_election("2020_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        swing_states = ps1.min_voters_moved(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        results_dp = ps1.relocate_voters(copy.deepcopy(election_states), copy.deepcopy(swing_states[0]))
        self.assertTrue(check_valid_mapping(election_states, results_dp, example), f"Your relocate_voters results did not give the correct result.\nFor the 2020 election you got {results_dp}.\nOne valid solution is {example}.")

        # 2016_results.txt
        example = (77747, 46, {('CO', 'MI'): 10705, ('CO', 'PA'): 44293, ('CO', 'WI'): 22749})
        election_states = ps1.load_election("2016_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        swing_states = ps1.min_voters_moved(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        results_dp = ps1.relocate_voters(copy.deepcopy(election_states), copy.deepcopy(swing_states[0]))
        self.assertTrue(check_valid_mapping(election_states, results_dp, example), f"Your relocate_voters results did not give the correct result.\nFor the 2016 election you got {results_dp}\nOne valid solution is {example}.")

        # 2012_results.txt
        example = (429526, 64, {('AK', 'FL'): 42035, ('AR', 'FL'): 32275, ('AR', 'NH'): 39644, ('AR', 'OH'): 166273, ('AR', 'VA'): 15142, ('GA', 'VA'): 134157})
        election_states = ps1.load_election("2012_results.txt")
        loser_lost_states = ps1.winner_states(election_states)
        loser_ecvotes_reqd = ps1.ec_votes_to_flip(election_states)
        swing_states = ps1.min_voters_moved(copy.deepcopy(loser_lost_states), loser_ecvotes_reqd)
        results_dp = ps1.relocate_voters(copy.deepcopy(election_states), copy.deepcopy(swing_states[0]))
        self.assertTrue(check_valid_mapping(election_states, results_dp, example), f"Your relocate_voters results did not give the correct result.\nFor the 2012 election you got {results_dp}\nOne valid solution is {example}.")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS1))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
