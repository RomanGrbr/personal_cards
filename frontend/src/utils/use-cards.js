import { useState } from 'react'

import api from '../api'

export default function useCards() {
  const [cards, setCards] = useState([]);
  const [cardsCount, setCardsCount] = useState(0);
  const [cardsPage, setCardsPage] = useState(1);

  const getCards = ({ page = 1, full_name = '' }) => {
    api.getCards({ page, full_name }).then((res) => {
      const { results, count } = res;
      setCards(results);
      setCardsCount(count);
    });
  };

  return {
    cards,
    getCards,
    cardsCount,
    setCardsCount,
    cardsPage,
    setCardsPage
  };
}
