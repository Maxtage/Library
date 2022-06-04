/* 
 * File:   Game.h
 * Author: volz
 *
 * Created on 20. Juni 2018, 13:41
 */

#ifndef GAME_H
#define GAME_H

#include "../simulation/Agent.h"
#include "../simulation/Deck.h"
#include "../simulation/Outcome.h"


class Game{
public:
    Game(Deck deck, int players, std::vector<Agent> agents, int seed);
        
    Outcome run(Outcome out, int verbose=0);
protected:
    int round(int won_last, std::vector<std::vector<Card>> cards, int verbose=0);
    
private:
    std::vector<Agent> agents;
    int players;
    Deck deck;
    std::default_random_engine re;
    
    int bestPlayer;//TODO Expects there to be exactly one best player
    
};


#endif /* GAME_H */

