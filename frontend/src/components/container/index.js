import cn from 'classnames'

import styles from './style.module.css'

const Container = ({ children, className }) => {
  return <div className={cn(styles.container, className)}>{children}</div>;
};

export default Container;
