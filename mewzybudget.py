#!/usr/bin/env python

import sys
import math


from gsp import GSP
from util import argmax_index

class Mewzybudget:
    """Balanced bidding agent"""
    def __init__(self, id, value, budget):
        self.id = id
        self.value = value
        self.budget = budget

    def initial_bid(self, reserve):
        return self.value / 2


    def slot_info(self, t, history, reserve):
        """Compute the following for each slot, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns list of tuples [(slot_id, min_bid, max_bid)], where
        min_bid is the bid needed to tie the other-agent bid for that slot
        in the last round.  If slot_id = 0, max_bid is 2* min_bid.
        Otherwise, it's the next highest min_bid (so bidding between min_bid
        and max_bid would result in ending up in that slot)
        """
        prev_round = history.round(t-1)
        other_bids = filter(lambda (a_id, b): a_id != self.id, prev_round.bids)

        clicks = prev_round.clicks
        def compute(s):
            (min, max) = GSP.bid_range_for_slot(s, clicks, reserve, other_bids)
            if max == None:
                max = 2 * min
            return (s, min, max)
            
        info = map(compute, range(len(clicks)))
#        sys.stdout.write("slot info: %s\n" % info)
        return info


    def expected_utils(self, t, history, reserve):
        """
        Figure out the expected utility of bidding such that we win each
        slot, assuming that everyone else keeps their bids constant from
        the previous round.

        returns a list of utilities per slot.
        """
        # TODO: Fill this in
        # Begin added code
        def iround(x):
            """Round x and return an int"""
            return int(round(x))

        def calc_clicks(t, history):
            top_slot_clicks = iround(30*math.cos(math.pi*t/24) + 50)
            num_slots = max(1, history.n_agents-1) 
            return [iround(top_slot_clicks * pow(.75, i))
                          for i in range(num_slots)]
        
        slots = self.slot_info(t, history, reserve)

        # prev_round = history.round(t-1)
        # clicks = prev_round.clicks
        new_clicks = calc_clicks(t, history)

        utilities = []   # Change this
        for (slot_id, min_bid, max_bid) in slots:
            utilities.append(new_clicks[slot_id] * (self.value - min_bid))
        # End added code

        
        return utilities

    def target_slot(self, t, history, reserve):
        """Figure out the best slot to target, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns (slot_id, min_bid, max_bid), where min_bid is the bid needed to tie
        the other-agent bid for that slot in the last round.  If slot_id = 0,
        max_bid is min_bid * 2
        """
        i =  argmax_index(self.expected_utils(t, history, reserve))
        info = self.slot_info(t, history, reserve)
        return info[i]

    def bid(self, t, history, reserve):
        # The Balanced bidding strategy (BB) is the strategy for a player j that, given
        # bids b_{-j},
        # - targets the slot s*_j which maximizes his utility, that is,
        # s*_j = argmax_s {clicks_s (v_j - p_s(j))}.
        # - chooses his bid b' for the next round so as to
        # satisfy the following equation:
        # clicks_{s*_j} (v_j - p_{s*_j}(j)) = clicks_{s*_j-1}(v_j - b')
        # (p_x is the price/click in slot x)
        # If s*_j is the top slot, we (arbitrarily) choose
        #        b' = (v_j + p_0(j)) / 2. We can 
        # thus deal with all slots uniformly by defining clicks_{-1} = 2 clicks_0.
        #
        prev_round = history.round(t-1)
        (slot, min_bid, max_bid) = self.target_slot(t, history, reserve)

        # TODO: Fill this in.
        clicks = prev_round.clicks

        def iround(x):
            """Round x and return an int"""
            return int(round(x))

        def calc_clicks(t, history):
            top_slot_clicks = iround(30*math.cos(math.pi*t/24) + 50)
            num_slots = max(1, history.n_agents-1) 
            return [iround(top_slot_clicks * pow(.75, i))
                          for i in range(num_slots)]

        new_clicks = calc_clicks(t, history)
        # top_slot_clicks = iround(30*math.cos(math.pi*t/24) + 50)

        # if t < 47:
        #     bid = 0  # change this
        #     set_aside = (48 - t) * (1 + self.value)
        #     spendable = self.budget - set_aside
        #     top_clicks = top_slot_clicks
        #     bid = spendable / top_clicks
        #     return bid
        # else:
        #     return 99999999

        if t < 46:
            if min_bid >= self.value:
                bid = self.value
            else:
                if slot > 0:
                    bid = self.value - (new_clicks[slot] * (self.value - min_bid) / new_clicks[slot - 1])
                else:
                    bid = self.value
            return bid
        elif t == 46:
            return self.budget - 1
        else:
            return 99999999

    def __repr__(self):
        return "%s(id=%d, value=%d)" % (
            self.__class__.__name__, self.id, self.value)


