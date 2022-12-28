################################################################################
# 6.100B Fall 2022
# Problem Set 1
# Name: Dima Yanovsky
# Collaborators: Arteim Saraiev, Makar Kuznietsov
# Time: 5hrs

from json import load
from state import State

##########################################################################################################
## Problem 1
##########################################################################################################

def load_election(filename):
    """
    Reads the contents of a file, with data given in the following tab-separated format:
    State[tab]Democrat_votes[tab]Republican_votes[tab]EC_votes

    Please ignore the first line of the file, which are the column headers, and remember that
    the special character for tab is '\t'

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    big_list = []

    with open(filename, 'r') as f:
        next(f)
        for row in f:
            big_list.append(row.replace('\t', ' ').replace('\n', '').split(' '))

    states_list = []
    for list in big_list:
        states_list.append(State(list[0],list[1],list[2],list[3]))
    
    return states_list
##########################################################################################################
## Problem 2: Helper functions
##########################################################################################################

def election_winner(election_states):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election_states - a list of State instances

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'rep') if Democrats won, else ('rep', 'dem')
    """
    dem_votes, rep_votes = 0,0

    for state in election_states:
        if state.get_winner() == "dem":
            dem_votes += state.get_ecvotes()
        else:
            rep_votes += state.get_ecvotes()

    if dem_votes > rep_votes:
        return('dem', 'rep')
    else:
        return('rep','dem')


def winner_states(election_states):
    """
    Finds the list of States that were won by the winning candidate (lost by the losing candidate).

    Parameters:
    election_states - a list of State instances

    Returns:
    A list of State instances won by the winning candidate
    """
    winner = election_winner(election_states)[0]
    won_states = []
    for state in election_states:
        if state.get_winner() == winner:
            won_states.append(state)

    return won_states


