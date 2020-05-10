from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .cards import Deck, Cards
import random

cards = Cards()


def game(request):
    if request.method == 'POST' or not cards.cards_open:
        try:
            req = request.POST['req']
        except KeyError:
            req = 'new_game'
        if req == 'new_game':
            cards.new_game()
        elif req == 'check_set':
            cards.check_for_set()
            if not cards.hint:
                if len(cards.deck) >= 3:
                    cards.open_extra_cards()
                else:
                    cards.end_of_game = True
        else:
            cards.end_of_game = False
            cards.hint = False
            cards.process_selection(req)
        return HttpResponseRedirect(reverse('game'))
    context = {'cards_open': cards.cards_open,
               'number_sets_found': cards.number_sets_found,
               'a_set': cards.hint,
               'end_of_game': cards.end_of_game,
               'row_length': len(cards.cards_open)/3,
               'correct_set_call': cards.correct_set_call}
    return render(request, 'game/home.html', context)
