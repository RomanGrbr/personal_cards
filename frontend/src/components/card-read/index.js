import { v4 as uuid } from 'uuid'

import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

import styles from './style.module.css'
import api from '../../api'
import media_type from '../../configs/constants'

const CardRead = ({allStats}) => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [card, setCard] = useState({})
  const [attrs, setAttrs] = useState([])
  const {image, audio, video, file} = media_type

  useEffect((_) => {
    api
      .getCard({
        card_id: id
      })
      .then((res) => {
        setCard(res);
      })
      .catch((err) => {
        navigate('/fpk');
      });
  }, []);

  useEffect((_) => {
    api
      .getCardAttrs({ card_id: id })
      .then((res) => {
        setAttrs(
          res.results.filter(
            attr => ![image, audio, video, file].includes(
              attr.attr_type)
              )
            )
      })
      .catch((err) => {
        navigate('/fpk');
      });
  }, []);

  return (
      <div className={styles.container}>
          <div className={styles.card}>
              <div className={styles.imageContainer}>
                  <img src={card.avatar} alt={card.avatar} className={styles.card__image} />
              </div>
              <div className={styles.info}>
                  <h2>ФИО персоны: {card.full_name}</h2>
                  <table className={styles.infoTable}>
                      <tbody>
                      {attrs.map((attr) => (
                          <tr key={uuid()}>
                              <td>{attr.label}</td>
                              <td>{attr.value}</td>
                          </tr>
                      ))}
                      <tr>
                        <td>Никнеймы</td>
                        <td>{allStats.users}</td>
                      </tr>
                      <tr>
                        <td>Число подписок</td>
                        <td>{allStats.followersCount}</td>
                      </tr>
                      <tr>
                        <td>Число подписчиков</td>
                        <td>{allStats.followingCount}</td>
                      </tr>
                      <tr>
                        <td>Число публикаций</td>
                        <td>{allStats.postsCount}</td>
                      </tr>
                      <tr>
                        <td>Число друзей</td>
                        <td>{allStats.friendsCount}</td>
                      </tr>
                      </tbody>
                  </table>
              </div>
          </div>
      </div>
  );
};

export default CardRead;
