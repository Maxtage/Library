/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   DeckTest.cpp
 * Author: volz
 *
 * Created on 20. Juni 2018, 14:06
 */

#include "../simulation/Deck.h"
#include "../simulation/Card.h"
#include "../utils/Hoy.h"
#include "../utils/Hoy2.h"

#include <stdlib.h>
#include <iostream>
#include <vector>

/*
 * Simple C++ Test Suite
 */

void createDeckDefault() {
    int n = 2;
    int m = 4;
    std::vector<double>values(n*m);
    for(int i=0; i<n*m; i++){
        values[i] = i;
    }
    std::vector<double> min(m, 0);
    std::vector<double> max(m,100);
    Deck deck(values, n, m, min, max);
    std::vector<Card> cards = deck.getCards();
    for(int i=0; i<n; i++){
        cards[i].toString();
    }
    std::cout << "Expected outcome" << "Card: 0, 1, 2, 3 and Card: 4,5,6,7" << std::endl;
}

void createDeckRandom(){
    int n=2;
    int m=4;
    double min = 1;
    double max = 10;
    Deck deck(n, m, min, max, 1);
    std::vector<Card> cards = deck.getCards();
    for(int i=0; i<n; i++){
        cards[i].toString();
    }
    std::cout << "Expected outcome: Two cards with 4 values ranging from 1-10" << std::endl;
    Deck deck3(n, m, min, max, 1);
    std::vector<Card> cards3 = deck3.getCards();
    for(int i=0; i<n; i++){
        cards3[i].toString();
    }
    std::cout << "Expected outcome: Two cards with 4 values ranging from 1-10" << std::endl;
    Deck deck2(n, m, min, max, 2);
    std::vector<Card> cards2 = deck2.getCards();
    for(int i=0; i<n; i++){
        cards2[i].toString();
    }
    std::cout << "Expected outcome: Different cards with 4 values ranging from 1-10" << std::endl;
}

void testShuffle(){
    int n = 10;
    int m = 4;
    std::vector<double>values(n*m);
    for(int i=0; i<n*m; i++){
        values[i] = i;
    }
    std::vector<double> min(m, 0);
    std::vector<double> max(m,100);
    Deck deck(values, n, m, min, max);
    deck.shuffle();
    std::vector<Card> cards = deck.getCards();
    for(int i=0; i<n; i++){
        cards[i].toString();
    }
    std::cout << "Expected outcome: 10 cards with increasing values, but reshuffled" << std::endl;
    deck.shuffle();
    std::vector<Card> cards2 = deck.getCards();
    for(int i=0; i<n; i++){
        cards2[i].toString();
    }
    std::cout << "Expected outcome: 10 cards with increasing values, but rereshuffled" << std::endl;
}

void testDistribute(){
    int n = 10;
    int m = 4;
    int players = 2;
    std::vector<double>values(n*m);
    for(int i=0; i<n*m; i++){
        values[i] = i;
    }
    std::vector<double> min(m, 0);
    std::vector<double> max(m,100);
    Deck deck(values, n, m, min, max);
    std::vector<std::vector<Card>> cards = deck.distribute(players);
    for(int i=0; i<players; i++){
        std::cout << "Player " << i << std::endl;
        std::vector<Card> hand = cards[i];
        for(int j=0; j<n/players; j++){
            hand[j].toString();
        }
    }
    std::cout << "Expected outcome: 10 cards with increasing value, distributed to 2 players" << std::endl;
}


void testHV(){
    int n = 10;
    int m = 4;
    std::vector<double>values(n*m);
    for(int i=0; i<n*m; i++){
        values[i] = i;
    }
    std::vector<std::vector<double>> values2;
    for(int i = 0; i < n; i++){
        std::vector<double> v(m);
        for(int j = 0; j < m; j++){
          v[j] = values[j + m*i];
        }
        values2.push_back(v);
    }
    for(int i=0; i<n*m; i++){
      std::cout << values[i] << " ";
    }
    std::cout << std::endl;
    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
          std::cout << values2[i][j] << " ";
        }
    }
    std::vector<double> refPoint ={37, 38, 39, 40};
    HVCalculator hv;
    Hoy hv2;
    std::cout << std::endl;
    std::cout << "Hypervolume: " << hv.computeHV(m,n,values,refPoint) << std::endl;
    std::cout << "Hypervolume2: " << hv2.compute(values2,refPoint) << std::endl;
    std::vector<double> min(m, 0);
    std::vector<double> max(m,100);
    Deck deck(values, n, m, min, max);
    std::cout << "Hypervolume: " << deck.getHV() << std::endl;
    std::cout << "Hypervolume2: " << deck.getHV2() << std::endl;
}

void testSD(){
    int n = 10;
    int m = 4;
    std::vector<double>values(n*m);
    for(int i=0; i<n*m; i++){
        values[i] = i;
    }
    std::vector<double> min(m, 0);
    std::vector<double> max(m,100);
    Deck deck(values, n, m, min, max);
    std::cout << "SD goal 1.290994: " << deck.getSD() << std::endl;
}

void testRanks(){
    int n = 10;
    int m = 4;
    Deck deck(n, m, 0, 10, 5);
    std::vector<Card> cards = deck.getCards();
    for(int i=0; i<n; i++){
        cards[i].toString();
        cards[i].printRanks();
    }
}

int main(int argc, char** argv) {
    createDeckDefault();
    std::cout << "----------------------------------------" <<std::endl;
    createDeckRandom();
    std::cout << "----------------------------------------" <<std::endl;
    testShuffle();
    std::cout << "----------------------------------------" <<std::endl;
    testDistribute();
    std::cout << "----------------------------------------" <<std::endl;
    testHV();
    std::cout << "----------------------------------------" <<std::endl;
    testSD();
    std::cout << "----------------------------------------" <<std::endl;
    testRanks();
    (void) argc; /* To avoid the unused warning */
    (void) argv; /* To avoid the unused warning */
    return (EXIT_SUCCESS);
}

