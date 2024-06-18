import { useState } from 'react'

import api from '../api'

export default function useCard() {
  const [card, setCard] = useState({});
  const [socials, setSocials] = useState([]);
  const [news, setNews] = useState([]);

  const getCard = ({ id }) => {
    api.getCard({ card_id: id }).then((res) => {
      setCard(res);
    });
  };

  const getSocials = ({ id }) => {
    api.getSocials({ card_id: id }).then((res) => {
      setSocials(res);
    });
  };

  const getNews = ({ id }) => {
    api.getNews({ card_id: id }).then((res) => {
      setNews(res);
    });
  };

  return {
    card,
    setCard,
    getCard,
    socials,
    setSocials,
    getSocials,
    news,
    setNews,
    getNews
  };
}