def ec_votes_to_flip(election_states, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election_states - a list of State instances
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    loser = election_winner(election_states)[1]

    loser_votes = 0
    for state in election_states:
        if state.get_winner() == loser:
            loser_votes += state.get_ecvotes()

    return (((total//2)+1) - loser_votes)


##########################################################################################################
## Problem 3: Brute Force approach
##########################################################################################################

def combinations(L):
    """
    Helper function to generate powerset of all possible combinations
    of items in input list L. E.g., if
    L is [1, 2] it will return a list with elements
    [], [1], [2], and [1,2].

    DO NOT MODIFY THIS.

    Parameters:
    L - list of items

    Returns:
    a list of lists that contains all possible
    combinations of the elements of L
    """

    def get_binary_representation(n, num_digits):
        """
        Inner function to get a binary representation of items to add to a subset,
        which combinations() uses to construct and append another item to the powerset.

        DO NOT MODIFY THIS.

        Parameters:
        n and num_digits are non-negative ints

        Returns:
            a num_digits str that is a binary representation of n
        """
        result = ''
        while n > 0:
            result = str(n%2) + result
            n = n//2
        if len(result) > num_digits:
            raise ValueError('not enough digits')
        for i in range(num_digits - len(result)):
            result = '0' + result
        return result

    powerset = []
    for i in range(0, 2**len(L)):
        binStr = get_binary_representation(i, len(L))
        subset = []
        for j in range(len(L)):
            if binStr[j] == '1':
                subset.append(L[j])
        powerset.append(subset)
    return powerset


def brute_force_swing_states(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states, these are our swing states. Iterate over
    all possible move combinations using the helper function combinations(L).
    Return the move combination that minimises the number of voters moved. If
    there exists more than one combination that minimises this, return any one of them.

    Parameters:
    winner_states - a list of State instances that were won by the winning candidate
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    * A tuple containing the list of State instances such that the election outcome would change if additional
      voters relocated to those states, as well as the number of voters required for that relocation.
    * A tuple containing the empty list followed by zero, if no possible swing states.
    """
    all_comb = combinations(winner_states)
    best_combo = []
    min_voters = None

    for combo in all_comb:
        new_ec_votes = sum([x.get_ecvotes() for x in combo])
        totalVoters = 0
        best = []
        if new_ec_votes >= ec_votes_needed:
            best.append(combo)
            totalVoters += sum([x.get_margin()+1 for x in combo])
            if min_voters == None or totalVoters < min_voters:
                best_combo = combo
                min_voters = totalVoters
    
    if min_voters == None:
        return([], 0)
    else:
        return(best_combo, min_voters)


##########################################################################################################
## Problem 4: Dynamic Programming
## In this section we will define two functions, max_voters_moved and min_voters_moved, that
## together will provide a dynamic programming approach to find swing states. This problem
## is analagous to the complementary knapsack problem, you might find Lecture 1 of 6.100B useful
## for this section of the pset.
##########################################################################################################

def max_voters_moved_helper(winner_states, ec_vote_limit, memo=None):
    if memo == None:
        memo = {}
    if (len(winner_states), ec_vote_limit) in memo:
        result = memo[(len(winner_states), ec_vote_limit)]
    elif winner_states == [] or ec_vote_limit == 0:
        result = (0, ())
    elif winner_states[0].get_ecvotes() > ec_vote_limit:
        #go to the right branch
        result = max_voters_moved_helper(winner_states[1:], ec_vote_limit, memo)
    else:
        nextItem = winner_states[0]
        #go to the left branch
        withVal, withToTake = max_voters_moved_helper(winner_states[1:], ec_vote_limit - nextItem.get_ecvotes(), memo)
        withVal += (nextItem.get_margin()+1)
        withoutVal, withoutToTake = max_voters_moved_helper(winner_states[1:], ec_vote_limit, memo)
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(winner_states), ec_vote_limit)] = result
    return result


def max_voters_moved(winner_states, ec_vote_limit):
    """
    Finds the largest number of voters needed to relocate to get at most ec_vote_limit
    for the election loser.

    Analogy to the knapsack problem:
        Given a list of states each with a weight(ec_votes) and value(margin+1),
        determine the states to include in a collection so the total weight(ec_votes)
        is less than or equal to the given limit(ec_vote_limit) and the total value(voters displaced)
        is as large as possible.

    Parameters:
    winner_states - a list of State instances that were won by the winner
    ec_vote_limit - int, the maximum number of EC votes

    Returns:
    * A tuple containing the list of State instances such that the maximum number of voters need to
      be relocated to these states in order to get at most ec_vote_limit, and the number of voters
      required required for such a relocation.
    * A tuple containing the empty list followed by zero, if every state has a # EC votes greater
      than ec_vote_limit.
    """
    result = max_voters_moved_helper(winner_states, ec_vote_limit)
    return result[1],result[0]

def min_voters_moved(winner_states, ec_votes_needed):
    """
    Finds a subset of winner_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated.
    Only return states that were originally won by the winner (lost by the loser)
    of the election.

    Hint: This problem is simply the complement of max_voters_moved. You should call
    max_voters_moved with ec_vote_limit set to (#ec votes won by original winner - ec_votes_needed)
    #maximum number of EC votes winner can keep if loser wins instead
    Parameters:
    winner_states - a list of State instances that were won by the winner
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    * A tuple containing the list of State instances (which we can call swing states) such that the
      minimum number of voters need to be relocated to these states in order to get at least
      ec_votes_needed, and the number of voters required for such a relocation.
    * * A tuple containing the empty list followed by zero, if no possible swing states.
    """
    ec_votes = sum([i.get_ecvotes() for i in winner_states])
    #return all non-swing states
    #non-swing b/c these are the states where maximum amount of voters needs to move to (i.e. costly states)
    result =  max_voters_moved(winner_states, ec_votes-ec_votes_needed)
    new_states = [state for state in winner_states if state not in result[0]]

    moved_voters =0
    for i in new_states:
        moved_voters += i.get_margin()+1

    return(new_states, moved_voters)



##########################################################################################################
## Problem 5
##########################################################################################################


def relocate_voters(election_states, swing_states, prohibited_states = ['AL', 'AZ', 'CA', 'TX']):
    """
    Finds a way to shuffle voters in order to flip an election outcome. Moves voters
    from states that were won by the losing candidate (states not in winner_states), to
    each of the states in swing_states. To win a swing state, you must move (margin + 1)
    new voters into that state. Any state that voters are moved from should still be won
    by the loser even after voters are moved. Also finds the number of EC votes gained by
    this rearrangement, as well as the minimum number of voters that need to be moved.
    Note: You cannot move voters out of Alabama, Arizona, California, or Texas.

    Parameters:
    election_states - a list of State instances representing the election
    swing_states - a list of State instances where people need to move to flip the election outcome
                   (result of min_voters_moved or brute_force_swing_states)
    prohibited_states - a list of Strings holding the names of states where residents cannot be moved from
                   (default states are AL, AZ, CA, TX)

    Return:
    * A tuple that has 3 elements in the following order:
        - an int, the total number of voters moved
        - an int, the total number of EC votes gained by moving the voters
        - a dictionary with the following (key, value) mapping:
            - Key: a 2 element tuple of str, (from_state, to_state), the 2 letter State names
            - Value: int, number of people that are being moved
    * None, if it is not possible to sway the election
    """
    winners = winner_states(election_states)
    losers = []
    for state in election_states:
        if state not in winners:
            if state.get_name() not in prohibited_states:
                losers.append(state)

    dict = {}
    total_vot_mov, total_ec_gained = 0,0
    for stateS in swing_states:
        for stateL in losers:
                #see if losing state has enought voters to satisfy margin of swing state to win
                if stateL.get_margin()-1 >= stateS.get_margin()+1:
                    #if so -> getting this margin
                    t = stateS.get_margin()+1
                    #using class functions to add/remove votes
                    stateS.add_losing_candidate_voters(t)
                    stateL.subtract_winning_candidate_voters(t)

                    #if this margin exists
                    if t:
                        #insert in dict
                        dict[stateL.get_name(), stateS.get_name()] = t
                    #adding to the total number
                    total_vot_mov += t
                    total_ec_gained += stateS.get_ecvotes()
                    break
                else:
                    #if margin is not enought
                    #we still remove all margin voters from the losing state and adding to swing state
                    x = stateL.get_margin()-1
                    stateS.add_losing_candidate_voters(x)
                    stateL.subtract_winning_candidate_voters(x)
                    if x:
                        dict[stateL.get_name(), stateS.get_name()] = x
                    total_vot_mov += x
    #finally if sum is enough - return, if not - return None
    if sum([i.get_margin()+1 for i in swing_states]) > total_vot_mov:
        return None
    else:
        return (total_vot_mov, total_ec_gained, dict)


if __name__ == "__main__":


    pass
    # Uncomment the following lines to test each of the problems

    # # tests Problem 1
    year = 2012
    election_states = load_election(f"{year}_results.txt")
    print(len(election_states))
    print(election_states[0])

    # # tests Problem 2
    winner, loser = election_winner(election_states)
    won_states = winner_states(election_states)
    names_won_states = [state.get_name() for state in won_states]
    reqd_ec_votes = ec_votes_to_flip(election_states)
    print("Winner:", winner, "\nLoser:", loser)
    print("States won by the winner: ", names_won_states)
    print("EC votes needed:",reqd_ec_votes, "\n")

    # # tests Problem 3
    brute_election = load_election("6100B_results.txt")
    brute_won_states = winner_states(brute_election)
    brute_ec_votes_to_flip = ec_votes_to_flip(brute_election, total=14)
    print(brute_ec_votes_to_flip)
    brute_swing, voters_brute = brute_force_swing_states(brute_won_states, brute_ec_votes_to_flip)
    print(brute_force_swing_states(brute_won_states, brute_ec_votes_to_flip))


    names_brute_swing = [state.get_name() for state in brute_swing]
    ecvotes_brute = sum([state.get_ecvotes() for state in brute_swing])
    print("Brute force swing states results:", names_brute_swing)
    print("Brute force voters displaced:", voters_brute, "for a total of", ecvotes_brute, "Electoral College votes.\n")

    # # tests Problem 4a: max_voters_moved
    print("max_voters_moved")
    total_lost = sum(state.get_ecvotes() for state in won_states)
    non_swing_states, max_voters_displaced = max_voters_moved(won_states, total_lost-reqd_ec_votes)
    print(max_voters_moved(won_states, total_lost-reqd_ec_votes))
    non_swing_states_names = [
    state.get_name() for state in non_swing_states]
    ec_vote_limit = sum([state.get_ecvotes() for state in non_swing_states])
    
    print("States with the largest margins (non-swing states):", non_swing_states_names)
    print("Max voters displaced:", max_voters_displaced, "for a total of", ec_vote_limit, "Electoral College votes.", "\n")

    # # tests Problem 4b: min_voters_moved
    print("min_voters_moved")
    swing_states, min_voters_displaced = min_voters_moved(won_states, reqd_ec_votes)

    print(swing_states, min_voters_displaced)
    swing_state_names = [state.get_name() for state in swing_states]
    swing_ec_votes = sum([state.get_ecvotes() for state in swing_states])
    print("Complementary knapsack swing states results:", swing_state_names)
    print("Min voters displaced:", min_voters_displaced, "for a total of", swing_ec_votes, "Electoral College votes. \n")

    # # tests Problem 5: relocate_voters
    print("relocate_voters")
    flipped_election = relocate_voters(election_states, swing_states)
    print("Flip election mapping:", flipped_election)
