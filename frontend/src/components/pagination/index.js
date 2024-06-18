import cn from 'classnames'

import { useState, useEffect } from 'react'

import styles from './style.module.css'
import arrowLeft from './arrow-left.png'
import arrowRight from './arrow-right.png'

const Pagination = ({ count = 0, limit = 6, initialActive = 1, onPageChange, page }) => {
  const [active, setActive] = useState(initialActive);
  const onButtonClick = (active) => {
    setActive(active);
    onPageChange(active);
  };
  useEffect(
    (_) => {
      if (page === active) {
        return;
      }
      setActive(page);
    },
    [page, active]
  );
  const pagesCount = Math.ceil(count / limit);
  if (count === 0 || pagesCount <= 1) {
    return null;
  }
  return (
    <div className={styles.pagination}>
      <img
        alt="left"
        title="Перейти на предыдущую страницу"
        className={cn(styles.arrow, styles.arrowLeft, {
          [styles.arrowDisabled]: active === 1
        })}
        src={arrowLeft}
        onClick={(_) => {
          if (active === 1) {
            return;
          }
          onButtonClick(active - 1);
        }}
      />
      {new Array(pagesCount).fill().map((item, idx) => {
        return (
          <div
            className={cn(styles.paginationItem, {
              [styles.paginationItemActive]: idx + 1 === active
            })}
            onClick={(_) => onButtonClick(idx + 1)}
            key={idx}
          >
            {idx + 1}
          </div>
        );
      })}
      <img
        alt="right"
        title="Перейти на следующую страницу"
        src={arrowRight}
        className={cn(styles.arrow, styles.arrowRight, {
          [styles.arrowDisabled]: active === pagesCount
        })}
        onClick={(_) => {
          if (active === pagesCount) {
            return;
          }
          onButtonClick(active + 1);
        }}
      />
    </div>
  );
};

export default Pagination;
