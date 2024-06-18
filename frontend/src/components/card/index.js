import PropTypes from 'prop-types'

import styles from './style.module.css'
import { LinkComponent } from '../index'

const Card = ({ id, full_name, avatar }) => {
  return (
    <div className={styles.card}>
      <LinkComponent
        className={styles.card__title}
        href={`/fpk/${id}`}
        title={<div
          className={styles.card__image}
          style={{ backgroundImage: `url(${avatar})` }} />}
      />
      <div className={styles.card__body}>
        <LinkComponent
          className={styles.card__title}
          href={`/fpk/${id}`}
          title={full_name} />
      </div>
    </div>
  );
};

Card.propTypes = {
  id: PropTypes.number,
  full_name: PropTypes.string,
  avatar: PropTypes.string
};

export default Card;